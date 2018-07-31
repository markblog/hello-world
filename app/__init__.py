import logging, pickle, random, copy
from flask import Flask
from config import config
from .ext import db, Api
from flask_sqlalchemy import SQLAlchemy
from app.api_v1 import user_resources as UserResources
from app.api_v1 import tableau_resources as TableauResources
from app.ext import mc
import os
from flask_debugtoolbar import DebugToolbarExtension
from app.charts import Myview




def create_app(config_name):
    app = Flask(__name__)

    # app.register_blueprint(bp)
    app.add_url_rule("/chart/", view_func=Myview.as_view("userview"))
    # the toolbar is only enabled in debug mode:
    app.debug = True

    # set a 'SECRET_KEY' to enable the Flask session cookies
    app.config['SECRET_KEY'] = '<replace with a secret key>'

    toolbar = DebugToolbarExtension(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.app = app
    db.init_app(app)
    app_logging_configure(app)
    register_api(app)
    return app

def app_logging_configure(app):
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def register_api(app):
    
    api = Api(app = app, prefix = '/api/v1')
    
    api.add_resource(TableauResources.TableauGrowthOfUnitResource, '/tableau/grow-of-unit/')
    api.add_resource(TableauResources.ManagerFeeResource, '/tableau/manager-fee')
    api.add_resource(TableauResources.CountryAnalysisResource, '/tableau/country-analysis')
    api.add_resource(TableauResources.PointToPointResource, '/tableau/point-to-point')
    api.add_resource(TableauResources.AggregatePlanOverviewResource, '/tableau/aggregate-plan-overview')
    api.add_resource(TableauResources.FlowByClassificationResource, '/tableau/flows-by-classification')
    api.add_resource(TableauResources.PerformanceByClassificationResource, '/tableau/performance-by-classification')
    api.add_resource(TableauResources.ContributionTOReturnResource, '/tableau/contribution-to-return')



