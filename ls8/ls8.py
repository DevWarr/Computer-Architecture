#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def run_cpu(file):
    cpu = CPU()

    cpu.load(file)
    cpu.run()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please pick an example program to execute like so:")
        print("py ls8.py examples/print8.ls8")
    elif sys.argv[1][-4:] != ".ls8":
        print("Please pick a program ending in '.ls8'")
    else:
        run_cpu(sys.argv[1])