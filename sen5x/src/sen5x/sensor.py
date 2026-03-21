import asyncio
from ctypes import c_bool, c_int, c_int32, c_int16, c_int8, c_uint, c_uint32, \
    c_uint16, c_uint8, c_char, c_char_p, c_float, POINTER

from . import libsen5x


async def device_reset() -> None:
    if libsen5x.sen5x_device_reset() < 0:
        raise RuntimeError("Failed to reset SEN5X device")
    # <100ms to complete per datasheet
    await asyncio.sleep(0.1)


async def get_serial_number() -> str:
    buffer = (c_uint8 * 32)()
    if libsen5x.sen5x_get_serial_number(buffer, 32) < 0:
        raise RuntimeError("Failed to get serial number")
    return bytes(buffer).rstrip(b'\x00').decode()


async def get_product_name() -> str:
    buffer = (c_uint8 * 32)()
    if libsen5x.sen5x_get_product_name(buffer, 32) < 0:
        raise RuntimeError("Failed to get product name")
    return bytes(buffer).rstrip(b'\x00').decode()


async def get_version() -> str:
    fw_major = c_uint8()
    fw_minor = c_uint8()
    fw_debug = c_bool()
    hw_major = c_uint8()
    hw_minor = c_uint8()
    prt_major = c_uint8()
    prt_minor = c_uint8()
    if libsen5x.sen5x_get_version(fw_major, fw_minor, fw_debug, hw_major, hw_minor, prt_major, prt_minor) < 0:
        raise RuntimeError("Failed to get version")
    return (
        f"FW:{fw_major.value}.{fw_minor.value}{'-debug' if fw_debug.value else ''}"
        f" HW:{hw_major.value}.{hw_minor.value} PRT:{prt_major.value}.{prt_minor.value}"
    )


async def read_device_status() -> int:
    status = c_uint32()
    if libsen5x.sen5x_read_and_clear_device_status(status) < 0:
        raise RuntimeError("Failed to read device status")
    return status.value


async def read_and_clear_device_status() -> int:
    status = c_uint32()
    if libsen5x.sen5x_read_and_clear_device_status(status) < 0:
        raise RuntimeError("Failed to read and clear device status")
    return status.value


async def start_measurement() -> None:
    if libsen5x.sen5x_start_measurement() < 0:
        raise RuntimeError("Failed to start measurement")
    await asyncio.sleep(0.05)  # <50ms


async def start_measurement_without_pm() -> None:
    if libsen5x.sen5x_start_measurement_without_pm() < 0:
        raise RuntimeError("Failed to start measurement without PM")
    await asyncio.sleep(0.05)  # <50ms


async def stop_measurement() -> None:
    if libsen5x.sen5x_stop_measurement() < 0:
        raise RuntimeError("Failed to stop measurement")
    await asyncio.sleep(0.2)  # <200ms


async def start_fan_cleaning() -> None:
    # In case the docs don't make it clear (they don't), fan cleaning only
    # works when the fan was previously started by calling start_measurement.
    # read_data_ready will return false until the fan cleaning is complete, which takes ~10s.
    # It is still possible to read the last (stale) dataframe during that period.
    # The process can be aborted by calling stop_measurement
    if libsen5x.sen5x_start_fan_cleaning() < 0:
        raise RuntimeError("Failed to start fan cleaning")
    await asyncio.sleep(0.02)  # <20ms


async def get_fan_auto_cleaning_interval() -> int:
    interval = c_uint32()
    if libsen5x.sen5x_get_fan_auto_cleaning_interval(interval) < 0:
        raise RuntimeError("Failed to get fan auto cleaning interval")
    await asyncio.sleep(0.02)  # <20ms
    return interval.value


async def set_fan_auto_cleaning_interval(interval: int) -> None:
    if interval < 0 or interval > 0xFFFFFFFF:
        raise ValueError("Interval must fit in uint32")
    if libsen5x.sen5x_set_fan_auto_cleaning_interval(interval) < 0:
        raise RuntimeError("Failed to set fan auto cleaning interval")
    await asyncio.sleep(0.02)  # <20ms


