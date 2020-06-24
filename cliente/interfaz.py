'''FPRTH Modulo para manejar la interfaz del usuario'''

from constantes import * #FPRTH Importando las constantes del archivo que las contiene
from CLASScliente import * #FPRTH Importando el programa que maneja la clase de clientes
from ClientComands import * #OAGM clse para manejo de comandos del "cliente"



#FPRTH Importando las librerias necesarias
import logging
import paho.mqtt.client as paho
import os 
import time
import sys

#FPRTH Configurando el logging que mostrara la informacion
FORMATO = '[%(levelname)s] %(message)s'
logging.basicConfig(level = logging.INFO, format=FORMATO)

cliente =clients() #FPRTH Se crea un nuevo objeto de tipo cliente

#FPRTH Se crea una funcion que maneja la interfaz para el usuario.  



'''FPRTH interfaz del menu principal'''
def menu_principal(): 
    os.system('clear') #FPRTH Se limpia la terminal
    logging.info('Menu principal\n')
    
    #FPRTH While para mantenerse en el menu de seleccion de inicio
    while True:
        t = input('Seleccione una opcion:\n1. Enviar texto\n2. Enviar mensaje de voz\n3. Salir\n') #FPRTH Se imprimen las opciones para el usuario
        #FPRTH se compara lo que ingreso el usuario
        if t == '1':
            menu_texto()
        elif t=='2':
            menu_voz()
        elif t=='3':
            menu_salir()
            break
        else:
            #FPRTH Se limpia la terminal y se vuelve a mostrar la informacion inicial
            os.system('clear')
            logging.info('Menu principal\n')
            logging.error('Entrada no válida\n')



'''FPRTH Interfaz del menu para enviar texto'''

def menu_texto():
    #FPRTH Se limpia la terminal y se imprime un encabezado
    os.system('clear')
    logging.info('Menu para enviar mensaje de texto\n')
    
    #FPRTH Ciclo while para esperar la seleccion del usuario
    while True:
        destino = input('A donde desea enviar el texto?\n1. Enviar a un usuario\n2. Enviar a una sala\n0. Regresar al menu anterior\n') #FPRTH Se imprimen las opciones para el usuario
        
        #FPRTH Se compara la entrada del usuario para tomar una decision
        if destino=='0':
            menu_principal()
            break
        elif destino=='1':
            menu_en_usuario('texto') #FPRTH Se va al menu para enviar hacia un usuario con el parametro texto
            break 
        elif destino=='2':
            menu_en_sala('texto') #FPRTH Se redirige al menu para enviar hacia un usuario con el parametro texto
            break
        else:
            #FPRTH Se limpia la terminal y se muestra un encabezado
            os.system('clear')
            logging.info('Menu para enviar mensaje de texto\n')
            logging.error('Entrada no válida\n')



'''FPRTH Interfaz del menu para enviar audio'''

def menu_voz():
    #FPRTH Se limpia la terminal y se imprime un encabezado
    os.system('clear')
    logging.info('Menu para enviar mensaje de voz\n')

    #FPRTH Ciclo while para que el usuario ingrese su opcion
    while True:
        destino = input('A donde desea enviar el audio?\n1. Enviar a un usuario\n2. Enviar a una sala\n0. Regresar al menu anterior\n')
        
        #FPRTH Se compara la entrada del usuario
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
            #FPRTH Se limpia la terminal y se imprime un encabezado
            os.system('clear')
            logging.info('Menu para enviar mensaje de voz\n')
            logging.error('Entrada no válida\n')



'''FPRTH Interfaz del menu para salida'''

def menu_salir():
    #FPRTH Se limpia la terminal y se imprime un encabezado
    os.system('clear')
    logging.warning('Esta a punto de salir de la mensajeria\n')

    #FPRTH Ciclo para esperar la entrada del usuario
    while True:
        salida = input('Esta seguro que desea salir de la mensajeria? [Y]/n\n')
        
        #FPRTH Se compara la entrada del usuario
        if salida == '' or salida == ' ' or salida == 'Y' or salida =='y':
            #FPRTH Se terminan todos los procesos y se cierra el programa
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
            #FPRTH Se limpia la terminal y se imprime el encabezado del menu
            os.system('clear')
            logging.warning('Esta a punto de salir de la mensajeria\n')
            logging.error('Entrada no válida\n')


'''FPRTH Interfaz del menu para enviar texto/audio hacia un usuario
La funcion recibe el tipo de elemento que enviaran para tomar decisiones posteriormente'''

def menu_en_usuario(tipo):
    #FPRTH se limpia la terminal y se imprime un encabezado
    os.system('clear')
    logging.info('Envio de mensaje de '+tipo+'\n')

    #FPRTH Ciclo para esperar la entrada del usuario
    while True:
        id_dest = input('Indique el usuario al que desea enviar el mensaje:\n') #FPRTH Se solicita el id del usuario al que se enviara el mensaje    
        if id_dest.isdigit() : #FPRTH Se verifica que el id corresponda a un numero
            if len(id_dest)==9: #FPRTH Se verifica que la longitud del id sea igual a la de un carnet

                #FPRTH Se verifica que tipo de elemento se enviara texto/audio 
                if tipo=='texto':
                    cliente.SetDestino(MQTT_USUARIOS+MQTT_GRUPO+id_dest) #FPRTH Se setea el topic del usuario al que se enviara el texto
                else:
                    cliente.SetDestino(MQTT_AUDIO+MQTT_GRUPO+id_dest) #FPRTH Se setea el topic del usuario al que se enviara el texto
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

