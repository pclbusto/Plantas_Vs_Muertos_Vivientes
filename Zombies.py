import arcade

from enum import Enum

class Estados(Enum):
    CAMINANDO = 0
    COMIENDO = 1

class Zombie(arcade.Sprite):
    def __init__(self, filename=None, juego=None):
        super().__init__(filename=filename)
        self.scale = 0.45
        self.juego = juego
        self.energia = 0
        self.velocidad_movimiento = 0
        self.danio = 15
        self.tiempo_mordida = 0
        self.timer_evento = 0
        self.estado = Estados.CAMINANDO

    def update(self):
        if self.energia < 0:
            self.kill()
        if self.estado == Estados.CAMINANDO:
            lista_plantas = self.collides_with_list(self.juego.lista_plantas)
            if lista_plantas:
                self.estado = Estados.COMIENDO
                self.center_x = 0
                lista_plantas[0].registrar_danio()
                self.timer_evento = self.tiempo_mordida
            else:
                self.estado = Estados.CAMINANDO
        elif self.estado == Estados.COMIENDO:
            lista_plantas = self.collides_with_list(self.juego.lista_plantas)
            if lista_plantas:
                if self.timer_evento == 0:
                    # muerde y reinicia el tiempo para morder de nuevo
                    lista_plantas[0].registrar_danio()
                    self.timer_evento = self.tiempo_mordida
            else:
                self.estado = Estados.CAMINANDO
                self.change_x = self.velocidad_movimiento
                self.center_x += self.change_x


    def registrar_danio(self, danio):
        self.energia -= danio

class BrownCoatZombie(Zombie):
    def __init__(self, juego, rectangulo_posicion):
        super().__init__(filename="imagenes/zombies/Browncoat_Zombie.png", juego=juego)
        self.estado = Estados.CAMINANDO
        self
        self.change_x = -0.2
        self.energia = 190
        self.center_x = juego.get_size()[0]-(juego.get_size()[0]/4)
        self.center_y = rectangulo_posicion.center_y




