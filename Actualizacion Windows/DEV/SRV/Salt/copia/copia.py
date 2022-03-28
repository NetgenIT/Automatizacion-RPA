import os

def copia():
    
    servidores =open('/srv/salt/copia/servidores.txt', mode='r')
    FL =open('/srv/salt/copia/FL.txt', mode= 'w')
    for x in servidores:
        xf =x.replace("$", "salt-cp '")
        FL.write(xf)
    FL.close
    servidores.close

    FL =open('/srv/salt/copia/FL.txt', mode='r')
    FL2 =open('/srv/salt/copia/FL2.txt', mode= 'w')
    for y in FL:
        yf =y.replace("!", "' /srv/salt/_modules/: /srv/salt/_modules/:  ")
        FL2.write(yf)
    FL.close()

    FL2 =open("/srv/salt/copia/FL2.txt", mode="r")
    FL3 =open("/srv/salt/copia/FL3.txt", mode="w")
    for x in FL2:
        xf =x.replace(":", "modulosapp.py")
        FL3.write(xf)
    FL3.close
    FL2.close 
    
    FL2 =open("/srv/salt/copia/FL2.txt", mode="r")
    FL4 =open("/srv/salt/copia/FL4.txt", mode="w")
    for x in FL2:
        xf =x.replace(":", "modulossql.py")
        FL4.write(xf)
    FL4.close
    FL2.close
    
    FL2 =open("/srv/salt/copia/FL2.txt", mode="r")
    FL5 =open("/srv/salt/copia/FL5.txt", mode="w")
    for x in FL2:
        xf =x.replace(":", "modulosCheck.py")
        FL5.write(xf)
    FL5.close
    FL2.close

def comando():

    f =open("/srv/salt/copia/FL3.txt", mode="r")
    for z in f:
        print(z)
        os.system(z)

    ff =open("/srv/salt/copia/FL4.txt", mode="r")
    for zf in ff:
        print(zf)
        os.system(zf)

    ffs =open("/srv/salt/copia/FL5.txt", mode="r")
    for zfs in ffs:
        print(zfs)
        os.system(zfs)
    

def actualiza():

    os.system('salt "*" saltutil.sync_modules')

def borrar():

    os.system('rm /srv/salt/copia/FL*.txt')


copia()
comando()
actualiza()
borrar()
