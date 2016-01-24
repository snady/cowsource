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
                print 'a'
                error = ""
                print request.form
                if request.form['location'] != '':
                    session['lati'] = json.loads(request.form['location'])['latitude']
                    session['longi'] = json.loads(request.form['location'])['longitude']
                if request.form.has_key('login'):
                        user = str(request.form['user'])
                        password = str(request.form['pass'])
                        if mongoutils.authenticate(user,password):
                                session['user'] = user
                                return redirect("/home")
                        else:
                                error = "Incorrect Username or Password. Try Again."
                                return render_template("index.html",error=error)            
                if request.form.has_key('register'):
                        print '1'
                        user = str(request.form['reguser'])
                        password = str(request.form['regpass'])
                        email = str(request.form['email'])
                        print '2'
                        if user in all_rows:
                                print '3'
                                error = "Username already exists. Please try another"
                                return render_template("index.html",regerror=error)
                        else:
                                print '4'
                                message = "Account Created!"
                                mongoutils.addUser(user,password,email)
                                session['user'] = user
                                return redirect("/home")
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
                if request.form['restid'] != '':
                        rest = request.form['restid']
                else:
                        rest = request.form['rest']
                price = request.form['price']
                tags = request.form['tags']
                user = session['user']
                idu = mongoutils.getUserId(user)
                idp = mongoutils.writePost(img,tags,name,price,desc,idu,rest)
                return redirect(url_for('showpost',idp=idp))
        else:
                return render_template("writepost.html")

@app.route("/post/<int:idp>", methods = ['GET','POST'])
def showpost(idp):
        if 'user' not in session:
                return redirect("/login")
        if request.method == 'POST':
                if 'remove' in request.form:
                        mongoutils.removePost(idp)
                        return redirect(url_for('showposts'))
                elif 'removec' in request.form:
                        print request.form['removec']
                        mongoutils.removeComment(int(request.form['removec']))
                else:
                        content = request.form['texty']
                        mongoutils.addComment(mongoutils.getUserId(session['user']),idp,content,datetime.now())
        posty = mongoutils.getPost(idp)
        posty['uname'] = mongoutils.getUserName(posty['uid'])
        commy = mongoutils.getComments(idp)
        return render_template("post.html",posty=posty,commy=commy)


#shows newest limi number of posts
@app.route("/posts/", methods = ['GET', 'POST'])
@app.route("/posts/<int:limi>", methods = ['GET', 'POST'])
def showposts(limi=30):
        display_msg  = ""
        if 'user' not in session:
                return redirect("/login")
        if 'search' in request.args:
                print request.args['query']
                posts = mongoutils.search(request.args['query'])
                display_msg = "Search for %s" % (request.args['query'])
        else:
                posts = mongoutils.getAllPosts()
                display_msg = "Browse"
        for post in posts:
            post['restaurant'] = mongoutils.getRestaurantName(post['yelpid'])
        #print posts
        return render_template("posts.html",posts=posts,display_msg=display_msg)

@app.route("/user/<int:idu>")
def user(idu):
        if 'user' not in session:
                return redirect("/login")
        userposts = mongoutils.getUserPosts(idu)
        username = mongoutils.getUserName(idu)
        return render_template("user.html",postsinrange=userposts,username=username)
                
        
@app.route("/logout")
def logout():
        del session['user']
        return redirect("/login")

@app.route("/home", methods = ['GET','POST'])
def home():
    if 'lati' not in session or 'longi' not in session:
            return render_template("home.html")
    lati = session['lati']
    longi = session['longi']
    jason = mongoutils.getNearbyPosts(lati,longi)
    location = mongoutils.getCityState(lati,longi)
    for post in jason:
        post['restaurant'] = mongoutils.getRestaurantName(post['yelpid'])
    return render_template("home.html",json=jason,location=location)
 
    

@app.route("/autocomplete")
def autocomplete():
	name = request.args.get('term')
    	location = mongoutils.getCityState(session['lati'],session['longi'])
        location = location.replace(',','')
        print location
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

@app.route("/about")
def about():
        return render_template("about.html")

if __name__ == '__main__':
        app.secret_key = "hello"
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
else:
        app.secret_key = "hello"

