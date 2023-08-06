# FastyBird IoT MQTT connector

[![Build Status](https://badgen.net/github/checks/FastyBird/fb-mqtt-connector/master?cache=300&style=flast-square)](https://github.com/FastyBird/fb-mqtt-connector/actions)
[![Licence](https://badgen.net/github/license/FastyBird/fb-mqtt-connector?cache=300&style=flast-square)](https://github.com/FastyBird/fb-mqtt-connector/blob/master/LICENSE.md)
[![Code coverage](https://badgen.net/coveralls/c/github/FastyBird/fb-mqtt-connector?cache=300&style=flast-square)](https://coveralls.io/r/FastyBird/fb-mqtt-connector)

![PHP](https://badgen.net/packagist/php/FastyBird/fb-mqtt-connector?cache=300&style=flast-square)
[![Latest stable](https://badgen.net/packagist/v/FastyBird/fb-mqtt-connector/latest?cache=300&style=flast-square)](https://packagist.org/packages/FastyBird/fb-mqtt-connector)
[![Downloads total](https://badgen.net/packagist/dt/FastyBird/fb-mqtt-connector?cache=300&style=flast-square)](https://packagist.org/packages/FastyBird/fb-mqtt-connector)
[![PHPStan](https://img.shields.io/badge/PHPStan-enabled-brightgreen.svg?style=flat-square)](https://github.com/phpstan/phpstan)

![Python](https://badgen.net/pypi/python/fastybird-fb-mqtt-connector?cache=300&style=flat-square)
[![Python latest stable](https://badgen.net/pypi/v/fastybird-fb-mqtt-connector?cache=300&style=flat-square)](https://pypi.org/project/fastybird-fb-mqtt-connector/)
[![Python downloads month](https://img.shields.io/pypi/dm/fastybird-fb-mqtt-connector?cache=300&style=flat-square)](https://pypi.org/project/fastybird-fb-mqtt-connector/)
[![Black](https://img.shields.io/badge/black-enabled-brightgreen.svg?style=flat-square)](https://github.com/psf/black)
[![MyPy](https://img.shields.io/badge/mypy-enabled-brightgreen.svg?style=flat-square)](http://mypy-lang.org)

## What is FastyBird IoT MQTT connector?

FB MQTT connector is a combined [FastyBird](https://www.fastybird.com) [IoT](https://en.wikipedia.org/wiki/Internet_of_things) extension which is integrating [MQTT](https://mqtt.org) protocol via [FastyBird MQTT Convention](https://github.com/FastyBird/mqtt-convention) for connected devices

[FastyBird](https://www.fastybird.com) [IoT](https://en.wikipedia.org/wiki/Internet_of_things) FB MQTT connector is
an [Apache2 licensed](http://www.apache.org/licenses/LICENSE-2.0) distributed extension, developed
in [PHP](https://www.php.net) with [Nette framework](https://nette.org) and in [Python](https://python.org).

### Features:

- FB MQTT v1 convention devices support
- FB MQTT connector management for [FastyBird](https://www.fastybird.com) [IoT](https://en.wikipedia.org/wiki/Internet_of_things) [devices module](https://github.com/FastyBird/devices-module)
- FB MQTT device management for [FastyBird](https://www.fastybird.com) [IoT](https://en.wikipedia.org/wiki/Internet_of_things) [devices module](https://github.com/FastyBird/devices-module)
- [{JSON:API}](https://jsonapi.org/) schemas for full api access
- Integrated connector Python worker

## Requirements

PHP part of [FastyBird](https://www.fastybird.com) FB MQTT connector is tested against PHP 7.4
and [ReactPHP http](https://github.com/reactphp/http) 0.8 event-driven, streaming plaintext HTTP server
and [Nette framework](https://nette.org/en/) 3.0 PHP framework for real programmers

Python part of [FastyBird](https://www.fastybird.com) FB MQTT connector is tested against [Python 3.7](http://python.org)

## Installation

### Manual installation

#### Application backend in PHP

The best way to install **fastybird/fb-mqtt-connector** is using [Composer](http://getcomposer.org/):

```sh
composer require fastybird/fb-mqtt-connector
```

#### Application workers in Python

The best way to install **fastybird-fb-mqtt-connector** is using [Pip](https://pip.pypa.io/en/stable/):

```sh
pip install fastybird-fb-mqtt-connector
```

### Marketplace installation

You could install this connector in your [FastyBird](https://www.fastybird.com) [IoT](https://en.wikipedia.org/wiki/Internet_of_things) application under marketplace section

## Documentation

Learn how to consume & publish messages in [documentation](https://github.com/FastyBird/fb-mqtt-connector/blob/master/.docs/en/index.md).

***
Homepage [https://www.fastybird.com](https://www.fastybird.com) and repository [https://github.com/FastyBird/fb-mqtt-connector](https://github.com/FastyBird/fb-mqtt-connector).
