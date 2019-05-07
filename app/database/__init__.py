from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from app import log
from app import config

LOG = log.get_logger()


def get_engine(uri):
    LOG.info('Connecting to database..')    
    return create_engine(uri)

db_session = scoped_session(sessionmaker())
engine = get_engine(config.DATABASE_URL)

def init_session():    
    db_session.configure(bind=engine)

    from app.model import Base
    Base.metadata.create_all(engine)