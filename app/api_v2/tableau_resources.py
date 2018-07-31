# from flask_restful import Resource
from app.utils.patch import BasicResource
from flask import request, g

from app.ext import db, redis_db
from app.utils.decorators import auth
from app.services import user_services
from app.services import  tableau_services


class TableauResource(BasicResource):
    """docstring for UserResource"""

    # def post(self):
    #
    #     print(g.args)
    #
    #     r = tableau_services.get_tableau_dashboard()
    #
    #     return r
    #     # invoke the function
    #
    def get(self):
        # return "connect successfully"
        return tableau_services.get_growth_of_unit()

