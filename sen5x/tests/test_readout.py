import asyncio
import math

import sen5x
import sen5x.sensor as sensor

sen5x.init_i2c("/dev/i2c-1")


async def test_readout():
    await sensor.device_reset()
    print("Device reset complete")

    print(f"Product name: {await sensor.get_product_name()}")
    print(f"Version: {await sensor.get_version()}")
    print(f"Serial number: {await sensor.get_serial_number()}")
    print(f"Device status: {await sensor.read_device_status()}")
    print(f"Initial data ready flag: {await sensor.read_data_ready()}")

    print("\nClearing device status...")
    await sensor.read_and_clear_device_status()

    print("\nSetting temperature offset...")
    print(f"Starting offset: {await sensor.get_temperature_offset_simple()}")
    print(f"Setting offset to 4.20...")
    await sensor.set_temperature_offset_simple(4.20)
    print(f"New offset: {await sensor.get_temperature_offset_simple()}")

    print("\nSetting fan cleaning interval...")
    print(f"Initial fan cleaning interval: {await sensor.get_fan_auto_cleaning_interval()}")
    print(f"Setting fan cleaning interval to 60 minutes...")
    await sensor.set_fan_auto_cleaning_interval(60 * 60)
    print(f"New fan cleaning interval: {await sensor.get_fan_auto_cleaning_interval()}")

    print("\nSetting RH/T adjustment...")
    print(f"Current adjustment mode: {await sensor.get_rh_t_acceleration_mode()}")
    print(f"Setting to 2 (medium)...")
    await sensor.set_rh_t_acceleration_mode(2)
    print(f"New adjustment mode: {await sensor.get_rh_t_acceleration_mode()}")

    print("\n Starting no-pm measurement...")
    await sensor.start_measurement_without_pm()
    print("Waiting for data ready...")
    while not await sensor.read_data_ready():
        await asyncio.sleep(0.1)
    no_pm_results = await sensor.read_measured_values()
    print("Data ready!")
    print(f"No-PM Results: {no_pm_results}")
    await sensor.stop_measurement()

    print("\n Starting full measurement...")
    await sensor.start_measurement()
    while not await sensor.read_data_ready():
        await asyncio.sleep(0.1)
    print("Waiting for an initial readout...")
    while math.isnan(res := (await sensor.read_measured_pm_values())['mass_concentration_pm1p0']) or res == 0.0:
        while not await sensor.read_data_ready():
            await asyncio.sleep(0.2)
    results = await sensor.read_measured_values()
    pm_results = await sensor.read_measured_pm_values()
    print("Data ready!")
    print(f"Results: {results}")
    print(f"PM Results: {pm_results}")

    print(f"\n Starting fan cleaning test...")
    await sensor.start_fan_cleaning()
    while not await sensor.read_data_ready():
        await asyncio.sleep(0.5)
    print("Fan cleaning complete!")
    await sensor.stop_measurement()

    print(f"\nDumping algorithm parameters:")
    print(f"VOc state: {await sensor.get_voc_algorithm_state()}")
    print(f"VOc params: {await sensor.get_voc_algorithm_tuning_parameters()}")
    print(f"NOx params: {await sensor.get_nox_algorithm_tuning_parameters()}")

    print("\nTest complete!")


asyncio.run(test_readout())
