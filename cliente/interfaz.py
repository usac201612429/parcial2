from constantes import * #FPRTH Importando las constantes del archivo que las contiene
from CLASScliente import * #Importando el programa que maneja la clase de clientes



#FPRTH Importando las librerias necesarias
import logging
import paho.mqtt.client as paho
import os 
import time
import sys

#FPRTH Configurando el logging que mostrara la informacion

FORMATO = '[%(levelname)s] %(message)s'
logging.basicConfig(level = logging.INFO, format=FORMATO)

cliente =clients()

#FPRTH Se crea una funcion que maneja la interfaz para el usuario.  

def menu_principal():
    os.system('clear')
    logging.info('Menu principal\n')
    while True:
        t = input('Seleccione una opcion:\n1. Enviar texto\n2. Enviar mensaje de voz\n3. Salir\n')
        if t == '1':
            menu_texto()
        elif t=='2':
            menu_voz()
        elif t=='3':
            menu_salir()
            break
        else:
            os.system('clear')
            logging.info('Menu principal\n')
            logging.error('Entrada no válida\n')

def menu_texto():
    os.system('clear')
    logging.info('Menu para enviar mensaje de texto\n')
    while True:
        destino = input('A donde desea enviar el texto?\n1. Enviar a un usuario\n2. Enviar a una sala\n0. Regresar al menu anterior\n')
        if destino=='0':
            menu_principal()
            break
        elif destino=='1':
            menu_en_usuario('texto')
            break 
        elif destino=='2':
            menu_en_sala('texto')
            break
        else:
            os.system('clear')
            logging.info('Menu para enviar mensaje de texto\n')
            logging.error('Entrada no válida\n')
    
def menu_voz():
    os.system('clear')
    logging.info('Menu para enviar mensaje de voz\n')
    while True:
        destino = input('A donde desea enviar el audio?\n1. Enviar a un usuario\n2. Enviar a una sala\n0. Regresar al menu anterior\n')
        if destino=='0':
            menu_principal()
            break
        elif destino=='1':
            menu_en_usuario('voz') 
            break
        elif destino=='2':
            menu_en_sala('voz')
            break
        else:
            os.system('clear')
            logging.info('Menu para enviar mensaje de voz\n')
            logging.error('Entrada no válida\n')

def menu_salir():
    os.system('clear')
    logging.warning('Esta a punto de salir de la mensajeria\n')
    while True:
        salida = input('Esta seguro que desea salir de la mensajeria? [Y]/n\n')
        if salida == '' or salida == ' ' or salida == 'Y' or salida =='y':
            cliente.cliente_paho.loop_stop()
            cliente.cliente_paho.disconnect()
            if cliente.hilo.isAlive():
                cliente.hilo._stop()
            logging.info('Terminando programa...')
            sys.exit()
        elif salida == 'n' or salida =='N':
            menu_principal()
            break
        else:
            os.system('clear')
            logging.warning('Esta a punto de salir de la mensajeria\n')
            logging.error('Entrada no válida\n')

def menu_en_usuario(tipo):
    os.system('clear')
    logging.info('Envio de mensaje de '+tipo+'\n')
    while True:
        id_dest = input('Indique el usuario al que desea enviar el mensaje:\n')    
        if id_dest.isdigit() :
            if len(id_dest)==9:
                if tipo=='texto':
                    cliente.SetDestino(MQTT_USUARIOS+MQTT_GRUPO+id_dest)
                else:
                    cliente.SetDestino(MQTT_AUDIO+MQTT_GRUPO+id_dest)
                break
            else:
                os.system('clear')
                logging.info('Envio de mensaje de '+tipo+'\n')
                logging.error('La longitud del id no corresponde a la longitud de un numero de carnet estandar (9 digitos)\n')
        else:
            os.system('clear')
            logging.info('Envio de mensaje de '+tipo+'\n')
            logging.error('Debido a que el id debe ser un numero de carnet solo se permiten numeros como entrada\n')

    if tipo=='texto':
        envio_texto()
    else:
        envio_audio()

def menu_en_sala(tipo):
    os.system('clear')
    logging.info('Envio de mensaje de '+tipo+'\n')
    salas = cliente.GetSalas()
    mensaje = 'Usted se encuentra dentro de las siguientes salas:'
    for i in salas:
        mensaje += '  '+i
    logging.info(mensaje+'\n')
    while True:
        destino = input('Indique la sala a la que desa enviar el mensaje: \n')
        if destino in salas:
            if tipo=='texto':
                cliente.SetDestino(MQTT_SALAS+MQTT_GRUPO+destino)
            else:
                cliente.SetDestino(MQTT_AUDIO+MQTT_GRUPO+destino)
            
            break
        else:
            os.system('clear')
            logging.info('Envio de mensaje de '+tipo+'\n')
            logging.error('No se encuentra dentro de la sala '+destino)
            logging.info(mensaje+'\n')

    if tipo=='texto':
        envio_texto()
    else:
        envio_audio()



def envio_texto():
    os.system('clear')
    logging.info('Enviando mensaje de texto hacia '+cliente.GetDestino()+'\n')
    msg = input('Escriba el mensaje que desea enviar: \n')
    cliente.EnviarTexto(msg)
    while True:
        salida = input('Desea enviar otro mensaje de texto? [Y]/n\n')
        if salida == '' or salida == ' ' or salida == 'Y' or salida =='y':
            os.system('clear')
            envio_texto()
            break
        elif salida == 'n' or salida =='N':
            menu_principal()
            break
        else:
            os.system('clear')
            logging.info('Enviando mensaje de texto hacia '+cliente.GetDestino()+'\n')
            logging.error('Entrada no válida\n')        

def envio_audio():
    os.system('clear')
    logging.info('Enviando mensaje de voz hacia '+cliente.GetDestino()+'\n')    
    while True:     
        duracion=input('Ingrese la duracion,en segundos, del audio que desea enviar:\n')
        if duracion.isdigit():
            grabacion(duracion)
            break
        else:
            os.system('clear')
            logging.info('Enviando mensaje de voz hacia '+cliente.GetDestino()+'\n') 
            logging.error('Solo se aceptan numeros como entrada\n')

def grabacion(duracion):
    os.system('arecord -d '+duracion+' -f U8 -r 8000 audio.wav')
    audio = open('audio.wav','rb')
    b_audio = audio.read()
    audio.close()
    cliente.EnviarTexto(b_audio)
