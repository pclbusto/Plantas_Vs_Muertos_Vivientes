
import arcade


class Planta(arcade.Sprite):
    def __init__(self, filename=None):
        super().__init__(filename=filename)
        self.scale = 0.20
        self.alpha = 200
class SunFlower(Planta):
    def __init__(self):
        super().__init__(filename="imagenes/plantas/Sunflower.png")

class PeaShooter(Planta):
    def __init__(self):
        super().__init__(filename="imagenes/plantas/Peashooter.png")

