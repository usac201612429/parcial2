from variables import *
import time
import binascii
import threading 

class ServerCommands:
    def __init__(self, servidor):
        self.servidor = servidor
        self.hiloFindCommands = threading.Thread(name = 'FindCommands', target = self.findCommand(), args = (()), daemon = True) #OAGM hilo para revisar comandos entrantes
        self.hiloFindCommands.start()

    def ack(self, toTopic):
            value = ACK + b'$' + toTopic
            print(value)
            # self.servidor.client.publish(f"{ROOTTOPIC}", value, qos = 2, retain = False)
            self.servidor.mqttcliente.publish(f"{ROOTTOPIC}/{toTopic.decode('UTF-8', 'strict')}", value, qos = 0, retain = False)
    
 
    # def frr(self, toTopic):
    #     client.publish(toTopic, (5).to_bytes(1, "little"), qos, retain = False)

    def findCommand(self):
        while True:
            #print(f'comando recibido: {self.servidor.msg[:1]}')
            if self.servidor.msg[:1] == ALIVE:
                print(self.servidor.msg[2:12])
                self.ack(self.servidor.msg[2:12]) 
                self.servidor.msg = b"00"
            time.sleep(0.1)
