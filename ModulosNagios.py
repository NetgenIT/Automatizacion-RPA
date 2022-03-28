import re
import os
import platform
import socket
import time
from datetime import datetime
from modulos_Funciones import _status_servicios_2012(), _docu_servicios(), _servicios(), _status_servicios_otros()

def servicionagios():
    
    """
    Funcion de modulo alta servicios nagios.
    CLI PRD:
        salt '*' modulosNagios.servicionagios
    """   
    #crea Carpeta donde estaran Archivos
    os.system('md C:\Temp')       
    #Rescada datos del sistema operativo hacia variables
    sistema = platform.platform(terse=True)
    hostname = socket.gethostname()
    ip_address1 = socket.gethostbyname(hostname)
    ahora = time.strftime("%c")
    
    try:
        
        if sistema == 'Windows-2012ServerR2':
            _status_servicios_2012()
            _docu_servicios()
            _servicios()           
        else:
            _status_servicios_otros()
            _docu_servicios()
            _servicios()                    
        
    except OSError as err:
        exit