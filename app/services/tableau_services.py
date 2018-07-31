from flask import g
from app.tableau.pages import GrowthOfUnit
import numpy as np
import pandas as pd
import time
from pandas import DataFrame
from sqlalchemy import create_engine
from app.utils.time_utils import datetime_to_timestamp,int_to_timestamp
import datetime
from app.ext import engine, db
from sqlalchemy.sql import text
from app.db_models.gpa_total_monthly import GPATotalMonthly
from app.sqls.tableau_sqls import growth_of_unit_sql


def get_growthOfunit(**kwargs):
    account = kwargs.get("account")
    rates_rules = kwargs.get("return_type")
    end_date = kwargs.get("end_date")
    starting_value = kwargs.get("starting_value")
    account_list = tuple(account.lstrip("[").rstrip("]").split(","))
    
    gpa =pd.read_sql(GPATotalMonthly.query.from_statement(text(
        growth_of_unit_sql)).params(account_codes=account_list, rates_rules=rates_rules, start=('2014-11-30'), end=end_date).statement, db.session.bind)

    growthOfunit = GrowthOfUnit(total_level_mon=gpa, account=list(
        account_list), starting_value=starting_value)
    gc = growthOfunit._calculate()

    formatdate = []
    for date in gc['growth_of_unit']['xAxis']:
        if isinstance(date, datetime.date):
            date = datetime_to_timestamp(date)
            date = int_to_timestamp(date)
            formatdate.append(date)
    gc['growth_of_unit']['xAxis'] = formatdate
    
    return gc


def get_managerfee(**kwargs):
    pass


def get_countryanalysis(**kwargs):
    pass


def get_pointtopoint(**kwargs):
    pass


def get_aggregateplanoverview(**kwargs):
    pass


def get_flowbyclassification(**kwargs):
    pass


def get_performancebyclassification(**kwargs):
    pass


def get_contributiontoreturn(**kwargs):
    pass
