import sys
cliente = (sys.argv[1])
archivo = ("/srv/salt/files_txt/Parchado_Minion"+cliente+".txt")
a =("salt '")
b =("' cmd.run 'type c:\Temp\status.txt'" + ">>/srv/salt/files_txt/Status_Parchado"+cliente+".txt")
with open(archivo, 'r+') as f_obj:
    for line in f_obj:
        print(a,line.strip()+ b)