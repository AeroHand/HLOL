#!/usr/bin/env python
#python 
import sys
import os
import configparser
from getMagnet import GetFromBTSpread
from getKey import getKey
import urllib
from test.test_userlist import UserListTest
def key2mag():
    ifpath=input("Please drag file here:");
    if not os.path.isfile(ifpath):
        print("please input correct file path to process!");
        input("Press any key");
        os._exit(0);
    #Start Parse Text
    print(ifpath);
    dfile=open(ifpath,'r');
    dlist=[];
    for rline in dfile:
        rline=rline.strip('\n');
        if len(rline)==0:
            continue;
        if rline[0]=='=' or rline[0]=='#':
            continue;
        dlist[len(dlist):]=rline.split(' ');
    dfile.close();
    dfile=open(ifpath,'a');
    dfile.write("\n\n====Generated by pyHLOL====\n")
    totcount=len(dlist);
    curcount=0;
    for des in dlist:
        curcount+=1;
        if des != '':
             mag=GetFromBTSpread(des);
             dfile.write(mag+'\n');
        print('{0} / {1}'.format(curcount,totcount));
    dfile.close();
    input("Press any key");
    os.system("C:/Windows/System32/notepad.exe "+ifpath);
def jfpage2keys():
    ifpath=input("Please drag file here:");
    if not os.path.isfile(ifpath):
        print("please input correct file path to process!");
        input("Press any key");
        os._exit(0);
    #Start Parse Text
    print(ifpath);
    dfile=open(ifpath,'r');
    inUrl=[];
    for rline in dfile:
        if len(rline)==0:
            continue;
        if rline[0]=='=' or rline[0]=='#':
            continue;
        inUrl.append(rline.strip('\n'));
    dfile.close();
    dfile=open(ifpath,'a');
    dfile.write("\n\n====Generated by pyHLOL====\n")
    totcount=len(inUrl);
    curcount=0;
    for des in inUrl:
        curcount+=1;
        if des != '':
            keys=getKey(des);
            out_line='';
            for k in keys:
                out_line+=k+' ';
            dfile.write(out_line+"\n\n");
        print('{0} / {1}'.format(curcount,totcount));
    dfile.close();
    input("Press any key");
    os.system("C:/Windows/System32/notepad.exe "+ifpath);

#Program entrance
global useProxy,proxy,username,password;
cf=configparser.ConfigParser();
try:
    cf.read('./proxy.ini');
    useproxy=int(cf.get('Proxy','useproxy'));
    proxy=cf.get('Proxy', 'proxy');
    username=cf.get('Proxy', 'username');
    password=cf.get('Proxy', 'password');
except:
    sys.exit(1);
#install proxy
if useproxy==1:
    proxyconfig='http://%s:%s@%s' %(username,password,proxy);
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({'http':proxyconfig}));
    urllib.request.install_opener(opener);
mode=int(input("Please select Mode:\n\t1.Keys to magnet links\n\t2.javfree page to all keys.\n\n"));
if mode==1:
    key2mag();
elif mode==2:
    jfpage2keys();
else:
    print("Please keyin 1 or 2");



