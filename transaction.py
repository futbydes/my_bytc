#!/usr/bin/env python3

import hashlib, binascii

class Transaction(object):

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    
    def transactionhash(self):
        #concatenation of the sender, recipient, amount in appropriate order
        concat = self.sender + self.recipient + self.amount
        hashed = hashlib.sha256(bytes(concat, 'utf-8')).hexdigest()
        return hashed


class CoinbaseTransaction(Transaction):

    def __init__(self, amount = '50'):
        self.sender = bytes(b'0' * 34).decode()
        self.amount = amount
        self.recipient = None

