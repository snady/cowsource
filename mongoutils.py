from pymongo import MongoClient
import pymongo
import hashlib, authy
import simplejson, urllib2

connection = MongoClient()
db = connection['database']
usersc = db.users
postsc = db.posts
restsc = db.rests
commsc = db.comms

'''
-------------------------------------------------------------------------------
--------------------------------Users------------------------------------------
-------------------------------------------------------------------------------
'''

'''
________________________________Login__________________________________________
'''

'''
Checks whether the username and password match a registered user 
 
Args:
    username: username to be checked
    password: password to be checked    
    
Returns:
    True if both match
    False otherwise
'''
def authenticate(username,password):
    result = list(usersc.find({'name':username}))
    for r in result:
        if(encrypt(password) == r['password']):
            return True
    return False

'''
Gets the id that corresponds to a username

Args:
    username: username
    
Returns:
    corresponding user id
'''
def getUserId(username):
    result = usersc.find_one({'name':username},{'_id':1})
    return result['_id']

'''
Gets the username that corresponds to a user id

Args:
    uid: user id 
    
Returns:
    corresponding username
'''
def getUserName(uid):
    result = usersc.find_one({'_id':uid},{'name':1})
    return result

'''
Gets all users that are registered in the database

Args:
    none
    
Returns:
    list of dictionaries containing each user's info
''' 
def getAllUsers():
    return list(usersc.find())

'''
________________________________Changing_______________________________________
'''

'''
Registers a user into the database

Args:
    username: string username
    password: string password
    email: string email
    
Returns:
    True if the registration was successful
    False otherwise
'''
def addUser(username,password,email):
    if usersc.find_one({'name':username}) == None:
        us = getAllUsers()
        print us
        if len(us)==0:
            idu = 1
        else:
            idu = us[-1]['_id']+1    
        password = encrypt(password)
        r = {'_id':idu, 'name':username, 'password':password, 'email':email}
        usersc.insert(r)
        return True
    return False
                
'''
-------------------------------------------------------------------------------
--------------------------------Posts------------------------------------------
-------------------------------------------------------------------------------
'''

'''
________________________________Getting________________________________________
'''

'''
Gets the info corresponding to a post id

Args:
    idp: post id
    
Returns:
    dictionary containing post info
''' 
def getPost(idp):
    result = postsc.find_one({'_id':idp})
    result['yelpname']=getRestaurantName(result['yelpid'])
    return result

'''
Gets all posts stored in the database

Args:
    none
    
Returns:
    list of dictionaries containing post info
''' 
def getAllPosts():
    posts = list(postsc.find())
    for p in posts:
        p['yelpname']=getRestaurantName(p['yelpid'])
    return posts

'''
Gets all posts stored in the database that were made by a specific user

Args:
    idu: user id to checl
    
Returns:
    list of dictionaries containing post info
''' 
def getUserPosts(idu):
    posts = list(postsc.find({'uid':idu}))
    for p in posts:
        p['yelpname']=getRestaurantName(p['yelpid'])
    return posts

'''
Gets the posts matching the yelpid

Args:
    yelpid: the yelpid to look for
    
Returns:
    dictionary of post info if one is found
    None otherwise
'''
def getRestaurantPosts(yelpid):
    return list(postsc.find({'yelpid':yelpid}))

'''
________________________________Changing_______________________________________
'''


'''
Adds a post to the database, adds the restaurant with addRestaurant()

Args:
    path: path to the image file
    tags: array of tags
    name: name of the food
    price: price of the food
    description: description of the food
    idu: user id
    idy: restaurant's yelp ID
    
Returns:
    none
''' 
def writePost(path, tags, name, price, description, idu, idy):
    ps = getAllPosts()
    print ps
    if len(ps)==0:
        idp = 1
    else:
        idp = ps[-1]['_id']+1
    tags = tags.split(',')
    tags2 = []
    for tag in tags:
        tag = tag.strip().lower()
        tags2.append(tag)
    r = {'_id':idp, 'tags':tags2, 'likes':[], 'name':name, 'price':price, 
         'description':description, 'file':path, 'uid':idu, 'yelpid':idy}
    postsc.insert(r)
    if restsc.find_one({'_id':idy}) == None:
        addRestaurant(idy)
        print "need restaurant"
    return idp

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''

def removePost(idp):
    postsc.remove({'_id':idp})

'''
________________________________Liking_________________________________________
'''

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def likePost(idu,idp):
    p = postsc.find_one({'_id':idp})
    if not liked(idu,idp):
        p['likes'].append(idu)
    else:
        p['likes'].remove(idu)
    postsc.update_one({'_id':idp},{'$set':{'likes':p['likes']}})
    return p['likes']

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def liked(idu,idp):
    p = postsc.find_one({'_id':idp})
    print p
    return (idu in p['likes'])

'''
________________________________Searching______________________________________
'''

'''
Looks through posts to find matching tags, names, or location

Args:
    query: string to look for
    
Returns:
    array of post dictionaries that match query 
'''
def search(query):
    query = query.strip()
    result = {}
    postsc.create_index([('tags',pymongo.TEXT),('name',pymongo.TEXT)])
    restsc.create_index([('address',pymongo.TEXT),('name',pymongo.TEXT)])
    r = list(restsc.find({'$text': {'$search': query}}, 
                         {'score':{'$meta': "textScore"}}).sort(
                             [('score',{'$meta':"textScore"})]))
    q = list(postsc.find({'$text': {'$search': query}}, 
                         {'score':{'$meta': "textScore"}}).sort(
                             [('score',{'$meta':"textScore"})]))
    for rest in r:
        for post in q:
            if post['yelpid'] == rest['_id']:
                post['score'] += rest['score']
    return sorted(list(q), key = lambda k: k['score'], reverse=True)

