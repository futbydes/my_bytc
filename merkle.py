#!/usr/bin/env python3

import hashlib

def merkle_root(trans):
    blocks = []
    x = 0

    while x != len(trans):
        blocks.append(hashlib.sha256(trans[x].encode('utf-8')).hexdigest())
        x += 1

    while len(blocks) != 1:
        if len(blocks) % 2 != 0:
            blocks.append(blocks[len(blocks) - 1])
        x = 0
        size = len(blocks)
        while x < size:
            blocks.append(hashlib.sha256((blocks[x] + blocks[x + 1])\
                    .encode('utf-8')).hexdigest())
            x += 2
        blocks = blocks[size:]

    return blocks

