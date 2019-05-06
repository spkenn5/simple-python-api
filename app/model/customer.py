from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from app.model import Base

import datetime

DB_URI = "postgres://postgres:postgres@localhost:5432/simple_python_api"

engine = create_engine(DB_URI)
base = declarative_base()

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


# if __name__ == "__main__":
#     import datetime
#     from sqlalchemy import create_engine    

#     Session = sessionmaker(engine)  
#     session = Session()

#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)

#     # Create 
#     d1 = datetime.datetime.strptime("25-12-1973", "%d-%m-%Y").date()
#     d2 = datetime.datetime.strptime("31-10-1988", "%d-%m-%Y").date()
#     d3 = datetime.datetime.strptime("09-08-1965", "%d-%m-%Y").date()
#     d4 = datetime.datetime.strptime("01-04-1945", "%d-%m-%Y").date()

#     print('Creating records', datetime.datetime.now().date())
#     user1 = Customer(name="Tony Stark", dob=d1, updated_at=datetime.datetime.now().date())
#     user2 = Customer(name="Stephen Strange", dob=d2, updated_at=datetime.datetime.now().date())
#     user3 = Customer(name="Bruce Banner", dob=d3, updated_at=datetime.datetime.now().date())
#     user4 = Customer(name="Steve Rogers", dob=d4, updated_at=datetime.datetime.now().date())
#     session.add(user1)
#     session.add(user2)
#     session.add(user3)
#     session.add(user4)
#     session.commit()

#     # Read
#     films = session.query(Customer)
#     for film in films:  
#         print(film.name)