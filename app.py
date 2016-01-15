from flask import Flask, render_template, session, request
from flask import redirect, url_for
import json
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
                error = ""
                message = ""
                if request.form.has_key('login'):
                        user = str(request.form['user'])
                        password = str(request.form['pass'])
                        if utils.authenticate(user,password):
                                session['user'] = user
                                message = "You are now logged in!"
                                return render_template("home.html",message=message)
                        else:
                                error = "Incorrect Username or Password. Try Again."
                                return render_template("login.html",error=error)                
                if request.form.has_key('register'):
                        user = str(request.form['reguser'])
                        password = str(request.form['regpass'])
                        email = str(request.form['email'])
                        if user in all_rows:
                                error = "Username already exists. Please try another"
                                return render_template("login.html",error=error)
                        else:
                                message = "Account Created!"
                                utils.addUser(user,password,email)
                                session['user'] = user
                                return render_template("home.html",message=messa)
        return render_template("login.html") #login failed

@app.route("/getrest")
def getRestaurant():
    name = request.args.get('name')
    location = request.args.get('location')
    dic = authy.search(name,location)
    print dic
    cleaned = []
    for i in dic['businesses']:
        a={}
        a['id']=i['id']
        a['name']=i['name']
        a['phone']=i['phone'][0]
        a['address']=[i['location']['address'],i['location']['city'],i['location']['state_code'],i['location']['postal_code']]
        a['rating']=i['rating']
        cleaned.append(a)
    clean = {}
    clean['results'] = cleaned
    return jsonify(result=clean)
    #address format = [street address, city, state, zip code]

@app.route("/makepost", methods = ['GET','POST'])
def makepost():
        if 'user' not in session:
                return redirect ("/login")
        if request.method == 'POST':
                name = request.form['name']
                desc = request.form['description']
                img = request.form['imgurl']
                rest = request.form['rest'] #need to replace with a yelp func that gets the yelp id instead of restaurant name
                price = request.form['price']
                user = session['user']
                idu = utils.getUserId(user)
                jason = {'name':name,'desc':desc,'price':price,'likes':0}
                print(json.dumps(jason))
                utils.writePost("rasta my pasta",img,idu,rest)
                message = "Post created!"
                return render_template("home.html",message=message)
        else:
                return render_template("makepost.html")

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
