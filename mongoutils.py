from pymongo import MongoClient
import hashlib, authy
import simplejson, urllib2

connection = MongoClient()
db = connection['database']
usersc = db.users
postsc = db.posts
restsc = db.rests

'''
--------------------------------Users------------------------------------------
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
Checks whether the username
 
Args:
    username: string username to be checked
    password: string password to be checked    
    
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
    username: string username
    
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
                
#addUser('hellopyk','my','friend')

'''
--------------------------------Posts------------------------------------------
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
    return result

'''
Gets all posts stored in the database

Args:
    none
    
Returns:
    list of dictionaries containing post info
''' 
def getAllPosts():
    return list(postsc.find())

'''
Gets all posts stored in the database that were made by a specific user

Args:
    idu: user id to checl
    
Returns:
    list of dictionaries containing post info
''' 
def getUserPosts(idu):
    return list(postsc.find({'uid':idu}))

'''
def likePost(idu,idp):
    p = postsc.find_one({'_id:':idp})
    if not liked(idu,idp):
        p['likes'].append(idu)
    else:
        p['likes'].remove(idu)

def liked(idu,idp):
    p = postsc.find_one({'_id:':idp})
    return idu in p['likes']
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
    r = {'_id':idp, 'tags':tags, 'likes':[], 'name':name, 'price':price, 'description':description, 'file':path, 'uid':idu, 'yelpid':idy}
    postsc.insert(r)
    if restsc.find_one({'_id':idy}) == None:
        addRestaurant(idy)
        print "need restaurant"

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
    r = list(postsc.find({'tags':{'$in':[query]}}))
    if len(r)>0:
        result.extend(r)
        return result
    #name
    r = list(postsc.find({'name':{'$in':[query]}}))
    if len(r)>0:
        result.extend(r)
        return result
    #retaurant name
    r = list(postsc.find({'tags':{'$in':[query]}}))
    if len(r)>0:
        result.extend(r)
        return result
    #location

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

#print getAllPosts()
#print getRestaurantPosts("dunkin-donuts-boston-24")
#writePost("/path/",["hello","i","am","a","tag"],"nameoffood",3.14,"this is a nice pie", 2, "starbucks-brooklyn-39")
#writePost("/path2/",["hello","i","am","another","tag"],"bestdrinkeva",6.28,"this is a nice frappuccino", 3, "starbucks-brooklyn-39")
#writePost("/path3/",["hello","i","am","another","tag"],"coffeeman",3.28,"this is best coffee i rate 5/7", 3, "dunkin-donuts-boston-24")
#writePost("/path4/",["hello","i","am","so many","tags"],"coffeewoman",3.28,"this is best coffee i rate 7/5", 3, "dunkin-donuts-boston-24")

'''
--------------------------------Restaurants------------------------------------
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
Gets all restaurants in the database

Args:
    none
    
Returns:
    list of restaurant dictionaries
'''
def getAllRestaurants():
    return list(restsc.find())

'''
def searchRestaurant(query):
    queries = query.lower().split(' ')
    rests = getAllRestaurants()
    results = {}
    for rest in rests:
        words = rest['name'].lower()
        for q in queries:
            if words.find(q) != -1:
                if rest['_id'] not in results:
                    results[rest['_id']] += 1
    return sorted(results, key=results.get, reverse=True)
'''

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
--------------------------------Miscellaneous----------------------------------
'''

'''
Gets the distance between two points

Args:
    
    
Returns:
    
'''
def getDistance(o_lat, o_lng, d_lat, d_lng):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s' % (o_lat, o_lng, d_lat, d_lng)
    result = simplejson.load(urllib2.urlopen(url))
    print result['rows'][0]
    return result['rows'][0]['elements'][0]['distance']['value']

#getDistance(40.60476,-73.95188,41.43206,-81.38992)

#print getNearby(40.60476,-73.95188)

##########Comments
