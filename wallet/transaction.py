from index import Wallet

import hashlib
import json
from time import time
from uuid import uuid4
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS

#Default Mining reward
MINING_REWARD = 5

class Transaction:

    def __init__(self):
        """
        Initializer for transaction object

        Args:
            trans_id (str): id of transaction 
            input (dictionary): includes timestamp, amount, address, signature of sender
            outputs (list): includes all transaction - sender and receipient
        """
        self.trans_id = uuid4()
        self.input = {
            "timestamp": None,
            "amount": None,
            "address": None,
            "signature": None,
        }
        self.outputs = []

    @staticmethod
    def outputs_to_dict(transaction_outputs):
        d = [
            {
                "amount": transaction_outputs[0]["amount"],
                "sender_address": transaction_outputs[0]["sender_address"]
            },{
                "amount": transaction_outputs[1]["amount"],
                "recipient_address": transaction_outputs[1]["recipient_address"]
            }
        ]
        return d
    
    def update(self, senderWallet, recipient, amount):
        """
        Update the transaction
        """
        #find the output that corresponds to the transaction that we want to update
        for output in self.outputs:
            if output.address == senderWallet.publicKey:
                senderOutput = output
        #do nothing if sender does not have enough amount to send
        if(amount > senderOutput.amount):
            print("Not enough funds to send money")
            return
        #update the transaction
        senderOutput.amount = senderOutput.amount - amount
        self.outputs.append({
            "amount": amount,
            "recipient_address": recipient
        })
        Transaction.signTransaction(self, senderWallet)

        return self

    @staticmethod
    def signTransaction(transaction, senderWallet):
        """
        Sender signs transaction
        """

        #message = hased(transaction.outputs)
        message = sha256(transaction.outputs)

        transaction.input["timestamp"] = time()
        transaction.input["amount"] = senderWallet.balance
        transaction.input["address"] = senderWallet.publicKey
        transaction.input["signature"] = senderWallet.sign(message)

    @staticmethod
    def newTransaction(senderWallet, recipient, amount):
        """
        New transaction when sender sends money to recipient
        """
        #if there is not enough amount left return
        if (amount > senderWallet.balance):
            print("Not enough funds")
            return
        #create a new transaction
        transaction = Transaction()
        #organize infomation into outputs format
        outputs = [
            {
                "amount": senderWallet.balance - amount,
                "sender_address": senderWallet.publicKey 
            },
            {
                "amount": amount,
                "recipient_address": recipient
            }
        ]
        #add the outputs list to transaction.outputs
        for i in range(len(outputs)):
            transaction.outputs.append(outputs[i])
        #sign the transaction
        Transaction.signTransaction(transaction, senderWallet)
        return transaction

    @staticmethod
    def rewardTransaction(minerWallet, blockchainWallet):
        """
        Reward the miner if mined successfully
        """
        transaction = Transaction()
        output = [{
            "amount": MINING_REWARD, 
            "recipient_address": minerWallet.publicKey
        }]
        transaction.outputs.append(output)
        Transaction.signTransaction(transaction, blockchainWallet)
        return transaction

    @staticmethod
    def verifyTransaction(self, transaction):
        """
        Verifies the transaction
        """
        return Wallet.verifySignature(self,
            transaction.input.address, 
            transaction.input.signature, 
            sha256(transaction.outputs)
        )

#organize the sha256
def sha256(message):
    """
    Hashes the message
    """
    h = SHA256.new()
    message = json.dumps(message)
    h.update(message.encode())
    return h
