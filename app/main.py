import falcon
from app.controller.timestamp import Timestamp
from app.controller.session_manager import DatabaseSessionManager
from app.api.common import base
from app.api.v1 import customer
from app.errors import AppError
from app import log
from app.database import db_session, init_session

from falcon_autocrud.middleware import Middleware
LOG = log.get_logger()

class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('API Server is starting')
        self.add_route('/', base.BaseResource())
        self.add_route('/timestamp', Timestamp())
        self.add_route('/api/v1/customers', customer.Collection())        
        self.add_route('/api/v1/customers/{user_id}', customer.Item())
        self.add_route('/api/v1/youngest/customer', customer.FindYoungest())
        self.add_error_handler(AppError, AppError.handle)

init_session()
middleware = [DatabaseSessionManager(db_session)]
application = App(middleware=middleware)

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 5000, application)
    httpd.serve_forever()