async def read_data_ready() -> bool:
    ready = c_bool()
    if libsen5x.sen5x_read_data_ready(ready) < 0:
        raise RuntimeError("Failed to read data ready status")
    return ready.value


async def get_warm_start_parameter() -> bool:
    param = c_uint16()
    if libsen5x.sen5x_get_warm_start_parameter(param) < 0:
        raise RuntimeError("Failed to get warm start parameter")
    return bool(param.value)


async def set_warm_start_parameter(param: bool) -> None:
    val = 0
    if param:
        val = 65535
    if libsen5x.sen5x_set_warm_start_parameter(val) < 0:
        raise RuntimeError("Failed to set warm start parameter")
    await asyncio.sleep(0.02)  # <20ms


async def get_temperature_offset_parameters() -> dict:
    offset = c_int16()
    gain = c_int16()
    scale = c_uint16()
    if libsen5x.sen5x_get_temperature_offset_parameters(offset, gain, scale) < 0:
        raise RuntimeError("Failed to get temperature offset parameters")
    return {
        "offset": offset.value,
        "slope": gain.value,
        "time_constant": scale.value
    }


async def get_temperature_offset_simple() -> float:
    # Call get_temperature_offset_parameters and apply the formula to return the actual offset in degrees Celsius
    params = await get_temperature_offset_parameters()
    return params["offset"] / 200.0


async def set_temperature_offset_parameters(offset: int, slope: int, time_constant: int) -> None:
    if offset < -32768 or offset > 32767:
        raise ValueError("Offset must fit in int16")
    if slope < -32768 or slope > 32767:
        raise ValueError("Slope must fit in int16")
    if time_constant < 0 or time_constant > 0xFFFF:
        raise ValueError("Time constant must fit in uint16")
    if libsen5x.sen5x_set_temperature_offset_parameters(offset, slope, time_constant) < 0:
        raise RuntimeError("Failed to set temperature offset parameters")
    await asyncio.sleep(0.02)  # <20ms


async def set_temperature_offset_simple(offset: float) -> None:
    # Convert the offset in degrees Celsius to the raw parameters and call set_temperature_offset_parameters
    raw_offset = int(offset * 200)
    await set_temperature_offset_parameters(raw_offset, 0, 0)


async def get_rh_t_acceleration_mode() -> int:
    mode = c_uint16()
    if libsen5x.sen5x_get_rht_acceleration_mode(mode) < 0:
        raise RuntimeError("Failed to get RH/T acceleration mode")
    return mode.value


async def set_rh_t_acceleration_mode(mode: int) -> None:
    if mode < 0 or mode > 2:
        # Yes, this is not an ommission, the valid modes are 0 (low), 1 (high) and 2 (medium)
        raise ValueError("Mode must be 0 (low), 1 (high) or 2 (medium)")
    if libsen5x.sen5x_set_rht_acceleration_mode(mode) < 0:
        raise RuntimeError("Failed to set RH/T acceleration mode")
    await asyncio.sleep(0.02)  # <20ms


async def get_voc_algorithm_tuning_parameters() -> dict:
    index_offset = c_int16()
    learning_time_offset_hours = c_int16()
    learning_time_gain_hours = c_int16()
    gating_time_max_duration_minutes = c_int16()
    std_initial = c_int16()
    gain_factor = c_int16()
    if libsen5x.sen5x_get_voc_algorithm_tuning_parameters(
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_time_max_duration_minutes, std_initial, gain_factor
    ) < 0:
        raise RuntimeError("Failed to get VOC algorithm tuning parameters")
    return {
        "index_offset": index_offset.value,
        "learning_time_offset_hours": learning_time_offset_hours.value,
        "learning_time_gain_hours": learning_time_gain_hours.value,
        "gating_time_max_duration_minutes": gating_time_max_duration_minutes.value,
        "std_initial": std_initial.value,
        "gain_factor": gain_factor.value
    }


