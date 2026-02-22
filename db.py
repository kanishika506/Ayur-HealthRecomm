import mysql.connector

def get_db():

    conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = ""
            )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS login_db")
    cursor.execute("USE login_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    return conn
