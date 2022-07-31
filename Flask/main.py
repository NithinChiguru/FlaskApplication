from tkinter import messagebox
from flask import Flask, render_template, request, redirect, url_for, session
from forms import LoginForm, RegistrationForm, ForgotForm, ConcertsForm,FeedbackForm
from flask_wtf import form
from jinja2 import defaults
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "TheEntertainaro"
mysql = MySQL(app)


@app.route('/',methods=['GET', 'POST'])
def index():
    form = FeedbackForm(request.form)
    if form.validate() and request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        phonenumber = userDetails['phonenumber']
        feedback = userDetails['feedback']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name=%s AND email=%s AND phonenumber=%s", (username, email, phonenumber))
        result = cur.fetchall()

        if result:
            cur.execute("INSERT INTO feedback(username,email,phonenumber,feedback) VALUES(%s,%s,%s,%s)",(username, email, phonenumber, feedback))
            mysql.connection.commit()
            return render_template("thankyou.html")
        else:
            messagebox.showerror("ERROR", "Username and email mismatch")
        cur.close()
    return render_template("base.html")


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    form = ForgotForm(request.form)
    if form.validate() and request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name=%s AND email=%s", (username, email))
        result = cur.fetchall()

        if result:
            cur.execute("SELECT * FROM forgotpasswords WHERE username=%s AND email=%s", (username, email))
            result2 = cur.fetchall()
            if result2:
                messagebox.showerror("REQUEST ERROR","You have already requested for password change and your request is being processed by the the E-TEAM")
            else:
                cur.execute("INSERT INTO forgotpasswords(username,email) VALUES(%s,%s)", (username, email))
                mysql.connection.commit()
                return render_template("thankyou.html")
        else:  # mismatch
            messagebox.showerror("ERROR", "Username and email mismatch")
        cur.close()
    return render_template("forgotpassword.html")


@app.route('/TheEntertainaroMultiplex')
def TheEntertainaroTheatre():
    return render_template("TheEntertainaroMultiplex.html")


@app.route('/TheEntertainaroMultiplexScreen')
def TheEntertainaroTheatreVideo():
    return render_template("TheEntertainaroMultiplexScreen.html")


@app.route('/TheEntertainaroConcerts', methods=['GET', 'POST'])
def TheEntertainaroConcerts():
    form = ConcertsForm(request.form)
    if form.validate() and request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        phone = userDetails['phone']
        date = userDetails['date']
        time = userDetails['time']
        message = userDetails['message']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name=%s AND email=%s AND phonenumber=%s", (username, email, phone))
        result = cur.fetchall()

        if result:
            cur.execute("SELECT * FROM concerts WHERE username=%s AND email=%s AND phonenumber=%s AND concertdate=%s", (username, email,phone,date))
            result2 = cur.fetchall()
            if result2:
                reply=messagebox.askquestion("CONFIRMATION","You have already requested E-TEAM to organize an event on the given date. Do you want us to organize other event for you on the same date?")
                if reply=='yes':
                    cur.execute("INSERT INTO concerts(username,email,phonenumber,concertdate,concerttime,message) VALUES(%s,%s,%s,%s,%s,%s)",(username, email, phone, date, time, message))
                    mysql.connection.commit()
                    return render_template("thankyou.html")
                else:
                    return render_template("TheEntertainaroConcerts.html")
            else:
                cur.execute("INSERT INTO concerts(username,email,phonenumber,concertdate,concerttime,message) VALUES(%s,%s,%s,%s,%s,%s)",(username, email, phone, date, time, message))
                mysql.connection.commit()
                return render_template("thankyou.html")

        else:  # mismatch
            messagebox.showerror("ERROR", "Username, email and phone number mismatch")
        cur.close()
    return render_template("TheEntertainaroConcerts.html")


@app.route('/thankyou')
def thankyou():
    return render_template("thankyou.html")


@app.route('/registrationSuccessful')
def registrationSuccessful():
    return render_template("registrationSuccessful.html")


@app.route('/gamezone')
def gamezone():
    return render_template("gamezone.html")

@app.route('/basicSubscription')
def basicSubscription():
    return render_template("basicSubscription.html")

@app.route('/standardSubscription')
def standardSubscription():
    return render_template("standardSubscription.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate() and request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name=%s AND password=%s", (username, password))
        result = cur.fetchall()

        if result:  # If there is such a record, then success
            cur.execute("SELECT * FROM users WHERE name=%s AND password=%s AND paymentstatus='unpaid'", (username, password))
            result2 = cur.fetchall()
            if result2:
                messagebox.showerror("LOGIN ERROR", "Subscription is not active")
            else:
                cur.execute("SELECT * FROM users WHERE name=%s AND password=%s AND paymentstatus='paid' AND subscriptionpack='100'",(username, password))
                result3 = cur.fetchall()
                if result3:
                    return render_template('basicSubscription.html', form=form)

                cur.execute("SELECT * FROM users WHERE name=%s AND password=%s AND paymentstatus='paid' AND subscriptionpack='150'",(username, password))
                result4 = cur.fetchall()
                if result4:
                    return render_template('standardSubscription.html', form=form)

                else:
                    return render_template('gamezone.html', form=form)

        else:  # Wrong password
            messagebox.showerror("LOGIN ERROR", "Username or Password is incorrect")
        cur.close()
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate() and request.method == 'POST':
        userDetails = request.form
        name = userDetails['username']
        password = userDetails['password']
        reenterpassword = userDetails['reenterpassword']
        email = userDetails['email']
        phonenumber = userDetails['phonenumber']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name=%s OR email=%s OR phonenumber=%s", (name, email, phonenumber))
        result = cur.fetchall()

        if result:
            messagebox.showerror("REGISTRATION ERROR",
                                 "Account already exist with same username or email or phone number")

        else:
            if password == reenterpassword:
                cur.execute("INSERT INTO users(name,password,reenterpassword,email,phonenumber) VALUES(%s,%s,%s,%s,%s)",(name, password, reenterpassword, email, phonenumber))
                mysql.connection.commit()
                cur.close()
                return render_template('registrationSuccessful.html', form=form)
            else:
                messagebox.showerror("MISMATCH ERROR", "Passwords didn't match")
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug='True')
