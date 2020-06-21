from variables import * #FPRTH Importando las constantes del archivo que las contiene
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
def menu_inicio():
    os.system('clear')
    logging.info('Bienvenido a la mensajeria instantanea del grupo 1\n')
    while True:  
        id = input('\tIngrese su ID de usuario (numero de carnet): \n \t\t')
        if id.isdigit() :
            if len(id)==9:
                cliente.SetId(id)
                break
            else:
                os.system('clear')
                logging.info('Bienvenido a la mensajeria instantanea del grupo 1\n')
                logging.error('La longitud de su id no corresponde a la longitud de un numero de carnet estandar (9 digitos)\n')
        else:
            os.system('clear')
            logging.info('Bienvenido a la mensajeria instantanea del grupo 1\n')
            logging.error('Debido a que el id debe ser su numero de carnet solo se permiten numeros como entradas\n')
    menu_principal()
    

def menu_principal():
    os.system('clear')
    logging.info('Menu principal\n')
    while True:
        t = input('\tSeleccione una opcion:\n\t1. Enviar texto\n\t2. Enviar mensaje de voz\n\t3. Salir\n\t\t')
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
        destino = input('\tA donde desea enviar el texto?\n\t0. Regresar al menu anterior\n\t1. Enviar a un usuario\n\t2. Enviar a una sala\n\t\t')
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
        destino = input('\tA donde desea enviar el audio?\n\t0. Regresar al menu anterior\n\t1. Enviar a un usuario\n\t2. Enviar a una sala\n\t\t')
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
        salida = input('\tEsta seguro que desea salir de la mensajeria? [Y]/n\n\t\t')
        if salida == '' or salida == ' ' or salida == 'Y' or salida =='y':
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
        id_dest = input('\tIndique el usuario al que desea enviar el mensaje:\n\t\t')    
        if id_dest.isdigit() :
            if len(id_dest)==9:
                cliente.SetDestino('usuarios/01/'+id_dest)
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
    salas =[]
    salas = cliente.GetSalas()
    mensaje = 'Usted se encuentra dentro de las siguientes salas:'
    for i in salas:
        mensaje += '  '+i
    logging.info(mensaje+'\n')
    while True:
        destino = input('\t Indique la sala a la que desa enviar el mensaje: \n\t\t')
        if destino in salas:
            cliente.SetDestino('salas/01/'+destino)
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
    msg = input('\tEscriba el mensaje que desea enviar: \n \t\t')
    cliente.EnviarTexto(msg)
    while True:
        salida = input('\tDesea enviar otro mensaje de texto? [Y]/n\n\t\t')
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
