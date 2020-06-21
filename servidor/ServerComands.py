from variables import *
import time

class ServerCommands:
    def __init__(self, servidor):
        self.servidor = servidor

    def ack(self, toTopic):
            value = ACK + b"$" + toTopic.encode('UTF-8', 'strict')
            self.servidor.client.publish(f"{ROOTTOPIC}/{str(toTopic)}", value, qos = 2, retain = False)
    
 
    # def frr(self, toTopic):
    #     client.publish(toTopic, (5).to_bytes(1, "little"), qos, retain = False)
