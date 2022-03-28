import sys
cliente = (sys.argv[1])
archivo3 = ("/srv/salt/"+ cliente +"1.txt")
a =("salt 'NGIT-AUT-001' cmd.run ")
print (a,'cat /var/lib/docker/volumes/jenkins_home/_data/jobs/'+"'" + cliente + "_(WINDOWS)_PARCHES_DE_SEGURIDAD" + "'" + '/config.xml | grep "&#xd;"'+" | sed 's/<description>//g' | sed 's/&#xd;//g' | sed -r 's/\s+//g'"+' >>'+archivo3)