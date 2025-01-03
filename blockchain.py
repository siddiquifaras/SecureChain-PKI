import hashlib
import time
from transaction import Transaction

# Class representing a single block in the blockchain
class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0  # Counter used for mining (proof-of-work)
        self.hash = self.calculate_hash()  # Compute the hash for the block

    # Calculates the hash of the block based on its contents.
    # returns SHA-256 hash of the block.
    def calculate_hash(self):
        data = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}{self.nonce}"  # Combine block properties into a single string
        return hashlib.sha256(data.encode()).hexdigest()

    # Mines the block by solving the proof-of-work problem.
    # Adjusts the nonce until the hash meets the required difficulty.
    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:  # Keep incrementing the nonce until hash has required leading zeroes
            self.nonce += 1
            self.hash = self.calculate_hash()  # Recalculate hash after updating nonce


# Class representing the blockchain
class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]  # Start blockchain with the genesis block
        self.pending_transactions = []  # List of transactions waiting to be mined
        self.processed_transactions = set()  # Set to track processed transaction hashes
        self.difficulty = difficulty
        self.target_mining_time = 10  # Target mining time in seconds

    # Creates the first block in the blockchain (genesis block).
    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    # Adds a new transaction to the list of pending transactions.
    def add_transaction(self, transaction):
        # Check for replay attack using transaction hash
        if transaction.hash_transaction() in self.processed_transactions:
            print("Replay attack detected: Transaction already processed!")
            return False

        # Validate the transaction
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            self.processed_transactions.add(transaction.hash_transaction())  # Mark transaction as processed
            return True
        print("Invalid transaction!")
        return False

    # Mines a new block containing all pending transactions.
    # Rewards the miner by adding a transaction to the miner's wallet.
    def mine_pending_transactions(self, miner_wallet_address):
        block = Block(len(self.chain), self.chain[-1].hash, self.pending_transactions)  # Create a new block with pending transactions
        block.mine_block(self.difficulty)  # Perform mining
        self.chain.append(block)  # Add the mined block to the blockchain
        self.pending_transactions = [Transaction("System", miner_wallet_address, 1)]  # Reward the miner with a "System" transaction of 1 unit
        self.adjust_difficulty()  # Adjust mining difficulty

    # Validates the integrity of the blockchain.
    # Checks the hashes and links between blocks.
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    # Adjusts the mining difficulty dynamically based on the target mining time.
    def adjust_difficulty(self):
        if len(self.chain) > 1:
            mining_time = self.chain[-1].timestamp - self.chain[-2].timestamp
            if mining_time < self.target_mining_time:
                self.difficulty += 1
                print(f"Difficulty increased to {self.difficulty}")
            elif mining_time > self.target_mining_time:
                self.difficulty = max(1, self.difficulty - 1)  # Ensure difficulty does not go below 1
                print(f"Difficulty decreased to {self.difficulty}")
