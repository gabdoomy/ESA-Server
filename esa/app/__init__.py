import logging
from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder
from flask.ext.appbuilder.security.manager import BaseSecurityManager
"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)

@app.route('/hello')
def hello_world():
    BaseSecurityManager.add_user(username = "username", first_name="first_name", last_name="last_name", email="email@email.com", role="Admin", password='password1234')
    return 'Hello World!'

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

