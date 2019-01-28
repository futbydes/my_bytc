#!/usr/bin/python3

import wallet, transaction, ecdsa, binascii, base58
from transaction import CoinbaseTransaction

def tx_validator(trans, verkey, sig, msg, pubkey):
    
    nosender = CoinbaseTransaction(None).sender
    if (trans.sender != nosender and tx_add_avail(trans.sender) == False) or\
            tx_add_avail(trans.recipient) == False:
                print("asa")
                return False
    elif trans.sender != nosender and\
            tx_add_verif(pubkey, trans.sender) == False:
        print("here?")
        return False
    elif tx_sig_verif(sig, verkey, msg) == False:
        print("yoo")
        return False
    else:
        return True


def tx_add_avail(address):

    b58dec = base58.b58decode(address)
    b58dec = binascii.hexlify(b58dec)
    if bytes(wallet.checksum(b58dec[:-8]), 'utf-8')[:8] == b58dec[-8:]:
        return True
    else:
        return False


def tx_add_verif(pubkey, address):

    address_ver = wallet.getnewaddress(pubkey)
    if bytes(address, 'utf-8') == address_ver:
        return True
    else:
        return False


def tx_sig_verif(sig, verkey, msg):
    try:
        verkey.verify(sig, bytes(msg, 'utf-8'))
        return True
    except ecdsa.BadSignatureError:
        return False
