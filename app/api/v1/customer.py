import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator

from app import log
from app.api.common import BaseResource
import json
import datetime
from app.model import Customer
from app.errors import AppError, InvalidParameterError, UserNotExistsError, PasswordNotMatch

LOG = log.get_logger()


FIELDS = {
    'name': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 20
    },
    'dob': {
        'type': 'string',
        'regex': '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}',
        'required': True,
        'maxlength': 320
    },
    'updated_at': {
        'type': 'string',
        'regex': '[0-9a-zA-Z]\w{3,14}',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    }
}


def validate_customer_create(req, res, resource, params):    
    customer_json = json.loads(req.stream.read())
    if customer_json['name'] is None or len(customer_json['name']) <= 0 :
        raise InvalidParameterError('Invalid Request %s' % req.context)
    if customer_json['dob'] is None or len(customer_json['dob']) <= 0 :
        raise InvalidParameterError('Invalid Request %s' % req.context)
class Collection(BaseResource):
    """
    Handle for endpoint: /v1/users
    """
    @falcon.before(validate_customer_create)
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

    # @falcon.before(auth_required)
    def on_put(self, req, res):
        pass


class Item(BaseResource):
    """
    Handle for endpoint: /v1/customers/{user_id}
    """    
    def on_get(self, req, res, user_id):        
        session = req.context['session']
        try:
            customer_db = Customer.find_one(session, user_id)            
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
    """
    Handle for endpoint: /v1/users/youngest
    """
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


class Self(BaseResource):
    """
    Handle for endpoint: /v1/users/self
    """
    LOGIN = 'login'
    RESETPW = 'resetpw'

    def on_get(self, req, res):
        cmd = re.split('\\W+', req.path)[-1:][0]
        if cmd == Self.LOGIN:
            self.process_login(req, res)
        elif cmd == Self.RESETPW:
            self.process_resetpw(req, res)

    def process_login(self, req, res):
        data = req.context['data']
        email = data['email']
        password = data['password']
        session = req.context['session']
        try:
            user_db = User.find_by_email(session, email)
            if verify_password(password, user_db.password.encode('utf-8')):
                self.on_success(res, user_db.to_dict())
            else:
                raise PasswordNotMatch()
        except NoResultFound:
            raise UserNotExistsError('User email: %s' % email)

    # @falcon.before(auth_required)
    def process_resetpw(self, req, res):
        pass