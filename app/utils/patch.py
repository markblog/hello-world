from flask_restful import Resource
from .decorators import parse_paremeters_and_modified_response
from functools import wraps
from flask import g
from flask_restful import reqparse


def parse_query_string(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('fund_tree', type = str, default = None)
        parser.add_argument('strategy', type = str, default = None)
        parser.add_argument('account',  type=str, default="[DEMOXYZ6,DEMOXYZ8,DEMOXYZ9]")
        parser.add_argument('end_date', type=str, default=('2017-11-30'))
        parser.add_argument('period', type=str, default=None)
        parser.add_argument('starting_value', type=str, default='1000')
        parser.add_argument('return_type', type=str, default='1')
        parser.add_argument('CumulativeOrAnnualized', type=str, default=None)
        g.my_dict = parser.parse_args()
        print(g.my_dict)
        return func(*args, **kwargs)
    return wrapper

class BasicResource(Resource):
    method_decorators = [parse_query_string]
    # method_decorators = [parse_paremeters_and_modified_response, parse_query_string]

