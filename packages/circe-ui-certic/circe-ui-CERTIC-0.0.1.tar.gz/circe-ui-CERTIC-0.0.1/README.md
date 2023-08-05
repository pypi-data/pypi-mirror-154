# Circe UI

This  is the web UI extracted from the [Circe server](https://git.unicaen.fr/fnso/i-fair-ir/circe-server).

## Pre-requisites

- Python >= 3.9
- A running Circe Server

## Installation

    make venv
    make install

## Configuration

Add a .env file and customize variables:

    CIRCEUI_HOST=127.0.0.1
    CIRCEUI_PORT=8001
    CIRCEUI_CRYPT_KEY=changeme
    CIRCEUI_CIRCE_ENDPOINT=http://circe.unicaen.fr/
    CIRCEUI_CIRCE_APP=changeme
    CIRCEUI_CIRCE_KEY=changeme

## How to run

    circeui