import os
import time

ipsv =open('/srv/salt/memlinux/ips.txt', mode ='r')
ipsv2 =open('/srv/salt/memlinux/ipsv2.txt', mode='w')

lines = ipsv.read()
first = lines.split('\n',1)[0]
ipsv2.write(first)
ipsv.close()
ipsv2.close()
ipsv2 =open('/srv/salt/memlinux/ipsv2.txt', mode='r')
for i in ipsv2:
        yf =i.replace(":","")
        com =yf
        print("salt" , com, "modulosmem.memoria")
        os.system("salt " + com + " modulosmem.memoria")
time.sleep(15)
print("salt " + "'"+com+"'"+" cmd.run " + "'cat /root/srv/salt/memlinux/Informe_Memoria.txt'"+" >/srv/salt/memlinux/Informe_Memoria.txt")
os.system("salt " + "'"+com+"'"+" cmd.run " + "'cat /root/srv/salt/memlinux/Informe_Memoria.txt'"+" >/srv/salt/memlinux/Informe_Memoria.txt")
time.sleep(5)
os.system("salt " + "'"+com+"'"+" cmd.run " + "'cat /root/srv/salt/memlinux/Informe_Memoria.txt'")
time.sleep(30)