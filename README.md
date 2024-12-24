# **Secure Blockchain System with Wallet Functionality**

This project is a Python implementation of a simple blockchain with wallet functionality. The blockchain supports secure transactions, mining, and basic wallet operations, while incorporating key security features from the CIA triad: **Confidentiality** (via RSA encryption) and **Integrity** (via cryptographic hashes).

---

## **Features**

### **Basic Blockchain**
- Creates a blockchain and adds blocks with cryptographic hashes.
- Maintains a chain integrity mechanism by linking blocks using the `previous_hash`.

### **Mining**
- Uses a proof-of-work (PoW) system with adjustable difficulty levels.

### **Wallets**
- RSA key pairs ensure secure wallet transactions.
- Wallets can send and receive funds.

### **Transaction Validation**
- Transactions are validated to ensure wallet balance sufficiency.

### **Blockchain Integrity Check**
- Ensures the chain remains unaltered using cryptographic validations.

### **CIA Security Features**
- **Confidentiality**: RSA encryption secures transactions.
- **Integrity**: Cryptographic hashes link and validate block data.

---

## **Prerequisites**

### **Install Anaconda**
1. Download and install Anaconda: [Download Link](https://www.anaconda.com/products/distribution).
2. Verify installation:
   ```bash
   conda --version
3. Create a virtual environment (recommended):
    ```bash
    conda create -n securechain python=3.10
    conda activate securechain

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
2. **Install dependencies from requirements.txt**
    ```bash
    pip install -r requirements.txt

## Usage

1. **Run the project**:
    ```bash
    python main.py


## Code Structure

- **`block.py`**: Contains the Block class for creating and mining blocks.
- **`blockchain.py`**: Manages the blockchain, transactions, and mining process.
- **`transaction.py`**: Implements the Transaction class for transferring funds between wallets.
- **`wallet.py`**: Defines wallet operations, including sending/receiving funds and managing RSA keys.
- **`security.py`**: Implements RSA encryption and decryption for secure transactions.
- **`main.py`**: Driver script to demonstrate blockchain functionality.