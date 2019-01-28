#!/usr/bin/env python3

from serializer import Deserializer,deserializeValidator
from tx_validator import tx_validator
from transaction import Transaction
import wallet, ecdsa, binascii

def pendingtopool(serialize):

    if deserializeValidator(serialize) == False:
        print("Not appended to pending pool")
        return False

    f = open('mempool', 'a')
    f.write(serialize + '\n')
    f.close

    f = open('mempool', 'r')
    trans = f.readlines()[-3:]
    f.close()
    return trans
