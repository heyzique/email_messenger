from flask import Flask, render_template, request, flash
from datetime import datetime

app = Flask(__name__)


# Running the application + linking to html file
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        purpose = request.form["purpose"]
        messages = request.form["messages"]
        print(first_name, last_name, email, date, purpose, messages)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
