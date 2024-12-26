from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class RSAKeyManager:
    @staticmethod
    def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def sign_data(private_key, data):
        return private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

    @staticmethod
    def verify_signature(public_key, signature, data):
        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False

    @staticmethod
    def serialize_public_key(public_key):
        return public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo,
        )

    @staticmethod
    def serialize_private_key(private_key):
        return private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),
        )

class HybridEncryption:
    @staticmethod
    def generate_aes_key():
        return os.urandom(32)  # AES-256 key

    @staticmethod
    def encrypt_with_aes(data, aes_key):
        iv = os.urandom(16)  # Initialization vector
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        return iv + encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt_with_aes(ciphertext, aes_key):
        iv = ciphertext[:16]
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext[16:]) + decryptor.finalize()

    @staticmethod
    def encrypt_transaction(transaction_data, rsa_public_key):
        aes_key = HybridEncryption.generate_aes_key()
        encrypted_data = HybridEncryption.encrypt_with_aes(transaction_data, aes_key)
        encrypted_key = rsa_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return encrypted_data, encrypted_key

    @staticmethod
    def decrypt_transaction(encrypted_data, encrypted_key, rsa_private_key):
        aes_key = rsa_private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return HybridEncryption.decrypt_with_aes(encrypted_data, aes_key)
