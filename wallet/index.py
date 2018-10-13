from transaction import Transaction
import blockchain

import functools
import binascii
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS


#defaiult balance
INITIAL_BALANCE = 5000

class Wallet(object):

    def __init__(self):
        randomGen = Crypto.Random.new().read
        privateKey = RSA.generate(1024, randomGen)
        
        self.balance = INITIAL_BALANCE
        self.privateKey = privateKey.exportKey('PEM').decode()
        self.publicKey = privateKey.publickey().exportKey('PEM').decode()
        self.signer = PKCS1_PSS.new(privateKey)

    def __str__(self):
        return f"""Balance: {self.balance} 
                publicKey: {self.publicKey} 
                """

    def sign(self, dataHash):
        """
        Sign a message in form of dataHash with this wallet
        """
        #dataHash is SHA256 object
        return self.signer.sign(dataHash)

    def verifySignature(self, wallet_address, signature, dataHash):
        """
        Checks that the signature corresponds to dataHash
        signed by the wallet at wallet_address
        """
        publicKey = RSA.importKey(wallet_address.encode())
        verifier = PKCS1_PSS.new(publicKey)
        return verifier.verify(dataHash, signature)

    def createTransaction(self, recipient, amount, blockchain, transactionList):
        """
        creates a transaction
        """
        self.balance = self.calculateBalance(blockchain)
        if (amount > self.balance):
            print("Not enough amount in balance")
            return

        transaction = transactionList.existingTransaction(self.publicKey)

        if (transaction == None):
            transaction = Transaction.newTransaction(self, recipient, amount)
            transactionList.updateOrAddTransaction(transaction)
        else:
            transaction.update(self, recipient, amount)

        return transaction


    def calculateBalance(self, blockchain):
        """
        calculates the balance of wallet based on blockchain
        """
        balance = self.balance
        transactions = []
        #find data for all blocks in blockchain
        for block in blockchain.chain:
            for i in block.data:
                transactions.append(i)
        #Add all transactions related to this wallet
        walletInputTrans = []
        for i in transactions:
            if(i.address == self.publicKey):
                walletInputTrans.append(i)

        startTime = 0
        #Start calculating balance
        if(len(walletInputTrans) > 0):
            recentInputTrans = functools.reduce(lambda prev,current : prev if prev.input.timestamp > current.input.timestamp else current, 
                                                walletInputTrans)
            for output in recentInputTrans.outputs:
                if (output.address == self.publicKey):
                    balance = output.amount
            
            startTime = recentInputTrans.input.timestamp

            for t in transactions:
                if(t.input.timestamp > startTime):
                    for i in t.outputs:
                        if i.address == self.publicKey:
                            balance += i.amount
        
        return balance