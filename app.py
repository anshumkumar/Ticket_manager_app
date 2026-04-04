from flask import Flask, render_template, request, redirect, session, url_for
from models.user import User
from models.ticket import Ticket
from datetime import datetime
import traceback

app = Flask(__name__)
app.secret_key = "akumar_secret_key"

@app.errorhandler(500)
def handle_error(error):
    print(f"500 ERROR: {error}")
    traceback.print_exc()
    return f"Error: {str(error)}", 500

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_user(username)
        
        if user and user.password == password:
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name
            
            if session['role'] == 'user':
                return redirect(url_for('user_dashboard'))
            elif session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['role'] == 'staff':
                return redirect(url_for('staff_dashboard'))
        
        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        
        existing_user = User.get_user(username)
        if existing_user:
            return render_template('register.html', error="Username already exists")
        
        new_user = User(id=None, name=name, username=username, password=password, role='user')
        new_user.save_user()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    
    tickets = Ticket.get_user_tickets(session['user_id'])
    return render_template('dashboard_user.html', user=session.get('name'), tickets=tickets)

@app.route('/staff/dashboard')
def staff_dashboard():
    if 'user_id' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))
    
    return render_template('dashboard_itstaff.html', user=session.get('name'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    return render_template('dashboard_admin.html', user=session.get('name'))

if __name__ == '__main__':
    app.run(debug=True)