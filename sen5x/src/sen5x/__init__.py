import atexit
import ctypes
import logging

from ctypes import c_bool, c_int, c_int32, c_int16, c_int8, c_uint, c_uint32, \
    c_uint16, c_uint8, c_char, c_char_p, c_float, POINTER

libsen5x = ctypes.CDLL('libsen5x.so')


def _setup_ctypes() -> None:
    libsen5x.sensirion_i2c_hal_free.argtypes = []
    libsen5x.sensirion_i2c_hal_free.restype = c_int

    libsen5x.sensirion_i2c_hal_init.argtypes = [c_char_p]
    libsen5x.sensirion_i2c_hal_init.restype = c_int

    libsen5x.sensirion_i2c_get_descriptor.argtypes = []
    libsen5x.sensirion_i2c_get_descriptor.restype = c_int

    libsen5x.sen5x_device_reset.argtypes = []
    libsen5x.sen5x_device_reset.restype = c_int16

    libsen5x.sen5x_get_fan_auto_cleaning_interval.argtypes = [
        POINTER(c_uint32)]
    libsen5x.sen5x_get_fan_auto_cleaning_interval.restype = c_int16
    libsen5x.sen5x_get_fan_auto_cleaning_interval_finish.argtypes = [
        POINTER(c_uint32)]
    libsen5x.sen5x_get_fan_auto_cleaning_interval_finish.restype = c_int16

    libsen5x.sen5x_get_nox_algorithm_tuning_parameters.argtypes = [POINTER(c_int16), POINTER(
        c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16)]
    libsen5x.sen5x_get_nox_algorithm_tuning_parameters.restype = c_int16
    libsen5x.sen5x_get_nox_algorithm_tuning_parameters_finish.argtypes = [POINTER(c_int16), POINTER(
        c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16)]
    libsen5x.sen5x_get_nox_algorithm_tuning_parameters_finish.restype = c_int16

    libsen5x.sen5x_get_product_name.argtypes = [POINTER(c_uint8), c_uint8]
    libsen5x.sen5x_get_product_name.restype = c_int16
    libsen5x.sen5x_get_product_name_finish.argtypes = [
        POINTER(c_uint8), c_uint8]
    libsen5x.sen5x_get_product_name_finish.restype = c_int16

    libsen5x.sen5x_get_rht_acceleration_mode.argtypes = [POINTER(c_uint16)]
    libsen5x.sen5x_get_rht_acceleration_mode.restype = c_int16
    libsen5x.sen5x_get_rht_acceleration_mode_finish.argtypes = [c_uint16]
    libsen5x.sen5x_get_rht_acceleration_mode_finish.restype = c_int16

    libsen5x.sen5x_get_serial_number.argtypes = [POINTER(c_uint8), c_uint8]
    libsen5x.sen5x_get_serial_number.restype = c_int16
    libsen5x.sen5x_get_serial_number_finish.argtypes = [
        POINTER(c_uint8), c_uint8]
    libsen5x.sen5x_get_serial_number_finish.restype = c_int16

    libsen5x.sen5x_get_temperature_offset_parameters.argtypes = [
        POINTER(c_int16), POINTER(c_int16), POINTER(c_uint16)]
    libsen5x.sen5x_get_temperature_offset_parameters.restype = c_int16
    libsen5x.sen5x_get_temperature_offset_parameters_finish.argtypes = [
        POINTER(c_int16), POINTER(c_int16), POINTER(c_uint16)]
    libsen5x.sen5x_get_temperature_offset_parameters_finish.restype = c_int16

    libsen5x.sen5x_get_version.argtypes = [POINTER(c_uint8), POINTER(c_uint8), POINTER(
        c_bool), POINTER(c_uint8), POINTER(c_uint8), POINTER(c_uint8), POINTER(c_uint8)]
    libsen5x.sen5x_get_version.restype = c_int16
    libsen5x.sen5x_get_version_finish.argtypes = [POINTER(c_uint8), POINTER(c_uint8), POINTER(
        c_bool), POINTER(c_uint8), POINTER(c_uint8), POINTER(c_uint8), POINTER(c_uint8)]
    libsen5x.sen5x_get_version_finish.restype = c_int16

    libsen5x.sen5x_get_voc_algorithm_state.argtypes = [
        POINTER(c_uint8), c_uint8]
    libsen5x.sen5x_get_voc_algorithm_state.restype = c_int16
    libsen5x.sen5x_get_voc_algorithm_state_finish.argtypes = [
        POINTER(c_uint8), c_uint8]
    libsen5x.sen5x_get_voc_algorithm_state_finish.restype = c_int16

    libsen5x.sen5x_get_voc_algorithm_tuning_parameters.argtypes = [POINTER(c_int16), POINTER(
        c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16)]
    libsen5x.sen5x_get_voc_algorithm_tuning_parameters.restype = c_int16
    libsen5x.sen5x_get_voc_algorithm_tuning_parameters_finish.argtypes = [POINTER(c_int16), POINTER(
        c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16), POINTER(c_int16)]
    libsen5x.sen5x_get_voc_algorithm_tuning_parameters_finish.restype = c_int16

    libsen5x.sen5x_get_warm_start_parameter.argtypes = [POINTER(c_uint16)]
    libsen5x.sen5x_get_warm_start_parameter.restype = c_int16
    libsen5x.sen5x_get_warm_start_parameter_finish.argtypes = [
        POINTER(c_uint16)]
    libsen5x.sen5x_get_warm_start_parameter_finish.restype = c_int16

    libsen5x.sen5x_read_and_clear_device_status.argtypes = [POINTER(c_uint32)]
    libsen5x.sen5x_read_and_clear_device_status.restype = c_int16
    libsen5x.sen5x_read_and_clear_device_status_finish.argtypes = [
        POINTER(c_uint32)]
    libsen5x.sen5x_read_and_clear_device_status_finish.restype = c_int16

    libsen5x.sen5x_read_device_status.argtypes = [POINTER(c_uint32)]
    libsen5x.sen5x_read_device_status.restype = c_int16
    libsen5x.sen5x_read_device_status_finish.argtypes = [POINTER(c_uint32)]
    libsen5x.sen5x_read_device_status_finish.restype = c_int16

    libsen5x.sen5x_read_data_ready.argtypes = [POINTER(c_bool)]
    libsen5x.sen5x_read_data_ready.restype = c_int16
    libsen5x.sen5x_read_data_ready_finish.argtypes = [POINTER(c_bool)]
    libsen5x.sen5x_read_data_ready_finish.restype = c_int16

    libsen5x.sen5x_read_measured_pm_values.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(
        c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float)]
    libsen5x.sen5x_read_measured_pm_values.restype = c_int16
    libsen5x.sen5x_read_measured_pm_values_finish.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(
        c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float)]
    libsen5x.sen5x_read_measured_pm_values_finish.restype = c_int16

    libsen5x.sen5x_read_measured_values.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(
        c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float)]
    libsen5x.sen5x_read_measured_values.restype = c_int16
    libsen5x.sen5x_read_measured_values_finish.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float), POINTER(
        c_float), POINTER(c_float), POINTER(c_float), POINTER(c_float)]
    libsen5x.sen5x_read_measured_values_finish.restype = c_int16

    libsen5x.sen5x_set_fan_auto_cleaning_interval.argtypes = [c_uint32]
    libsen5x.sen5x_set_fan_auto_cleaning_interval.restype = c_int16

    libsen5x.sen5x_set_nox_algorithm_tuning_parameters.argtypes = [
        c_int16, c_int16, c_int16, c_int16, c_int16, c_int16]
    libsen5x.sen5x_set_nox_algorithm_tuning_parameters.restype = c_int16

    libsen5x.sen5x_set_rht_acceleration_mode.argtypes = [c_uint16]
    libsen5x.sen5x_set_rht_acceleration_mode.restype = c_int16

    libsen5x.sen5x_set_temperature_offset_parameters.argtypes = [
        c_int16, c_int16, c_uint16]
    libsen5x.sen5x_set_temperature_offset_parameters.restype = c_int16

    libsen5x.sen5x_set_voc_algorithm_state.argtypes = [
        POINTER(c_uint8), c_uint8]
    libsen5x.sen5x_set_voc_algorithm_state.restype = c_int16

    libsen5x.sen5x_set_voc_algorithm_tuning_parameters.argtypes = [
        c_int16, c_int16, c_int16, c_int16, c_int16, c_int16]
    libsen5x.sen5x_set_voc_algorithm_tuning_parameters.restype = c_int16

    libsen5x.sen5x_set_warm_start_parameter.argtypes = [c_uint16]
    libsen5x.sen5x_set_warm_start_parameter.restype = c_int16

    libsen5x.sen5x_start_fan_cleaning.argtypes = []
    libsen5x.sen5x_start_fan_cleaning.restype = c_int16

    libsen5x.sen5x_start_measurement.argtypes = []
    libsen5x.sen5x_start_measurement.restype = c_int16

    libsen5x.sen5x_start_measurement_without_pm.argtypes = []
    libsen5x.sen5x_start_measurement_without_pm.restype = c_int16

    libsen5x.sen5x_stop_measurement.argtypes = []
    libsen5x.sen5x_stop_measurement.restype = c_int16


def _cleanup() -> None:
    if libsen5x.sensirion_i2c_hal_free() < 0:
        logging.error("Failed to release file descriptor")


_setup_ctypes()
atexit.register(_cleanup)


def init_i2c(device_path: str) -> None:
    if (descriptor := libsen5x.sensirion_i2c_get_descriptor()) >= 0:
        logging.warning(f"Closing dangling I2C file descriptor: {descriptor}")
    if libsen5x.sensirion_i2c_hal_init(device_path.encode()) < 0:
        raise IOError(
            f"Failed to initialize I2C with device path: {device_path}")
