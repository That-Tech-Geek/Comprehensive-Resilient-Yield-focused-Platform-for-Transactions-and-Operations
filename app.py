import streamlit as st
import pandas as pd
import hashlib
import time
from datetime import datetime

# Blockchain Implementation
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash="0")  # Genesis block

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transactions": self.pending_transactions,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount):
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
        }
        self.pending_transactions.append(transaction)
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        encoded_block = str(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] == "0000":  # Difficulty level
                check_proof = True
            else:
                new_proof += 1
        return new_proof

# Initialize Blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Streamlit App
st.title("Decentralized Financial Platform")
st.subheader("Enhanced Security and Accessibility")

# Wallet Generation
st.sidebar.header("Wallet Management")
if "wallets" not in st.session_state:
    st.session_state.wallets = {}

wallet_name = st.sidebar.text_input("Wallet Name")
if st.sidebar.button("Create Wallet"):
    if wallet_name:
        public_key = hashlib.sha256(f"{wallet_name}public".encode()).hexdigest()
        private_key = hashlib.sha256(f"{wallet_name}private".encode()).hexdigest()
        st.session_state.wallets[wallet_name] = {
            "public_key": public_key,
            "private_key": private_key,
        }
        st.sidebar.success(f"Wallet Created!\nPublic Key: {public_key}")
    else:
        st.sidebar.error("Please enter a wallet name.")

# Wallets Overview
if st.sidebar.checkbox("Show Wallets"):
    st.sidebar.write(pd.DataFrame(st.session_state.wallets).T)

# Add Transactions
st.header("Simulate Transactions")
sender = st.text_input("Sender Public Key")
receiver = st.text_input("Receiver Public Key")
amount = st.number_input("Transaction Amount", min_value=0.01, step=0.01)

if st.button("Add Transaction"):
    if sender and receiver and amount > 0:
        st.session_state.blockchain.add_transaction(sender, receiver, amount)
        st.success("Transaction added to the pool!")
    else:
        st.error("All fields are required.")

# Mining New Blocks
st.header("Mine a New Block")
if st.button("Mine Block"):
    blockchain = st.session_state.blockchain
    previous_block = blockchain.last_block
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    st.success(f"Block Mined Successfully! Block Index: {block['index']}")

# Display Blockchain
st.header("Blockchain Ledger")
blockchain_data = []
for block in st.session_state.blockchain.chain:
    blockchain_data.append(
        {
            "Index": block["index"],
            "Timestamp": block["timestamp"],
            "Transactions": block["transactions"],
            "Proof": block["proof"],
            "Previous Hash": block["previous_hash"],
        }
    )
st.write(pd.DataFrame(blockchain_data))

# Performance Metrics
st.header("Transaction Speed Test")
if st.button("Run Speed Test"):
    blockchain = st.session_state.blockchain
    start_time = time.time()
    for i in range(50):  # Simulating 50 transactions and blocks
        blockchain.add_transaction(f"User{i}", f"User{i+1}", 100.0)
        previous_block = blockchain.last_block
        previous_proof = previous_block["proof"]
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        blockchain.create_block(proof, previous_hash)
    end_time = time.time()
    st.success(f"Processed 50 transactions in {end_time - start_time:.2f} seconds!")
