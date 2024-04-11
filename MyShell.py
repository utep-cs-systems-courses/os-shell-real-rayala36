#! /usr/bin/env python3

import os, sys, re

pid = os.getpid()
waiting = 0
childToCmdMap = {}

while(True):
    print("Parent ID: "+str(pid)+", Child ID: "+str(os.getpid()))
    # If the Parent ID and the Child ID are not equal, the shell will terminate; The Child is a clone of the Parent,
    # so you would want to have the two PIDs be equal.
    if(pid != os.getpid()):
        sys.exit(1)
    while(childToCmdMap.keys()):
        if(waiting != None):
            # Child process will need to complete first
            waitingStatus = os.waitid(os.P_ALL, waiting, os.WEXITED)
            zombieId = waitingStatus.si_pid
            zombieStatus = waitingStatus.si_status
            del childToCmdMap[waiting]
            waiting = None
            print("The Zombie has been reaped\n")
        elif(waitingStatus := os.waitid(os.P_ALL, 0, os.WNOHANG | os.WEXITED)):
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
        filesToExec = re.split(" \| ", filesToExec)
        for x in range(len(filesToExec)):
                
            if(os.getpid() != pid):
                os.write(1, "Child Terminating".encode())
                sys.exit(1)
                    
            if(len(filesToExec) > 1):
                pipeReader, pipeWriter = os.pipe()
                for fileDesc in (pipeReader, pipeWriter):
                    os.set_inheritable(fileDesc, True)
                childProcessWriter = os.fork()
                if (childProcessWriter < 0):
                    os.write(2, ("Child Process %d could not be created." %childProcessWriter).encode())
                    sys.exit(1)
                elif(childProcessWriter == 0):
                    os.close(1)
                    os.dup(pipeWriter)
                    for fileDescriptor in (pipeReader, pipeWriter):
                        os.close(fileDescriptor)

                else:
                    x += 1
                    childProcessReader  = os.fork()
                    if(childProcessReader < 0):
                        os.write(2, ("Child Process %d could not be created." %childProcessReader).encode())
                        sys.exit(1)
                    elif(childProcessReader == 0):
                        os.close(0)
                        os.dup(pipeReader)
                        for fileDescriptor in (pipeWriter, pipeReader):
                            os.close(fileDescriptor)
                    else:
                        for fileDescriptor in (pipeWriter, pipeReader):
                            os.close(fileDescriptor)
                        os.wait()

            filesToEval = re.split(" > ", clArgs[x])
            redirects = None
            if(len(filesToEval) > 1):
                redirects = filesToEval.pop(1)

            argLine = re.split(" ", filesToEval[0])
            y = 0
            while(y < len(argLine)):
                if(argLine[y] == "exit"):
                    os.write(1, "Terminating Shell...\n".encode())
                    exit()
                elif(argLine[y] == "cd"):
                    if(len(argLine) > y+1):
                        os.chdir(filesToEval[y+1])
                        x+=1
                elif(argLine[y] == "cat"):
                    if(len(argLine) > y+1):
                        os.write("Printing Command of File Contents".encode())
                elif(argLine[y] == "ls"):
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

                            command = argLine[y]
                            filesToManipulate = argLine[y:]
                            try:
                                os.execve(command, filesToManipulate, os.environ)
                            except FileNotFoundError:
                                pass
                        else:
                            command = argLine[y]
                            filesToManipulate = argLine[y:]
                            try:
                                os.execve(command, filesToManipulate, os.environ)
                            except FileNotFoundError:
                                pass
                    else:
                        childToCmdMap[child] = argLine[y]
                        if(argLine[y][-1] != "&"):
                            waiting = child
                        else:
                            waiting = None                        
