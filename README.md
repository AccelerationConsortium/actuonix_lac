# Package name: actuonix_lac
Python controller for Actuonix Linear Actuator Control Board
Modified from https://github.com/DamnedFacts/actuonix-lac

# Tested on
Actuonix L16-P Linear Actuators with 5-wire connectors.

    https://www.actuonix.com/l16-p
Actuonix Linear Actuator Control (LAC) Board.

    https://www.actuonix.com/lac
Connect the actuator to the LAC and the LAC to your computer using a mini-USB cable.

# Supported actuator strokes
The same LAC board drives multiple actuator lengths. This package has been used with three stroke variants:

| Stroke  | mm per count (stroke / 1023) |
|---------|------------------------------|
| 100 mm  | ~0.0978 mm                   |
| 200 mm  | ~0.1956 mm                   |
| 300 mm  | ~0.2933 mm                   |

The LAC always uses a 10-bit position scale `[0, 1023]` over the full stroke, so the conversion is:

    count    = round(distance_mm * 1023 / stroke_mm)
    distance = count * stroke_mm / 1023

Avoid commanding `0` or `1023` — those hit the mechanical end stops. Use small buffers (e.g. `90` / `950`) instead.

# Installation

## Option A — uv (recommended)
[uv](https://docs.astral.sh/uv/) handles the virtualenv and dependency resolution in one step.

    # from the repo root
    uv venv
    uv pip install -e .
    uv pip install "pyusb>=1.3.1" "libusb>=1.0.28"

Activate with `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS/Linux), or just prefix commands with `uv run`:

    uv run python src/pylac.py

## Option B — conda

    conda install -c conda-forge pyusb libusb
    pip install -e .

## Option C — pip

    pip install -e .
    pip install libusb

# Additional Windows setup
1. Install the LAC driver / configuration utility:

        https://www.actuonix.com/assets/images/Actuonix%20LAC%20Configuration%20Utility-24-Setup.zip

2. Double-check the VendorID and ProductID under
   Device Manager → "Custom USB Devices" → "WinUSB Devices" → "Hardware Ids":

        USB\VID_04D8&PID_FC5F
        VID = 0x04d8
        PID = 0xfc5f

   The device must be bound to the WinUSB driver for `pyusb` to talk to it.
