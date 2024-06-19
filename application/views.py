from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase
import smtplib
import random
import re
view = Blueprint("views", __name__)


# GLOBAL CONSTANTS
NAME_KEY = 'name'
MSG_LIMIT = 20
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
global OTP
OTP = random.randint(10000, 99999)
global Name

def OTPapi(email):
    TEXT = f"Dear Customer,\n\n{OTP} is your One Time Password (OTP). Please enter to proceed \n\nThank you,"
    SUBJECT = "LAN CHAT APP"
    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("otpbot9094@gmail.com", "qqpbvnzvfveabtkr")
    emailid = email
    s.sendmail("&&", emailid, msg)

    return True

# VIEWS
@view.route("/login", methods=["POST", "GET"])
def login():
    """
    displays main login page and handles saving name in session
    :exception POST
    :return: None
    """
    if request.method == "POST":  # if user input a name
        Name = request.form["inputName"]
        email = request.form["email"]
        if len(Name) >= 2 and re.fullmatch(regex, email):
            session[NAME_KEY] = Name
            if OTPapi(email):
                flash('0OTP sent successfully...')
                return redirect(url_for("views.verify"))
        else:
            flash(' Enter valid characters.')
    return render_template("login.html", **{"session": session})

@view.route("/verifyotp" ,methods=["GET" , "POST"] ) #methods=["POST"]
def verify():
    if request.method == "POST":
        otp = request.form["OTP"]
        if len(otp) >=5:
            c = int(otp)
            #session[NAME_KEY] = Name
            if c == OTP:
                flash('You were successfully logged')
                return redirect(url_for("views.home"))
        else:
            flash('0Please check the code again')
    return render_template("verifyotp.html", **{"session": session})

@view.route("/logout")
def logout():
    """
    logs the user out by popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash("0You were logged out...")
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    """
    displays home page if logged in
    :return: None
    """
    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("index.html", **{"session": session})


@view.route("/history")
def history():
    if NAME_KEY not in session:
        flash("0Please login before viewing message history")
        return redirect(url_for("views.login"))

    json_messages = get_history(session[NAME_KEY])
    print(json_messages)
    return render_template("history.html", **{"history": json_messages})


@view.route("/get_name")
def get_name():
    """
    :return: a json object storing name of logged in user
    """
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    """
    :return: all messages stored in database
    """
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)

    return jsonify(messages)


@view.route("/get_history")
def get_history(name):
    """
    :param name: str
    :return: all messages by name of user
    """
    db = DataBase()
    msgs = db.get_messages_by_name(name)
    messages = remove_seconds_from_messages(msgs)

    return messages


# UTILITIES
def remove_seconds_from_messages(msgs):
    """
    removes the seconds from all messages
    :param msgs: list
    :return: list
    """
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)

    return messages


def remove_seconds(msg):
    """
    :return: string with seconds trimmed off
    """
    return msg.split(".")[0][:-3]
