#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print("Please provide a program file!")

ls8_re = re.compile(r"^(?P<byte>[01]{8})?(\s*#(?P<comment>.*))?")

filename = sys.argv[1]
program = []

with open(filename, "r") as f:

    for line in f.readlines():
        m = ls8_re.match(line)
        if m and m.group("byte"):
            program.append(int(m.group("byte"), 2))

cpu.load(program)
cpu.run()