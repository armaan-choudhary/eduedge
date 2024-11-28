import sqlite3
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def fetch_attendance_data(date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT status, COUNT(*) FROM attendance WHERE date = ? GROUP BY status', (date,))
    data = cursor.fetchall()
    conn.close()
    return data

def plot_attendance(date):
    data = fetch_attendance_data(date)
    statuses = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    plt.bar(statuses, counts, color=['green' if status == 'present' else 'red' for status in statuses])
    plt.xlabel('Status')
    plt.ylabel('Number of Students')
    plt.title(f'Attendance on {date}')
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    # Encode the image to base64
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url