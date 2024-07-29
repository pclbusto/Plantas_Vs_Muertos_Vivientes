
import arcade
from enum import Enum

class Planta(arcade.Sprite):
    def __init__(self, filename=None, juego=None):
        super().__init__(filename=filename)
        self.scale = 0.25
        self.timer = 0
        self.juego = juego
        self.puntos_vida = 0

    def accion(self):
        pass

    def update(self):
        if self.puntos_vida <= 0:
            self.kill()
        self.contador -= 1
        if self.contador == 0:
            self.accion()


    def registrar_danio(self, danio):
        self.puntos_vida -= danio

class SunFlower(Planta):
    def __init__(self, juego=None):
        super().__init__(filename="imagenes/plantas/Sunflower.png", juego=juego)
        self.timer = 60 * 5
        self.contador = self.timer
        self.puntos_vida = 60



    def accion(self):
        sol = Sun(self, extra_y=self.center_y)
        self.juego.agregar_sol(sol)
        self.contador = self.timer


class Pea(Planta):
    def __init__(self, juego, punto=None):
        super().__init__(filename="imagenes/plantas/Pea.png", juego=juego)
        self.change_x = 4
        self.danio = 20
        if punto:
            self.center_x = punto[0]
            self.center_y = punto[1]
        self.puntos_vida = 300

    def update(self):
        self.center_x += self.change_x
        lista_zombies = self.collides_with_list(self.juego.lista_zombies)
        if lista_zombies:
            lista_zombies[0].registrar_danio(self.danio)
            self.kill()
        if self.center_x >= self.juego.get_size()[0]-self.width:
            self.kill()

class PeaShooter(Planta):
    def __init__(self, juego):
        super().__init__(filename="imagenes/plantas/Peashooter.png", juego=juego)
        self.timer = 60 * 5
        self.contador = self.timer

    def accion(self):
        pea = Pea(juego=self.juego, punto=(self.center_x, self.center_y+(self.height/5)))
        self.juego.agregar_objeto(pea)
        self.contador = self.timer



class Threepeater(Planta):
    def __init__(self, juego=None):
        super().__init__(filename="imagenes/plantas/Threepeater.png", juego=juego)
        self.change_x = 4
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





