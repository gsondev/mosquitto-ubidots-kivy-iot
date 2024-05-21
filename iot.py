from _thread import start_new_thread
import time

from kivy.clock import mainthread
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import Screen

from internal_comm import Listener, Publisher
from external_comm import UbidotsPublisher


class IoT(Screen):
    estadoLuz = BooleanProperty(False)
    imagen_luz = StringProperty('light_off.png')
    imagen_termometro = StringProperty('thermometer.jpg')
    temperatura = NumericProperty(45)
    temperatura_str = StringProperty('45°C')

    def __init__(self, **kw):
        super().__init__(**kw)
        escuchador = Listener(self)
        try:
            start_new_thread(escuchador.start, ())
            start_new_thread(self.update_temperature, ())
        except Exception as ex:
            print("Error: no se pudo iniciar el hilo. ex: {}".format(ex))


    def alternarLuz(self):
        Publisher.send_message('alternar_luz')

    def updateTemperature(self):
        Publisher.send_message('update_temperature')
    
    @mainthread
    def procesarMensajeLuz(self, msg):
        print(f'Recibido: {msg}')
        if msg == 'alternar_luz':
            self.estadoLuz = not self.estadoLuz
            if self.estadoLuz:
                print('Encendiendo luz')
                self.imagen_luz = 'light_on.png'
                UbidotsPublisher.send_message('lampara', 1)
            else:
                print('Apagando luz')
                self.imagen_luz = 'light_off.png'
                UbidotsPublisher.send_message('lampara', 0)
        else:
            if self.temperatura < 40:
                self.imagen_termometro = 'thermometer_cold.jpg'
            elif self.temperatura < 50:
                self.imagen_termometro = 'thermometer.jpg'
            else:
                self.imagen_termometro = 'thermometer_hot.jpg'
            UbidotsPublisher.send_message('temperature', self.temperatura)
    
    ## Método que actualiza la temperatura
    def update_temperature(self):
        while True:
            time.sleep(1)
            if self.estadoLuz:
                self.temperatura += 1
            else:
                self.temperatura -= 1
            if self.temperatura > 53:
                self.temperatura = 53
            if self.temperatura < 37:
                self.temperatura = 37
            self.temperatura_str = f'{self.temperatura}°C'
            self.updateTemperature()