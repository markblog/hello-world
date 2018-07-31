from app.utils.patch import BasicResource
from flask import request, g
from app.ext import db, redis_db
from app.utils.decorators import auth
from app.services import user_services
from app.services import  tableau_services
from flask import current_app
import collections
# http: // 172.16.63.145: 5001/api/v1/tableau/grow-of-unit /?account = [DEMOXYZ6, DEMOXYZ8, DEMOXYZ9] & return_type = 1 & starting_value = 1000
# http get localhost:5001/api/v1/tableau/grow-of-unit/ account==[DEMOXYZ6,DEMOXYZ8,DEMOXYZ9] return_type==1 starting_value==10000
# http: // localhost: 5001/api/v1/tableau/grow-of-unit /?account = [DEMOXYZ6, DEMOXYZ8, DEMOXYZ9] & return_type = 1 & starting_value = 1000
class TableauGrowthOfUnitResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_growthOfunit(**g.my_dict)
        print(ggu['growth_of_unit']['xAxis'])
        return ggu


class ManagerFeeResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_managerfee(**g.my_dict)
        return ggu

class CountryAnalysisResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_countryanalysis(**g.my_dict)
        return ggu


class PointToPointResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_pointtopoint(**g.my_dict)
        return ggu


class AggregatePlanOverviewResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_aggregateplanoverview(**g.my_dict)
        return ggu

class FlowByClassificationResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_flowbyclassification(**g.my_dict)
        return ggu


class PerformanceByClassificationResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_performancebyclassification(**g.my_dict)
        return ggu


class ContributionTOReturnResource(BasicResource):

    def get(self):
        ggu = tableau_services.get_contributiontoreturn(**g.my_dict)
        return ggu
