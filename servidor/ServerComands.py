from variables import *
import time
import binascii
import threading 

class ServerCommands:
    """ OAGM:
        Se recibe un servidor para manipular. 
        Luego se crea e inicia un hilo llamado "hiloFindCommands" para verificar constantemente
        los comandos que ingresan al servidor   """

    def __init__(self, servidor):
        self.servidor = servidor
        self.hiloFindCommands = threading.Thread(name = 'FindCommands', target = self.findCommand(), args = (()), daemon = True) #OAGM hilo para revisar comandos entrantes
        self.hiloFindCommands.start()

    """ OAGM:
        Funcion para devolver un ACK al recivir distintos comandos. Utiliza el valor de "toTopic" para saber a
        quien debe enviar el ACK.   """

    def ack(self, toTopic):
            value = ACK + b'$' + toTopic
            self.servidor.mqttcliente.publish(f"{ROOTTOPIC}/{toTopic.decode('UTF-8', 'strict')}", value, qos = 0, retain = False)
    
 
    # def frr(self, toTopic):
    #     client.publish(toTopic, (5).to_bytes(1, "little"), qos, retain = False)

    """ OAGM:
        Metodo que se ejecuta sobre un hilo (hiloFindCommand). Constantemete revisa si ha recivido un comando de los
        esperados y decide que otro metodo ejecutar. al finalizar establece el valor de self.sevidor.msg = "00", con
        esto no ejecutara un comando mas veces de las debidas.  """

    def findCommand(self):
        while True:

            """ OAGM:
                si el comando es ALIVE, se llamará al metodo ack y se le envia quien lo envia.  """
                
            if self.servidor.msg[:1] == ALIVE:
                self.ack(self.servidor.msg[2:12]) 
                self.servidor.msg = b"00"
