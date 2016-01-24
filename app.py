from flask import Flask, render_template, session, request
from flask import redirect, url_for
from datetime import datetime
'''from pymongo import MongoClient
import utils'''
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
                if request.form.has_key('location'):
                    session['lati'] = json.loads(request.form['location'])['latitude']
                    session['longi'] = json.loads(request.form['location'])['longitude']
                if request.form.has_key('login'):
                        user = str(request.form['user'])
                        password = str(request.form['pass'])
                        if mongoutils.authenticate(user,password):
                                session['user'] = user
                                message = "You are now logged in!"
                                return redirect(url_for('showposts', limi = 30))
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

@app.route('/like')
def like():
        if 'idu' not in request.args:
                return 'illegal access'
        idu = request.args.get('idu',0,type = int)
        idp = request.args.get('idp',0,type = int)
        likes = {}
        likes['likes'] = len(mongoutils.likePost(idu,idp))
        return json.dumps(likes)

@app.route('/see')
def see():
        if 'idp' not in request.args:
                return 'illegal access'
        idp = request.args.get('idp',0,type = int)
        likes = {}
        likes['people']=[]
        for i in mongoutils.getPost(idp)['likes']:
                likes['people'].append([i,mongoutils.getUserName(i)['name']])
        print json.dumps(likes)
        return json.dumps(likes)

@app.route("/makepost", methods = ['GET','POST'])
def makepost():
        if 'user' not in session:
                return redirect ("/login")
        if request.method == 'POST':
                print request.form
                name = request.form['name']
                desc = request.form['description']
                img = request.form['path']
                rest = request.form['restid']
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

@app.route("/post/<int:idp>", methods = ['GET','POST'])
def showpost(idp):
        if 'user' not in session:
                return redirect("/login")
        if request.method == 'POST':
                content = request.form['texty']
                mongoutils.addComment(mongoutils.getUserId(session['user']),idp,content,datetime.now())
        posty = mongoutils.getPost(idp)
        posty['uname'] = mongoutils.getUserName(posty['uid'])
        commy = mongoutils.getComments(idp)
        return render_template("post.html",posty=posty,commy=commy)


#shows newest limi number of posts
@app.route("/posts/", methods = ['GET', 'POST'])
@app.route("/posts/<int:limi>", methods = ['GET', 'POST'])
@app.route("/posts/<int:start>/<int:limi>", methods = ['GET', 'POST'])
def showposts(limi=30,start=None):
        if 'user' not in session:
                return redirect("/login")
        if 'search' in request.args:
                print request.args['query']
                posts = mongoutils.search(request.args['query'])
        else:
                posts = mongoutils.getAllPosts()
        postsinrange = [[],[],[],[],[]]
        i = 0
        if start==None:
                start = 1
        for post in posts[-start:-limi-start:-1]:
                postsinrange[i%5].append(post)
                i += 1
        return render_template("posts.html",postsinrange=postsinrange)

@app.route("/user/<int:idu>")
def user(idu):
        if 'user' not in session:
                return redirect("/login")
        userposts = mongoutils.getUserPosts(idu)
        username = mongoutils.getUserName(idu)
        postsinrange = [[],[],[],[],[]]
        i = 0
        for post in userposts[-1::-1]:
                postsinrange[i%5].append(post)
                i += 1
        return render_template("user.html",postsinrange=postsinrange,username=username)
                
        
@app.route("/logout")
def logout():
        del session['user']
        return redirect("/login")

@app.route("/home", methods = ['GET','POST'])
def home():
    jason = []
    lati = session['lati']
    longi = session['longi']
    jason = mongoutils.getNearbyPosts(lati,longi)
    return render_template("home.html",json=jason)
 
    

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

@app.route("/nearby")
def nearby():
	return render_template("homhom.html")
'''
@app.route("/location", methods = ['GET','POST'])
def location():
    print "Request: ",request.json
    lati = request.json['latitude']
    longi = request.json['longitude']
    print lati,longi
	#mongoutils.getNearbyPosts(lati,longi)
    jason = json.dumps(mongoutils.getNearbyPosts(lati,longi))
    print jason
    return jason
'''

@app.route("/about")
def about():
        pass

if __name__ == "__main__":
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
