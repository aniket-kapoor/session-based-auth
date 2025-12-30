from . import database
from sqlalchemy import Column, String, Integer,Boolean
from sqlalchemy import ForeignKey 
from sqlalchemy import DateTime
from datetime import datetime, timezone


class Users(database.Base):

    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    email=Column(String , index=True, unique=True ,nullable=False)
    hashed_password=Column(String, nullable=False)
    is_active=Column(Boolean, default=True , nullable=False) 

class Session(database.Base):
    __tablename__='sessions'

    id=Column(Integer, primary_key=True, index=True)
    session_id=Column(String, unique=True )
    user_id=Column(Integer, ForeignKey('users.id') )

    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
   

    


    


