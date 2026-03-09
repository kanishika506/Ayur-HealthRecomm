from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from ai.face_analyzer import run_face_analysis

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('first.html')

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/analyzer")
def analyzer():
    run_face_analysis()
    return  "camera close"

@app.route("/login", methods = ["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor(dictionary = True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"],password):
            message = "Login successful"
        else:
            message = "Invalid credentials"

    return render_template("login.html", message = message)

@app.route("/register", methods = ["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            message = "Passwords do not match"
            return render_template("register.html", message = message)

        if len(password) < 6:
            message = "Password must be at least 6 characters long"
            return render_template("register.html", message = message)

        hashed_password = generate_password_hash(password)
        conn = get_db()
        cursor = conn.cursor(dictionary = True)

        cursor.execute("SELECT * FROM users WHERE username = %s",(username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            message = "Username already exists"
            return render_template("register.html", message = message)

        cursor.execute("INSERT INTO users (username,password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("login"))
    
    return render_template("register.html", message = message)

if __name__ == "__main__":
    app.run(debug=True)
