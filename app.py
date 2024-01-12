from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Sample user data (for demonstration purposes)
users = {
    'user1': {'username': 'user1', 'password': 'password1', 'balance': 1000},
    'user2': {'username': 'user2', 'password': 'password2', 'balance': 500},
}

@app.route('/')
def home():
    if 'username' in session:
        user = users.get(session['username'])
        if user:
            return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'username' in session:
        sender = users[session['username']]
        recipient_username = request.form['recipient']
        amount = float(request.form['amount'])

        if recipient_username in users and amount > 0 and sender['balance'] >= amount:
            recipient = users[recipient_username]
            sender['balance'] -= amount
            recipient['balance'] += amount
            return redirect(url_for('home'))

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
