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

#FPRTH Configuraciones
cliente_paho = paho.Client(clean_session=True)
cliente_paho.on_connect = on_connect
cliente_paho.on_publish = on_publish
cliente_paho.username_pw_set(MQTT_USER,MQTT_PASS)
cliente_paho.connect(host=MQTT_HOST,port=MQTT_PORT)

menu_inicio()
