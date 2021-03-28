import sys
import os
import hashlib
import json
import base64
import time
from configparser import ConfigParser
from PoW import PoW


class Block:
    def __init__(self, prev_height, time, bits, nonce, transactions, prev_hash):
        self.height = prev_height + 1
        self.time = time
        self.bits = bits
        self.nonce = nonce
        # transactions is a list
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = ''

    # print block information

    def __str__(self):
        print(f"Block Information: ")
        print(f"---")
        print(f"height: {self.height}")
        print(f"time: {self.time}")
        print(f"hardness: {self.bits}")
        print(f"nonce: {self.nonce}")
        print(f"transactions: {self.transactions}")
        print(f"previous hash: {self.prev_hash}")
        print(f"hash: {self.hash}")
        print(f"---")
        return ''

    def set_hash(self):
        # read salt from config file
        Pow = PoW(self)
        self.nonce, self.hash = Pow.run()

    # serialize a block

    @staticmethod
    def serialize(block):
        prev_hash = base64.b64encode(block.prev_hash).decode()
        block_hash = base64.b64encode(block.hash).decode()
        d = {'height': block.height, 'bits': block.bits, 'time': block.time, 'nonce': block.nonce,
             'transactions': block.transactions, 'prev_hash': prev_hash, 'hash': block_hash}
        data = json.dumps(d)
        # print(data)
        return data

    # deserialize a block
    @staticmethod
    def deserialize(raw_data):
        data = json.loads(raw_data)
        height = data['height']
        time = data['time']
        bits = data['bits']
        nonce = data['nonce']
        transactions = data['transactions']
        prev_hash = base64.b64decode(data['prev_hash'].encode())
        block = Block(height - 1, time, bits, nonce, transactions, prev_hash)
        block.hash = base64.b64decode(data['hash'].encode())
        return block
