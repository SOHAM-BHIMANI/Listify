from flask import Flask, render_template, request, redirect, url_for, session, flash
from cryptography.fernet import Fernet
import json
import os
from functools import wraps
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Set up logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Fernet for encryption
def load_key():
    try:
        with open('key.key', 'rb') as key_file:
            key = key_file.read()
            return key
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)
        return key

fer = Fernet(load_key())

# User session decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Load todos from file
def load_todos():
    try:
        with open('todos.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save todos to file
def save_todos(todos):
    with open('todos.json', 'w') as f:
        json.dump(todos, f, indent=4)  # Pretty print JSON for better readability

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('todo'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            with open('passwords.txt', 'r') as f:
                for line in f:
                    stored_name, encrypted_password = line.strip().split('|')
                    if stored_name == username:
                        try:
                            decrypted_password = fer.decrypt(encrypted_password.encode()).decode()
                            if password == decrypted_password:
                                session['username'] = username
                                logging.info(f'Successful login for user: {username}')
                                return redirect(url_for('todo'))
                        except Exception as e:
                            logging.error(f'Decryption error for user {username}: {str(e)}')
                
                # If we get here, either username wasn't found or password didn't match
                logging.warning(f'Failed login attempt for user: {username}')
                return render_template('login.html', message='Invalid username or password', error=True)
                
        except FileNotFoundError:
            logging.error('passwords.txt file not found')
            return render_template('login.html', message='No users registered yet', error=True)
    
    return render_template('login.html', message=request.args.get('message'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', message='Passwords do not match')
        
        try:
            with open('passwords.txt', 'r') as f:
                for line in f:
                    stored_name, _ = line.strip().split('|')
                    if stored_name == username:
                        return render_template('register.html', message='Username already exists')
        except FileNotFoundError:
            pass
        
        encrypted_password = fer.encrypt(password.encode()).decode()
        with open('passwords.txt', 'a') as f:
            f.write(f"{username}|{encrypted_password}\n")
        
        return redirect(url_for('login', message='Registration successful! Please login.'))
    
    return render_template('register.html')

@app.route('/todo')
@login_required
def todo():
    username = session['username']
    todos = load_todos()
    user_todos = todos.get(username, [])
    return render_template('todo.html', username=username, todos=user_todos)

@app.route('/add_todo', methods=['POST'])
@login_required
def add_todo():
    todos = load_todos()
    username = session['username']
    if username not in todos:
        todos[username] = []
    
    todo_text = request.form['todo']
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_todo = {
        'text': todo_text,
        'completed': False,
        'created_at': current_time,
        'last_modified': current_time,
        'completed_at': None
    }
    
    todos[username].append(new_todo)
    save_todos(todos)
    logging.info(f'User {username} added new todo: {todo_text} at {current_time}')
    return redirect(url_for('todo'))

@app.route('/toggle_todo/<int:todo_id>', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    todos = load_todos()
    username = session['username']
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if username in todos and 0 <= todo_id < len(todos[username]):
        todo = todos[username][todo_id]
        todo['completed'] = not todo['completed']
        todo['last_modified'] = current_time
        todo['completed_at'] = current_time if todo['completed'] else None
        save_todos(todos)
        status = 'completed' if todo['completed'] else 'uncompleted'
        logging.info(f'User {username} marked todo "{todo["text"]}" as {status} at {current_time}')
    return redirect(url_for('todo'))

@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todos = load_todos()
    username = session['username']
    if username in todos and 0 <= todo_id < len(todos[username]):
        todos[username].pop(todo_id)
        save_todos(todos)
    return redirect(url_for('todo'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
