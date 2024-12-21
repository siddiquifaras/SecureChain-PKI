from security import RSAKeyManager

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def is_valid(self):
        if self.sender == "System":  # Mining rewards
            return True
        if not self.signature:
            return False
        return RSAKeyManager.verify_signature(self.sender, self.signature, self.hash_transaction())

    def hash_transaction(self):
        return f"{self.sender}{self.recipient}{self.amount}".encode()

class Wallet:
    def __init__(self):
        self.private_key, self.public_key = RSAKeyManager.generate_keys()

    def sign_transaction(self, transaction):
        transaction.signature = RSAKeyManager.sign_data(self.private_key, transaction.hash_transaction())
