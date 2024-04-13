#! /usr/bin/env python3

import os, sys, re

def redirecting(args):
    if('>' in args):
        redirSymbol = args.index('>')
        outputFile = args.pop(redirSymbol + 1)
        args.pop(redirSymbol)
        os.close(1)
        os.open(outputFile, os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        return True

    if('<' in args):
        redirSymbol = args.index('<')
        inputFile = args.pop(redirSymbol + 1)
        args.pop(redirSymbol)
        os.close(0)
        os.open(inputFile, os.O_RDONLY)
        os.set_inheritable(0, True)
        return True
    
    return False
