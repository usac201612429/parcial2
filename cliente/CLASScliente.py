from constantes import *
from ClientComands import *

import os
import paho.mqtt.client as paho
import logging
import time
import threading

FORMATO = '[%(levelname)s] %(message)s'
logging.basicConfig(level = logging.DEBUG, format=FORMATO)


''' def on_publish(client,userdata,mid):
    comandos.publicar() '''


#FPRTH Se crea la clase que manejara al cliente
class clients (object):
    def __init__(self):
        self.usuario = self.DetID()
        self.subscripciones = [(MQTT_COMANDOS+MQTT_GRUPO+self.usuario,MQTT_QOS),(MQTT_USUARIOS+MQTT_GRUPO+self.usuario,MQTT_QOS),(MQTT_AUDIO+MQTT_GRUPO+self.usuario,MQTT_QOS)]
        self.SubSalas()


        self.cliente_paho = paho.Client(clean_session=True)
        self.cliente_paho.on_publish = self.on_publish
        self.cliente_paho.on_message = self.on_message
        self.cliente_paho.username_pw_set(MQTT_USER,MQTT_PASS)
        self.cliente_paho.connect(host=MQTT_HOST,port=MQTT_PORT)
        self.cliente_paho.subscribe(self.subscripciones)
        self.cliente_paho.loop_start()

        

        
    def SetDestino(self,dest):
        self.destino=dest

    def SetId(self,id):
        self.id = id
        os.system('echo "'+id+'" > usuario')
    
    def GetDestino(self):
        return self.destino

    def EnviarTexto(self,msg):
        self.cliente_paho.publish(self.destino,msg,qos=0,retain=False)
        
    def GetUsuario(self):
        return self.usuario

    def DetID(self):
        arch_usuario=open('usuario','r')
        texto_usuario =''
        for line in arch_usuario:
            texto_usuario += line      
        return texto_usuario[:-1]

    def DetSalas(self):
        self.lista_salas=[]
        texto_salas = ''

        arch_salas = open('salas','r')
        for line in arch_salas:
            texto_salas+=line
        arch_salas.close()

        lista = texto_salas[:-1].split('\n')
        for i in lista:
            self.lista_salas.append(i[2:])
        
    def GetSalas(self):
        self.DetSalas()
        return self.lista_salas

    def SubSalas(self):
        self.DetSalas()
        for i in self.lista_salas:
            self.subscripciones.append((MQTT_SALAS+MQTT_GRUPO+i,MQTT_QOS))


    def on_publish(self,client,userdata,mid):
        info='Mensaje enviado'
        logging.debug(info)

    def on_message(self,client,userdata,msg):
        topic=str(msg.topic)
        ltopic=topic.split('/')
        if ltopic[0]=='usuarios':
            print('\n\n')
            logging.info("[MENSAJE NUEVO DE USUARIO]\n\t"+msg.payload.decode()+'\n')
        elif ltopic[0]=='salas':
            print('\n\n')
            logging.info("[MENSAJE NUEVO USUARIO EN LA SALA " +ltopic[2]+"]\n\t"+msg.payload.decode()+'\n')
        elif ltopic[0]=='audio':
            print('\n\n')
            logging.info("[MENSAJE DE AUDIO NUEVO]")
            archivo_nombre=str(time.time())+'.wav'
            brcibidos = msg.payload
            self.hilo = threading.Thread(name='Reproductor de audio recibido',target=self.Reproducir_Audio, args=((archivo_nombre,brcibidos)),daemon=False)
            self.hilo.start()
        elif ltopic[0] == 'comandos':
            comandos.verificarMensajes(msg.payload, msg.topic)


    def Reproducir_Audio(self,nombre,bytes_recibidos):
        audio = open(nombre,'wb')
        audio.write(bytes_recibidos)
        audio.close()
        os.system('aplay '+nombre)




''' #OAGM: objeto comandos. Recibe la cliente mqtt como parametro (paho.Client)
comandos = ClientCommands(cliente_paho) '''