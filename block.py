#!/usr/bin/env python3

from merkle import merkle_root
from serializer import deserializeValidator
import time, hashlib

class Block(object):

    def __init__(self, previous_hash, transactions):
        self.timestamp = time.time()
        self.nonce = 0
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.merkle_root = merkle_root(transactions)
        self.hash = 0


    def blockhash(self):
        return hashlib.sha256((str(self.timestamp) + str(self.nonce) +\
                str(self.previous_hash) + str(self.transactions) +\
                str(self.merkle_root)).encode()).hexdigest()


    def validatesall(self):
        x = 0

        while x < len(self.transactions):
            if deserializeValidator(self.transactions[x][:-1]) == False:
                return False
            x += 1
        if x == len(self.transactions):
            return True

