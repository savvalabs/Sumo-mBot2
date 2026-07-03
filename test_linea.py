import cyberpi as cpi
import mbuild
import time

cpi.console.clear()
cpi.console.print("Test linea")

while True:
    try:
        izq = mbuild.quad_rgb_sensor.get_color_sta(1, 1)
        der = mbuild.quad_rgb_sensor.get_color_sta(2, 1)
        cpi.console.clear()
        cpi.console.print("I: " + str(izq))
        cpi.console.print("D: " + str(der))
    except Exception as e:
        cpi.console.clear()
        cpi.console.print("Err: " + str(e))
    time.sleep(0.3)
