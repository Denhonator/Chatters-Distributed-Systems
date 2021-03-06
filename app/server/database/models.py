from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy import exc
from datetime import datetime
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "chatters_database.db")

Base = declarative_base()
engine = create_engine('sqlite:///'+ db_path)
session = scoped_session(sessionmaker(bind=engine))

class Message(Base):
    __tablename__ = 'messages'
    serverID = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True, default = datetime.utcnow)
    message = Column(String, nullable = False)
    user = Column(String, nullable = False)

    def __init__(self, serverID, message, user):
        self.serverID = serverID
        self.message = message
        self.user = user


class Server(Base):
    __tablename__ = 'servers'
    id = Column(String, primary_key=True)
    address = Column(String, nullable = False)

    def __init__(self, id, address):
        self.id = id
        self.address = address

def get_messages():
    try:
        messages = session.query(Message).all()
        return messages
    except Exception as e:
        print(e)
        print("couldn't get messages")

def get_servers():
    try:
        servers = session.query(Server).all()
        return servers
    except Exception as e:
        print(e)
        print("couldn't get servers")

def save_new_message(sID, mes, usr, ts=None):
    try:
        new_message = Message(serverID=sID, message=mes, user=usr)
        if ts:
            print(ts)
            new_message.timestamp = datetime.strptime(ts,'%Y-%m-%d %H:%M:%S.%f' )
        session.add(new_message)
        session.commit()
    except exc.IntegrityError as e:
        pass
    except Exception as e:
        print(e)
    finally:
        session.close()

def save_server(serverID, addr):
    try:
        new_server = Server(id = serverID, address = addr)
        session.add(new_server)
        session.commit()
    except exc.IntegrityError as e:
        pass
    except Exception as e:
        print(e)
