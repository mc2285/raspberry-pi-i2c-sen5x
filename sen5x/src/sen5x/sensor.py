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
