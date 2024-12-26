from blockchain import Blockchain
from transaction import Transaction, Wallet

def main():
    # Initialize the blockchain
    blockchain = Blockchain()

    # Create wallets
    wallet1 = Wallet()
    wallet2 = Wallet()

    # Create a transaction, sign it, and secure it with hybrid encryption
    transaction1 = Transaction(wallet1.public_key, wallet2.public_key, 10)
    wallet1.sign_transaction(transaction1)  # Sign the transaction
    transaction1.secure_transaction(wallet2.public_key)  # Secure the transaction using hybrid encryption

    # Add the transaction to the blockchain
    success = blockchain.add_transaction(transaction1)
    if success:
        print("Transaction added successfully.")
    else:
        print("Failed to add transaction.")

    # Reveal and print transaction details for demonstration
    print("\nDecrypted Transaction Data:")
    decrypted_data = transaction1.reveal_transaction(wallet2.private_key)
    print(decrypted_data)

    # Mine transactions
    blockchain.mine_pending_transactions(wallet1.public_key)

    # Display the blockchain
    print("\nBlockchain State:")
    for block in blockchain.chain:
        print(f"Block {block.index}, Hash: {block.hash}, Prev Hash: {block.previous_hash}")

    # Verify the integrity of the blockchain
    print("\nBlockchain valid:", blockchain.is_chain_valid())

if __name__ == "__main__":
    main()
