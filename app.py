from flask import Flask, render_template_string
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'db'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'password'),
            database=os.environ.get('DB_NAME', 'mydb')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    status = "Successfully Connected to MySQL Database!" if conn and conn.is_connected() else "Failed to Connect to MySQL Database."
    if conn and conn.is_connected():
        conn.close()
        
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Two-Tier Web App</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f6f9; }
            .container { background: white; padding: 30px; inline-size: 50%; margin: 0 auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .status { font-size: 20px; font-weight: bold; color: {{ 'green' if 'Successfully' in status else 'red' }}; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Two-Tier Web App Deployment</h1>
            <p>Tech Stack: Flask, MySQL, Docker, & Jenkins</p>
            <div class="status">{{ status }}</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

