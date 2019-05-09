import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from app import log
from app.api.common import BaseResource
import json
import datetime
from app.model import Customer
from app.errors import AppError, InvalidParameterError, UserNotExistsError

LOG = log.get_logger()

class Collection(BaseResource):
    def on_post(self, req, res):        
        session = req.context['session']
        customer_json = json.loads(req.stream.read())
        if customer_json:
            customer = Customer()
            customer.name = customer_json['name']
            customer.dob = customer_json['dob']
            customer.updated_at = datetime.datetime.now()
            session.add(customer)
            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])
    
    def on_get(self, req, res):
        session = req.context['session']
        customer_dbs = session.query(Customer).all()
        if customer_dbs:
            obj = [user.to_dict() for user in customer_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

class Item(BaseResource):
    def on_get(self, req, res, user_id):        
        session = req.context['session']
        try:
            customer_db = Customer.find_one(session, user_id)            
            self.on_success(res, customer_db.to_dict())
        except NoResultFound:
            raise UserNotExistsError('customer id: %s' % user_id)
    def on_put(self, req, res, user_id):
        session = req.context['session']
        try:
            customer_json = json.loads(req.stream.read())
            customer_db = Customer.find_one(session, user_id)
            if customer_db:
                customer_db.name = customer_json['name']
                customer_db.dob = customer_json['dob']
                customer_db.updated_at = datetime.datetime.now()
                session.add(customer_db)
                self.on_success(res, customer_db.to_dict())
        except NoResultFound:
            raise UserNotExistsError('customer id: %s' % user_id)        
    def on_delete(self, req, res, user_id):
        session = req.context['session']
        try:
            customer_db = Customer.find_one(session, user_id)
            session.delete(customer_db)
            self.on_success(res, customer_db.to_dict())
        except NoResultFound:
            raise UserNotExistsError('customer id: %s' % user_id)

class FindYoungest(BaseResource):
    def on_get(self, req, res):
        session = req.context['session']
        try:
            customer_dbs = session.query(Customer).order_by(Customer.dob.desc()).first()            
            if customer_dbs:
                self.on_success(res, customer_dbs.to_dict())                
            else:
                raise AppError()
        except NoResultFound:
            raise UserNotExistsError('Unable to find costumer')