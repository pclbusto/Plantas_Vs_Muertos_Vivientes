"""
Planta vs No Muertos (Lawn of the deads)
Clase que representa el juego en su totalidad. Lleva la ejecucion del juego con el hilo pricipal de ejecucion.
Controla el dibujado de las diferentes listas de sprites, los eventos de mouse y el llamado de actualizacion del
estado general del juego.
Debe gestionar las diferentes ventas que tiene el juego.


"""
import random
import arcade
import os
from Botones import *

PLAYER_SCALING = 1
COIN_SCALING = 0.25

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Plantas vs Muertos Vivientes"



class PlantaVsNoMuertos(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        # Background image will be stored in this variable

        self.background = None


        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.button_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)


    def setup(self):
        """ Set up the game and initialize the variables. """


        # Load the background image. Do this in the setup so we don't keep reloading it all the time.

        # Image from:

        # https://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html

        self.background = arcade.load_texture("imagenes/fondos/dia-jardin-pasto.png")


        # Sprite lists
        self.plant_list = arcade.SpriteList()
        # self.zombies_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        # self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
        #                                    PLAYER_SCALING)
        # self.player_sprite.center_x = 50
        # self.player_sprite.center_y = 50
        # self.player_list.append(self.player_sprite)
        seed = BotonPeashooterSeed()
        sun = BotonSunflowerSeed()

        self.administrar_lista_botones(seed)
        self.administrar_lista_botones(sun)

    def administrar_lista_botones(self, boton):
        '''
        chequea cuantos botonoes estan cargados para poder calcular la pos del nuevo boton
        asumiendo que todo los botones de semillas tienen el mismo tamanio
        '''
        pos_y = self.height - boton.height-(boton.height*len(self.button_list))
        pos_x = 50
        boton.left = pos_x
        boton.bottom = pos_y
        self.button_list.append(boton)
        self.recuadro = arcade.Sprite(filename="imagenes/botones/seleccionado.png")
        self.recuadro.visible = False
        self.recuadro.scale = 0.25
        self.aux = None
        self.estado = "nada"

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        # This command has to happen before we start drawing
        self.clear()


        # Draw the background texture

        arcade.draw_lrwh_rectangle_textured(0, 0,

                                            SCREEN_WIDTH, SCREEN_HEIGHT,

                                            self.background)


        # Draw all the sprites.
        self.button_list.draw()
        self.recuadro.draw()
        self.plant_list.draw()

        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        boton_aux = None

        if self.estado == "boton_clickeado":
            self.aux.center_x = x
            self.aux.center_y = y

        elif self.estado == "nada":

            for boton in self.button_list:
                if boton.esta_mouse_arriba(x=x, y=y):
                    boton_aux = boton
            if boton_aux :
                self.recuadro.center_y = boton_aux.center_y
                self.recuadro.center_x = boton_aux.center_x
                self.recuadro.visible = True
            else:
                self.recuadro.visible = False



    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        '''
        revisar que objeto se va a hacer cargo del click. Para esto preguntamos de los objecto clickeables quien esta
        dentro de las coordenas donde se hizo click y trabajar con este objeto.
        '''
        boton_aux = None
        for boton in self.button_list:
            if boton.esta_mouse_arriba(x=x, y=y):
                boton_aux = boton
        if boton_aux:
            self.aux = boton_aux.on_click()
            self.plant_list.append(self.aux)
            self.estado = "boton_clickeado"


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on the coin sprites (The sprites don't do much in this
        # example though.)
        pass


def main():
    """ Main function """
    window = PlantaVsNoMuertos(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()