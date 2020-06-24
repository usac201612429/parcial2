from interfaz import *
from CLASScliente import *
from constantes import *

import time
import paho.mqtt.client as paho

'''FPRTH Configuracion del cliente MQTT'''



#FPRTH definiendo las funciones de on_connect y on_publish
try:

    os.system('clear')
    logging.info('Bienvenido a la mensajeria instantanea del grupo 1')
    logging.info('Se ha loggeado con el siguiente usuario: ' +cliente.GetUsuario())
    a=input('\nPresione "Enter" para continuar...')

    menu_principal()
except KeyboardInterrupt:
    cliente.cliente_paho.loop_stop()
    cliente.cliente_paho.disconnect()
    if cliente.hilo.isAlive():
        cliente.hilo._stop()
    logging.info('Terminando programa...')
    
finally:
    sys.exit()
