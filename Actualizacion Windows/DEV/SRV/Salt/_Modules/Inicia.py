import os
import time

def inicia():
    """
    Funcion de modulo inicia servicios despues del reinicio del sistema.
    CLI PRD:
        salt '*' inicia.inicia
    """
    i=1
    while i<=8:
        try:
            Iniciar_Servicios = open("C:\Temp\Servicios_Ejecutandose.txt", mode="r")
            for x in Iniciar_Servicios:
                xf =x.replace("SERVICE_NAME: ", "net start ")
                os.system(xf)
            Iniciar_Servicios.close
            os.system ("del C:\Temp\Servicios_Ejecutandose.txt")
            i=8
            exit
        except OSError as err:
            time.sleep(900) #espera de 45 minutos para que el servidor reinicie sin problemas
            i=i+1

~                                                              