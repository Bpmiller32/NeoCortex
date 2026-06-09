# PsTas

A simple TAS (tool-assisted speedrun) bot for the PlayStation 5, starting with
Crash Bandicoot N-Sane Trilogy. The long-term goal is to build clean, reusable
parts that could later support reinforcement learning on the PC version.

## Design in one paragraph

We cannot react to the screen frame-by-frame because the video feedback loop is
too slow. So input is played open-loop: a fixed, frame-indexed script is sent
blind, and it works because the game is deterministic from a known start. Video
is only checked at sparse checkpoints (level start, after a load, a clear visual
landmark) where we are allowed to wait. At each checkpoint we verify the screen
matches what we expect, then play the next segment or retry.

## Modules

- controller: presses DS4 buttons through a Raspberry Pi Pico and optocouplers.
- capture: grabs video frames from the Elgato HD60 S.
- detect: game-specific checks on frames (loading, death, timer). Not built yet.
- timeline: the input sheet format and parser. Not built yet.
- runner: plays segments and checks detectors at checkpoints. Not built yet.
- tools: small utilities like latency measurement. Not built yet.

Only the detect module and the input sheets are Crash-specific. Everything else
is meant to be reusable for other games.

## Hardware

- A used DualShock 4 (DS4), with wires soldered to the button contacts.
- An Unexpected Maker TinyS2 (ESP32-S2), the timing authority for input.
- Eight PC817 optocouplers, one per button, that act as the button switches.
- Eight 220 ohm resistors, one per optocoupler LED.
- Optional: eight indicator LEDs (plus eight more 220 ohm resistors) that light
  when a button is pressed, so you can see what the bot is doing.
- An Elgato HD60 S capture card feeding the PC the PlayStation video.

A full visual wiring guide is in docs/wiring.html (open it in a browser, or
print it to PDF).

### TinyS2 pin map

Driving a TinyS2 pin HIGH turns its optocoupler on, which presses the button.
Wire each optocoupler to match this map. These names must match the firmware.

- GPIO5: up
- GPIO6: down
- GPIO7: left
- GPIO8: right
- GPIO9: cross (the X button, used to jump)
- GPIO14: circle
- GPIO17: square
- GPIO18: triangle

The TinyS2 only breaks out these general-purpose pins: GPIO 0, 4, 5, 6, 7, 8, 9,
14, 17, 18, 33, 35, 36, 37, 38. We use eight of them above. Avoid GPIO1 (RGB
LED), GPIO2 (LED power), GPIO3 (battery monitor), GPIO43 and GPIO44 (serial),
and GPIO0 (boot button). Match the GPIO numbers printed on the board silkscreen.

### Per-button wiring

For each button, repeat this same circuit:

- TinyS2 GPIO pin -> 220 ohm resistor -> PC817 pin 1 (anode).
- PC817 pin 2 (cathode) -> TinyS2 GND.
- PC817 pin 4 (collector) -> the DS4 button signal pad.
- PC817 pin 3 (emitter) -> the DS4 button common rail.

Optional indicator LED, wired in parallel off the same GPIO pin:

- TinyS2 GPIO pin -> 220 ohm resistor -> LED long leg (anode).
- LED short leg (cathode) -> TinyS2 GND.

We confirm which DS4 contact is the common rail with a multimeter before
soldering. Leave the DS4 powered normally over its own USB; we only tap buttons.

## Setup

Install Python dependencies:

    pip install -r requirements.txt

### Flashing the TinyS2

The TinyS2 needs MicroPython on it once, then our firmware file on top.

Easiest path, using Thonny (a free editor at thonny.org):

1. Plug the TinyS2 into USB-C.
2. In Thonny, open Tools -> Options -> Interpreter and pick MicroPython (ESP32).
3. Click the "Install or update MicroPython" link at the bottom of that window.
4. Choose your port and the Unexpected Maker TinyS2 board, then install.
   If it cannot connect, put the board in bootloader mode first: hold BOOT,
   tap RESET, release BOOT, then try again.
5. Back in Thonny, select the TinyS2 port as the interpreter. You should see
   the MicroPython prompt (>>>) in the shell.
6. Open controller/firmware/main.py, then File -> Save as -> MicroPython device,
   and save it as main.py. It now runs automatically when the board powers on.

Command line path instead, using esptool:

1. pip install esptool
2. Download the TinyS2 MicroPython firmware (.bin) from unexpectedmaker.com or
   micropython.org/download/UM_TINYS2.
3. Bootloader mode: hold BOOT, tap RESET, release BOOT.
4. esptool.py --chip esp32s2 --port <PORT> erase_flash
5. esptool.py --chip esp32s2 --port <PORT> --baud 460800 write_flash -z 0x1000 <firmware.bin>
6. Tap RESET, then upload main.py with Thonny or mpremote.

On macOS the port looks like /dev/cu.usbmodemXXXX.

## Testing each module on its own

Run these from the project root.

Controller (no video needed). This makes Crash jump ten times. Replace the port
with your Pico's serial port (on macOS it looks like /dev/tty.usbmodemXXXX):

    python -m controller.demo_jump /dev/tty.usbmodemXXXX

Capture. This grabs frames, saves a few to disk, and prints the frame rate.
Replace the index with whichever device the Elgato shows up as:

    python -m capture.demo_save 0

## Status

- controller: scaffolded, ready to test when the Pico and DS4 are wired.
- capture: scaffolded, ready to test when the Elgato is connected.
- Everything else: not started.
