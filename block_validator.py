#!/usr/bin/env python3

from merkle import merkle_root

def chain_verify(chain):
    x = 0
    y = len(chain)
    while x < y:
        if x + 1 != y and chain[x]['hash'] == chain[x + 1]['previous_hash']:
            if merkle_root(chain[x]['transactions']) == chain[x]['merkle_root']:
                x += 1
            else:
                return False
        elif x + 1 == y:
            return True
        else:
            return False
