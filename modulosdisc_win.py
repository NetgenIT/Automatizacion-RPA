import os
import platform
import socket
import psutil
from modulos_Funciones import _dism(), to_gb()

def capacidad():

    """
    Funcion de modulo liberacion memoria windows.
    CLI PRD:
        salt '*' modulosdisc_win.capacidad
    """
    #Rescada datos del sistema operativo hacia variables
    sistema = platform.platform(terse=True)
    hostname = socket.gethostname()
    ip_address1 = socket.gethostbyname(hostname)

    ruta = 'c:\\'
    c_info = psutil.disk_usage(ruta)

    os.system('del c:\Windows\Temp /f /s /q')

    _dism()
    
    c_info2 = psutil.disk_usage(ruta)

    to_gb2(bytes)

    archivo01 = ("c:\\Temp\\informe_disco.txt")
    
    #crea informe de actualizacion
    archivo = open (archivo01, mode="w")
    archivo.write("I N F O R M E   E S P A C I O   E N   D I S C O    D E L   S I S T E M A  O P E R A T I V O \n")
    archivo.write("---------------------------------------------------------------------------------------------- \n")
    archivo.write(" \n")
    archivo.write("Nombre del Sistema Operativo  :{}".format(sistema))
    archivo.write(" \n")
    archivo.write("Nombre del Equipo             :%s" % hostname)
    archivo.write(" \n")
    archivo.write("Direccion Ip del Equipo       :%s" % ip_address1)
    archivo.write(" \n")
    archivo.write("CAPACIDAD DISCO Total GB      :{}" .format(to_gb(c_info.total)))
    archivo.write("---------------------------------------------------------------------------------------------- \n")
    archivo.write("Capacidad de disco duro ocupada antes del proceso\n")
    archivo.write("---------------------------------------------------------------------------------------------- \n")
    archivo.write(" \n")
    archivo.write(" \n")
    archivo.write("CAPACIDAD DISCO Usado GB      :{}" .format(to_gb(c_info.used)))
    archivo.write(" \n")
    archivo.write("CAPACIDAD DISCO Libre GB      :{}" .format(to_gb(c_info.free)))
    archivo.write(" \n")
    archivo.write("CAPACIDAD DISCO Libre %       :{}%.".format(c_info.percent))
    archivo.write(" \n")
    archivo.write("--------------------------------------------------------------------------------------------- \n")
    archivo.write("Capacidad de disco duro ocupada despues del proceso\n")
    archivo.write("--------------------------------------------------------------------------------------------- \n")
    archivo.write(" \n")
    archivo.write("CAPACIDAD DISCO Usado GB      :{}" .format(to_gb(c_info2.used)))
    archivo.write(" \n")
    archivo.write("CAPACIDAD DISCO Libre GB      :{}" .format(to_gb(c_info2.free)))
    archivo.write(" \n")
    archivo.write("CAPACIDAD DISCO Libre %       :{}%.".format(c_info2.percent))
    archivo.write(" \n")
    archivo.write(" \n")
    if c_info.percent > c_info2.percent:
        archivo.write("RESULTADO : Espacio en Disco liberado con exito \n")
        archivo.write(" \n")
    else:
        archivo.write("RESULTADO : Espacio en Disco no liberado \n")
        archivo.write(" \n")
    archivo.close()
    archivo.close 
   
    