# Password Manager

A simple and secure password manager built with Python using the Fernet encryption system.

## Features

- Securely store account passwords using Fernet encryption
- Add new account passwords
- View stored passwords
- Encrypted storage of passwords
- Safe key management

## Requirements

- Python 3.x
- cryptography package

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
```

2. Install required packages:
```bash
pip install cryptography
```

## Usage

Run the password manager:
```bash
python password_manager.py
```

The program will:
- Generate a new encryption key on first run
- Allow you to add new passwords
- Allow you to view existing passwords
- Automatically encrypt all stored passwords

## Security Note

- Keep your `key.key` file safe - it's required to decrypt your passwords
- Never share your `key.key` file
- The `passwords.txt` and `key.key` files are automatically ignored by git for security
