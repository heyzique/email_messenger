from flask import Flask, render_template, request, flash
from datetime import datetime

app = Flask(__name__)


# Running the application + linking to html file
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
