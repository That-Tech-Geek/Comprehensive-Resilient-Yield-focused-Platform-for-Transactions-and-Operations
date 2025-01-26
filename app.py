import streamlit as st
import os
import sqlite3
from cryptography.fernet import Fernet
import hashlib
import random

# Constants
DB_FILE = "wallets.db"
MINING_REWARD = 10  # Tokens awarded for mining a block

# Ensure encryption key persists
if "encryption_key" not in st.session_state:
    if os.path.exists("encryption_key.key"):
        with open("encryption_key.key", "rb") as key_file:
            st.session_state.encryption_key = key_file.read()
    else:
        st.session_state.encryption_key = Fernet.generate_key()
        with open("encryption_key.key", "wb") as key_file:
            key_file.write(st.session_state.encryption_key)

# Create a Fernet instance for encryption/decryption
fernet = Fernet(st.session_state.encryption_key)

# Function to initialize the SQLite database and create the necessary table
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallets (
                        username TEXT PRIMARY KEY,
                        password_hash TEXT NOT NULL,
                        wallet_name TEXT NOT NULL,
                        public_key TEXT NOT NULL,
                        private_key TEXT NOT NULL,
                        balance INTEGER NOT NULL,
                        transactions TEXT
                    )''')
    conn.commit()
    conn.close()

# Function to load wallets from the SQLite database
def load_wallets():
    wallets = {}
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wallets")
    rows = cursor.fetchall()
    for row in rows:
        wallets[row[0]] = {
            "password_hash": row[1],
            "wallet_name": row[2],
            "public_key": row[3],
            "private_key": row[4],
            "balance": row[5],
            "transactions": json.loads(row[6]) if row[6] else []
        }
    conn.close()
    return wallets

# Function to save wallets to the SQLite database
def save_wallet(wallet_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO wallets (username, password_hash, wallet_name, public_key, private_key, balance, transactions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                        wallet_data["username"],
                        wallet_data["password_hash"],
                        wallet_data["wallet_name"],
                        wallet_data["public_key"],
                        wallet_data["private_key"],
                        wallet_data["balance"],
                        json.dumps(wallet_data["transactions"])
                    ))
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Load wallets at startup
if "wallets" not in st.session_state:
    st.session_state.wallets = load_wallets()

# Hashing function for password storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# App Interface
st.title("CRYPTO Platform")
st.sidebar.header("Wallet Management")

# Tab for wallet creation
st.sidebar.subheader("Create a New Wallet")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
wallet_name = st.sidebar.text_input("Wallet Name")

if st.sidebar.button("Create Wallet"):
    if username and password and wallet_name:
        if username in st.session_state.wallets:
            st.sidebar.error("Username already exists. Choose a different username.")
        else:
            public_key = hashlib.sha256(f"{wallet_name}public".encode()).hexdigest()
            private_key = hashlib.sha256(f"{wallet_name}private".encode()).hexdigest()
            wallet_data = {
                "username": username,
                "password_hash": hash_password(password),
                "wallet_name": wallet_name,
                "public_key": public_key,
                "private_key": private_key,
                "balance": 0,  # Start with zero balance
                "transactions": [],  # Store transaction history
            }
            st.session_state.wallets[username] = wallet_data
            save_wallet(wallet_data)
            st.sidebar.success(f"Wallet '{wallet_name}' created successfully!")
    else:
        st.sidebar.error("All fields are required.")

# Tab for wallet login and access
st.sidebar.subheader("Access Your Wallet")
login_username = st.sidebar.text_input("Login Username", key="login_user")
login_password = st.sidebar.text_input("Login Password", type="password", key="login_pass")

if st.sidebar.button("Login"):
    wallets = st.session_state.wallets
    if login_username in wallets:
        if wallets[login_username]["password_hash"] == hash_password(login_password):
            st.sidebar.success(f"Welcome back, {login_username}!")
            st.session_state.active_wallet = wallets[login_username]
            st.session_state.username = login_username
        else:
            st.sidebar.error("Incorrect password.")
    else:
        st.sidebar.error("Username not found.")

# Display wallet details after login
if "active_wallet" in st.session_state:
    st.subheader("Your Wallet Details")
    active_wallet = st.session_state.active_wallet
    st.write(f"**Wallet Name:** {active_wallet['wallet_name']}")
    st.write(f"**Public Key:** {active_wallet['public_key']}")
    st.write(f"**Balance:** {active_wallet['balance']} tokens")
    st.write("**Transaction History:**")
    if active_wallet["transactions"]:
        for tx in active_wallet["transactions"]:
            st.write(tx)
    else:
        st.write("No transactions yet.")

    # Transaction functionality
    st.subheader("Send Tokens")
    recipient_username = st.text_input("Recipient Username")
    amount = st.number_input("Amount to Send", min_value=1, step=1)
    if st.button("Send"):
        wallets = st.session_state.wallets
        if recipient_username in wallets:
            if active_wallet["balance"] >= amount:
                # Deduct from sender
                wallets[st.session_state.username]["balance"] -= amount
                wallets[st.session_state.username]["transactions"].append(
                    f"Sent {amount} tokens to {recipient_username}"
                )
                # Add to recipient
                wallets[recipient_username]["balance"] += amount
                wallets[recipient_username]["transactions"].append(
                    f"Received {amount} tokens from {st.session_state.username}"
                )
                save_wallet(wallets[st.session_state.username])
                save_wallet(wallets[recipient_username])
                st.session_state.wallets = wallets
                st.success(f"Sent {amount} tokens to {recipient_username}")
            else:
                st.error("Insufficient balance!")
        else:
            st.error("Recipient not found!")

    # Mining functionality
    st.subheader("Mine Tokens")
    if st.button("Mine"):
        mining_reward = random.randint(1, MINING_REWARD)  # Randomized reward
        wallets = st.session_state.wallets
        wallets[st.session_state.username]["balance"] += mining_reward
        wallets[st.session_state.username]["transactions"].append(
            f"Mined {mining_reward} tokens"
        )
        save_wallet(wallets[st.session_state.username])
        st.session_state.wallets = wallets
        st.success(f"You mined {mining_reward} tokens!")

# Logout option
if "active_wallet" in st.session_state:
    if st.sidebar.button("Logout"):
        del st.session_state.active_wallet
        st.sidebar.success("Logged out successfully.")
