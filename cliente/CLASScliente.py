from constantes import *

import os
import paho.mqtt.client as paho
import logging
import time

FORMATO = '[%(levelname)s] %(message)s'
logging.basicConfig(level = logging.DEBUG, format=FORMATO)


def on_publish(client,userdata,mid):
    info='Mensaje enviado'
    logging.debug(info)

def on_message(client,userdata,msg):
    topic=str(msg.topic)
    ltopic=topic.split('/')
    mensaje=msg.payload.decode()
    usuario = mensaje[:9]
    mensaje = mensaje[9:]
    if ltopic[0]=='usuarios':
        logging.info("[MENSAJE NUEVO DEL USUARIO "+usuario+"]\n\t"+mensaje+'\n')
    elif ltopic[0]=='salas':
        logging.info("[MENSAJE NUEVO DEL USUARIO "+usuario+' EN LA SALA '+ltopic[2]+"]\n\t"+mensaje+'\n')

    


cliente_paho = paho.Client(clean_session=True)
cliente_paho.on_publish = on_publish
cliente_paho.on_message = on_message
cliente_paho.username_pw_set(MQTT_USER,MQTT_PASS)
cliente_paho.connect(host=MQTT_HOST,port=MQTT_PORT)



#FPRTH Se crea la clase que manejara al cliente
class clients (object):
    def __init__(self):
        self.usuario = self.DetID()
        self.subscripciones = [(MQTT_COMANDOS+MQTT_GRUPO+self.usuario,MQTT_QOS),(MQTT_USUARIOS+MQTT_GRUPO+self.usuario,MQTT_QOS)]
        self.SubSalas()
        cliente_paho.subscribe(self.subscripciones)
        cliente_paho.loop_start()

    def SetDestino(self,dest):
        self.destino=dest

    def SetId(self,id):
        self.id = id
        os.system('echo "'+id+'" > usuario')
    
    def GetDestino(self):
        return self.destino

    def EnviarTexto(self,msg):
        cliente_paho.publish(self.destino,self.usuario+msg,qos=0,retain=False)
        
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
