from flask import Flask
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event, DateTime
from sqlalchemy.exc import IntegrityError, OperationalError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Message(db.Model):
    __tablename__ = 'messages'
    serverID = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, primary_key=True, default = datetime.datetime.utcnow)
    message = db.Column(db.String, nullable = False)
    user = db.Column(db.String, nullable = False)


class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable = False)
