#! /usr/bin/env python3

import os, sys, re

pid = os.getpid()
waiting = 0
childToCmdMap = {}

def execShell(pid, waiting, childToCmdMap):
    while(True):
        while(childToCmdMap.keys()):
            if(waiting != None):
                # Child process will need to complete first
                waitingStatus = os.waitid(os.P_ALL, waiting, os.WEXITED)
                zombieId = waitingStatus.si_pid
                zombieStatus = waitingStatus.si_status
                del childToCmdMap[waiting]
                waiting = None
                print("The Zombie has been reaped\n")
            else:
                waitingStatus =  os.waitid(os.P_ALL, 0, os.WNOHANG | os.WEXITED)
                # Background process will not hang
                zombieId = waitingStatus.si_pid
                zombieStatus = waitingStatus.si_status
                del childToCmdMap[zombieId]
                print("The zombie has been reaped.\n")
                
        os.write(1, "$ ".encode())
        clArgs = os.read(0, 100)
        if len(clArgs)==0:
            sys.exit(1)
        else:
            filesToExec = clArgs.decode().replace('\n', '')
            filesToExec = re.split(" - ", filesToExec)
            for files in filesToExec:
                files = re.split(" < ", files)
                x = 0
                while(x < len(files)):
                    if(files[x]=="exit"):
                        os.write(1, "Terminating\n".encode())
                        sys.exit(1)
                    elif(files[x]=="ls"):
                        print("Listing Command")
                    elif(files[x]=="cat"):
                        if((len(files)) > x+1):
                            print("Printing Command")
                    elif(filesToExec[x]=="cd"):
                        if((len(files)) > x+1):
                            os.chdir(files[x+1])
                            x = x+1
                    else:
                        # Child Process will execute first
                        childProcess = os.fork()
                        if(childProcess < 0):
                            os.write(2, ("Child Process %d could not be created." %childProcess).encode())
                        
                        elif(childProcess==0):
                            if( (len(files)) > 1):
                                os.close(1)
                                os.open(files[x+1], os.O_CREAT | os.O_WRONLY)
                                os.set_inheritable(1, True)

                                # If the command line reads

                                files = re.split(" ", files[x])
                                command = files[x]
                                filesToExec = files[x:]
                                try:
                                    os.execve = args[i:]
                                except FileNotFoundError:
                                    print("It would seem one of your files is missing :/")
                                    pass
                            else:
                                    
                                command = files[x]
                                filesToExec = files[x:]
                                try:
                                    os.execve(command, filesToExec, os.environ)
                                except FileNotFoundError:
                                    os.write(2, ("Command %s could not be executed" % command).encode())
                                    pass
                        else:
                            # Child ID mapped to command
                            childToCmdMap[childProcess] = argv[x]
                            if(argv[x][-1] != "&"):
                                waiting = childProcess
                            else:
                                waiting = None
                    x+=1

execShell(pid, waiting, childToCmdMap)
                        
