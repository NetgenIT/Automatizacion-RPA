import re
import os
import paramiko
import sys
import time
import subprocess
import os
import smtplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

ahora = time.strftime("%c")
cliente = (sys.argv[1])

tecnico="Claudio Gonzalez Rodriguez "
mail="squadretail&fintech@tivit.com"

frase = cliente
if re.findall('ESSBIO*', frase):
    tecnico="German Jose Sandoval Martinis"
    mail="SquadUtilities@tivit.com"

archivo1 = ("/srv/salt/files_txt/Parchado_Minion"+cliente+".txt")
archivo2 = ("/srv/salt/files_txt/Status_Parchado"+cliente+".txt")
archivo3 = ("/srv/salt/"+ cliente +".txt")
archivo4 = ("/srv/salt/files_txt/"+cliente+"comando.txt")
archivo5 = ("/srv/salt/files_txt/"+cliente+"comando2.txt")



def conecta1():

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('10.251.205.11', 22, 'root', 'T1v1t$01.')
    ssh_client.exec_command("rm "+ archivo3 +" -f")
    ssh_client.exec_command("rm /srv/salt/*.txt -f")

    ssh_client.exec_command('cat /var/lib/docker/volumes/jenkins_home/_data/jobs/'+"'" + cliente + " - (WINDOWS) - Parches de Seguridad" + "'" + '/config.xml | grep "<target>" |  awk'+" '/,/ {print}'"+" | sed 's/<target>//g'"+" | sed 's/<\/target>//g'"+" | sed -r 's/\s+//g'"+" | awk '{ split($0,a,"+'",")'+"; for (i in a) print a[i]; }'"+' >>'+archivo3)
    ssh_client.exec_command('cat /var/lib/docker/volumes/jenkins_home/_data/jobs/'+"'" + cliente + " - (SQL) - Parches de Seguridad" + "'" + '/config.xml | grep "<target>" |  awk'+" '/,/ {print}'"+" | sed 's/<target>//g'"+" | sed 's/<\/target>//g'"+" | sed -r 's/\s+//g'"+" | awk '{ split($0,a,"+'",")'+"; for (i in a) print a[i]; }'"+' >>'+archivo3)
    
    ssh_client.close()

def Lectura():

    try:
        os.system ("salt 'NGITQA-AUT-001' cmd.run 'cat /srv/salt/"+ cliente +".txt'"+">/srv/salt/files_txt/Parchado_Minion"+ cliente +".txt")
        
    except:
        print('Nombre del servidore erroneo')

def limpia():

    try:
        subprocess.call(['sed','-i','/.*NGITQA-AUT-001:*/d',archivo1])
        
    except:
        print('Nombre del servidore erroneo')

def crea():

    try:
        os.system("python3 /srv/salt/revisiones/crea.py "+cliente+" >/srv/salt/files_txt/"+cliente+"comando.txt")
    except:
        print('Archivo no encontrado')



def limpia2():

    try:
        r =open(archivo4, mode='r')
        s =open(archivo5, mode='w')
        for i in r:
            yf =i.replace("salt ' ","salt '")
            s.write(yf)
        r.close()
        s.close()
    except:
        print('archivos no encontrados')

def ejecuta():

    try:
        f =open(archivo5, mode="r")
        for z in f:
            os.system(z)
        f.close()
    except:
        print('Archivos no encontrados')

def correo():

    try:
        #pedir datos

        username = 'netgenittivit@synapsis-it.com'

        destinatario =[mail,'claudio.gonzalez@tivit.com','walterio.mendez@tivit.com','demian.rivas@tivit.com','ruben.galaz@tivit.com']

        asunto = 'ROBOT AUTOMATIZACION PARCHADO TIVIT'

        #Crear mensaje
        mensaje = MIMEMultipart("alternative") #estandar
        mensaje["Subject"] = asunto
        mensaje["From"] = username
        mensaje["To"] = ','.join(destinatario)

        html = f"""
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>ROBOT AUTOMATIZACION PARCHES TIVIT</title>
        </head>
        <body>
        <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>
        <table id="top-message" cellpadding="10" cellspacing="10" width="600" align="center">
            <tr>
            <td align="center">
                <p><a href="#"></a></p>
            </table>
        <table id="main" width="600" align="center" cellpadding="0" cellspacing="5" bgcolor="ffffff">
            <tr>
            <td>
            <td align="center" bgcolor="#d80a3e">
            <FONT COLOR="white"><h2>SISTEMA DE PARCHADO AUTOMATIZADO</h2></FONT>
            <?php echo $cliente;?>
                <table id="header" cellpadding="0" cellspacing="10" align="center" bgcolor="#FFFFFF">
                <tr>
                    <td width="570" align="center" bgcolor="#FFFFFF"><h2>Ha finalizado el parchado para servidores de nuestro cliente "{cliente}"".</h2></td>
                </tr>
            </tr>
                <td width="570" align="center" bgcolor="#B0ACAB"><h3>Listado de servidores en archivo adjunto</h3></td>
            </tr>
                <td>Fecha: {ahora}</td>
                </tr>
                <td>Responsable Tecnico :"{tecnico} "</td>
                </tr>
                </table>
                <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                </tr>
                <td width="570" align="center" bgcolor="#FFFFFF"></td>
                </td>
                </td>
                </tr>
                </table>
            </td>
            </tr>
        </table>
        <table id="bottom" cellpadding="0" cellspacing="0" width="600" align="center">
            <tr>
            <td align="center">
                <p>Correo enviado por Robot Automation NETGENIT TIVIT</p>
                <p>Correo de uso interno, Favor no difundir</p>
        </body>
        </html>
        """
        #el contenido del mensaje como html
        parte_html = MIMEText(html, "html")
        #agregar este contenido al mensaje
        mensaje.attach(parte_html)



        with open(archivo2, "rb") as adjunto:
            contenido_adjunto = MIMEBase("application","octet-stream")
            contenido_adjunto.set_payload(adjunto.read())

        encoders.encode_base64(contenido_adjunto)

        contenido_adjunto.add_header(
            "content-Disposition",
            f"attachment; filename= {archivo2}",
        )

        mensaje.attach(contenido_adjunto)
        text = mensaje.as_string()

        #crear la conexion
        with smtplib.SMTP("10.33.27.18", 25) as server:
            server.sendmail(username, destinatario, text)
    except:
        print('imposible enviar correo')

def borrar():

    try:
        os.system ("rm "+ archivo2 +" -f")
        os.system ("rm "+ archivo4 +" -f")
        os.system ("rm "+ archivo5 +" -f")
        os.system ("rm "+ archivo1 +" -f")
    except:
        print('no fueron encontrados los archivos')


conecta1()
Lectura()
limpia()
crea()
limpia2()
ejecuta()
correo()
borrar()