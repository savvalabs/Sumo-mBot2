import cyberpi as cpi
import mbuild
import time

VEL_ATAQUE     = 100
VEL_BUSCAR     = 40
VEL_ESCAPE     = 80
DIST_RIVAL     = 40
T_ESCAPE_RETRO = 0.5
T_ESCAPE_GIRO  = 0.5

BUSCAR  = "BUSCAR"
ATACAR  = "ATACAR"
ESCAPAR = "ESCAPAR"

estado         = BUSCAR
direccion_giro = 1

sin_rival_count = 0
borde_count     = 0

CONFIRMACIONES_BORDE    = 3
CONFIRMACIONES_SIN_RIVAL = 40

def detener():
    cpi.mbot2.EM_stop(port="all")

def avanzar(vel):
    cpi.mbot2.forward(speed=vel)

def retroceder(vel):
    cpi.mbot2.backward(speed=vel)

def girar_derecha(vel):
    cpi.mbot2.turn_right(speed=vel)

def girar_izquierda(vel):
    cpi.mbot2.turn_left(speed=vel)

def hay_rival():
    try:
        distancia = mbuild.ultrasonic2.get(1)
        if distancia is not None and 0 < distancia < DIST_RIVAL:
            return True
    except Exception:
        pass
    return False

def hay_borde():
    try:
        izq = mbuild.quad_rgb_sensor.get_color_sta(1, 1)
        der = mbuild.quad_rgb_sensor.get_color_sta(2, 1)
        if izq == "black" or der == "black":
            return True
    except Exception:
        pass
    return False

def indicar_estado(est):
    cpi.console.clear()
    if est == BUSCAR:
        cpi.led.on(0, 0, 255)
        cpi.console.print("BUSCAR")
    elif est == ATACAR:
        cpi.led.on(255, 0, 0)
        cpi.console.print("ATACAR!")
    elif est == ESCAPAR:
        cpi.led.on(255, 165, 0)
        cpi.console.print("ESCAPAR")

def cuenta_regresiva():
    cpi.console.clear()
    cpi.console.print("Robot Sumo")
    for i in range(3, 0, -1):
        cpi.console.print(str(i) + "...")
        cpi.led.on(255, 255, 0)
        time.sleep(0.5)
        cpi.led.off()
        time.sleep(0.5)
    cpi.console.print("LUCHA!")
    time.sleep(0.3)

def modo_buscar():
    global direccion_giro, borde_count
    indicar_estado(BUSCAR)

    if direccion_giro == 1:
        girar_derecha(VEL_BUSCAR)
    else:
        girar_izquierda(VEL_BUSCAR)

    time.sleep(0.05)

    if hay_borde():
        borde_count += 1
        if borde_count >= CONFIRMACIONES_BORDE:
            borde_count = 0
            direccion_giro *= -1
            return ESCAPAR
    else:
        borde_count = 0

    if hay_rival():
        return ATACAR

    return BUSCAR

def modo_atacar():
    global sin_rival_count, borde_count
    indicar_estado(ATACAR)
    avanzar(VEL_ATAQUE)
    time.sleep(0.05)

    if hay_borde():
        borde_count += 1
        if borde_count >= CONFIRMACIONES_BORDE:
            borde_count = 0
            return ESCAPAR
    else:
        borde_count = 0

    if not hay_rival():
        sin_rival_count += 1
        if sin_rival_count >= CONFIRMACIONES_SIN_RIVAL:
            sin_rival_count = 0
            return BUSCAR
    else:
        sin_rival_count = 0

    return ATACAR

def modo_escapar():
    global direccion_giro, borde_count, sin_rival_count
    indicar_estado(ESCAPAR)
    borde_count     = 0
    sin_rival_count = 0

    retroceder(VEL_ESCAPE)
    time.sleep(T_ESCAPE_RETRO)

    if direccion_giro == 1:
        girar_derecha(VEL_ESCAPE)
    else:
        girar_izquierda(VEL_ESCAPE)
    time.sleep(T_ESCAPE_GIRO)

    detener()
    time.sleep(0.1)
    return BUSCAR

cpi.console.clear()
cpi.console.print("Presiona A")
cpi.led.on(255, 255, 255)

while not cpi.controller.is_press('a'):
    time.sleep(0.1)

cpi.led.on(0, 255, 0)
cuenta_regresiva()

while True:
    if estado == BUSCAR:
        estado = modo_buscar()
    elif estado == ATACAR:
        estado = modo_atacar()
    elif estado == ESCAPAR:
        estado = modo_escapar()
    else:
        estado = BUSCAR
