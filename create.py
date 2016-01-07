import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

q = "drop table users"
c.execute(q)
q = "drop table posts"
c.execute(q)
q = "drop table comments"
c.execute(q)

q = "create table users(id integer, name text, password text)"
c.execute(q)

q = "create table posts(id integer, info text, file text, likes integer, datething, uid integer)"
c.execute(q)

q = "create table comments(id integer, content text, pid integer, uid integer)"
c.execute(q)

q = "create table restaurants(id integer, name text, location text)"
c.execute(q)

conn.commit()

