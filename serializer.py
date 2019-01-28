#!/usr/bin/env python3

import binascii,ecdsa
from transaction import CoinbaseTransaction, Transaction
from tx_validator import tx_validator

class Serializer(object):

    def __init__(self, sender, recipient, amount, pubkey, sig):
        self.amount = int(amount)
        self.amount = "{0:0{1}x}".format(self.amount,4)
        self.serialize = self.amount + sender + '0' + recipient + '0' +\
                pubkey + binascii.hexlify(sig).decode('utf-8')



class Deserializer(object):

    def __init__(self, serialize):
        self.amount = int(serialize[:4], 16)
        self.sender = serialize[4:38]
        self.recipient = serialize[39:73]
        self.pubkey = serialize[74:202]
        self.sig = serialize[202:]
        if (len(self.sig) % 2 != 0):
            self.sig = '0' + self.sig
            #for odd lenght string
        self.sig = binascii.unhexlify((self.sig).encode('utf-8'))


def deserializeValidator(serialize):
    des = Deserializer(serialize)
    trans = Transaction(des.sender, des.recipient,\
            str(des.amount))
    hashed = trans.transactionhash()
    verkey = ecdsa.VerifyingKey.from_string(binascii.unhexlify(des.pubkey),\
            curve=ecdsa.SECP256k1)

    if (tx_validator(trans, verkey, des.sig, hashed, ('03' if\
            int(des.pubkey[127], 16) & 1 else '02') + des.pubkey[:64])):
        pass
    else:
        print("Invalid transaction.")
        return False
