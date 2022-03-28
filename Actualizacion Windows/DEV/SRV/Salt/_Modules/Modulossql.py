import re
import os
import platform
import socket
import time
from datetime import datetime
import salt.modules.win_wua
import salt.utils.win_reg
import salt.modules.win_service
import salt.modules.win_file



def actualizaapp():
    
    """
    Funcion de modulo actualizacion parches Microsoft.
    CLI PRD:
        salt '*' modulosapp.actualizaapp
    """
    

    try:
        #crea Carpeta donde estaran Archivos
        os.system('md c:\Informes_Parchado')
        os.system('md C:\Temp')

        #lleva servicios activos antes de la actualizacion a un archivo
        os.system('sc queryex type= service >C:\Temp\servicios.txt')
        Servicios_Running = open('C:\Temp\servicios.txt',mode='r')
        Servicios_Depurados = open("C:\Temp\Servicios_Ejecutandose.txt", mode="w")
        for elemento in Servicios_Running:
            if re.findall('^SERVICE_NAME:', elemento):
                f= elemento
                Servicios_Depurados.write(f)
                Servicios_Depurados.close
        Servicios_Running.close
        

        #Modifica registo opciones de busqueda de parches
        hive = 'HKLM'
        key = 'SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU'
        salt.utils.win_reg.set_value(hive, key, 'AUOptions', vtype='REG_DWORD', vdata='2')
        
        #rescata informacion de Update disponibles e instaldos en servidor via saltstack
        disponibles = salt.modules.win_wua.available(categories=["Security Updates"])
        instalados = salt.modules.win_wua.list(categories=["Security Updates"], summary=True)

        #Rescada datos del sistema operativo hacia variables
        sistema = platform.platform(terse=True)
        hostname = socket.gethostname()
        ip_address1 = socket.gethostbyname(hostname)
        ahora = time.strftime("%c")


        #Comprueba que existe Registro de wsus, de ser verdadero ejecuta comando de actualizacion para wsus, de lo contrario si registro no existe en vez de error realiza ejecucion de comandos para baja de parchado via internet
        try:
            hive = 'HKLM'
            key = 'SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU'
            WSUSSER = salt.utils.win_reg.read_value(hive, key, 'UseWUServer').get('vdata')

            hive = 'HKLM'
            key = 'SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate'
            WSUSIP = salt.utils.win_reg.read_value(hive, key, 'WUServer').get('vdata')

            if WSUSSER == 1:
                
                #Modifica registro wsus para eliminar mensajes del sistema update
                hive = 'HKLM'
                key = 'SOFTWARE\\Policies\\Services\\Microsoft\\Windows\\WindowsUpdate\\AU'
                salt.utils.win_reg.set_value(hive, key, 'DetectionFrequencyEnabled', vtype='REG_DWORD', vdata='0')
            
                hive = 'HKLM'
                key = 'SYSTEM\\ControlSet001\\Services\\msiserver'
                salt.utils.win_reg.set_value(hive, key, 'Start', vtype='REG_DWORD', vdata='2')


                #Modulo actualizaicon parches
                salt.modules.win_wua.list(categories=["Security Updates"], install=True)
            
            else:

                #varible para ver donde esta conectado
                WSUSIP = "Internet"

                #forzar actualizacion de parches
                salt.modules.win_wua.list(categories=["Security Updates"], install=True)
              
            
        except OSError as err:
            
            #varible para ver donde esta conectado
            WSUSIP = "Internet"

            #forzar actualizacion de parches
            salt.modules.win_wua.list(categories=["Security Updates"], install=True)
            
            
        #Variables e informacion de la actualizacion
        hive = 'HKLM'
        key = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\Results\\Install'
        last_updated = salt.utils.win_reg.read_value(hive, key, 'LastSuccessTime').get('vdata')

        hive = 'HKLM'
        key = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\Results\\Detect'
        Detect = salt.utils.win_reg.read_value(hive, key, 'LastSuccessTime').get('vdata')

        hive = 'HKLM'
        key = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\Results\\Download'
        Download = salt.utils.win_reg.read_value(hive, key, 'LastSuccessTime').get('vdata')

        os.system('wmic qfe get Description,hotfixid,installedon /format:texttablewsys > "c:\Temp\ListadoParches.txt"')
        Listado_Parches_Instalados = open('C:\Temp\ListadoParches.txt', mode="r")
        Listado_Parches = Listado_Parches_Instalados.read()
        Listado_Parches_Instalados.close()

        now = datetime.today().strftime('%Y_%m_%d_%H_%M')

        hostname = socket.gethostname()
        archivo01 = ("c:\\Temp\\informe_actualizacion.txt")
        archivo1 = ("c:\\Informes_Parchado\\"+hostname+"_Informe_Actualizacion_"+now+".txt")

        #crea informe de actualizacion
        archivo = open (archivo01, mode="w")
        archivo.write("I N F O R M E   A C T U A L I Z A C I O N   D E L   S I S T E M A  O P E R A T I V O \n")
        archivo.write("------------------------------------------------------------------------------------ \n")
        archivo.write(" \n")
        archivo.write("                     Actualizacion realizada conectada a %s" % WSUSIP)
        archivo.write(" \n")
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
        archivo.write("Lugar que realiza descargas   :%s" % WSUSIP)
        archivo.write(" \n")
        archivo.write(" \n")
        archivo.write("W I N D O W S   U P D A T E   R E S U M E N  \n")
        archivo.write("-------------------------------------------- \n")
        archivo.write(" \n")
        archivo.write("Most recent check for Update : %s"  % Detect)
        archivo.write(" \n")
        archivo.write("Update were Installed        : %s"  % Download)
        archivo.write(" \n")
        archivo.write("Most recent successful Update: %s"  %last_updated)
        archivo.write(" \n")
        archivo.write(" \n")
        archivo.write("                       I N F O R M E   D E   P A R C H A D O  \n")
        archivo.write("                       -------------------------------------- \n")
        archivo.write(" \n")
        archivo.write("D E T A L L E   P A R C H E S   D I S P O N I B L E S   P A R A   S E R   I N S T A L A D O S  \n")
        archivo.write("---------------------------------------------------------------------------------------------- \n")
        archivo.write(" \n")
        if disponibles == "Nothing to return":
            archivo.write("No existen parches disponibles para instalar")
            archivo.write(" \n")
        else:
            archivo.write("%s"%disponibles)
            archivo.write(" \n")
        archivo.write(" \n")
        archivo.write("D E T A L L E   P A R C H E S    I N S T A L A D O S  \n")
        archivo.write("---------------------------------------------------- \n")
        archivo.write(" \n")
        if instalados == "Nothing to return":
            archivo.write("No hubo instalacion de parches")
            archivo.write(" ")
            archivo.write(" \n")
        else:
            archivo.write("%s"%instalados)
        archivo.write(" \n")
        archivo.write("L I S T A D O   D E   P A R C H E S   E N   E L   S I S T E M A  \n")
        archivo.write("---------------------------------------------------------------- \n")
        archivo.write(" \n")
        archivo.write("%s"%Listado_Parches)
        archivo.close()


        #remueve archivos temporales   
        os.system ("del C:\Temp\Cantidad_Parches_Instalados_ING.txt")
        os.system ("del C:\Temp\Cantidad_Parches_Instalados_SPA.txt")
        os.system ("del C:\Temp\Cantidad_Parches_Instalados_ING_B.txt")
        os.system ("del C:\Temp\Cantidad_Parches_Instalados_SPA_B.txt")
        os.system ("del C:\Temp\ListadoParches.txt")
        os.system ("del C:\Temp\servicios.txt") 
        os.system ("del C:\Temp\servicios_run.txt")
        os.system ("del C:\Temp\Status.txt")
        os.system ("copy "+archivo01+" "+archivo1)

        #crea archivo de chequeo
        archivo = open("C:\Temp\Status.txt", mode="w")
        archivo.write("Actualizacion exitosa en Servidor: %s" % hostname)
        archivo.close()  

        if disponibles == "Nothing to return":
            exit
        else:
            os.system('sc query type= service state= all |find "SQL" |find /V "DISPLAY_NAME" |find /V "AD" | find /V "Writer" >C:\Temp\SQLServices.txt')
            Servicios_Running =open('c:\Temp\SQLservices.txt',mode='r')
            Servicios_Depurados = open("C:\Temp\servicios_SQL_run.txt", mode="w")
            for elemento in Servicios_Running:
                if re.findall('SERVICE_NAME: MSS', elemento):                    
                    f= elemento
                    Servicios_Depurados.write(f)
                    Servicios_Depurados.close
                    Servicios_Running.close
                    Detener_Servicios_sql = open("C:\Temp\servicios_SQL_run.txt", mode="r")
                    for xx in Detener_Servicios_sql:
                        xfx =xx.replace("SERVICE_NAME:", "net stop ")
                        os.system(xfx)
                        #reinicio del servidor
                        os.system('shutdown /r /t 0')
                    else:
                        exit

    except OSError as err:

        hostname = socket.gethostname()
        archivo =open("C:\Temp\Status.txt", mode ='r')
        archivo.write("Actualizacion Fallida!!!")
        archivo.close()