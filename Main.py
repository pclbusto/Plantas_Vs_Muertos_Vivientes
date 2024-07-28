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

import Plantas
from Botones import *
from enum import Enum

PLAYER_SCALING = 1
SCREEN_WIDTH = 2100
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Plantas vs Muertos Vivientes"


class SunGenerator():
    '''
    El timer determina cuanto tiempo esperar hasta generar un sol.
    El timer se revisa cada vez que se actualiza el juego. Si se acabo el tiempo lanza un sol. El lugar por donde
    lanza el sol lo determina con la lista de cuadrados de la cuadricula del juebo. hace una selecicn aleatoria de en
    que cuadrado va a depositar el sol e inicializa el sol con las coordenadas para empezar y donde se va a detener.
    cuadrado
    '''

    def __init__(self, padre):
        self.timer = 60*2 #son milisegundos a 60 fps
        self.contador = 0
        self.timer_corriendo = False
        self.cuadricula = padre.get_cuadricula()
        self.padre = padre

    def comenzar_timer(self):
        self.timer_corriendo = True

    def update(self):
        if self.timer_corriendo:
            self.contador += 1
            if self.contador == self.timer:
                self.generar_sol()
                self.contador = 0



    def generar_sol(self):
        cuadrado = random.choice(self.cuadricula)
        sol = Plantas.Sun(cuadrado)
        self.padre.agregar_sol(sol)



class Estado(Enum):
    NADA = 0
    BTN_CLICKEADO = 1


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
        self.cuadricula = None
        self.button_list = None
        self.lista_ocupados = None
        self.boton_clickeado = None
        self.lista_soles = None
        self.lista_objetos_emitidos_por_plantas = None
        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.score_text = None
        self.generador_soles = None
        self.cartel_soles = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def get_cuadricula(self):
        return self.cuadricula

    def agregar_objeto(self, objeto):
        self.lista_objetos_emitidos_por_plantas.append(objeto)
    def agregar_sol(self, sol):

        self.lista_soles.append(sol)

    def setup(self):
        """ Set up the game and initialize the variables. """


        # Load the background image. Do this in the setup so we don't keep reloading it all the time.

        # Image from:

        # https://wallpaper-gallery.net/single/free-background-images/free-background-images-22.html

        self.background = arcade.load_texture("imagenes/fondos/dia-jardin-pasto.png")
        self.cartel_soles = Cartel_Sol()
        self.cartel_soles.center_x = 380
        self.cartel_soles.center_y = SCREEN_HEIGHT- 45

        # Sprite lists
        self.lista_plantas = arcade.SpriteList()
        # self.zombies_list = arcade.SpriteList()
        self.lista_ocupados = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.cuadricula = arcade.SpriteList()
        self.lista_soles = arcade.SpriteList()
        self.lista_objetos_emitidos_por_plantas = arcade.SpriteList()
        self.cuadricula.visible = False
        # Set up the player
        self.score = 0
        seed = BotonPeashooterSeed(self)
        sun = BotonSunflowerSeed(self)
        three = BotonThreepeaterSeed(self)
        self.pea = Plantas.Pea()
        self.pea.center_y =300


        self.administrar_lista_botones(seed)
        self.administrar_lista_botones(sun)
        self.administrar_lista_botones(three)
        self.generador_soles = SunGenerator(self)
        self.generador_soles.comenzar_timer()

        for x in range(0,9):
            for y in range (0,5):
                self.cuadricula.append(arcade.SpriteSolidColor(114, 138, (10, 10, 10,200)))
                self.cuadricula[len(self.cuadricula)-1].left = 118*x+386
                self.cuadricula[len(self.cuadricula)-1].top = 142*y+195



    def administrar_lista_botones(self, boton):
        '''
        chequea cuantos botones estan cargados para poder calcular la pos del nuevo boton
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
        self.estado = Estado.NADA

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
        self.lista_plantas.draw()
        self.cuadricula.draw()
        self.pea.draw()
        self.lista_soles.draw()
        self.cartel_soles.draw()
        self.lista_objetos_emitidos_por_plantas.draw()
        # Render the text
        arcade.draw_text(f"{self.score}", self.cartel_soles.center_x, self.cartel_soles.center_y-15, arcade.color.BLACK, 34)


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        boton_aux = None
        if self.estado == Estado.NADA:

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
        for boton in self.button_list:
            if boton.esta_mouse_arriba(x=x, y=y):
                self.aux = boton.on_click()
                self.lista_plantas.append(self.aux)
                self.estado = Estado.BTN_CLICKEADO
                self.boton_clickeado = boton
                return
        for sol in self.lista_soles:
            if sol.collides_with_point((x,y)):
                self.score += 1
                sol.guardar_en(self.cartel_soles)


    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if self.estado == Estado.BTN_CLICKEADO:
            self.aux.center_x = x
            self.aux.center_y = y

        return super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):

        if self.estado == Estado.BTN_CLICKEADO:
            '''tenemos un sprite creado que hay que soltar. detectamos con que hacemos colision y lo soltamos en el 
            centro del rectangulo que haga colision'''
            lista_colision = arcade.get_sprites_at_point((x,y), self.cuadricula)
            if lista_colision and lista_colision[0] not in self.lista_ocupados:
                self.lista_ocupados.append(lista_colision[0])
                self.aux.center_x = lista_colision[0].center_x
                self.aux.center_y = lista_colision[0].center_y
                self.aux.alpha = 255
                self.boton_clickeado.iniciar_temporizador()
            else:
                self.lista_plantas.pop()
                self.aux = None

            self.estado = Estado.NADA
        return super().on_mouse_release(x, y, button, modifiers)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on the coin sprites (The sprites don't do much in this
        # example though.)
        self.button_list.update()
        self.pea.update()
        self.generador_soles.update()
        self.lista_soles.update()
        self.lista_plantas.update()

def main():
    """ Main function """
    window = PlantaVsNoMuertos(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
