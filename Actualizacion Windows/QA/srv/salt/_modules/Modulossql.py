import re
import os
import platform
import socket
import time
import salt.modules.win_wua
import salt.utils.win_reg
import salt.modules.win_service
import salt.modules.win_file


def actualizasql():
        
    """
    Funcion de modulo actualizacion parches Microsoft.
    CLI PRD:
        salt '*' modulossql.actualizasql
    """
    
    #crea Carpeta donde estaran Archivos
    os.system('md c:\Informes_Parchado')
    os.system('md C:\Temp')

    #lleva servicios activos antes de la actualizacion a un archivo
    os.system('sc queryex type= service >C:\Temp\servicios.txt')
    Servicios_Running = open('c:\Temp\servicios.txt',mode='r')
    Servicios_Depurados = open("C:\Temp\Servicios_Running.txt", mode="w")
    for elemento in Servicios_Running:
        if re.findall('^SERVICE_NAME', elemento):
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

        #wsusip = registro_wsus(r"HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate", "")
        if WSUSSER == 1:
            
            #Modifica registro wsus para eliminar mensajes del sistema update
            hive = 'HKLM'
            key = 'SOFTWARE\\Policies\\Services\\Microsoft\\Windows\\WindowsUpdate\\AU'
            salt.utils.win_reg.set_value(hive, key, 'DetectionFrequencyEnabled', vtype='REG_DWORD', vdata='0')
         
            hive = 'HKLM'
            key = 'SYSTEM\\ControlSet001\\Services\\msiserver'
            salt.utils.win_reg.set_value(hive, key, 'Start', vtype='REG_DWORD', vdata='2')

            #baja Servicios involucatados en parchado
            salt.modules.win_service.stop ('wuauserv')
            salt.modules.win_service.stop ('cryptSvc')
            salt.modules.win_service.stop ('bits')
            salt.modules.win_service.stop ('msiserver')

            #renombra archivo de parchado
            os.system('ren C:\Windows\SoftwareDistribution SoftwareDistribution_old')
            os.system('ren C:\Windows\System32\catroot2 Catroot2.old')

            #Sube Servicios involucrados en parchado
            salt.modules.win_service.start ('wuauserv')
            salt.modules.win_service.start ('cryptSvc')
            salt.modules.win_service.start ('bits')
            salt.modules.win_service.start ('msiserver')

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

    hive2 = 'HKLM'
    key2 = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\Results\\Detect'
    Detect = salt.utils.win_reg.read_value(hive2, key2, 'LastSuccessTime').get('vdata')

    hive3 = 'HKLM'
    key3 = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\Results\\Download'
    Download = salt.utils.win_reg.read_value(hive3, key3, 'LastSuccessTime').get('vdata')

    os.system('wmic qfe get Description,hotfixid,installedon /format:texttablewsys > "c:\Temp\ListadoParches.txt"')
    Listado_Parches_Instalados = open('C:\Temp\ListadoParches.txt', mode="r")
    Listado_Parches = Listado_Parches_Instalados.read()
    Listado_Parches_Instalados.close()


    #crea informe de actualizacion
    Informe = open("C:\Temp\Informe_actualizacion.txt", mode="w")
    Informe.write("I N F O R M E   A C T U A L I Z A C I O N   D E L   S I S T E M A  O P E R A T I V O \n")
    Informe.write("------------------------------------------------------------------------------------ \n")
    Informe.write(" \n")
    Informe.write("                     Actualizacion realizada conectada a %s" % WSUSIP)
    Informe.write(" \n")
    Informe.write("------------------------------------------------------------------------------------ \n")
    Informe.write(" \n")
    Informe.write("Nombre del Sistema Operativo  :{}".format(sistema))
    Informe.write(" \n")
    Informe.write("Nombre del Equipo             :%s" % hostname)
    Informe.write(" \n")
    Informe.write("Direccion Ip del Equipo       :%s" % ip_address1)
    Informe.write(" \n")
    Informe.write("Fecha y hora del Equipo       :%s" % ahora )
    Informe.write(" \n")
    Informe.write("Lugar que realiza descargas   :%s" % WSUSIP)
    Informe.write(" \n")
    Informe.write(" \n")
    Informe.write("W I N D O W S   U P D A T E   R E S U M E N  \n")
    Informe.write("-------------------------------------------- \n")
    Informe.write(" \n")
    Informe.write("Most recent check for Update : %s"  % Detect)
    Informe.write(" \n")
    Informe.write("Update were Installed        : %s"  % Download)
    Informe.write(" \n")
    Informe.write("Most recent successful Update: %s"  %last_updated)
    Informe.write(" \n")
    Informe.write(" \n")
    Informe.write("                       I N F O R M E   D E   P A R C H A D O  \n")
    Informe.write("                       -------------------------------------- \n")
    Informe.write(" \n")
    Informe.write("D E T A L L E   P A R C H E S   D I S P O N I B L E S   P A R A   S E R   I N S T A L A D O S  \n")
    Informe.write("---------------------------------------------------------------------------------------------- \n")
    Informe.write(" \n")
    if disponibles == "Nothing to return":
        Informe.write("No existen parches disponibles para instalar")
        Informe.write(" \n")
    else:
        Informe.write("%s"%disponibles)
        Informe.write(" \n")
    Informe.write(" \n")
    Informe.write("D E T A L L E   P A R C H E S    I N S T A L A D O S  \n")
    Informe.write("---------------------------------------------------- \n")
    Informe.write(" \n")
    if instalados == "Nothing to return":
        Informe.write("No hubo instalacion de parches")
        Informe.write(" ")
    else:
        Informe.write("%s"%instalados)
    Informe.write(" \n")
    Informe.write("L I S T A D O   D E   P A R C H E S   E N   E L   S I S T E M A  \n")
    Informe.write("---------------------------------------------------------------- \n")
    Informe.write(" \n")
    Informe.write("%s"%Listado_Parches)
    Informe.close()

    #Generar informe archivo con fecha y hora    
    os.system('copy C:\Temp\informe_actualizacion.txt c:\Python\Informe_actualizacion_%date:~-4,4%-%date:~-7,2%-%date:~-10,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%.txt')
         
    #remueve archivos temporales
    os.system ("del C:\Temp\Cantidad_Parches_Instalados_ING.txt")
    os.system ("del C:\Temp\Cantidad_Parches_Instalados_SPA.txt")
    os.system ("del C:\Temp\Cantidad_Parches_Instalados_ING_B.txt")
    os.system ("del C:\Temp\Cantidad_Parches_Instalados_SPA_B.txt")
    os.system ("del C:\Temp\ListadoParches.txt")
    os.system ("del C:\Temp\servicios.txt") 
    os.system ("del C:\Temp\servicios_run.txt")
    ## para ejecutar modulo de rescate informe este paso,, debe ser creado en modulo revision
    os.system ("del C:\Temp\informe_actualizacion.txt")


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