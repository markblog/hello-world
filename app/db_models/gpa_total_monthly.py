from app.ext import db
from app.mixins.dict import DictMixin


class GPATotalMonthly(DictMixin, db.Model):

    # __tablename__ = 'gpa_dgf_total_level_monthly_publish_1'
    __tablename__ = 'gpa_total_monthly'

    id=db.Column(db.Integer,primary_key=True)
    account_code=db.Column(db.String(64),index=True)
    account_name_long=db.Column(db.String(64),index=True)
    effective_date=db.Column(db.Date,index=True)
    performance_scheme_code=db.Column(db.Integer)
    asset_class=db.Column(db.String(64),nullable=True)
    country=db.Column(db.String(64),nullable=True)
    sector = db.Column(db.String(64),nullable=True)
    industry = db.Column(db.String(64),nullable=True)
    security_name = db.Column(db.String(64),nullable=True)
    security_name_long= db.Column(db.String(64),nullable=True)
    sec_ssc_id= db.Column(db.String(64),nullable=True)
    emv= db.Column(db.Float)
    bmv = db.Column(db.Float)
    abal = db.Column(db.Float)
    abal_zero = db.Column(db.Float)
    abal_mid = db.Column(db.Float)
    abal_full = db.Column(db.Float)
    base_flows = db.Column(db.Float)
    value_add = db.Column(db.Float)
    gain_loss = db.Column(db.Float)
    inc = db.Column(db.Float)
    inflws = db.Column(db.Float)
    otflw_val = db.Column(db.Float)
    net_csh_flw = db.Column(db.Float)
    ror= db.Column(db.Float)
    rates_rule = db.Column(db.Integer,index=True)
    mgr_fees = db.Column(db.Float)
    oth_fees = db.Column(db.Float)
    index_code = db.Column(db.String(64),index=True)
    index_ror = db.Column(db.Float)
    index_short_name = db.Column(db.String(128))
    account_type = db.Column(db.String(64),index=True)
    daily_flag = db.Column(db.String(64),index=True)
    as_of_tms = db.Column(db.DateTime)
    as_at_tms = db.Column(db.Integer)
    p_c_flag = db.Column(db.String(4),index=True)
    country_date = db.Column(db.DateTime)
    day_type=db.Column(db.Integer)
    monthend = db.Column(db.Integer)
    last_business_date = db.Column(db.DateTime)
    next_business_date=db.Column(db.DateTime)
    last_month_end_date=db.Column(db.DateTime)
    next_month_end_date = db.Column(db.DateTime)
    bda_as_at_tms= db.Column(db.DateTime)

    def __repr__(self):
        return '<gpa_total_monthly>'


# class Total_Monthly_Mapping(db.Model):
#     __tablename__='total_monthly_mapping'

#     id=db.Column(db.Integer,primary_key=True)
#     account_code=db.Column(db.String(32),index=True)
#     effective_date=db.Column(db.Date,index=True)
#     fund_tree_name=db.Column(db.String(128),index=True)
#     concat_all=db.Column(db.String(128),index=True)

#     def __repr__(self):
#         return '<total_monthly_mapping>'



