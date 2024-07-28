
import arcade
from enum import Enum

class Planta(arcade.Sprite):
    def __init__(self, filename=None, juego=None):
        super().__init__(filename=filename)
        self.scale = 0.35
        self.alpha = 200
        self.timer = 0
        self.juego = juego

    def accion(self):
        pass

class SunFlower(Planta):
    def __init__(self, juego=None):
        super().__init__(filename="imagenes/plantas/Sunflower.png", juego=juego)
        self.timer = 60 * 5
        self.contador = self.timer

    def update(self):
        self.contador -=1
        if self.contador == 0:
            self.accion()
            self.contador = self.timer
    def accion(self):
        sol = Sun(self, extra_y=self.center_y)
        self.juego.agregar_sol(sol)
        self.timer


class PeaShooter(Planta):
    def __init__(self, juego=None):
        super().__init__(filename="imagenes/plantas/Peashooter.png", juego=juego)

class Pea(Planta):
    def __init__(self, juego=None):
        super().__init__(filename="imagenes/plantas/Pea.png", juego=juego)
        self.change_x = 4
        self.alpha = 255
    def update(self):
        self.center_x += self.change_x

class Threepeater(Planta):
    def __init__(self, juego=None):
        super().__init__(filename="imagenes/plantas/Threepeater.png", juego=juego)
        self.change_x = 4
        self.alpha = 255
    def update(self):
        self.center_x += self.change_x

class Estados_sol(Enum):
    CAYENDO = 0
    GUARDANDO = 1

class Sun(arcade.Sprite):
    def __init__(self, cuandrado, extra_y=None):
        super().__init__(filename="imagenes/plantas/Sun.png")
        self.center_x = cuandrado.center_x
        if extra_y:
            self.center_y = extra_y
        else:
            self.center_y = 900
        self.change_y = 1
        self.cuadrado = cuandrado
        self.scale = 0.35
        self.estado = Estados_sol.CAYENDO
        hb = self.hit_box
        self.meta= None
        # reduccion del 50% del tamaño del hitbox para que no haya solapamientos y sea mas preciso el click
        ll = list(list(e*0.5 for e in sub) for sub in hb)
        self.hit_box = tuple(tuple(sub) for sub in ll)

    def update(self):
        if self.estado == Estados_sol.CAYENDO:
            if self.center_y != self.cuadrado.center_y:
                self.center_y -= self.change_y
        if self.estado == Estados_sol.GUARDANDO:
            self.center_x += self.change_x
            self.center_y += self.change_y
            if self.collides_with_sprite(self.meta):
                self.kill()


    def guardar_en(self, meta):
        dx = meta.center_x - self.center_x
        dy = meta.center_y - self.center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        # Normalize direction vector
        if distance > 0:
            dx /= distance
            dy /= distance
        self.change_x = dx * 20
        self.change_y = dy * 20
        self.estado = Estados_sol.GUARDANDO
        self.meta = meta





