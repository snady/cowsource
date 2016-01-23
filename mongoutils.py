from pymongo import MongoClient
import hashlib
import simplejson, urllib2

connection = MongoClient()
db = connection['database']
usersc = db.users
postsc = db.posts
restsc = db.rests

#########Users

'''
Args:
    
Returns:
'''
def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()

'''
Args:
    
Returns:
'''
def authenticate(username,password):
    result = list(usersc.find({'name':username}))
    for r in result:
        if(encrypt(password) == r['password']):
            return True
    return False

'''
Args:
    
Returns:
'''
def getUserId(username):
    result = usersc.find_one({'name':username},{'_id':1})
    return result['_id']

'''
Args:
    
Returns:
'''
def getUserName(uid):
    result = usersc.find_one({'_id':uid},{'name':1})
    return result

'''
Args:
    
Returns:
''' 
def getAllUsers():
    return list(usersc.find())

'''
Args:
    
Returns:
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
##########Posts

'''
Args:
    
Returns:
''' 
def getPost(idp):
    result = postsc.find_one({'_id':idp})
    return result

'''
Args:
    
Returns:
''' 
def getAllPosts():
    return list(postsc.find())

def getUserPosts(idu):
    return list(postsc.find({'uid':idu}))

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
Args:
    
Returns:
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
        #addRestaurant(idy)
        print "need restaurant"

#writePost("/path/",["hello","i","am","a","tag"],"nameoffood",3.14,"this is a nice pie", 2, "coolest-restaurant")

'''
Args:
    
Returns:

def addRestaurant():
'''
def addRestaurant(cleany, yelpid):
    for i in cleany:
        if i['id'] == yelpid:
            restsc.update({'_id':i['id']},{'name':i['name'], 'phone':i['phone'], 'address':[i['location']['address'][0],i['location']['city'],i['location']['state_code'],i['location']['postal_code'],i['location']['coordinate']], 'rating':i['rating']},{upsert:true})

def getRestaurant(yelpid):
    return restsc.findone({'_id':yelpid})

def getAllRestaurants():
    return list(restsc.find())

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

def getNearby(lat,lng):
    rests = getAllRestaurants()
    for r in rests:
        rcoord = r['address'][-1]
        r['distance'] = getDistance(lat,lng,rcoord[0],rcoord[1])
    srests = sorted(rests, key=lambda r:r[distance])
    return srests

##########APIs
def getDistance(o_lat, o_lng, d_lat, d_lng):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s' % (o_lat, o_lng, d_lat, d_lng)
    result = simplejson.load(urllib2.urlopen(url))
    return result['rows'][0]['distance']['value']

getDistance(40.60476,-73.95188,41.43206,-81.38992)
##########Comments
