# Secure Password Manager with Todo List

A web-based password manager and todo list application with secure encryption.

## Features

- User Authentication System
- Secure Password Storage with Encryption
- Personal Todo List for Each User
- Timestamp Tracking for All Activities
- Activity Logging System

## Requirements

- Python 3.x
- Flask
- cryptography

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/soham-bhimani/password_manager.git
cd password_manager
```

2. Install required packages:
```bash
pip install flask cryptography
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

## Using the Application

1. Register a new account or login with existing credentials
2. Add, complete, and manage your todos
3. All activities are automatically logged
4. Your passwords are securely encrypted

## Security Features

- Passwords are encrypted using Fernet encryption
- Secure session management
- Activity logging for security monitoring

## Important Notes

- Keep your `key.key` file secure - it's required to decrypt passwords
- The `passwords.txt` and `key.key` files are automatically ignored by git
- Each user gets their own secure todo list

## Contributing

Feel free to:
- Fork the repository
- Create a feature branch
- Submit pull requests

## License

Free to use and modify. Please credit the original source.

## Contact

- GitHub: [soham-bhimani](https://github.com/soham-bhimani)
