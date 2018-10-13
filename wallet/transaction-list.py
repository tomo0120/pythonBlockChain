from transaction import Transaction
from functools import reduce

class TransactionList:

    def __init__(self):
        """
        Initializes the transaction list
        """
        self.transactions = []

    def updateOrAddTransaction(self, transaction):
        #find the transaction in transactions where we want to update of add transaction
        transactionWithId = None
        index = 0
        for i in self.transactions:
            index += 1
            if i.id == transaction.id:
                transactionWithId = i
                break
        #if the transaction is a new transaction
        if(transactionWithId == None):
            self.transactions.append(transaction)
        #if the transaction exists and want to update it
        else:
            self.transactions[index] = transaction
        
    def existingTransaction(self, address):
        """
        returns the transaction if address of transaction corresponds to address
        """
        for i in self.transactions:
            if i.input["address"] == address:
                return i
        return None

    def validTransactions(self):
        """
        verifies if the transactions are valid
        """
        validTransactions = []
        for transaction in self.transactions:

            #if the transaction is not verifed
            if(not Transaction.verifyTransaction(self, transaction)):
                print("Illicit signature: ${transaction.input.address}")
                continue

            outputTotal = 0
            outputList =[]
            for i in transaction.outputs:
                outputList.append(i["amount"])
            outputTotal = reduce(lambda total, output: total + output, outputList)
            
            #if the input amount does not equal the total output then transaction is illicit
            if(transaction.input["amount"] != outputTotal):
                print("Illicit transaction conducted: ${transaction.input.address}")
                continue
            
            validTransactions.append(transaction)
        
        return validTransactions


    def clear(self):
        """
        clear all transactions 
        """
        self.transactions = []