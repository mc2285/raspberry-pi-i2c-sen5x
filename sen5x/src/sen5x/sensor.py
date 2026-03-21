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
        f"FW {fw_major.value}.{fw_minor.value}{'-debug' if fw_debug.value else ''},"
        f"HW {hw_major.value}.{hw_minor.value}, PRT {prt_major.value}.{prt_minor.value}"
    )


async def start_measurement() -> None:
    if libsen5x.sen5x_start_measurement() < 0:
        raise RuntimeError("Failed to start measurement")
