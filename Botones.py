'''
Este script es el encargado de tener todo los botos del juego.
como tipos de botones tenemos los de semillas que estan al costado izquierdo de la pantalla. estos botones ademas
de responder al click tienen que evaluar si estan disponibles para hacer algo. Los botones de semillas tienen dos
condiciones que evaluar para ver si puede ejecutar si accione. Primero que el tiempo de cadencia para efectuar
su operacion este ok. Lo segundo es que los botones de semilas tienen que ver si hay soles disponibles para poder
ejecutar su accion.
'''
import arcade
import Plantas

class BotonGenerico(arcade.Sprite):

    def __init__(self, filename=None):
        super().__init__(filename=filename)
        self.scale = 0.25
        self.cadencia = 100
        self.contador = 0
        self.danio = 5
        self.costo = 4

    def on_click(self):
        pass

    def esta_mouse_arriba(self, x: float, y: float):
        if self.collides_with_point((x,y)):
            return True
        else:
            return False

class BotonPeashooterSeed(BotonGenerico):
    def __init__(self):
        super().__init__(filename="imagenes/botones/PeashooterSeed-b.png")
        self.scale = 0.25
        self.cadencia = 100
        self.contador = 0
        self.danio = 5
        self.costo = 4


    def update(self):
        if self.contador < self.cadencia:
            self.contador += 1

    def on_click(self):
        return Plantas.PeaShooter()

class BotonSunflowerSeed(BotonGenerico):
    def __init__(self):
        super().__init__(filename="imagenes/botones/SunflowerSeed-b.png")
        self.scale = 0.25
        self.cadencia = 80
        self.contador = 0
        self.danio = 0
        self.costo = 2

    def update(self):
        if self.contador < self.cadencia:
            self.contador += 1

    def on_click(self):
        return Plantas.SunFlower()


