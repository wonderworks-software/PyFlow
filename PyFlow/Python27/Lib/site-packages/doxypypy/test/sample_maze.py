#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a simple maze pattern.

Tip of the hat to both the original Commodore 64 program and the book
"10 Print Chr$(205.5+rnd(1)); Goto 10" that it inspired.

Note that this is neither the shortest nor the most faithful way to
write this program in Python. Rather it is being used as a simple
example for the doxypypy Doxygen input filter for Python and makes use
of features like keyword arguments and generators and has a docstring
that documents them both appropriately.
"""

from sys import stdout
from random import choice


def generateBlock(blockOptions=u"╱╲"):
    """
    Generates a single block of a maze.

    This simple generator randomly picks a character from a list (the two
    diagonal lines by default) and returns it on each iteration.

    Kwargs:
        blockOptions -- The list of characters to choose from.

    Yields:
        A single character chosen from blockOptions.
    """
    while True:
        yield choice(blockOptions)

# Establish our block generator and generate a series of blocks.
blockGenerator = generateBlock()
blockCount = 0
while blockCount < 3200:
    blockCount += 1
    print(next(blockGenerator)),
    # Deal with Python's extra space print weirdness.
    stdout.softspace = False
