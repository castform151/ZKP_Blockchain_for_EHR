import json
import os
import pickle
from flask import Flask
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from forms import SignupUser,SignIn, ViewReportForm,ViewTransactionForm,AddReportForm,SendReportForm
from flask import Flask, jsonify, request, flash, redirect, url_for, render_template
from config import Config
from blockchain import Blockchain,User,Transaction,userList


login=False
login_username=""
password=""

class SimpleObject(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return {key:value for key, value in obj.__dict__.items() if not key.startswith("_")}
        return super().default(obj)
b = Blockchain()
if os.path.exists('blockchain.pkl'):
    with open('blockchain.pkl', 'rb') as f:
        b= pickle.load(f)
else:
    print("Pickle not found")

        
app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET'])
def home():

    global login
    global login_username

    if(not login):
        return redirect('/home')

    return render_template('home.html', user=login_username + " (logout)")


# @app.route('/home', methods=['GET'])
# def home():
#     global login
#     global login_username
#     return render_template('home',user=login_username + " (logout)")

@app.route('/signup', methods=['GET','POST'])
def signup():
    global login
    global login_username
    global password
    # if login:
    #     return redirect('/signup')
    form=SignupUser(request.form)
    if(request.method =='POST' and form.validate()):
        username =form.username.data
        for user in userList:
            if (user.username == username):
                flash("This username is already taken")
                return redirect("/signup")
        u1 = User(form.username.data,form.password.data)
        userList.append(u1)
        flash("Successfully signed in. You can Login now ",'success')

        return redirect('/login')


    return render_template('signup.html',form=form)


@app.route('/login',methods =['GET','POST'])
def login():
    global login
    global login_username
    global password
    # if not login:
    form =SignIn(request.form)
    if(request.method =='POST' and form.validate()):
        u1 = User(form.username.data,form.password.data)
        for user in userList:
            if (user.username == u1.username and user.password==u1.password):
                login=True
                login_username=u1.username
                flash("Successfully logged in", 'success')
                return redirect('/index')
            else:
                flash("invalid username or password")
                return redirect('/login')


    return render_template('signup.html',form=form)

@app.route('/viewreport', methods=['POST', 'GET'])
def viewreport():
    global login
    global login_username
    global password
    if(not login):
        return redirect('/login')


    form = ViewReportForm(request.form)
    # global login_username

    if (request.method == 'POST' and form.validate()):
        for user in userList:
            if (user.username == login_username):
                data=user.reportList
                if data is None:
                    flash("No reports for this user ")

                return render_template('viewreport.html', data=data, form=form, user=login_username + " (logout)")

    return render_template('viewreport.html', form=form, user=login_username + " (logout)")


@app.route('/viewtransaction', methods=['POST', 'GET'])
def viewtransaction():
    global login
    global login_username   
    global password
    if(not login):
        return redirect('/login')


    form = ViewTransactionForm(request.form)
    # global login_username

    if (request.method == 'POST' and form.validate()):
        transactions = b.viewUser(login_username)
        return render_template('viewtransaction.html', data=transactions, form=form, user=login_username + " (logout)")

    return render_template('viewtransaction.html', form=form, user=login_username + " (logout)")



@app.route('/addreport', methods=['POST', 'GET'])
def addreport():

    global login    
    global login_username
    global password

    if(not login):
        return redirect('/login')

    form = AddReportForm(request.form)


    if (request.method == 'POST' and form.validate()):
        # user = form.username.data
        report = form.report.data
        for user in userList:
            if (user.username == login_username):
                user.reportList.append(report)
                flash("Report added succesfully",'success')
        return redirect('/index')

    return render_template('addreport.html', form=form, user=login_username + " (logout)")


@app.route('/sendreport', methods=['POST', 'GET'])
def sendreport():

    global login    
    global login_username
    global password

    if(not login):
        return redirect('/login')

    form = SendReportForm(request.form)
    for user in userList:
            if (user.username == login_username):
                sender = user

    if (request.method == 'POST' and form.validate()):
        recipient_un = form.recipient.data
        if recipient_un == login_username:
            flash("Sender and Recipient can't be the same person")
            return redirect('/sendreport')
        report = form.report.data
        for user in userList:
            if (user.username == recipient_un):
                recipient = user
                b.addTransaction(Transaction(sender, recipient,report))
                flash("Transaction added succesfully",'success')
                return redirect('/index')
            else:
                flash("Recipient does not exist")
                return redirect('/sendreport')


    return render_template('sendreport.html', form=form, user=login_username + " (logout)")


app.run(debug=True, port=5000)
