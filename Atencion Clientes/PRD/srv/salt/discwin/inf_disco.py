import os
import time

ipsv =open('/srv/salt/discwin/ips.txt', mode ='r')
ipsv2 =open('/srv/salt/discwin/ipsv2.txt', mode='w')

lines = ipsv.read()
first = lines.split('\n',1)[0]
ipsv2.write(first)
ipsv.close()
ipsv2.close()
ipsv2 =open('/srv/salt/discwin/ipsv2.txt', mode='r')
for i in ipsv2:
        yf =i.replace(":","")
        com =yf
        os.system("salt " + com + " modulosdisc_win.capacidad")
time.sleep(60)
os.system("salt " + "'"+com+"'"+" cmd.run " + "'type C:\Temp\Informe_disco.txt'")
time.sleep(60)
~                                                                                 