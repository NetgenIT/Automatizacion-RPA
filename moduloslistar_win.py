import salt.modules.win_useradd
import salt.modules.win_status

def listar():

    """
    Funcion de modulo liberacion memoria windows.
    CLI PRD:
        salt '*' moduloslistar_win.listar
    """

    listar = salt.modules.win_useradd.list_users()
    disco =  salt.modules.win_status.diskusage()
    memoria = salt.modules.win_status.meminfo()

    archivo02 = ("c:\\Temp\\listado__users.txt")

    archivo2 = open (archivo02, mode="w")
    archivo2.write("L I S T A D O   U S U A R I O S\n")
    archivo2.write("---------------------------------------------------------------------------------------------- \n")
    archivo2.write(" \n")
    archivo2.write(" \n")
    archivo2.write("Listado de Usuario en servidor :%s" % listar)
    archivo2.write(" \n")
    archivo2.write(" \n")
    archivo2.write("Disco  :%s" % disco)
    archivo2.write(" \n")
    archivo2.write(" \n")
    archivo2.write("memoria  :%s" % memoria)
    archivo2.close