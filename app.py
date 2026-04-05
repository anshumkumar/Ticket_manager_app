from flask import Flask, render_template, request, redirect, session, url_for
from models.user import User
from models.ticket import Ticket
from datetime import datetime
import traceback
from database.db import db_connection

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

@app.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    
    # Get ticket from database
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE id = ? AND user_id = ?", (ticket_id, session['user_id']))
    ticket = cursor.fetchone()
    conn.close()
    
    if not ticket:
        return "Ticket not found", 404
    
    return render_template('view_ticket.html', ticket=ticket)



@app.route('/submit-ticket', methods=['GET', 'POST'])
def submit_ticket():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        priority = request.form.get('priority')
        
        # Create ticket object
        ticket = Ticket(
            ticket_id=None,
            user_id=session['user_id'],
            staff_id=None,
            title=title,
            description=description,
            category=category,
            priority=priority,
            status='Open',
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        ticket.create_ticket()
        
        return redirect(url_for('user_dashboard'))
    
    return render_template('submit_ticket.html')

@app.route('/ticket/<int:ticket_id>/cancel', methods=['POST'])
def cancel_ticket(ticket_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    
    if not ticket or ticket[0] != session['user_id']:
        return "Unauthorized", 403
    
    # Cancel the ticket
    Ticket.cancel_ticket(ticket_id)
    
    return redirect(url_for('user_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)