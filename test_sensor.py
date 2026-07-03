import cyberpi as cpi
import mbuild
import time

cpi.console.clear()
cpi.console.print("Test ultrasonido")

while True:
    try:
        d = mbuild.ultrasonic2.get(1)
        cpi.console.clear()
        cpi.console.print("Dist: " + str(d))
    except Exception as e:
        cpi.console.clear()
        cpi.console.print("Error: " + str(e))
    time.sleep(0.5)
