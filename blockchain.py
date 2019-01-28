#!/usr/bin/env python3

from block import Block
from transaction import CoinbaseTransaction as CT
from pending_pool import pendingtopool
from tx_validator import tx_validator
from serializer import Serializer
from block_validator import chain_verify
from wallet import signmessage,wiftopriv,getnewaddress, getnewpubkey
import json

class Blockchain(object):

    def __init__(self, compl = 2):
        self.complexity = compl
        self.lasthash = '0'

    def mine(self, block):
        bread = bytes(b'0' * self.complexity).decode()
        while block.blockhash()[:self.complexity] != bread:
            block.nonce += 1
        if block.blockhash()[:self.complexity] == bread:
            print(block.blockhash())
        else:
            print ("Mining failure.Cannot compute hash")
            return False
        block.hash = block.blockhash()
        self.lasthash = block.hash
        return block.nonce

    def resolve_conflicts(self):
        pass

    def is_valid_chain(self):
        chain = []
        f = open('blockchain.db', 'r')
        jread = json.loads(f.read())
        f.close()
        for block in jread:
            chain.append(block)
        if chain_verify(chain) == True:
            print("Valid chain")
            return True
        else:
            print("Invalid chain")
            return False


    def add_node(self, url):
        #parsed_url = urlparse(url)
        #self.nodes.add(parsed_url.netloc)
        pass

    def genesis_block(self, genesis_recipient = '0'):

        f = open('minerkey', 'r')
        minerkey = f.read()
        f.close()
        if (genesis_recipient == '0'):
            genesis_recipient = (getnewaddress(getnewpubkey(wiftopriv\
                    (minerkey), 1))).decode()
        trans = CT(None)
        trans.recipient = genesis_recipient
        trans.amount = '65000'
        hashed = trans.transactionhash()
        sig, verkey = signmessage(hashed, wiftopriv(minerkey))
        if (tx_validator(trans, verkey, sig, hashed,\
                getnewpubkey(wiftopriv(minerkey), 0)) == False):
            print("Invalid genesis transaction")
            return False
        serialize = Serializer(trans.sender, trans.recipient, trans.amount,\
                getnewpubkey(wiftopriv(minerkey), 0), sig)
        ser = list()
        ser.append(serialize.serialize + '\n')
        genesis_block = Block('0', ser)
        self.mine(genesis_block)
        return genesis_block

    def submit_tx(self, serialize):
        pendingtopool(serialize)
