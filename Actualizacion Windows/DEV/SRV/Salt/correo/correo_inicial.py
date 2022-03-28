import os
import re
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


archivo1 = ("/srv/salt/files_txt/text"+cliente+"1.txt")
archivo3 = ("/srv/salt/"+ cliente +"1.txt")
archivo15 = ("/srv/salt/files_txt/"+cliente+"comandoss.txt")
archivo16 = ("/srv/salt/TIVIT_GRUPO011.txt")


def conecta1():

    try:
        os.system("python3 /srv/salt/correo/crea2.py "+cliente+" >/srv/salt/files_txt/"+cliente+"comandoss.txt")
    except:
        print('Archivo no encontrado')

   
def ejecuta():

    try:
        f =open(archivo15, mode="r")
        for z in f:
            os.system(z)
        f.close()
    except:
        print('Archivos no encontrados')


def correo():

    #pedir datos

    username = 'netgenittivit@synapsis-it.com'

    #destinatario =[mail,'claudio.gonzalez@tivit.com','ruben.galaz@tivit.com','walterio.mendez@tivit.com','demian.rivas@tivit.com']
    destinatario =['walterio.mendez@tivit.com']

    asunto = 'ROBOT AUTOMATIZACION PARCHADO TIVIT'

    #Crear mensaje
    mensaje = MIMEMultipart("alternative") 
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
            <table id="header" cellpadding="0" cellspacing="10" align="center" bgcolor="#FFFFFF">
            <tr>
                <td width="570" align="center" bgcolor="#FFFFFF"><h2>Se da inicio al parchado para servidores de nuestro cliente "{cliente}"</h2></td>
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



    with open(archivo3, "rb") as adjunto:
        contenido_adjunto = MIMEBase("application","octet-stream")
        contenido_adjunto.set_payload(adjunto.read())

    encoders.encode_base64(contenido_adjunto)
    contenido_adjunto.add_header(
        "content-Disposition",
        f"attachment; filename= {archivo3}",
    )

    mensaje.attach(contenido_adjunto)
    text = mensaje.as_string()

    #crear la conexion
    with smtplib.SMTP("10.33.27.18", 25) as server:
        server.sendmail(username, destinatario, text)

def borrar():

    os.system ("rm "+ archivo3 +" -f")



conecta1()
ejecuta()
correo()
borrar()