from blockchain import Blockchain
from transaction import Transaction, Wallet

def test_replay_attack():
    # Initialize the blockchain
    blockchain = Blockchain()

    # Create wallets
    wallet1 = Wallet()
    wallet2 = Wallet()

    # Create and sign a valid transaction
    transaction1 = Transaction(wallet1.public_key, wallet2.public_key, 10)
    wallet1.sign_transaction(transaction1)

    # Add the transaction to the blockchain
    print("Adding valid transaction...")
    success = blockchain.add_transaction(transaction1)
    if success:
        print("Transaction added successfully.")
    else:
        print("Failed to add transaction.")

    # Attempt to replay the same transaction
    print("\nAttempting replay attack with the same transaction...")
    success = blockchain.add_transaction(transaction1)  # Same transaction
    if success:
        print("Replay attack successful! (This should NOT happen.)")
    else:
        print("Replay attack detected and prevented!")

    # Mine pending transactions
    print("\nMining pending transactions...")
    blockchain.mine_pending_transactions(wallet1.public_key)

    # Display blockchain state
    print("\nCurrent Blockchain State:")
    for block in blockchain.chain:
        print(f"Block {block.index}, Transactions: {[t.amount for t in block.transactions]}, Hash: {block.hash}")

if __name__ == "__main__":
    test_replay_attack()
