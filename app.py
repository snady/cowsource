from flask import Flask, render_template, session, request
from flask import redirect, url_for
import sqlite3
import utils

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
@app.route("/login", methods = ['GET','POST'])
def login():
        all_rows = utils.getAllUsers()
        for n in range(len(all_rows)):
                all_rows[n] = all_rows[n][0]
        if request.method == 'POST':
                #user = str(request.form['user'])
                #password = str(request.form['pass'])
                error = ""
                message = ""
                if request.form['login'] == "login":
                        if utils.authenticate(user,password):
                                session['user'] = user
                                message = "You are now logged in!"
                                return render_template("home.html",message=message)
                        else:
                                error = "Incorrect Username or Password. Try Again."
                                return render_template("login.html",error=error)
                                
                if request.form['register'] == "register":
                        '''
                        if user in all_rows:
                                error = "Username already exists. Please try another"
                                return render_template("login.html",error=error)
                        else:
                                message = "Account Created!"
                                utils.addUser(user,password,email)
                                session['user'] = user
                                return redirect("/home",message=message)
                        '''
                        pasta = "pasta"
        return render_template("login.html") #login failed

@app.route("/logout")
def logout():
        del session['user']
        return redirect("/login")

@app.route("/home")
def home():
        return render_template("home.html")

if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)