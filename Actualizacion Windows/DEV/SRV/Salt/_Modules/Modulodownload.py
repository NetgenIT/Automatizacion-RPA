import re
import os
import platform
import socket
import time
from datetime import datetime
import salt.modules.win_wua
import salt.utils.win_reg




def bajada():
    
    """
    Funcion de modulo actualizacion parches Microsoft.
    CLI PRD:
        salt '*' modulosbajada.bajada
    """
    
    #crea Carpeta donde estaran Archivos

    #os.system('md C:\Temp')
        

    #Rescada datos del sistema operativo hacia variables
    sistema = platform.platform(terse=True)
    hostname = socket.gethostname()
    ip_address1 = socket.gethostbyname(hostname)
    ahora = time.strftime("%c")


    #Modifica registo opciones de busqueda de parches
    hive = 'HKLM'
    key = 'SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU'
    salt.utils.win_reg.set_value(hive, key, 'AUOptions', vtype='REG_DWORD', vdata='3')


    bajados = salt.modules.win_wua.list(categories=["Security Updates"], summary=True, online=True, download=True)

    bajados

    now = datetime.today().strftime('%Y_%m_%d_%H_%M')
    hostname = socket.gethostname()
    archivo01 = ("c:\\Temp\\informe_Parches_Bajados.txt")
    archivo1 = ("c:\\Informes_Parchado\\"+hostname+"_Informe_Parches_Bajados_"+now+".txt")

    #crea informe de actualizacion
    archivo = open (archivo01, mode="w")
    archivo.write("I N F O R M E   P A R C H E S   B A J A D O S   E N   E L   S I S T E M A  \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write(" \n")
    archivo.write("Nombre del Sistema Operativo  :{}".format(sistema))
    archivo.write(" \n")
    archivo.write("Nombre del Equipo             :%s" % hostname)
    archivo.write(" \n")
    archivo.write("Direccion Ip del Equipo       :%s" % ip_address1)
    archivo.write(" \n")
    archivo.write("Fecha y hora del Equipo       :%s" % ahora )
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("-------------------------------------------- \n")
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("                                    I N F O R M E     \n")
    archivo.write("------------------------------------------------------------------------------------ \n")
    archivo.write(" \n")
    archivo.write("D E T A L L E   P A R C H E S   D I S P O N I B L E S   P A R A   S E R   I N S T A L A D O S  \n")
    archivo.write("---------------------------------------------------------------------------------------------- \n")
    archivo.write(" \n")
    archivo.write("%s"%bajados)
    archivo.close()


    #remueve archivos temporales   
    os.system ("copy "+archivo01+" "+archivo1)
