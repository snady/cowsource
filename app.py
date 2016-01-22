from flask import Flask, render_template, session, request
from flask import redirect, url_for
from pymongo import MongoClient
import utils
import mongoutils
import json
import authy

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
@app.route("/login", methods = ['GET','POST'])
def login():
        all_rows = mongoutils.getAllUsers()
        for n in range(len(all_rows)):
                all_rows[n] = all_rows[n]['name']
        print all_rows
        if request.method == 'POST':
                error = ""
                message = ""
                print request.form
                if request.form.has_key('login'):
                        user = str(request.form['user'])
                        password = str(request.form['pass'])
                        if mongoutils.authenticate(user,password):
                                session['user'] = user
                                message = "You are now logged in!"
                                return render_template("home.html",message=message)
                        else:
                                error = "Incorrect Username or Password. Try Again."
                                return render_template("index.html",error=error)            
                if request.form.has_key('register'):
                        user = str(request.form['reguser'])
                        password = str(request.form['regpass'])
                        email = str(request.form['email'])
                        if user in all_rows:
                                error = "Username already exists. Please try another"
                                return render_template("index.html",regerror=error)
                        else:
                                message = "Account Created!"
                                mongoutils.addUser(user,password,email)
                                session['user'] = user
                                return render_template("home.html",message=message)
        return render_template("index.html") #login failed

@app.route("/getrest")
def getRestaurant(limit=5):
    name = request.args.get('name')
    location = request.args.get('location')
    dic = authy.search(name,location,limit)
    print dic
    cleaned = []
    for i in dic['businesses']:
        a={}
        a['id']=i['id']
        a['name']=i['name']
        a['address']=[i['location']['address'][0],i['location']['city'],i['location']['state_code'],i['location']['postal_code']]
        cleaned.append(a)
    return cleaned
    #address format = [street address, city, state, zip code]

@app.route('/like')
def like():
        idu = request.args.get('idu')
        idp = request.args.get('idp')
        mongoutils.likePost(idu,idp)

@app.route("/makepost", methods = ['GET','POST'])
def makepost():
        if 'user' not in session:
                return redirect ("/login")
        if request.method == 'POST':
                print request.form
                name = request.form['name']
                desc = request.form['description']
                img = request.form['path']
                rest = request.form['rest'] #need to replace with a yelp func that gets the yelp id instead of restaurant name
                price = request.form['price']
                tags = request.form['tags']
                user = session['user']
                idu = mongoutils.getUserId(user)
                mongoutils.writePost(img,tags,name,price,desc,idu,rest)
                message = "Post created!"
                print mongoutils.getAllPosts()
                return render_template("home.html",message=message)
        else:
                return render_template("writepost.html")

@app.route("/post/<int:idp>")
def showpost(idp):
        if 'user' not in session:
                return redirect("/login")
        posty = mongoutils.getPost(idp)
        return render_template("post.html",posty=posty)


#shows newest limi number of posts
@app.route("/posts/<int:limi>")
def showposts(limi):
        if 'user' not in session:
                return redirect("/login")
        posts = mongoutils.getAllPosts()
        postsinrange = []
        i = 0
        for post in posts[-1:-limi-1:-1]:
                postsinrange.append(post)
        return render_template("posts.html",postsinrange=postsinrange)

@app.route("/user/<int:idu>")
def user(idu):
        if 'user' not in session:
                return redirect("/login")
        userposts = mongoutils.getUserPosts(idu)
        username = mongoutils.getUserName(idu)
        return render_template("user.html",userposts=userposts,username=username)
                
        
@app.route("/logout")
def logout():
        del session['user']
        return redirect("/login")

@app.route("/home")
def home():
        return render_template("home.html")

@app.route("/autocomplete")
def autocomplete():
	name = request.args.get('term')
    	location = 'ny'
    	dic = authy.search(name,location,7)
    	#print dic
    	cleaned = []
    	for i in dic['businesses']:
        	a={}
        	a['id']=i['id']
        	a['label']=i['name']
        	a['address']=[i['location']['address'][0],i['location']['city'],i['location']['state_code'],i['location']['postal_code']]
        	cleaned.append(a)
	#print request.args
	return json.dumps(cleaned)

@app.route("/sriracha")
def sriracha():
	return render_template("otto.html")

if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
