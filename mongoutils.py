from pymongo import MongoClient
import hashlib

connection = MongoClient()
db = connection['database']
usersc = db.users
postsc = db.posts

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
    result = usersc.findOne({'name':username},{'_id':1})
    return result

'''
Args:
    
Returns:
'''
def getUserName(uid):
    result = usersc.findOne({'_id':uid},{'name':1})
    return result

'''
Args:
    
Returns:
''' 
def getAllUsers():
    return list(usersc.find())
#.sort({'_id':1}))

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
                
addUser('hellopy','my','friend')
##########Posts
'''
def writePost():

def getPost(idp):

def getAllPosts():

def addRestaurant():

##########Comments


'''
