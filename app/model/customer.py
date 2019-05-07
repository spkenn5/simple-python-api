from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from app.model import Base
import datetime

class Customer(Base):
    __tablename__ = 'customer'
    id      = Column(Integer, primary_key=True)
    name    = Column(String(50))
    dob     = Column(Date)    
    updated_at     = Column(Date)

    def __repr__(self):
        return "<Customer(id='%d', name='%s', dob='%s', updated_at='%s')>" % \
            (self.id, self.name, self.dob.strftime("%B %d, %Y"), self.updated_at.strftime("%B %d, %Y"))

    @classmethod
    def get_id(cls):
        return Customer.id

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(Customer).filter(Customer.id == id).one()

    @classmethod
    def find_youngest(cls, session):
        return session.query(Customer).order_by(desc(Customer.dob)).one()

    FIELDS = {
        'id': str,
        'name': str,
        'dob': str,
    }

    FIELDS.update(Base.FIELDS)