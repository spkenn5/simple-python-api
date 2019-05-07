import json
import time
import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta


def new_alchemy_encoder():    
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):                
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)                
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    fields[field] = obj.__getattribute__(field)                
                return fields

            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder


def passby(data):
    return data


def datetime_to_timestamp(date):
    if isinstance(date, datetime.date):
        return int(time.mktime(date.timetuple()))
    else:
        return None

def datetime_to_string(date):
    if isinstance(date, datetime.date):
        return date.strftime("%d-%m-%Y")
    else:
        return None