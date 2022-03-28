import os
import time

def copias():

    """
    Funcion de modulo liberacion memoria windows.
    CLI PRD:
        salt '*' copia_win.copias
    """
    
    os.system('copy \\10.33.27.104\c:\FreeMemory\EmptyStandbyList.exe c:\Temp\EmptyStandbyList.exe')

    
