#aipg este programa hara la primera parte del servidor, eso es reconocer los clientes y el comando ALIVE

import paho.mqtt.client as mqtt
import os
import threading
import socket
import logging
import time
import binascii
import sys
from server_class import *
from ServerComands import *

servidor1 = servidor()
comandos = ServerCommands(servidor1)

try:
    while True:
        #print("Hola mundo 2")
        time.sleep(9)
        #servidor1.publicar("01S01",'hola sala 01')
        
except KeyboardInterrupt:
    if comandos.hiloFindCommands.isAlive():
        comandos.hiloFindCommands._stop()
    sys.exit()