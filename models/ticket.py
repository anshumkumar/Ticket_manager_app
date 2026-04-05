from database.db import db_connection

# ticket class is added here, to manage tickets.

class Ticket:
    def __init__(self, ticket_id, user_id, staff_id, title, description, category, priority, status, created_at, updated_at):
        self.ticket_id = ticket_id
        self.user_id = user_id          
        self.staff_id = staff_id        
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at 
    # mostly based on my uml diagram, if new features are added, I will update them.


    def create_ticket(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (user_id, staff_id, title, description, category, priority, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.user_id, self.staff_id, self.title, self.description, self.category, self.priority, self.status, self.created_at, self.updated_at))
        conn.commit()
        conn.close()
    # adds these details to database, and creates a new ticket.
    


    @staticmethod
    def cancel_ticket(ticket_id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE tickets SET status = 'Cancelled', updated_at = CURRENT_TIMESTAMP where id = ?
                       """, (ticket_id,))
        
        conn.commit()
        conn.close()
    # this just updates ticket status, it doesnt remove ticket from database. Its history remains there for records.

    @staticmethod
    def ticket_priority(ticket_id, new_priority):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE tickets SET priority = ?, updated_at = CURRENT_TIMESTAMP where id = ?
                       """, (new_priority, ticket_id,))
        
        conn.commit()
        conn.close()

    @staticmethod
    def ticket_category(ticket_id, new_category):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE tickets SET category = ?, updated_at = CURRENT_TIMESTAMP where id = ?
                       """, (new_category, ticket_id,))
        
        conn.commit()
        conn.close()

    @staticmethod
    def detailed_info(ticket_id, new_description):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE tickets SET description = ?, updated_at = CURRENT_TIMESTAMP where id = ?
                       """, (new_description, ticket_id,))
        
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_tickets(user_id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows 
