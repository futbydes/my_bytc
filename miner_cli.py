#!/usr/bin/env python3

from transaction import CoinbaseTransaction, Transaction
from wallet import wiftopriv, getnewpubkey, getnewaddress, signmessage
from tx_validator import tx_validator
from serializer import Serializer
from block import Block
from blockchain import Blockchain as chain
import cmd,requests, json,collections


class MinerCli(cmd.Cmd):

    intro = 'Pitcoin miners inteface starting'
    prompt = '(mpitcoin) '
    minerkey = None
    lasthash = 0
    bl = chain()
    bs = []

    f = open('blockchain.db', 'r')
    lines = f.read()
    f.close()
    lines = json.loads(lines)
    for item in lines:
        lasthash = item['hash']

    
    def do_add_node(self, arg):
        pass
    
    def do_mine(self, arg):
        "Start mining process."

        while (1):
            
            f = open('mempool', 'r') #get trans from file
            nf = f.readlines()
            if (len(nf) < 3):
                print("Stopped.Required at least 3 valid transaction")
                return False
            trans = nf[-3:]
            f.close()

            f = open('minerkey', 'r') #get miners address
            minerkey = f.read()
            f.close()

            minerkey = wiftopriv(minerkey)
            miner = CoinbaseTransaction()
            pubkey = getnewpubkey(minerkey, 1)
            miner.recipient = (getnewaddress(pubkey)).decode()

            #form transaction
            hashed = miner.transactionhash()
            sig, verkey = signmessage(hashed, minerkey)
            if (tx_validator(miner, verkey, sig, hashed, pubkey)\
                    == False):
                print("Invalid transaction")
                return False
            serialize = Serializer(miner.sender, miner.recipient,\
                miner.amount, getnewpubkey(minerkey, 0), sig)
            trans.append(serialize.serialize + '\n')

            newb = Block(self.lasthash, trans)
            if newb.validatesall() == True and self.bl.mine(newb) != False:
                #append to chain
                block = {'timestamp': newb.timestamp,
                        'nonce': newb.nonce,
                        'previous_hash': self.lasthash,
                        'transactions': newb.transactions,
                        'merkle_root': newb.merkle_root,
                        'hash': newb.blockhash()}
                url_tn = "http://127.0.0.1:5000/mine"
                try:
                    r = requests.post(url = url_tn,\
                            json=block)
                    if r.ok:
                        print("Block is added to blockchain!")
                except:
                    print("Error.Check if the server is running")
                    return False
                f = open('mempool', 'w') #delete last trans from file
                f.write(''.join(nf[:-3]))
                f.close()
                self.lasthash = newb.blockhash()
            else:
                return False

        
        
    def do_consensus(self, arg):
        pass
    
    def do_exit(self, arg):
        'Stop working and exit'
        print('Thank you for using pitcoin')
        return True
    
    def do_EOF(self, line):
        return True
    

if __name__ == "__main__":
    MinerCli().cmdloop()
