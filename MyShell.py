#! /usr/bin/env python3

import os, sys, re
from RunCommands import runCmd
from Pipe import piping
from Redirection import redirecting

while(True):
    shellPrompt = os.getenv('PS1', '$ ')
    print(shellPrompt, end='', flush=True)
    args = input().strip()

    if(args == ''):
        print("------")
        print("You entered no command >:(")
        print("------")
        continue

    if(args.lower() == 'exit'):
        print("Goodbye!")
        exit(0)

    args = list(filter(None, args.split(' ')))

    if(args[0].lower() == 'cd'):
        if(len(args) >= 2):
            if(args[1] == '..'):
                os.chdir('..')
            else:
                try:
                    os.chdir(args[1])
                except FileNotFoundError:
                    os.write(2, f"bash: cd: {args[1]}: This file/directory does not exit\n".encode())
        else:
            os.chdir(os.environ['HOME'])
        continue

    rc = os.fork()
    waitingStatus = True
    if(args[-1] == '&'):
        watingStatus = False
        args.pop()
    if(rc < 0):
        exit(1)
    elif(rc==0):
        if('|' in args):
            piping(args)
        elif('>' in args or '<' in args):
            if not redirecting(args):
                os.write(2, "Make sure your redirection command is written correctly\n".encode())
                continue
        runCmd(args)
    else:
        if(waitingStatus):
            os.wait()

    
    
        
