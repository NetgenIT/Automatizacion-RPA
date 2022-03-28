import sys
cliente = (sys.argv[1])
archivo1 = ("/srv/salt/files_txt/Lista_Servidores_Parchados_Cliente_"+cliente+".txt")
a =("salt '")
b =("' cmd.run 'type c:\Temp\status.txt'" + ">>/srv/salt/files_txt/Status_Parchado"+cliente+".txt")
with open(archivo1, 'r+') as f_obj:
    for line in f_obj:
        print(a,line.strip()+ b)