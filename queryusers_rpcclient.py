#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# yay termcolor
# check you have rpcclient tools
# ;)
#

import subprocess
import os
import subprocess
import getopt
from sys import *
from termcolor import colored, cprint

banner = '''
                          _  _               _   
                         | |(_)             | |  
  _ __  _ __    ___  ___ | | _   ___  _ __  | |_ 
 | '__|| '_ \  / __|/ __|| || | / _ \| '_ \ | __|
 | |   | |_) || (__| (__ | || ||  __/| | | || |_ 
 |_|   | .__/  \___|\___||_||_| \___||_| |_| \__|
       | |                                       
       |_| query all users found.                                     

by g0h4n

'''
messagebox = "[+] command execute : "
log = False

def usage():
    cprint(banner, 'cyan', attrs=['bold'], file=stderr)
    cprint("Usage: queryusers_rpcclient.py -u <URL>\n", 'red', attrs=['bold'], file=stderr)
    cprint("Arguments:\n", 'red', attrs=['bold'], file=stderr)
    cprint("-h --help			-print this help", 'red', attrs=['bold'], file=stderr)
    cprint("-i --ip			    -You need to add one host", 'red', attrs=['bold'], file=stderr)
    cprint("-o --outputfile	    -Add file name to save the output", 'red', attrs=['bold'], file=stderr)
    cprint("")
    exit(0)
#Fin_de_def_usage


def argscheck():
    #No args ? help
    if not len(argv[1:]):
        usage()

    #Check args
    try:
        opts, args = getopt.getopt(argv[1:],"-h-i:-o:", ["help","ip", "outputfile"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        exit(1)

    host = ""
    path = ""
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-i","--ip"):
            host = str(a)
        elif o in ("-o","--outputfile"):
            path = str(a)
        else:
            assert False, "unhandled option"
    return (host, path)
#End_def_argscheck


#Main script :
ipaddress, path = argscheck()

if path != "":
    log = True
    outputfile = open(path,"w")

try :
    cprint(banner, 'cyan', attrs=['bold'])
    if log == True:
        outputfile.write(banner)
        cprint("[?] The file will be save at : " + path + "\n", 'cyan', attrs=['bold'])

    command = 'rpcclient -U "" -N ' + ipaddress + ' -c enumdomains'
    cprint(messagebox + command + "\n", 'magenta', attrs=['bold'])
    out_command = subprocess.getoutput([command])
    cprint(out_command, 'green', attrs=['bold'])
    if log == True:
        outputfile.write("\n" + command + "\n" + out_command + "\n")

    command = 'rpcclient -U "" -N ' + ipaddress + ' -c enumdomusers'
    cprint("\n" + messagebox + command + "\n", 'magenta', attrs=['bold'])
    out_command = subprocess.getoutput([command])
    cprint(out_command, 'green', attrs=['bold'])
    if log == True:
        outputfile.write(command + "\n" + out_command + "\n")

    usersfile = open("/tmp/rpcclientlogs_users",'w')
    usersfile.write(out_command)
    usersfile.close()

    usersfile = open("/tmp/rpcclientlogs_users","r")
    lines = usersfile.readlines()
    usersfile.close()

    command = 'rpcclient -U "" -N ' + ipaddress + ' -c enumdomgroups'
    cprint("\n" + messagebox + command + "\n", 'magenta', attrs=['bold'])
    out_command = subprocess.getoutput([command])
    cprint(out_command, 'green', attrs=['bold'])
    if log == True:
        outputfile.write(command + "\n" + out_command + "\n")

    for line in lines:
        if ('user:' in line):
            name_user = str(line.split('[')[1].split(']')[0])
            id_user = str(line.split('[')[2].split(']')[0])
            command = 'rpcclient -U "" -N ' + ipaddress + ' -c "queryuser ' + id_user + '"'
            cprint("\n" + messagebox + command + "\n[+] user = " + name_user + "\n", 'magenta', attrs=['bold'])
            out_command = subprocess.getoutput([command])
            cprint(out_command, 'green', attrs=['bold'])

            if log == True:
                outputfile.write("\n" + command + "\n" + out_command + "\n")
                
    if log == True:
        outputfile.close()

except :
    cprint("\n[!] Error\n", 'red', attrs=['bold'], file=stderr)
    exit(1)
