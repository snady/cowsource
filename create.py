 import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

"""
q = "drop table users"
c.execute(q)
q = "drop table posts"
c.execute(q)
q = "drop table comments"
c.execute(q)
"""

q = "create table users(id integer, name text, password text, email text)"
c.execute(q)

q = "create table posts(id integer, jasondata text, file text, time timestamp default current_timestamp, uid integer, yelpid text)"
c.execute(q)

q = "create table comments(id integer, content text, pid integer, uid integer)"
c.execute(q)

q = "create table restaurants(yelpid text, name text, location text, rating text, phone text)"
c.execute(q)

conn.commit()

'''
jasonSS
name
description
price
likes
tags
'''

