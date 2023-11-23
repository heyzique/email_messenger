# --- Libraries ---
from flask import Flask, render_template, request, flash
from datetime import datetime

# Library to connect to database using flask
from flask_sqlalchemy import SQLAlchemy
# Library to send email
from flask_mail import Mail, Message

# Instances
app = Flask(__name__)

# Data Base Config
app.config["SECRET_KEY"] = "sendmessage123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# Mail Config (GMAIL)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""

db = SQLAlchemy(app)
mail = Mail(app)


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
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        purpose = request.form["purpose"]
        messages = request.form["messages"]
        print(request.method)
        print(first_name, last_name, email, date, purpose, messages)

        # Creating variables to store user input
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, purpose=purpose, messages=messages)

        # Updating variables to the db session and committing to db
        db.session.add(form)
        db.session.commit()

        # User/Client Message
        message_body = f"<NO REPLY>\n\nDate: {date}\nThank you for taking the time to write me a message, {first_name}!\n\n" \
                       f"Here are the details submitted. \nName: {first_name} {last_name}\nPurpose: {purpose} " \
                       "\n\nI will get back to you soon. Hope you have a blessed day!\n\n " \
                       "<NO REPLY: Please do not reply to this email!>"

        # Admin Message
        ownmessage_body = "You just recieved a message from EMAIL MESSENGER!\n\n" \
                          f"Sender Name: {first_name} {last_name}\nSender Email: {email}\nPurpose: {purpose}\n" \
                          f"Message: {messages}"

        # -- Email Format --
        clientmessage = Message(subject="Your Message Submitted Successfully!",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)

        ownmessage = Message(subject="PYTHON EMAIL MESSENGER NOTIFICATION",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=["hey.zique@gmail.com"],
                          body=ownmessage_body)

        mail.send(clientmessage)
        mail.send(ownmessage)

        # Flash Notification function
        flash(f"Hi {first_name}, your message was submitted successfully!", "success")

    return render_template("index.html")


# Creating new database (if no existing database matching the set URI
# & run app on local terminal
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
