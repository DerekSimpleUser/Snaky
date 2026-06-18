#################################################################################
# Copyright (C) 2026 Binryan-void y Patagonian Boy
#
# Este programa es software libre: puedes redistribuirlo y/o modificarlo
# bajo los terminos de la Licencia Publica General GNU publicada por la 
# Free Software Foundation, ya sea la version 3 de la Licencia o 
# (a tu eleccion) cualquier version posterior
#
# Este programa se distribuye con la esperanza de que sea util, pero 
# SIN GARANTIA ALGUNA; ni siquiera garantia implicita de 
# MERCANTILIDAD o APTITUD PARA UN PROPOSITO DETERMINADO.
# Consulte la Licencia Publica General GNU para obtener mas detalles.
#
# Deberias haber recibido una copia de la Licencia Publica General GNU 
# junto con este programa. Si no es asi, consulta <https://www.gnu.org/licenses/>.
##################################################################################

import curses
import random
import os

def juego(ventana):
    curses.curs_set(0)  # Ocultar cursor
    ventana.nodelay(1)  # No bloquear al esperar input
    ventana.timeout(100)  # Velocidad del juego (ms)

    max_y, max_x = ventana.getmaxyx()  # Tamaño de la ventana
    serpiente = [[max_y // 2, max_x // 4]]
    comida = [max_y // 2, max_x // 2]
    ventana.addstr(comida[0], comida[1], ' ')
    puntaje:int = 0

    # borde del juego/mapa
    for i in range(1, max_x):
        ventana.addch(max_y-2, i, '-')
        ventana.addch(0, i, '-')
    for j in range(1, max_y):
        ventana.addch(j, max_x-2, '|')
        ventana.addch(j, 0, '|')

    dx = 1
    dy = 0
    
    direcciones = {
        "Arriba": [ord('W'), ord('w'), curses.KEY_UP],
        "Abajo": [ord('S'), ord('s'), curses.KEY_DOWN],
        "Izquierda": [ord('A'), ord('a'), curses.KEY_LEFT],
        "Derecha": [ord('D'), ord('d'), curses.KEY_RIGHT]
    }

    while True:
        tecla = ventana.getch()
        if tecla in direcciones["Arriba"] and dy == 0:
            dx, dy = 0, -1
        elif tecla in direcciones["Abajo"] and dy == 0:
            dx, dy = 0, 1
        elif tecla in direcciones["Izquierda"] and dx == 0:
            dx, dy = -1, 0
        elif tecla in direcciones["Derecha"] and dx == 0:
            dx, dy = 1, 0

        # Nueva cabeza
        nueva_cabeza = [serpiente[0][0] + dy, serpiente[0][1] + dx]
        serpiente.insert(0, nueva_cabeza)

        # Colisión con bordes o consigo misma
        if (nueva_cabeza[0] in [0, max_y] or
            nueva_cabeza[1] in [0, max_x] or
            nueva_cabeza in serpiente[1:]):
            break

        # Comer comida que se come con la boca
        if nueva_cabeza == comida:
            comida = [random.randint(3, max_y - 5), random.randint(3, max_x - 5)]
            puntaje += 1
            ventana.addstr(comida[0], comida[1], ' ')
        else:
            # Quitar cola
            cola = serpiente.pop()
            ventana.addch(cola[0], cola[1], ' ')

        ventana.addch(serpiente[0][0], serpiente[0][1], curses.ACS_CKBOARD)
    return puntaje


def limpiar():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    limpiar()
    print("-~"*15, "M~E~N~U", "~-"*15)
    descicion = input("Quieres jugar? (s/n) \n=>> ").lower()
    if descicion == 's':
        limpiar()
        puntos = curses.wrapper(juego)
        print("===*"*10)
        print(f"tu putaje final es {puntos}")

if __name__ == "__main__":
    main()
