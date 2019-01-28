#!/usr/bin/env python3

from flask import Flask, request, jsonify
from blockchain import Blockchain
from uuid import uuid4
import requests, json

app = Flask(__name__)
chain = []
node_address = uuid4().hex
genesis_recipient = '0'
bl = Blockchain()
#chain sync

try:
    f = open('blockchain.db', 'r')
    s = f.read()
    bl = json.loads(s)
    for block in bl:
        chain.append(block)
    f.close()

except IOError:
    print("Empty 'blockchain.db'.Genesis block will be created")
    block = bl.genesis_block(genesis_recipient)
    dic = {'timestamp': block.timestamp,
            'nonce': block.nonce,
            'previous_hash': block.previous_hash,
            'transactions': block.transactions,
            'merkle_root': block.merkle_root,
            'hash': block.hash}
    f = open('blockchain.db', 'w')
    chain.append(dic)
    f.write(json.dumps(chain))
    f.close()
    print("Genesis block created")


@app.route("/")
def hello():
    return "Hello World!"

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route("/transaction/new", methods=['POST'])
def newtrans():
    bl = Blockchain()
    data = request.get_json()
    serialize = data['submit_tx']
    bl.submit_tx(serialize)
    return "Transaction is submited to pending pool"

@app.route("/transaction/pendings")
def getppool():
    f = open('mempool', 'r')
    pool = f.read()
    f.close()
    pool = pool.split('\n')
    return jsonify(pool)

@app.route("/mine", methods=['POST'])
def getnewblock():
    block = request.get_json()
    dic = {'timestamp': block['timestamp'],
            'nonce': block['nonce'],
            'previous_hash': block['previous_hash'],
            'transactions': block['transactions'],
            'merkle_root': block['merkle_root'],
            'hash': block['hash']}
    f = open('blockchain.db', 'w')
    chain.append(dic)
    f.write(json.dumps(chain))
    f.close()
    return "Yea"


@app.route("/chain")
def full_chain():
    f = open('blockchain.db', 'r')
    chain = f.read()
    f.close()
    f = json.dumps(chain)
    return (f)



@app.route("/chain/lenght", methods=['GET'])
def chain_lenght():
    x = 0
    f = open('blockchain.db', 'r')
    chain = f.read()
    f.close()
    lines = json.loads(chain)
    for item in lines:
        x += 1
    string = "Chain len is: " + str(x) + " transactions."

    return string

#@app.route("/nodes")

if __name__ == '__main__':
    app.run(debug=True)
