from security import RSAKeyManager, HybridEncryption

class Transaction:
    def __init__(self, sender, recipient, amount, encrypted_data=None, encrypted_key=None, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.encrypted_data = encrypted_data
        self.encrypted_key = encrypted_key
        self.signature = signature

    # Secure the transaction using hybrid encryption
    def secure_transaction(self, rsa_public_key):
        transaction_data = f"{self.sender}{self.recipient}{self.amount}".encode()
        self.encrypted_data, self.encrypted_key = HybridEncryption.encrypt_transaction(
            transaction_data, rsa_public_key
        )

    # Reveal the transaction by decrypting it
    def reveal_transaction(self, rsa_private_key):
        decrypted_data = HybridEncryption.decrypt_transaction(
            self.encrypted_data, self.encrypted_key, rsa_private_key
        )
        return decrypted_data.decode()

    # Check the validity of the transaction
    def is_valid(self):
        if self.sender == "System":  # Mining rewards
            return True
        if not self.signature:
            return False
        return RSAKeyManager.verify_signature(self.sender, self.signature, self.hash_transaction())

    # Compute the hash of the transaction
    def hash_transaction(self):
        return f"{self.sender}{self.recipient}{self.amount}".encode()


class Wallet:
    def __init__(self):
        # Generate RSA key pairs for the wallet
        self.private_key, self.public_key = RSAKeyManager.generate_keys()

    # Sign a transaction with the private key
    def sign_transaction(self, transaction):
        transaction.signature = RSAKeyManager.sign_data(self.private_key, transaction.hash_transaction())

    # Secure a transaction using the wallet's public key
    def secure_transaction(self, transaction):
        transaction.secure_transaction(self.public_key)
