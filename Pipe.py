#! /usr/bin/env python3

import os, sys, re

def piping(args):
    pipeSymbol = args.index('|')
    left = args[:pipeSymbol]
    right = args[pipeSymbol + 1:]

    pipeReader, pipeWriter = os.pipe()

    rc = os.fork()
    if(rc < 0):
        exit(1)

    elif(rc == 0):
        os.close(1)
        os.dup(pipeWriter)
        os.set_inheritable(1, True)
        os.close(pipeReader)
        os.close(pipeWriter)
        runCmd(left)

    else:
        os.close(0)
        os.dup(pipeReader)
        os.set_inheritable(0, True)
        os.close(pipeReader)
        os.close(pipeWriter)
        runCmd(right)

