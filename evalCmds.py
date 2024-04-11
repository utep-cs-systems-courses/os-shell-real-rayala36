#! /usr/bin/env python3

import sys, os, re

def evalCmds(clArgs, pid, waiting, childToCmdMap):
    filesToEval = re.split(" > ", clArgs)
    redirects = None
    if(len(filesToEval) > 1):
        redirects = filesToEval.pop(1)

    argLine = re.split(" ", filesToEval[0])
    x = 0
    while(x < len(argLine)):
        if(argLine[x] == "exit"):
            os.write(1, "Terminating Shell...\n".encode())
            exit()
        elif(argLine[x] == "cd"):
            if(len(argLine) > x+1):
                os.chdir(filesToEval[x+1])
                x+=1
        elif(argLine[x] == "cat"):
            if(len(argLine) > x+1):
                os.write("Printing Command of File Contents".encode())
        elif(argLine[x] == "ls"):
            os.write("Print Command of All File Names in a Directory".encode())
        else:
            child = os.fork()

            if(child < 0):
                print("Child Process Could Not Be Generated :/")

            elif(child==0):
                #At least one redirect was detected 
                if(redirects != None):
                    os.close(1)
                    os.open(redirects, os.O_CREAT | os.O_WRONLY)
                    os.set_inheritable(1, True)

                    command = argLine[x]
                    filesToManipulate = argLine[x:]
                    try:
                        os.execve(command, filesToManipulate, os.environ)
                    except FileNotFoundError:
                        pass
                else:
                    command = argLine[x]
                    filesToManipulate = argLine[x:]
                    try:
                        os.execve(command, filesToManipulate, os.environ)
                    except FileNotFoundError:
                        pass
            else:
                childToCmdMap[child] = argLine[x]
                if(argLine[x][-1] != "&"):
                    waiting = child
                else:
                    waiting = None
                
