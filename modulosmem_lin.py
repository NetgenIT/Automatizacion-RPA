import os
import platform
import socket
import time
import sys
from modulos_Funciones import _Libmem(), _Libmem_2(), _Libmem_3()

def memoria():

    """
    Funcion de modulo actualizacion parches Microsoft.
    CLI PRD:
        salt '*' modulosmem.memoria
    """
    #crea Carpeta donde estaran Archivos
    os.system('mkdir -p root/srv/salt/memlinux')

    #Rescada datos del sistema operativo hacia variables
    sistema = platform.platform(terse=True)
    sistema2 = platform.linux_distribution()
    hostname = socket.gethostname()
    ip_address1 = socket.gethostbyname(hostname)
    ahora = time.strftime("%c")

    _Libmem()
    
    _Libmem_3()

    _Libmem_2()

    archivo = open("root/srv/salt/memlinux/Informe_Memoria.txt", mode="w")
    archivo.write("I N F O R M E   L I B E R A C I O N   M E M O R I A   S I S T E M A S   L I N U X \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write(" \n")
    archivo.write("Nombre del Sistema Operativo  :{}".format(sistema))
    archivo.write(" \n")
    archivo.write("Version Sistema Operativo     :{}".format(sistema2))
    archivo.write(" \n")
    archivo.write("Nombre del Equipo             :%s" % hostname)
    archivo.write(" \n")
    archivo.write("Direccion Ip del Equipo       :%s" % ip_address1)
    archivo.write(" \n")
    archivo.write("Fecha y hora del Equipo       :%s" % ahora )
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("                     MEMORIA ANTES DE EJECUTAR PROCEDIMIENTO ")
    archivo.write(" \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write("%s"%MemoriaUtil)
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("                     MEMORIA DESPUES DE EJECUTAR PROCEDIMIENTO ")
    archivo.write(" \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write(" \n")
    archivo.write("%s"%MemoriaLib)
    archivo.close
