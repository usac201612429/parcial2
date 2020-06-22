from interfaz import *
from CLASScliente import *
from constantes import *

import time
import paho.mqtt.client as paho

'''FPRTH Configuracion del cliente MQTT'''


#FPRTH definiendo las funciones de on_connect y on_publish
def on_connect(client,userdata,mid):
    info = 'Conexion del broker MQTT exitosa.\n\n'
    logging.info(info)
    time.sleep(2)
    menu_inicio()


os.system('clear')
logging.info('Bienvenido a la mensajeria instantanea del grupo 1')
logging.info('Se ha loggeado con el siguiente usuario: ' +cliente.GetUsuario())
a=input('\nPresione "Enter" para continuar...')

menu_principal()
