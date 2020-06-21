import os

#FPRTH Se crea la clase que manejara al cliente
class clients (object):
    def __init__(self):
        pass

    def SetDestino(self,dest):
        self.destino=dest

    def SetId(self,id):
        self.id = id
        os.system('echo "'+id+'" > usuario')
    
    def GetDestino(self):
        return self.destino

    def EnviarTexto(self,msg):
        self.mensaje = msg
        

    def GetID(self):
        arch_usuario=open('usuario','r')
        texto_usuario =''
        for line in arch_usuario:
            texto_usuario += line      
        return texto_usuario

    def GetSalas(self):
        self.lista_salas=[]
        texto_salas = ''

        arch_salas = open('salas','r')
        for line in arch_salas:
            texto_salas+=line
        arch_salas.close()

        lista = texto_salas[:-1].split('\n')
        for i in lista:
            self.lista_salas.append(i[2:])
        return self.lista_salas

    def GetSalasMensaje():
        mensaje = 'Usted se encuentra en las siguientes salas: '