from constantes import *
import time
import threading 
import logging
import sys

class ClientCommands:
    def __init__(self, cliente_paho):
        self.lastCommandSent = b'00'                #OAGM: variable para que en poho.publish() se sepa si se envio un comando o no
        self._periodosAlivePerdidos = 0             #OAGM: variable para contar periodos ALIVE perdidos
        self._alivePeriod = ALIVE_PERIOD
        self.cliente_paho = cliente_paho            #OAGM: se traen todas los metodos paho.Client
        with (open("usuario", "rb")) as archivo:    #OAGM: obtenemos el userID        
            self.userID = archivo.read()[:-1]       
        archivo.close()
        self.hiloCommands = threading.Thread(name = 'hiloCommands', target = self.alive, args = (()), daemon = True) #OAGM hilo para revisar comandos entrantes
        self.hiloCommands.start()   

    def alive(self):
        while True:
            value = ALIVE + b"$" + self.userID
            self.lastCommandSent = ALIVE
            self.cliente_paho.publish(f"{MQTT_COMANDOS}{MQTT_GRUPO}{self.userID.decode('UTF-8', 'strict')}", value, qos = 0, retain = False)
            print("alive enviado", self._periodosAlivePerdidos)
            time.sleep(self._alivePeriod)
            self._periodosAlivePerdidos += 1
            if self._periodosAlivePerdidos == 3:
                self._alivePeriod = 0.1
            elif self._periodosAlivePerdidos == int(20 // self._alivePeriod) + 3:
                self._alivePeriod = ALIVE_PERIOD
                print("alive enviado", self._periodosAlivePerdidos)
                logging.critical('Conexión finalizada, el servidor no responde')
                self.cliente_paho.loop_stop()
                self.cliente_paho.disconnect()
                sys.exit()
                
                

    def ackRespuesta(self):
        pass

    
    def publicar(self):
        if self.lastCommandSent in [FRR, FTR, ALIVE, ACK, OK, NO]:
            self.lastCommandSent = b'00'
        else:
            info='Mensaje enviado'
            logging.info(info)


    def verificarMensajes(self, payload, topic):
        """ OAGM: si el comando es ALIVE, se llamará al metodo ack y se le envia quien lo envia.  """ 

        if topic[:12] == f"{MQTT_COMANDOS}{MQTT_GRUPO}":    
            if payload[:1] == ACK:
                self._periodosAlivePerdidos = 0
                self._alivePeriod = ALIVE_PERIOD
                payload = "00"            
        elif topic[:12] == f'{MQTT_USUARIOS}{MQTT_GRUPO}':
            logging.info("Ha llegado un mensaje del topic "+str(topic))
            logging.info(str(payload))

