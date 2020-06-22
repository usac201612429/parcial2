from variables import *
import time
import threading 

class ServerCommands:
    def __init__(self, servidor):
        self.servidor = servidor
        self.hiloFindCommands = threading.Thread(name = 'FindCommands', target = self.findCommand(), args = (()), daemon = True) #OAGM hilo para revisar comandos entrantes
        self.hiloFindCommands.start()

    def ack(self, toTopic):
            print(toTopic)
            value = ACK + b"$" + toTopic.encode('UTF-8', 'strict')
            # self.servidor.client.publish(f"{ROOTTOPIC}", value, qos = 2, retain = False)
            self.servidor.client.publish(f"{ROOTTOPIC}/{str(toTopic)}", value, qos = 2, retain = False)
    
 
    # def frr(self, toTopic):
    #     client.publish(toTopic, (5).to_bytes(1, "little"), qos, retain = False)

    def findCommand(self):
        while True:

            if self.servidor.msg.payload[:2] == ALIVE:
                self.ack(self.servidor.msg.payload[3:11]) 
                self.servidor.ultimoComando = 0
