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
from datetime import datetime
import shutil

ahora = time.strftime("%c")
cliente = (sys.argv[1])
now = datetime.today().strftime('%Y_%m_%d_%H_%M')


os.system ("mkdir /srv/salt/Informes_Parchados_"+cliente)
os.system ("mkdir /srv/salt/Informes_Parchados")




tecnico="Claudio Gonzalez Rodriguez "
mail="squadretail&fintech@tivit.com"

frase = cliente
if re.findall('ESSBIO*', frase):
    tecnico="German Jose Sandoval Martinis"
    mail="SquadUtilities@tivit.com"

a=("/srv/salt/files_txt/")


#archivo = ("/srv/salt/files_txt/Parchado_Minion"+cliente+".txt")
archivo1 = (a+"Lista_Servidores_Parchados_Cliente_"+cliente+".txt")
archivo2 = (a+"Status_Parchado"+cliente+".txt")
archivo3 = ("/srv/salt/"+ cliente +".txt")
archivo4 = (a+cliente+"comando.txt")
archivo5 = (a+cliente+"comando2.txt")
archivo6 = (a+"Informe"+ cliente +".txt")
archivo7 = (a+cliente+"informecmd.txt")
archivo8 = (a+cliente+"informecmd2.txt")
archivo9 = ("/srv/salt/correos_informes/Informe_Parchado_"+cliente+"_"+now+".zip")
archivo10 = ("/srv/salt/Informes_Parchados/*.*")




def conecta1():

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('10.33.27.124', 22, 'root', 'T1v1t$01.')
    ssh_client.exec_command("rm "+ archivo3 +" -f")
    ssh_client.exec_command("rm /srv/salt/*.txt -f")

    ssh_client.exec_command('cat /var/lib/docker/volumes/jenkins_home/_data/jobs/'+"'" + cliente + "_(WINDOWS)_PARCHES_DE_SEGURIDAD" + "'" + '/config.xml | grep "&#xd;"'+" | sed 's/<description>//g' | sed 's/&#xd;//g' | sed -r 's/\s+//g'"+' >>'+archivo3)

    ssh_client.close()

#def conecta1():

#    try:
#        os.system ("salt 'NGIT-AUT-001' cmd.run +"'cat /var/lib/docker/volumes/jenkins_home/_data/jobs/'+"'" + cliente + "_(WINDOWS)_PARCHES_DE_SEGURIDAD" + "'" + '/config.xml | grep "&#xd;"'+" | sed 's/<description>//g' | sed 's/&#xd;//g' | sed -r 's/\s+//g'"+' >>'+archivo3)

#    except:
#        print('no ejecuto comando')


def Lectura():

    try:
        os.system ("salt 'NGIT-NODO-001' cmd.run 'cat /srv/salt/"+ cliente +".txt'"+">/srv/salt/files_txt/Lista_Servidores_Parchados_Cliente_"+ cliente +".txt")
        os.system ("salt 'NGIT-NODO-001' cmd.run 'cat /srv/salt/"+ cliente +".txt'"+">/srv/salt/files_txt/Informe"+ cliente +".txt")

    except:
        print('Nombre del servidore erroneo')
        
def limpia():

    try:
        subprocess.call(['sed','-i','/.*NGIT-NODO-001:*/d',archivo1])
        subprocess.call(['sed','-i','/.*NGIT-NODO-001:*/d',archivo6])

    except:
        print('Nombre del servidore erroneo')
def crea():

    try:
        os.system("python3 /srv/salt/revisiones/crea3.py "+cliente+" >/srv/salt/files_txt/"+cliente+"comando.txt")
        os.system("python3 /srv/salt/revisiones/informe.py "+cliente+" >/srv/salt/files_txt/"+cliente+"informecmd.txt")


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


def limpiainf():

    try:
        ir =open(archivo7, mode='r')
        sinf =open(archivo8, mode='w')
        for i in ir:
            yfi =i.replace("salt ' ","salt '")
            sinf.write(yfi)
        ir.close()
        sinf.close()
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

def ejecuta2():

    try:
        ff =open(archivo8, mode="r")
        for z in ff:
            os.system(z)
        ff.close()
    except:
        print('Archivos no encontrados')

def copias():

    os.system("cp /srv/salt/Informes_Parchados/*.* /srv/salt/Informes_Parchados_"+cliente+"/")

def compresion():

    try:
        shutil.make_archive("/srv/salt/files_txt/Informe_Parchado","zip",root_dir="/srv/salt/Informes_Parchados/")

    except:
        print('no pudo comprimir')


def mueve():

    os.system("mv /srv/salt/files_txt/Informe_Parchado.zip /srv/salt/correos_informes/Informe_Parchado_"+cliente+"_"+now+".zip")

def correo():

    try:
        #pedir datos

        username = 'netgenittivit@synapsis-it.com'

        destinatario =['claudio.gonzalez@tivit.com','walterio.mendez@tivit.com','demian.rivas@tivit.com']
#        destinatario =['walterio.mendez@tivit.com']


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
                <td width="570" align="center" bgcolor="#B0ACAB"><h3>Adjunto Listado Servidores Pachados -- Adjunto Informe Parchado por servidor</h3></td>
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

        with open(archivo9, "rb") as adjunto2:
            contenido_adjunto2 = MIMEBase("application","octet-stream")
            contenido_adjunto2.set_payload(adjunto2.read())

        encoders.encode_base64(contenido_adjunto2)
        contenido_adjunto2.add_header(
            "content-Disposition",
            f"attachment; filename= {archivo9}",
        )

        mensaje.attach(contenido_adjunto2)

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
        os.system ("rm "+ archivo7 +" -f")
        os.system ("rm "+ archivo8 +" -f")
        os.system ("rm "+ archivo10 +" -f")
        os.system ("rm "+ archivo6 +" -f")

    except:
        print('no fueron encontrados los archivos')


conecta1()
Lectura()
limpia()
crea()
limpia2()
limpiainf()
ejecuta()
ejecuta2()
copias()
compresion()
mueve()
correo()
borrar()






