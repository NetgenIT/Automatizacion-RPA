import re
import os
import platform
import socket
import time
from datetime import datetime

# alta servicios nagios(hostdown)

def _status_servicios_2012():
    os.system('sc query nscp >C:\Temp\Servnagios.txt')

def _docu_servicios():
    Nagios_Running = open('C:\Temp\Servnagios.txt',mode='r')
    Nagios_Depurados = open("C:\Temp\Servnagios_Ejecutandose.txt", mode="w")
    for elemento in Nagios_Running:
        if re.findall('^SERVICE_NAME:', elemento):
            f= elemento
            Nagios_Depurados.write(f)
            Nagios_Depurados.close
        Nagios_Running.close

def _status_servicios_otros():
    os.system('sc query NSClientpp >C:\Temp\Servnagios1.txt')

def _servicios():
    Nagios_Depurados = open("C:\Temp\Servnagios_Ejecutandose.txt", mode="r")
    for x in Nagios_Depurados:
        r =x.replace("SERVICE_NAME:", "SC STOP")
        os.system(r)
        time.sleep(10)
        rr =x.replace("SERVICE_NAME:", "SC START")
        os.system(rr)

# Liberacion Espacio en Disco Window

def _dism():
    os.system('Dism /online /cleanup-image /spsuperseded /hidesp')
    os.system('DISM /online /Cleanup-Image /SpSuperseded')
    os.system('Dism.exe /online /Cleanup-Image /StartComponentCleanup')
    os.system('Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase')
    os.system('dism /Online /Cleanup-Image /AnalyzeComponentStore')
    os.system('dism /online /Cleanup-Image /scanhealth')

def to_gb(bytes):
        "Convierte bytes a gigabytes."
        return bytes / 1024**3

# Liberacion Memoria Linux

def _Libmem():
    os.system ('free -m > root/srv/salt/memlinux/MemoriasistemaUtil.txt')
    ArchivoMemoriaUtil = open('root/srv/salt/memlinux/MemoriasistemaUtil.txt', mode="r")
    MemoriaUtil = ArchivoMemoriaUtil.read()
    ArchivoMemoriaUtil.close()

def _Libmem_2():
    os.system ('free -m > root/srv/salt/memlinux/MemoriasistemaLib.txt')
    ArchivoMemoriaLib = open('root/srv/salt/memlinux/MemoriasistemaLib.txt', mode="r")
    MemoriaLib = ArchivoMemoriaLib.read()
    ArchivoMemoriaLib.close()

def _Libmem_3():
    os.system ('sync; echo 3 > /proc/sys/vm/drop_caches')

#Liberacion Memoria Windows

def _memwin():
    os.system('c:\FreeMemory\EmptyStandbyList.exe workingsets modifiedpagelist standbylist priority0standbylist')
    os.system('c:\Temp\EmptyStandbyList.exe workingsets modifiedpagelist standbylist priority0standbylist')
