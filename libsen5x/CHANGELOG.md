# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Changes for this port

- Hal init no longer leaks descriptors and returns the descriptor on call
- Split functions with delays to use asyncio delays in Python code instead

## [0.2.0] - 2022-03-30

Add support for SEN50

## [0.1.0] - 2022-01-05

Initial release

[0.2.0]: https://github.com/Sensirion/raspberry-pi-i2c-sen5x/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/Sensirion/raspberry-pi-i2c-sen5x/releases/tag/0.1.0
