import sqlite3
DB_NAME = "Leave_management.db"
def initialize_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT NOT NULL,
        designation TEXT NOT NULL,
        personal_number INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        report_date TEXT NOT NULl
    )
    """)
    connection.commit()
    connection.close()

def insert_leave_request(username, designation, personal_Number, start_date, end_date, report_date):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO leave_requests (username, designation, personal_number, start_date, end_date, report_date)
    VALUES(?,?,?,?,?,?)
    """,(username, designation, personal_Number, start_date, end_date, report_date))
    connection.commit()
    connection.close()

def fetch_all_leave_requests():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM leave_requests")
    records=cursor.fetchall()
    connection.close()
    return records

