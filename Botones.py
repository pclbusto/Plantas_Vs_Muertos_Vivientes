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

    def __init__(self, filename=None, juego=None):
        super().__init__(filename=filename)
        self.scale = 0.25
        self.cadencia_limite = 10000
        self.cadencia = 0
        self.contador = 0
        self.costo = 4
        self.contador_activo = False
        self.juego = juego

    def on_click(self):
        pass

    def iniciar_temporizador(self):
        self.alpha = 50
        self.contador_activo = True
        self.contador = 0

    def esta_mouse_arriba(self, x: float, y: float):
        if self.collides_with_point((x,y)):
            return True
        else:
            return False

    def update(self):
        if self.contador_activo:
            if self.contador <= self.cadencia_limite - self.cadencia:
                self.contador += self.cadencia
                self.alpha = 255 *(self.contador/self.cadencia_limite)



class BotonPeashooterSeed(BotonGenerico):
    def __init__(self, juego=None):
        super().__init__(filename="imagenes/botones/PeashooterSeed-b.png", juego=juego)
        self.scale = 0.25
        self.cadencia = 10
        self.contador = 0
        self.danio = 5
        self.costo = 4


    def on_click(self):
        print("retornamos una planta PeaShooter")
        return Plantas.PeaShooter(self.juego)

class BotonSunflowerSeed(BotonGenerico):
    def __init__(self, juego = None):
        super().__init__(filename="imagenes/botones/SunflowerSeed-b.png", juego=juego)
        self.scale = 0.25
        self.cadencia = 20
        self.contador = 0
        self.costo = 2

    def on_click(self):
        print(self.juego)
        return Plantas.SunFlower(self.juego)


class BotonThreepeaterSeed(BotonGenerico):
    def __init__(self, juego = None):
        super().__init__(filename="imagenes/botones/ThreepeaterSeed-b.png", juego=juego)
        self.scale = 0.25
        self.cadencia = 5
        self.contador = 0
        self.danio = 5
        self.costo = 4

    def on_click(self):
        return Plantas.Threepeater()

class Cartel_Sol(arcade.Sprite):
    def __init__(self):
        super().__init__(filename="imagenes/plantas/SunCounter.png")
        self.scale = 1
