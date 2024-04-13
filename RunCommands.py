#! /usr/bin/env python3

import os, sys, re

def runCmd(args):
    try:
        os.execve(args[0], args, os.environ)
    except FileNotFoundError:
        pass

    for directory in re.split(":", os.environ['PATH']):
        commandToExec = f"{directory}/{args[0]}"
        try:
            os.execve(commandToExec, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, f"{args[0]}: This command does not exist.  Sorry!".encode())
    exit(1)
