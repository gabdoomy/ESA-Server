import logging
from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder
from flask.ext.appbuilder.security.manager import BaseSecurityManager
import urllib, hashlib
import sqlite3
from flask import g, abort, redirect, url_for, request
from werkzeug.security import check_password_hash, generate_password_hash

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
 
default = "https://lh4.googleusercontent.com/-9AWNcPu8Hjo/AAAAAAAAAAI/AAAAAAAALBQ/OI4aDuBHnag/s100-c-k-no/photo.jpg"
size = 100

DATABASE = '/root/esa/app.db'

def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/listusers')
def listusers():
    response='';
    for user in query_db('select * from ab_user'):
        response+=user[1].encode("utf-8")+" - "+user[2].encode("utf-8")+" - "+user[3].encode("utf-8")+" - "+user[4].encode("utf-8")+" - "+user[6].encode("utf-8")+'<br>'
    return response+"<br>Finish"

@app.route('/adduser')
def insert():
    db=get_db();
    db.execute('insert into ab_user (first_name, last_name, username, password, email) values (?, ?, ?, ?, ?)', ['alextest','alextest','username',generate_password_hash('password'),'emailtest'])
    db.commit()
    return redirect('/listusers')

@app.route('/checkpass')
def checkpass():
    user = request.args.get("username")
    passwordcheck = request.args.get("password")
    passvar=''
    for user in query_db('select * from ab_user where username=?',[user]):
        if check_password_hash(user[4].encode("utf-8"), passwordcheck) == True:
            return 'True'
        else:
            return 'False'
    return 'False'

@app.route('/profilepic/<email>')
def profilepic(email):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return '<img src="'+gravatar_url+'\" />'

appbuilder = AppBuilder(app, db.session)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    

from app import views

