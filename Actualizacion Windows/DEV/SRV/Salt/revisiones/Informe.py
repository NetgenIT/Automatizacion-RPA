import sys
import os
from datetime import datetime
now = datetime.today().strftime('%Y_%m_%d_%H_%M')


cliente = (sys.argv[1])

archivo = ("/srv/salt/files_txt/Informe"+cliente+".txt")
a =("salt '")
b =("' cmd.run 'type C:\Temp\informe_actualizacion.txt'" + ">/srv/salt/Informes_Parchados/")
c =("_Informe_Parchado_")
with open(archivo, 'r+') as f_obj:
    for line in f_obj:
        print(a,line.strip()+ b+line.strip()+c+now+".txt")



