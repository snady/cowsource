import sqlite3,hashlib,authy

def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()

def authenticate(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.password FROM users WHERE users.name = "%s"'
    result = cur.execute(q%username)
    for r in result:
        if(encrypt(password) == r[0]):
            return True
    conn.close()
    return False

def getUserId(name):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.id FROM users WHERE users.name = "%s"'
    result = cur.execute(q%name).fetchone()
    conn.close()
    if result==None:
        return None
    return result[0]

def getUserName(uid):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.id = %d'
    result = cur.execute(q%uid).fetchone()
    conn.close()
    return result[0]
    
def getAllUsers():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT users.name FROM users"
    cur.execute(q)
    all_rows = cur.fetchall()
    print all_rows
    conn.commit()
    return all_rows

def addUser(username,password,email):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.name = ?'
    result = cur.execute(q,(username,)).fetchone()
    if result == None:
        q = 'SELECT max(users.id) FROM users'
        uid = cur.execute(q).fetchone()[0]
        if uid==None:
            uid=0
        q = 'INSERT INTO users VALUES (?, ?, ?, ?)'
        cur.execute(q, (uid+1, username, encrypt(password), email))
        #print str(uid+1)+","+username
        conn.commit()
        conn.close()
        return True
    conn.commit()
    conn.close()
    return False


def writePost(jason,path,idu,idy):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(id) FROM posts"
    idp = cur.execute(q).fetchone()[0]
    if idp == None:
        idp = 0
    print idp+1
    q = "INSERT INTO posts(id,jasondata,file,uid,yelpid) VALUES(?,?,?,?,?)"
    cur.execute(q,(idp+1,jason,path,idu,idy))
    q = "SELECT * FROM restaurants WHERE yelpid = '%s'"
    rests = cur.execute(q%idy).fetchall()
    print rests
    if len(rests)==0:
        q = "INSERT INTO restaurants VALUES (?,?,?,?,?)"
        cur.execute(q,(idy,"a","b","c","d"))
    conn.commit()
    conn.close()
    return idp + 1

def getPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.id = ?"
    result = cur.execute(q,(idp,)).fetchone()
    conn.commit()
    conn.close()
    return result

def getAllPost():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts"
    result = cur.execute(q).fetchall()
    conn.commit()
    conn.close()
    return result

# if yelpid not in rest then add to rest

def addRestaurant(cleany, yelpid):
    # cleany is dictionary
    result = None
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT restaurants.yelpid FROM restaurants WHERE restaurants.yelpid = ?"
    result = cur.execute(q,(yelpid,)).fetchone()
    if result == None:
        return
    q = "INSERT INTO restaurants VALUES (?, ?, ?, ?, ?)"
    for i in cleany:
        if cleany['id'] == yelpid:
            cur.execute(q,(i['id'],i['name'],'\n'.join(i['address']),i['rating'],i['phone']))
    conn.commit()
    conn.close()
    
