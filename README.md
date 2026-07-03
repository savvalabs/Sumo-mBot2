# 🤖 mBot2 Sumo Robot

Autonomous sumo robot programmed in Python (MicroPython) for the **Makeblock mBot2**.

## How it works

The robot operates in 3 states that switch automatically based on sensor input:

- 🔵 **SEARCH** — Spins slowly until the opponent is detected by the ultrasonic sensor
- 🔴 **ATTACK** — Drives forward at full speed to push the opponent out of the ring
- 🟠 **ESCAPE** — If the black edge of the ring is detected, backs up and turns 180° to return to the center

## Repository structure

```
mbot2-sumo/
├── mbot2_sumo.py              # Main sumo program
├── README.md
└── tests/
    ├── test_ultrasonic.py     # Reads and prints ultrasonic distance
    ├── test_line_sensor.py    # Reads and prints line/edge sensor status
    └── list_sensor_methods.py # Lists all available methods on the line sensor
```

The `tests/` scripts are optional but recommended. mBot2 firmware versions vary,
and some sensor functions (`get_value`, `get_grey`, `get_color_sta`, etc.) may or
may not exist depending on your unit. Run these first to confirm which functions
work on your robot before trusting the main program.

## Required hardware

- mBot2 (CyberPi + Chassis)
- Ultrasonic sensor (port 1) — detects the opponent
- Quad RGB sensor (port 1) — detects the black edge of the ring

## Step-by-step: how to upload the code

1. **Install mBlock** (desktop app) if you haven't already: https://www.mblock.cc/en-us/download
2. **Connect the mBot2** to your computer via USB cable
3. Open mBlock and make sure the device is detected in the bottom-left device panel
4. In the top toolbar, switch from **Live mode** to **Upload mode** — this is critical.
   Live mode only runs code while connected to your PC; Upload mode saves the code
   permanently onto the robot so it works standalone in the ring
5. Click the **Python** tab (not Blocks) in the code editor
6. Paste the full contents of `mbot2_sumo.py`
7. Click **Upload** and wait for the confirmation
8. Disconnect the USB cable
9. Place the robot inside the sumo ring
10. Press the **A button** on the CyberPi screen to begin the 3-second countdown
11. The robot starts fighting automatically

### If you get sensor errors

If the screen shows something like `'module' object has no attribute 'xxxx'`,
your firmware version uses different method names. Upload the scripts inside
`tests/` one at a time to discover which functions actually exist on your unit,
then update `mbot2_sumo.py` accordingly.

## Adjustable parameters

| Parameter | Value | Description |
|---|---|---|
| `VEL_ATAQUE` | 100 | Attack speed (0-100) |
| `VEL_BUSCAR` | 40 | Search rotation speed |
| `VEL_ESCAPE` | 80 | Speed when escaping the edge |
| `DIST_RIVAL` | 40 | Distance in cm to detect the opponent |
| `CONFIRMACIONES_SIN_RIVAL` | 40 | Readings without opponent before returning to search (~2 sec) |
| `CONFIRMACIONES_BORDE` | 3 | Consecutive black readings before escaping |

## Line sensor behavior

The quad RGB sensor returns the string `"black"` when it detects the ring's black edge.
Three consecutive confirmations are used to avoid false positives on white flooring.

## Notes

- The code was developed and debugged live by testing each function directly on
  the robot, since the `cyberpi` and `mbuild` libraries only exist inside the
  mBot2 firmware — they cannot be run or linted on a regular computer.
- The correct functions for motor control are `cpi.mbot2.forward()`, `backward()`,
  `turn_left()`, `turn_right()`.
- The ultrasonic sensor is read with `mbuild.ultrasonic2.get(1)` using a numeric port.
- The line sensor is read with `mbuild.quad_rgb_sensor.get_color_sta(channel, port)`.
