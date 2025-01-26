# Crypto Platform

## Overview
The **Crypto Platform** is a Streamlit-based decentralized application (DApp) for managing crypto wallets. It allows users to create wallets, manage tokens, mine tokens, and perform transactions in a secure environment. The app uses encryption to protect wallet data and provides a user-friendly interface for wallet management.

---

## Features
1. **Create Wallets**: 
   - Users can register with a username, password, and wallet name.
   - Each wallet is assigned unique public and private keys.
   - Wallet data is securely stored using AES encryption.

2. **Login & Access Wallets**:
   - Secure login using username and password.
   - View wallet details such as balance, public key, and transaction history.

3. **Send Tokens**:
   - Transfer tokens to another user by entering the recipient's username and amount.
   - Transactions are securely recorded for both the sender and recipient.

4. **Mine Tokens**:
   - Users can mine tokens to earn rewards.
   - Mining rewards are randomized up to a configurable maximum.

5. **Transaction History**:
   - Each wallet maintains a detailed history of sent, received, and mined tokens.

6. **Secure Data Storage**:
   - Wallet data is encrypted using the `cryptography` library.
   - Passwords are hashed with SHA-256 for added security.

7. **Logout**:
   - Users can securely log out to prevent unauthorized access.

---

## Installation

### Prerequisites
- Python 3.8 or later
- Required libraries:
  - `streamlit`
  - `cryptography`

### Steps
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Usage

### 1. **Create a Wallet**
   - Open the app and navigate to the **Create a New Wallet** section in the sidebar.
   - Enter a unique username, password, and wallet name.
   - Click **Create Wallet**. Your wallet will be created with an initial balance of 0 tokens.

### 2. **Login to Your Wallet**
   - Navigate to the **Access Your Wallet** section in the sidebar.
   - Enter your username and password, then click **Login**.
   - Once logged in, you can view your wallet details, transaction history, and manage tokens.

### 3. **Send Tokens**
   - After logging in, go to the **Send Tokens** section.
   - Enter the recipient's username and the amount to send.
   - Click **Send** to complete the transaction.

### 4. **Mine Tokens**
   - After logging in, go to the **Mine Tokens** section.
   - Click **Mine** to earn a random amount of tokens as a reward.

### 5. **Logout**
   - Use the **Logout** button in the sidebar to securely log out.

---

## Security
- **Password Hashing**: Passwords are hashed using SHA-256.
- **Encryption**: Wallet data is encrypted using AES encryption provided by the `cryptography` library.
- **Session State**: All user data is managed in `st.session_state` to ensure a secure and temporary session.

---

## Future Improvements
1. Add multi-factor authentication (MFA) for wallet access.
2. Integrate blockchain for a fully decentralized transaction system.
3. Provide token exchange and trading functionalities.
4. Implement a more robust mining algorithm.

---

## License
This project is licensed under the Apache License. See `LICENSE` for more details.

---

## Acknowledgments
- **Streamlit** for creating interactive web apps with ease.
- **Cryptography** for secure encryption and decryption.

```
