#!/usr/bin/env python3

import sys,wallet,cmd, binascii
from transaction import Transaction, CoinbaseTransaction
from serializer import Serializer,Deserializer
from tx_validator import tx_validator
from pending_pool import pendingtopool
from merkle import merkle_root
from block import Block
import requests

class WalletCli(cmd.Cmd):

    intro = 'Welcome to pitcoin.vludan command line.Type help or ? to list commands.'
    privkey = None
    pubkey = None
    prompt = '(wpitcoin) '
    serialize = None

    def do_import(self, arg):
        "Import a private key type WIF from a file.Takes one argument as path.For example: import ~/pitcoin/key"
        try:
            f = open(arg, 'rb')
        except FileNotFoundError:
            print("File not found.Use help for more information.")
            return False
        f = f.read()
        print(f.decode())
        self.privkey = wallet.wiftopriv(f)
        self.pubkey = wallet.getnewpubkey(self.privkey, 1)
        address = wallet.getnewaddress(self.pubkey)
        f = open('address', 'wb')                   #save address
        f.write(address)
        f.close()

    def do_new(self, arg):
        "Generate private and public key.Dont use any optional arguments"

        if arg:
            print("Invalid action.Use help for information")
            return False
        self.privkey = wallet.getnewprivkey()
        print((wallet.privtowif(self.privkey)).decode())
        self.pubkey = wallet.getnewpubkey(self.privkey, 1)
        address = wallet.getnewaddress(self.pubkey)
        f = open('address', 'wb')                   #save address
        f.write(address)
        f.close()

        #clean send funtion!!!11

    def do_send(self, arg):
        'Send to <% Recipient Address%> some <% Amount%>, takes 2 arguments.Use address file and pre generated (or import) private key.Amount precise is from 1 to 50000'

        try:
            f = open('address', 'r')                    #get address
        except FileNotFoundError:
            print("Address file cant be found.")
            return False
        sender = f.read()
        f.close()
        args = arg.split(' ')
        if len(args) < 2 or self.privkey == None or int(args[1]) < 1\
                or int(args[1]) > 50000:
            print("Invalid action.Use help for information")
            return False
        trans = Transaction(sender, args[0], args[1])
        hashed = trans.transactionhash()                #hash transaction
        sig, verkey = wallet.signmessage(hashed, self.privkey)
        if (tx_validator(trans, verkey, sig, hashed, self.pubkey)\
                == False):
            print("Invalid transaction")
            return False
        self.serialize = Serializer(trans.sender, trans.recipient,\
                trans.amount, wallet.getnewpubkey(self.privkey, 0), sig)
        print(self.serialize.serialize)

    def do_broadcast(self, arg):
        "Add last transaction to pool"
        url_tn = "http://127.0.0.1:5000/transaction/new"
        try:
            r = requests.post(url = url_tn,\
                    json={'submit_tx':self.serialize.serialize})
            if r.ok:
                print("Transaction added to pool!")
        except:
            print("Error.Check if the server is running")

    def do_balance(self, arg):
        "Balance of the address submited as parameter"
        pass

    def do_syscleanmpool(self, arg):
        "Clean mempool file"
        f = open('mempool', 'w')
        f.close()

    def do_exit(self, arg):
        'Stop working and exit'
        print('Thank you for using pitcoin')
        self.close()
        return True

    def do_EOF(self, line):
        return True 
    
    def close(self):
        if self.privkey:
            self.privkey = None



#app.run(debug=True, port=8000)

if __name__ == "__main__":
    WalletCli().cmdloop()
