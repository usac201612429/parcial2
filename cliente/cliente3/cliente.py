'''FPRTH Modulo principal'''


#FPRTH Se importan los modulos necesarios
from interfaz import *
from CLASScliente import *
from constantes import *

#FPRTH Se importan las librerias necesarias
import time
import paho.mqtt.client as paho




try:
    #FPRTH Se imprime un mensaje de inicio
    os.system('clear')
    logging.info('Bienvenido a la mensajeria instantanea del grupo 1')
    logging.info('Se ha loggeado con el siguiente usuario: ' +cliente.GetUsuario())
    a=input('\nPresione "Enter" para continuar...')
    #FPRTH Se redirige a la interfaz del menu principal
    menu_principal()
except KeyboardInterrupt:
    #FPRTH Se detienen todos los proceso 
    cliente.cliente_paho.loop_stop()
    cliente.cliente_paho.disconnect()
    if cliente.hilo.isAlive():
        cliente.hilo._stop()
    logging.info('Terminando programa...')
    
finally:
    sys.exit() #FPRTH Se cierra el programa
