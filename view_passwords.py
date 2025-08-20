from cryptography.fernet import Fernet

# Load key
with open('key.key', 'rb') as f:
    key = f.read()

fer = Fernet(key)

# Read passwords.txt
with open('passwords.txt', 'r') as f:
    for line in f:
        username, encrypted_password = line.strip().split('|')
        try:
            password = fer.decrypt(encrypted_password.encode()).decode()
        except Exception:
            password = "<Error decrypting>"
        print(f"Username: {username}, Password: {password}")
