from block import Block
from time import time
import json

#Default difficulty
DIFFICULTY = 4
#Default Nonce
NONCE = 0

class Blockchain:

    def __init__(self):
        """
        Initialize a blockchain with genesis as first block
        """
        self.chain = [Block.genesis()]


    def addBlock(self, data):
        """
        add a block to the blockchain
        Args:
            data (list): data of block
        Returns:
            Block: the added block 
        """
        #get the hashVal of last block in blockchain
        lastHash = self.chain[len(self.chain) - 1].hashVal
        timestamp = time()
        hashVal = Block.hashSHA(timestamp, lastHash, data, NONCE, DIFFICULTY)
        adding_block = Block(timestamp, lastHash, hashVal, data, NONCE, DIFFICULTY)
        
        self.chain.append(adding_block)
        return adding_block

    @staticmethod
    def validChain(bc):
        """
        Checks if the blockchain is valid

        Args:
            bc (Blockchain): the blockchain that is being verified
        Returns:
            bool: True if chain is valid and false otherwise
        """
        #If the first block of chain is not equal to the genesis block, then chain is invalid
        if (json.dumps(Block.to_dict(bc.chain[0])) != json.dumps(Block.to_dict(Block.genesis()))):
            return False
        #check validity for all blocks in the blockchain
        for i in range(1,len(bc.chain)):
            curr_block = bc.chain[i]
            prev_block = bc.chain[i-1]
            #if lastHash of curr_block is not equal to the hash value of prev_block then chain is not valid
            #if the hash value of curr_block is not equal to the hash value produced from hashBlock then chain is not valid
            if((curr_block.lastHash != prev_block.hashVal) or (curr_block.hashVal != Block.hashBlock(curr_block))):
                return False
        return True

    def replaceChain(self, newbc):
        """
        Replaces the current blockchain with a new blockchain (newbc)

        Args:
            newbc (Blockchain): the new blockchain that will replace the old one
        """
        if (Blockchain.validChain(newbc) == False):
            print("New Blockchain is invalid")
            return
        elif (len(newbc.chain) < len(self.chain)):
            print("Not enough blocks on new Blockchain")
            return
        
        print("Updating blockchain to newest version")
        self.chain = newbc
        
