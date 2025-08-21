from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------------------
# Helper functions
# ---------------------
def read_users():
    users = []
    if os.path.exists('password.txt'):
        with open('password.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append({'username': username, 'password': password})
    return users

def add_user(username, password):
    with open('password.txt', 'a') as f:
        f.write(f"{username}|{password}\n")

# ---------------------
# Routes
# ---------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()

        # Check if user already exists
        for user in users:
            if user['username'] == username:
                flash('Username already exists!')
                return redirect(url_for('register'))

        add_user(username, password)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                flash('Login successful!')
                return redirect(url_for('todos'))
        flash('Invalid credentials!')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/todos')
def todos():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    todo_file = f"{username}_todos.txt"

    todos_list = []
    if os.path.exists(todo_file):
        with open(todo_file, 'r') as f:
            todos_list = [line.strip() for line in f]

    return render_template('todos.html', todos=todos_list, username=username)

@app.route('/admin')
def admin():
    try:
        users = read_users()
    except Exception as e:
        return f"Error reading users: {e}"
    return render_template('admin.html', users=users)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
