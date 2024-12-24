from blockchain import Blockchain
from transaction import Transaction, Wallet

def main():
    # Initialize blockchain
    blockchain = Blockchain()

    # Create wallets
    wallet1 = Wallet()
    wallet2 = Wallet()

    # Create and sign transactions
    transaction1 = Transaction(wallet1.public_key, wallet2.public_key, 10)
    wallet1.sign_transaction(transaction1)
    blockchain.add_transaction(transaction1)

    # Mine transactions
    blockchain.mine_pending_transactions(wallet1.public_key)

    # Display blockchain
    for block in blockchain.chain:
        print(f"Block {block.index}, Hash: {block.hash}, Prev Hash: {block.previous_hash}")

    # Verify chain integrity
    print("Blockchain valid:", blockchain.is_chain_valid())

if __name__ == "__main__":
    main()
