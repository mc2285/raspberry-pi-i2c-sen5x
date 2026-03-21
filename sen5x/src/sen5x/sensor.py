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
        f"HW:{hw_major.value}.{hw_minor.value} PRT:{prt_major.value}.{prt_minor.value}"
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
    if libsen5x.sen5x_start_fan_cleaning() < 0:
        raise RuntimeError("Failed to start fan cleaning")
    await asyncio.sleep(0.02)  # <20ms


async def get_fan_auto_cleaning_interval() -> int:
    interval = c_uint32()
    if libsen5x.sen5x_get_fan_auto_cleaning_interval(interval) < 0:
        raise RuntimeError("Failed to get fan auto cleaning interval")
    asyncio.sleep(0.02)  # <20ms
    return interval.value


async def set_fan_auto_cleaning_interval(interval: int) -> None:
    if interval < 0 or interval > 0xFFFFFFFF:
        raise ValueError("Interval must fit in uint32")
    if libsen5x.sen5x_set_fan_auto_cleaning_interval(interval) < 0:
        raise RuntimeError("Failed to set fan auto cleaning interval")
    asyncio.sleep(0.02)  # <20ms


async def read_data_ready() -> bool:
    ready = c_bool()
    if libsen5x.sen5x_read_data_ready(ready) < 0:
        raise RuntimeError("Failed to read data ready status")
    return ready.value


async def get_warm_start_parameter() -> bool:
    param = c_bool()
    if libsen5x.sen5x_get_warm_start_parameter(param) < 0:
        raise RuntimeError("Failed to get warm start parameter")
    return param.value


async def set_warm_start_parameter(param: bool) -> None:
    if libsen5x.sen5x_set_warm_start_parameter(param) < 0:
        raise RuntimeError("Failed to set warm start parameter")
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
