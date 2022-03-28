import socket
import os

def chequeo():
    """
    Funcion de modulo actualizacion parches Microsoft.
    CLI PRD:
        salt '*' moduloschq.chequeo
    """
    try:
        check =open("C:\Temp\Status.txt", mode ='r')
        lines = check.read()
        first = lines.split('\n',1)[0]
        print(first)

    except OSError as err:

        os.system('md C:\Temp')
        archivo =open("C:\Temp\Status.txt", mode ='r')
        archivo.write("Actualizacion Fallida!!!")
        archivo.close()