'''
Gets the restaurant matching the yelpid

Args:
    yelpid: the yelpid to look for
    
Returns:
    dictionary of post info if one is found
    None otherwise
'''
def getNearbyPosts(lat,lng):
    rests = getNearbyRestaurants(lat,lng)
    result = []
    for r in rests:
        result.extend(getRestaurantPosts(r['_id']))
    return result

'''
-------------------------------------------------------------------------------
--------------------------------Comments---------------------------------------
-------------------------------------------------------------------------------
'''

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def addComment(idu,idp,content,time):
    idc = len(list(commsc.find()))+1
    commsc.insert({'_id':idc,'uid':idu,'pid':idp,'content':content,
                    'time': time  })
   
'''
Gets the distance between two points

Args:
    
    
Returns:
    
''' 
def removeComment(idc):
    commsc.remove({'_id':idc})

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def getComments(idp):
    commy = list(commsc.find({'pid':idp}))
    for c in commy:
        c['name'] = getUserName(c['uid'])
    return commy


'''
-------------------------------------------------------------------------------
--------------------------------Restaurants------------------------------------
-------------------------------------------------------------------------------
'''

'''
________________________________Getting________________________________________
'''

'''
Gets the restaurant matching the yelpid

Args:
    yelpid: the yelpid to look for
    
Returns:
    dictionary of post info if one is found
    None otherwise
'''
def getRestaurant(yelpid):
    return restsc.find_one({'_id':yelpid})

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def getRestaurantName(yelpid):
    if restsc.find_one({'_id':yelpid}) == None:
        return yelpid
    return restsc.find_one({'_id':yelpid})['name']

'''
Gets all restaurants in the database

Args:
    none
    
Returns:
    list of restaurant dictionaries
'''
def getAllRestaurants():
    return list(restsc.find())

'''
Gets restaurants that are nearby

Args:
   lat:
   lng:
    
Returns:
    
'''
def getNearbyRestaurants(lat,lng):
    rests = getAllRestaurants()
    filtered = []
    for r in rests:
        rcoord = r['address'][-1]
        dist = getDistance(lat,lng,rcoord['latitude'],rcoord['longitude'])
        if dist < 15000:
            r['distance'] = dist
            filtered.append(r) 
    srests = sorted(filtered, key=lambda r:r['distance'])
    return srests

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def getRestaurantName(yelpid):
    try:
        yelpname=getRestaurant(yelpid)['name']
    except:
        yelpname=''
    return yelpname                              

'''
________________________________Changing_______________________________________
'''


'''
Adds a restaurant to the database using information from the Yelp API

Args:
    yelpid: string id used by Yelp to identify a restaurant
    
Returns:
    none
'''
def addRestaurant(yelpid):
    i = authy.get_business(yelpid)
    restsc.insert({'_id':i['id'], 'name':i['name'], 'phone':i['phone'], 'address':[i['location']['address'][0],i['location']['city'],i['location']['state_code'],i['location']['postal_code'],i['location']['coordinate']], 'rating':i['rating']})

'''
-------------------------------------------------------------------------------
--------------------------------Miscellaneous----------------------------------
-------------------------------------------------------------------------------
'''

'''
Encrypts a password using the hashlib library for python

Args:
    word: string to be encrypted

Returns:
    encrypted string
'''
def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def getDistance(o_lat, o_lng, d_lat, d_lng):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s' % (o_lat, o_lng, d_lat, d_lng)
    result = simplejson.load(urllib2.urlopen(url))
    return result['rows'][0]['elements'][0]['distance']['value']

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def getCityState(o_lat, o_lng):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s' % (o_lat, o_lng)
    result = simplejson.load(urllib2.urlopen(url))
    addr = result['results'][len(result)-6]['formatted_address']
    addr = addr[:addr.rfind(",")]
    return addr[:addr.rfind(" ")]
    #this format works for most u.s addresses






#getDistance(40.60476,-73.95188,41.43206,-81.38992)

#print getNearbyPosts(40.60476,-73.95188)

#print getCityState(42.376765, -71.116724)

#print getRestaurantName("audreys-concerto-brooklyn")

##########Comments

#addUser('hellopyk','my','friend')



#print search('pizza ave')
#print getAllPosts()
#print getRestaurantPosts("dunkin-donuts-boston-24")
#writePost("/path/",["hello","i","am","a","tag"],"nameoffood",3.14,"this is a nice pie", 2, "starbucks-brooklyn-39")
#writePost("/path2/",["hello","i","am","another","tag"],"bestdrinkeva",6.28,"this is a nice frappuccino", 3, "starbucks-brooklyn-39")
#writePost("/path3/",["hello","i","am","another","tag"],"coffeeman",3.28,"this is best coffee i rate 5/7", 3, "dunkin-donuts-boston-24")
#writePost("/path4/",["hello","i","am","so many","tags"],"coffeewoman",3.28,"this is best coffee i rate 7/5", 3, "dunkin-donuts-boston-24")

