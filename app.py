# --- Libraries ---
from flask import Flask, render_template, request, flash
from datetime import datetime

# Library to connect to database using flask
from flask_sqlalchemy import SQLAlchemy

# Instances
app = Flask(__name__)

# Data Base Config
app.config["SECRET_KEY"] = "sendmessage123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


# Data Base Model with field specifications
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    purpose = db.Column(db.String(80))
    messages = db.Column(db.String(500))


# --- Running the application + linking to html file ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        purpose = request.form["purpose"]
        messages = request.form["messages"]
        print(request.method)
        print(first_name, last_name, email, date, purpose, messages)
    return render_template("index.html")


# Creating new database (if no existing database matching the set URI
# & run app on local terminal
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
