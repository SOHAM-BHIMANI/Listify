from cryptography.fernet import Fernet
import base64

def generate_key():
    # Generate a proper Fernet key
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    try:
        with open('key.key', 'rb') as key_file:
            key = key_file.read()
            # Verify the key is valid
            Fernet(key)
            return key
    except FileNotFoundError:
        print("No encryption key found. Creating a new one...")
        print("Warning: This will only work for new passwords. Any existing passwords will need to be re-added.")
        return generate_key()
    except Exception as e:
        print(f"Error with encryption key: {e}")
        print("Creating a new key. You will need to re-add your passwords.")
        return generate_key()

# Initialize the key when the program starts
key = load_key()

def view():
    fer = Fernet(key)  # Use the global key
    try:
        with open('passwords.txt', 'r') as f:
            passwords = f.readlines()
            if not passwords:
                print("No passwords stored.")
                return
            print("Stored passwords:")
            for line in passwords:
                try:
                    name, encrypted_password = line.strip().split('|')
                    decrypted_password = fer.decrypt(encrypted_password.encode()).decode()
                    print(f"Account: {name}, Password: {decrypted_password}")
                except Exception as e:
                    print(f"Error decrypting password: {e}")
    except FileNotFoundError:
        print("No passwords stored yet.")
def add():
    name = input("Enter the name of the account: ")
    password = input("Enter the password: ")
    
    fer = Fernet(key)  # Use the global key
    encrypted_password = fer.encrypt(password.encode()).decode()
    
    with open('passwords.txt', 'a') as f:
        f.write(f"{name}|{encrypted_password}\n")
    print("Password added successfully!")
# password_manager.py
while True:
    mode = input("would you like to add a new password or view existing passwords? (add/view) press q to quit : ").lower()
    if mode == 'q':
        print("Exiting the password manager.")
        break
    elif mode == 'view':
        view()
    elif mode == 'add':
        add()
    else:
        print("Invalid option. Please choose 'add' or 'view'.")
        continue