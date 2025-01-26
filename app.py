import streamlit as st
import os
import json
from cryptography.fernet import Fernet
import hashlib

# Key for encryption (Generated only once)
if "encryption_key" not in st.session_state:
    st.session_state.encryption_key = Fernet.generate_key()
fernet = Fernet(st.session_state.encryption_key)

# Local storage for wallets
WALLET_FILE = "wallets.json"

def load_wallets():
    """Load wallets from the local file."""
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as file:
            encrypted_data = file.read()
            if encrypted_data:
                decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
                return json.loads(decrypted_data)
    return {}

def save_wallets(wallets):
    """Save wallets to the local file."""
    encrypted_data = fernet.encrypt(json.dumps(wallets).encode()).decode()
    with open(WALLET_FILE, "w") as file:
        file.write(encrypted_data)

# Load wallets at startup
if "wallets" not in st.session_state:
    st.session_state.wallets = load_wallets()

# Hashing for secure password storage
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
            st.session_state.wallets[username] = {
                "password_hash": hash_password(password),
                "wallet_name": wallet_name,
                "public_key": public_key,
                "private_key": private_key,
            }
            save_wallets(st.session_state.wallets)
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
    st.write(f"**Private Key:** {active_wallet['private_key']}")

# Logout option
if "active_wallet" in st.session_state:
    if st.sidebar.button("Logout"):
        del st.session_state.active_wallet
        st.sidebar.success("Logged out successfully.")
