#aipg archivo donde esta construida la clase

import paho.mqtt.client as mqtt
import os
import threading
import socket
import logging
import time
import binascii
from variables import *
#from credenciales import *

#Parametros de conexion
MQTT_HOST = "167.71.243.238"
MQTT_PORT = 1883

#Credenciales
MQTT_USER = "proyectos"
MQTT_PASS = "proyectos980"

logging.basicConfig(
    level = logging.INFO,
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

class servidor(object):
    def __init__(self):
        self.lista_activos = []
        self.lista_clientes_enviados = []
        self.lista_hilos = []
        self._iniciar_mqtt()
        self.hilo_holamundo = threading.Thread(name="hilo del hola mundo",target=self._hello,daemon=False)#aipg hilo adicional solo para correrlo, imprime un hola mundo
        self.hilo_holamundo.start()
        self.hilo_leer_archivo_salas = threading.Thread(name='hilo de leer archivos salas',target=self._leer_archivo,args=(('salas'),),daemon=False)#aipg hilo para leer el archivo de salas
        self.hilo_leer_archivo_salas.start()
        self.hilo_leer_archivo_usuarios = threading.Thread(name='hilo de leer archivos usuarios',target=self._leer_archivo,args=(('usuarios'),),daemon=False)#aipg hilo para leer el archivo de salas
        self.hilo_leer_archivo_usuarios.start()

        self.msg = ""        #OAGM mensaje entrante

        #args = (range(100), ),
    def _hello(self):
        while True:
            logging.info("hola mundo")
            time.sleep(10)


    def susc_topic(self,topic):#metodo para suscribirse a un topic
        self.mqttcliente.subscribe((topic,0))
        self.mqtthilo = threading.Thread(name= 'MQTT suscripcion',target=self.mqttcliente.loop_start)#aipg hilo para recibir notificaciones del tipic
        self.mqtthilo.start()#aipg el hilo es para que si me suscribo a algo, lo revise siempre


    def _iniciar_mqtt(self):

        #aipg configuraciones de mqtt
        self._conf_mqtt()

        self.susc_topic(ROOTTOPIC)

    def _conf_mqtt(self):
        self.mqttcliente = mqtt.Client(clean_session=True)#aipg se crea el objeto de mqtt

        #aipg metodos de callback de mqtt para publciar o que se recibio algo a lo que se esta suscrito
        self.mqttcliente.on_message = self.on_message
        self.mqttcliente.on_connect = self.on_connect
        self.mqttcliente.on_publish = self.on_publish

        try:
            #print("entro aqui")
            self.mqttcliente.username_pw_set(MQTT_USER,MQTT_PASS)
            self.mqttcliente.connect(host=MQTT_HOST,port=MQTT_PORT)
        except Exception as e:
            logging.info(e)
        
    def publicar(self,topic,value, qos = 0, retain = False):#aipg metodo para publicar en el topic
        #topic = 'comandos/14'
        self.mqttcliente.publish(topic, value, qos, retain)

    def _leer_archivo(self,file):#aipg metodo que lee el archivo de salas para suscribirse
        lista_salas_o_usuarios=[]
        try:
            while True:
                file_archivo=open(file,'r')
                archivo=file_archivo.read()
                file_archivo.close()
                lista_salas_o_usuarios=archivo.split('\n')
                lista_salas_o_usuarios.pop()
                #logging.info(lista_salas_o_usuarios)
                for i in lista_salas_o_usuarios:
                    self.susc_topic(i)
                time.sleep(6)
        except Exception as identifier:
            logging.error(identifier)
    
    def _revisar_activo(self):
        pass

    
    #aipg metodos callback de mqtt
    def on_message(self,mqttcliente,userdata,msg):#aipg metodo cuando entra un mensaje a un topic suscrito
        self.msg = msg #OAGM haciendo atributo el ID del ultimo comando recibido
        logging.info("Ha llegado un mensaje de este topic: " + str(msg.topic))
        logging.info("Su contenido es: " + str(msg.payload))

        trama=msg.payload#aipg trama en binario
        print("trama recibida",trama)
        #print(trama[:1])
        #if trama[:1]==binascii.unhexlify('03'):#si es una trama alive
        if trama[:2]== b'03':
            

            print("exito")
            trama_id=trama[3:]
            trama_id=trama_id.decode('ascii')#user id queda como string
            #print(trama_id,type(trama_id))

            if trama_id not in self.lista_activos:
                self.lista_activos.append(trama_id)
            print(self.lista_activos)#aipg tengo la lista con los clientes activos

            #aipg lo agrega independientemente de si es activo o no, media vez mande el alive
            self.lista_clientes_enviados.append(trama_id)#aipg va a estar recibiendo todos los ALIVE de los clientes.


            '''for i in range(len(self.lista_activos)):#aipg este for es para hacer hilos conforme lleguen las tramas de ALIVE
                self.lista_hilos.append(
                                    threading.Thread(name = 'hilo de topic entrante' + str(i),
                                    target = self._usuario_activo,
                                    args = ((trama_id),),
                                    daemon = False
                                    )
                        )
            for j in self.lista_hilos:
                j.start()'''

            self.hilo_prueba = threading.Thread(name="hilo prueba",target=self._usuario_activo,args=((trama_id),),daemon=False)#aipg hilo para monitorizar los clientes activos
            self.hilo_prueba.start()
                
            

    def _usuario_activo(self,user_id):
        cnt=0
        while cnt < 3:
            cnt+=1
            time.sleep(2)
            #logging.info("se ha cumplido un ciclo del hilo 1")

        #if cnt==3:
            #self.lista_activos.remove(user_id)
        logging.info("SE TERMINARON LOS 3 PERIODOS")
        self.lista_clientes_enviados.remove(user_id)
        if user_id not in self.lista_clientes_enviados:
            self.lista_activos.remove(user_id)#aipg borra el user id que no ha seguido enviando paquetes de ALIVE

        logging.info(self.lista_activos)#muestra los usuarios activos si se saca alguno


    def on_connect(self,mqttcliente,userdata,flags,rc):#aipg metodo que desplega si se ha conectado con exito
        logging.info("Conectado al broker")
        
    def on_publish(self,mqttcliente,userdata,mid):#aipg metodo que desplega si se ha publicado con exito
        publishText= "publicacion exitosa"
        logging.info(publishText)