async def set_voc_algorithm_tuning_parameters(
    index_offset: int, learning_time_offset_hours: int, learning_time_gain_hours: int,
    gating_time_max_duration_minutes: int, std_initial: int, gain_factor: int
) -> None:
    if any(param < -32768 or param > 32767 for param in [
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_time_max_duration_minutes, std_initial, gain_factor
    ]):
        raise ValueError("All parameters must fit in int16")
    if libsen5x.sen5x_set_voc_algorithm_tuning_parameters(
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_time_max_duration_minutes, std_initial, gain_factor
    ) < 0:
        raise RuntimeError("Failed to set VOC algorithm tuning parameters")
    await asyncio.sleep(0.02)  # <20ms


async def get_voc_algorithm_state() -> bytes:
    state = (c_uint8 * 12)()
    if libsen5x.sen5x_get_voc_algorithm_state(state) < 0:
        raise RuntimeError("Failed to get VOC algorithm state")
    return bytes(state)


async def set_voc_algorithm_state(state: bytes) -> None:
    if len(state) != 12:
        raise ValueError("State must be exactly 12 bytes")
    state_array = (c_uint8 * 12).from_buffer_copy(state)
    if libsen5x.sen5x_set_voc_algorithm_state(state_array) < 0:
        raise RuntimeError("Failed to set VOC algorithm state")
    await asyncio.sleep(0.02)  # <20ms


async def get_nox_algorithm_tuning_parameters() -> dict:
    index_offset = c_int16()
    learning_time_offset_hours = c_int16()
    learning_time_gain_hours = c_int16()
    gating_time_max_duration_minutes = c_int16()
    std_initial = c_int16()
    gain_factor = c_int16()
    if libsen5x.sen5x_get_nox_algorithm_tuning_parameters(
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_time_max_duration_minutes, std_initial, gain_factor
    ) < 0:
        raise RuntimeError("Failed to get NOx algorithm tuning parameters")
    return {
        "index_offset": index_offset.value,
        "learning_time_offset_hours": learning_time_offset_hours.value,
        "learning_time_gain_hours": learning_time_gain_hours.value,
        "gating_time_max_duration_minutes": gating_time_max_duration_minutes.value,
        "std_initial": std_initial.value,
        "gain_factor": gain_factor.value
    }


async def set_nox_algorithm_tuning_parameters(
    index_offset: int, learning_time_offset_hours: int, learning_time_gain_hours: int,
    gating_time_max_duration_minutes: int, std_initial: int, gain_factor: int
) -> None:
    if any(param < -32768 or param > 32767 for param in [
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_time_max_duration_minutes, std_initial, gain_factor
    ]):
        raise ValueError("All parameters must fit in int16")
    if libsen5x.sen5x_set_nox_algorithm_tuning_parameters(
        index_offset, learning_time_offset_hours, learning_time_gain_hours,
        gating_time_max_duration_minutes, std_initial, gain_factor
    ) < 0:
        raise RuntimeError("Failed to set NOx algorithm tuning parameters")
    await asyncio.sleep(0.02)  # <20ms


async def read_measured_values() -> dict:
    mass_concentration_pm1p0 = c_float()
    mass_concentration_pm2p5 = c_float()
    mass_concentration_pm4p0 = c_float()
    mass_concentration_pm10p0 = c_float()
    ambient_humidity = c_float()
    ambient_temperature = c_float()
    voc_index = c_float()
    nox_index = c_float()

    if libsen5x.sen5x_read_measured_values(
        mass_concentration_pm1p0, mass_concentration_pm2p5,
        mass_concentration_pm4p0, mass_concentration_pm10p0,
        ambient_humidity, ambient_temperature, voc_index, nox_index
    ) < 0:
        raise RuntimeError("Failed to read measured values")

    return {
        "mass_concentration_pm1p0": mass_concentration_pm1p0.value,
        "mass_concentration_pm2p5": mass_concentration_pm2p5.value,
        "mass_concentration_pm4p0": mass_concentration_pm4p0.value,
        "mass_concentration_pm10p0": mass_concentration_pm10p0.value,
        "ambient_humidity": ambient_humidity.value,
        "ambient_temperature": ambient_temperature.value,
        "voc_index": voc_index.value,
        "nox_index": nox_index.value
    }
