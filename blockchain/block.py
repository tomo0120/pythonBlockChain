import hashlib as hb
import json
import pprint
from time import time

#Default difficulty
DIFFICULTY = 4
#Defualt Mining rate
MINE_RATE = 4000

class Block:

    def __init__(self, timestamp, lastHash, hashVal, data, nonce, difficulty):   
        """
        Initializes block object

        Args:
            timestamp (float): time of transaction 
            lastHash (str): hash value of previous block
            hashVal (str): hash value of block
            data (list): data inside block
            nonce (int): nonce value for mining
            difficulty (int): difficulty setting for mining 
        """
        self.timestamp = timestamp
        self.lastHash = lastHash
        self.hashVal = hashVal
        self.data = data
        self.nonce = nonce
        self.difficulty = difficulty

    def __str__(self):
        return f"""Timestamp: {self.timestamp} 
                lastHash: {self.lastHash} 
                hashVal: {self.hashVal} 
                data: {self.data} 
                nonce: {self.nonce} 
                difficulty: {self.difficulty}"""

    def to_dict(self):
        """
        Changes into dictionary format
        """
        d = {
            "timestamp" : self.timestamp,
            "lastHash" : self.lastHash,
            "hashVal" : self.hashVal,
            "data" : self.data,
            "nonce" : self.nonce,
            "difficulty" : self.difficulty
        }
        return d

    @staticmethod
    def genesis():
        """
        Creates the genesis block, first block, of blockchain
        
        Returns:
            Block: the genesis block
        """
        return Block("initial_timestamp", 
                    "genesis-(^_^)-block",
                    Block.hashSHA("initial_timestamp", "genesis-(^_^)-block", [],0, DIFFICULTY),
                    [],
                    0,
                    DIFFICULTY)

    @staticmethod
    def hashSHA(timestamp, lastHash, data, nonce, difficulty):
        """
        Creates a SHA-256 hash

        Args:
            timestamp (float): time of transaction 
            lastHash (str): hash value of previous block
            hashVal (str): hash value of block
            data (list): data inside block
            nonce (int): nonce value for mining
            difficulty (int): difficulty setting for mining 
        Returns:
            Str: hashed value
        """
        hash_string = f"${timestamp}${lastHash}${data}${nonce}${difficulty}".encode("ascii")
        return hb.sha256(hash_string).hexdigest()

    @staticmethod
    def hashBlock(block):
        """
        Returns a hash value for a block
        Args:
            Block: A Block object
        Returns:
            Str: hash value for block
        """
        return Block.hashSHA(block.timestamp, block.lastHash, block.data, block.nonce, block.difficulty)

    @staticmethod
    def mineBlock(lastBlock, data):
        """
        Returns block that was mined

        Args:
            lastBlock (Block): last block of blockchain
            data (list): data to put into new block
        Return:
            Block: block that was mined
        """
        return Block.proof_of_work(lastBlock, data)

    @staticmethod
    def proof_of_work(lastBlock, data):
        """
        A simple proof of work algorithm

        Args:
            lastBlock (Block): last block
            data (list): 
        Return:
            Block: block verified by proof of work
        """
        lastHash = lastBlock.hashVal
        difficulty = lastBlock.difficulty
        timestamp = 0
        hashVal = ""
        nonce = 0
        #check if the hashVal has [0]*difficulty
        while(hashVal[0:difficulty] != "".join(["0"] * difficulty)):
            timestamp = time()
            nonce += 1
            #adjust the difficulty if it takes too much or too less time to verify
            if (lastBlock.timestamp + MINE_RATE < timestamp):
                difficulty -= 1
            else:
                difficulty += 1
            hashVal = Block.hashSHA(timestamp, lastHash, data, nonce, difficulty)
        
        return Block(timestamp, lastHash, hashVal, data, nonce, difficulty)