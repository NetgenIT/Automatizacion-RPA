import os
import platform
import socket
import time
import sys
import psutil
from datetime import datetime

def memoria():

    """
    Funcion de modulo liberacion memoria windows.
    CLI PRD:
        salt '*' modulosmem_win.memoria
    """

    #crea Carpeta donde estaran Archivos
    #os.system('mkdir -p root/srv/salt/memwindows')

    os.system('md c:\Informes_Parchado')
    os.system('md C:\Temp')

    #Rescada datos del sistema operativo hacia variables
    sistema = platform.platform(terse=True)
    hostname = socket.gethostname()
    ip_address1 = socket.gethostbyname(hostname)
    ahora = time.strftime("%c")
    now = datetime.today().strftime('%Y_%m_%d_%H_%M')

    memoriatot = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    memoriadis = psutil.virtual_memory()[1] / (1024.0 ** 3)
    memoriapor = psutil.virtual_memory()[2]
    memoriausa = psutil.virtual_memory()[3] / (1024.0 ** 3)
    memorialib = psutil.virtual_memory()[4] / (1024.0 ** 3)

    #liberacion de Memoria

    os.system('c:\FreeMemory\EmptyStandbyList.exe workingsets modifiedpagelist standbylist priority0standbylist')
    os.system('c:\Temp\EmptyStandbyList.exe workingsets modifiedpagelist standbylist priority0standbylist')
    time.sleep(60)
    memoriadis2 = psutil.virtual_memory()[1] / (1024.0 ** 3)
    memoriapor2 = psutil.virtual_memory()[2]
    memoriausa2 = psutil.virtual_memory()[3] / (1024.0 ** 3)
    memorialib2 = psutil.virtual_memory()[4] / (1024.0 ** 3)

    #Archivos Temporales
    
    archivo01 = ("c:\\Temp\\informe_memoria.txt")
    archivo02 = ("c:\\Temp\\mem1.txt")
    archivo03 = ("c:\\Temp\\mem2.txt")


    #crea informe de actualizacion
    archivo = open (archivo01, mode="w")
    archivo.write("I N F O R M E   M E M O R I A    D E L   S I S T E M A  O P E R A T I V O \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write("Informacion del Sistema Operativo\n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write(" \n")
    archivo.write("Nombre del Sistema Operativo     :{}".format(sistema))
    archivo.write(" \n")
    archivo.write("Nombre del Equipo                :%s" % hostname)
    archivo.write(" \n")
    archivo.write("Direccion Ip del Equipo          :%s" % ip_address1)
    archivo.write(" \n")
    archivo.write("Memory Total del Sistema         :%s" % memoriatot)
    archivo.write(" \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write("Memoria antes del proceso de liberación\n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("Memory usada en Porcentaje       :%s" % memoriapor)
    archivo.write(" %%")
    archivo.write(" \n")
    archivo.write("Memory usada por el Sistema      :%s" % memoriausa + " GB")
    archivo.write(" \n")
    archivo.write("Memory libre antes del sistema   :%s" % memorialib + " GB")
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write("Memoria despues del proceso de liberación \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("Memory usada en porcentaje       :%s" % memoriapor2)
    archivo.write(" %%")
    archivo.write(" \n")
    archivo.write("Memory usada por el Sistema      :%s" % memoriausa2 + " GB")
    archivo.write(" \n")
    archivo.write("Memory libre despues del sistema :%s" % memorialib2 + " GB")
    archivo.write(" \n")
    archivo.write(" \n")
    if memoriausa > memoriausa2:
        archivo.write("RESULTADO : Memoria liberada con exito \n")
        archivo.write(" \n")
    else:
        archivo.write("RESULTADO : Memoria no liberada \n")
        archivo.write(" \n")
    archivo.close()
