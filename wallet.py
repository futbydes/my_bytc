#!/usr/bin/env python3

import hashlib, binascii, base58, ecdsa
from secrets import randbits
from transaction import Transaction

def privtowif(key):

    if key == None:
        s_file = open('privkey', 'r')
        key = s_file.read(64) #32b
        s_file.close()

    verByte = "80" #0xEF - testnet
    comByte = "01" #optional Indicates if the public key is compressed.

    extended = verByte + key + comByte
    extended = extended + checksum(extended)[:8]
    wif = base58.b58encode(binascii.unhexlify(extended))
    return wif

def checksum(string):

    checksum = hashlib.sha256(binascii.unhexlify(string)).hexdigest()
    checksum = hashlib.sha256(binascii.unhexlify(checksum)).hexdigest()
    return (checksum)



def getnewprivkey():

    bits = randbits(256)
    bits_hex = hex(bits)
    privkey = bits_hex[2:]
    while len(privkey) < 64:
        privkey = '0' + privkey
    return privkey


def getnewpubkey(key, compress):

    key = binascii.unhexlify(key)
    key = ecdsa.SigningKey.from_string(key,curve=ecdsa.SECP256k1).verifying_key
    key = binascii.hexlify(key.to_string()).decode()
    if compress == 0:
        return (key)
    x = key[:64]
    y = key[64:]

    #getaxis
    
    if int(y[63:], 16) % 2 == 0:
        axis = '02'
    else:
        axis = '03'
    x = axis + x                 #03 - odd - 02 - not odd
    return x

def getnewaddress(pubkey):

    round_one = hashlib.sha256(binascii.unhexlify(pubkey)).hexdigest()
    round_two = hashlib.new('ripemd160')
    round_two.update(binascii.unhexlify(round_one))
    hashed = "00" + round_two.hexdigest() #add network byte
    extended = hashed + checksum(hashed)[:8]
    address = base58.b58encode(binascii.unhexlify(extended))
    return address


def signmessage(message, privkey):
    
    if (len(privkey) > 32):
        privkey = binascii.unhexlify(privkey)
    signkey = ecdsa.SigningKey.from_string(privkey,curve=ecdsa.SECP256k1)
    verkey = ecdsa.SigningKey.from_string(privkey,curve=ecdsa.SECP256k1).verifying_key
    message = bytes(message, 'utf-8')
    sig = signkey.sign(message)
    return sig, verkey


def wiftopriv(wif):

    x = base58.b58decode(wif)
    x = binascii.hexlify(x)
    privkey = x[2:-10] # -newtwork -compflag -checksum
    return privkey

