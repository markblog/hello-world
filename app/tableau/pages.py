from .config import t,tran_classification
import numpy as np
import pandas as pd
import datetime
import time
from .util import ROR,Tag,Configuration_Options
from dateutil.relativedelta import relativedelta
from calendar import monthrange


class CalcBasic(object):

    def __init__(self,**kwargs):
        self._parse(**kwargs)

    def _parse(self,*args,**kwargs):
        pass

    def _calculate(self):
        pass

    def _ret(self):
        pass


class Aggregate_Plan_Overview(CalcBasic):
    def _parse(self,source_db,fund_tree=None,strategy=None,account=None,CumulativeOrAnnualized=None,
               MonthlyTotalReturnMethodology=None):
        self.source = source_db
        self.fund_tree = fund_tree
        self.strategy = strategy
        self.accounts = account
        self.annualized = CumulativeOrAnnualized
        self.return_method = Configuration_Options[MonthlyTotalReturnMethodology]

    def _calculate(self):
        _Total_Return = ROR.total_return(self.return_method, self.source) - 1
        _Top_or_Bottom_10_Value_Added = self.bottom_top_value_added()
        _Portfolios_by_Strategy = self.PortfolioByStrategy()
        return _Total_Return, _Top_or_Bottom_10_Value_Added, _Portfolios_by_Strategy

    def _ret(self):
        pass

    @staticmethod
    def get_last_emv(arr):
        return arr.iat[-1]

    @staticmethod
    def get_first_bmv(arr):
        return arr.iat[0]

    def PortfolioByStrategy(self):

        def get_last_emv(arr):
            return arr.iat[-1]

        def get_first_bmv(arr):
            return arr.iat[0]

        source=self.source.loc[:,[t.account,t.effective_date,t.emv,t.bmv,t.net_csh_flw,t.value_add,t.ror]]
        source_g=source.groupby(t.account).agg({t.emv:get_last_emv,t.bmv:get_first_bmv,t.net_csh_flw:sum,t.value_add:sum,t.ror:ROR.ror_cum})
        source_g=source_g.reset_index(drop=False)
        return source_g

    def bottom_top_value_added(self):
        source=self.source.loc[:,[t.account,t.value_add]]
        source_grouped=source.groupby(t.account).agg(sum)
        source_grouped_sort=source_grouped.sort_values(by=t.value_add)#ascending=True
        source_grouped_sort=source_grouped_sort.reset_index()
        bottom,top=source_grouped_sort.head(10),source_grouped_sort.tail(10)
        return bottom,top

    @staticmethod
    def TotalEndingMarketValue(source_db):
        source = source_db
        last_date = source[t.effective_date].iat[-1]
        source = source[source[t.effective_date] == last_date]
        return source[t.emv].sum()


class PointToPoint(CalcBasic):
    def _parse(self,source_db,account=None,date_type=None,range_start=None,end_date=None,
               period=None,return_type=None,CumulativeOrAnnualized=None):
        self.source=source_db
        self.accounts=account
        self.date_type=date_type
        self.range_start=range_start
        self.end_date=end_date
        self.period=period
        self.return_type=return_type
        self.annualized=CumulativeOrAnnualized#True if annualized, False if cumulative.

    def _calculate(self):
        source = self.source
        res = {}
        ###delete the following lines when fetch data from database(assume: data in database has been pretreatment)
        if source[t.ror].min() > -99.0:
            pass
        else:
            source[t.ror] = np.where(source[t.ror] > -99.0, source[t.ror], -99.0)
        ###
        for account in self.accounts:
            source_account = source[source[t.account] == account]
            source_account = source_account.reset_index(drop=True)
            ror = source_account[t.ror]
            returns_cum_ann = ROR.ror_cum_ann(source_account, self.annualized)
            res[account] = [list(ror), list(returns_cum_ann.iloc[:, 0]), list(returns_cum_ann.iloc[:, 1])]
        return res

    def _ret(self):
        pass
    

class GrowthOfUnit(CalcBasic):
    def _parse(self, total_level_mon, fund_tree=None, strategy=None, account=None, end_date=None, period=None, 
                starting_value=None, return_type=None, CumulativeOrAnnualized=None):
        # Note:need to deal with source_db or front_parameters if empty
        self.source = total_level_mon
        self.accounts = account
        print(type(starting_value))
        self.starting_value = int(starting_value)
        self.annualized = False

    # def _calculate(self,accounts,starting_value,annualized=False):
    def _calculate(self):
        """The output is a dictionary->res.
               res['account_vs_benchmark']['xAxis'] is col of accounts name(ex. US EQUITY FUND(DEMOXY16)).
               res['account_vs_benchmark']['series'] if 4 cols, 1th is account's growth amount,
                                                                2th is bench's growth amount,
                                                                3th is account's return,
                                                                4th is bench's return.
        """
        source = self.source
        res = {}
        l_cols = [[], [], [], []]
        r_lines = {}
        dateline=None
        ###delete the below code when fetch data from database(assume: data in database has been pretreatment)
        if source[t.ror].min() > -99.0:
            pass
        else:
            source[t.ror] = np.where(
                source[t.ror] > -99.0, source[t.ror], -99.0)
        ###
        for account in self.accounts:
            source_account = source[source[t.account] == account]
            source_account = source_account.reset_index(drop=True)
            dateline=source_account[t.effective_date]
            ror=source_account[t.ror]/100
            returns_cum = ROR.ror_cum_ann(source_account, self.annualized)
            # double_return_cum=round(double_return_cum,2)+1
            returns_cum = returns_cum + 1
            growth_amounts = returns_cum * self.starting_value
            returns_cum, growth_amounts = round(returns_cum - 1, 4), \
                                          round(growth_amounts, 2)
            l_cols[0].append(growth_amounts.iloc[-1, 0])#account growth amount
            l_cols[1].append(growth_amounts.iloc[-1, 1])#bench growth amount
            l_cols[2].append(returns_cum.iloc[-1, 0])#account return
            l_cols[3].append(returns_cum.iloc[-1, 1])#bench return
            r_lines[account] = [list(returns_cum.iloc[:,0]), list(growth_amounts.iloc[:, 0]),#list(returns_cum.iloc[:, 0])
                                list(growth_amounts.iloc[:, 1])]#account return, account growth amount, bench growth amount
        res['account_vs_benchmark'] = {'xAxis': self.accounts,
                                       'series': l_cols}
        res['growth_of_unit'] = {'xAxis': list(dateline),
                                 'series': r_lines}
        return res
        # ret_dict = self._ret(accounts, starting_value, source, annualized)
        # return ret_dict

    def _ret(self, accounts, starting_value, source, annualized):
        l = {}
        l['form'] = {}
        d = time.strptime("2017-11-30", "%Y-%m-%d")

        l['form']['returnType'] = []
        l['form']['cumulative'] = []
        l['form']['fundTree'] = [{"value": v, "id": k + 1} for k, v in enumerate(Tag.FUNDTREE.value)]
        l['form']['strategy'] = [{"value": v, "id": k + 1} for k, v in enumerate(Tag.STRATEGY.value)]
        l['form']['account'] = [{"value": v, "id": k + 1} for k, v in enumerate(Tag.ACCOUNTCODE.value)]
        l['form']['period'] = [{"value": v, "id": k + 1}
                               for k, v in enumerate(Tag.PERIOD.value)]
        l['form']['returnType'] = [{"value": v, "id": k + 1} for k, v in enumerate(Tag.RETURNTYPE.value)]
        l['form']['cumulative'] = [{"value": v, "id": k + 1}
                                   for k, v in enumerate(Tag.CumulativeOrAnnualized.value)]

        l['form']['endDate'] = datetime.timedelta(d.tm_year, d.tm_mon, d.tm_mday).total_seconds()

        l['form']['startingValue'] = starting_value

        l['leftChart'] = {}
        l['rightChart'] = {}
        l['rightChart']['id'] = 2
        l['rightChart']['title'] = 'Growth of ' + str(starting_value)
        for account in accounts:
            source_account = source[source[t.account] == account]
            source_account = source_account.reset_index(drop=True)
            source_account_cum = ROR.ror_cum_ann(source_account, annualized)
            source_account_cum = round(source_account_cum, 2) + 1
            source_account_amount = source_account_cum * starting_value  # growth amount
            source_account_amount = round(source_account_amount, 2)
            l['rightChart']['Series'] = []
            l['rightChart']['Series'].append(
                dict(name=account, data=list(source_account_amount.iloc[:, 0])))
        return l


class ManagerFee(CalcBasic):
    def _parse(self,source_db,account=None,relation_strategy_account=None):
        self.source=source_db
        self.accounts=account
        self.relation=relation_strategy_account#relations tell how many accounts in each strategy

    def _calculate(self):
        source = self.source.loc[:,
                 [t.account, t.index_code, t.effective_date, t.return_type, t.emv, t.mgr_fees, t.ror, t.index_ror]]
        _emv_and_fee_divide_active_gross = {'Account_Nm': [], 'EMV': [], 'Fee/Active_Gross': []}
        _watchlist = {'Account_Nm': [], 'EMV': [], 'Fee_Ratio': [], 'Active_Gross': []}
        _active_return_and_bps_by_account_or_strategy = []
        _table = {'Account': [], 'Ending_market_Value': [], 'Manager_Expenses': [], 'Fund_Return': [],
                  'Bench_Return': [], 'Active_Return': [], 'BPS': []}

        for account in self.accounts:
            source_account = source[source[t.account] == account]
            source_account_1 = source_account[source_account[t.return_type] == 1]
            source_account_10 = source_account[source_account[t.return_type] == 10]
            source_account_1 = source_account_1.reset_index(drop=True)
            source_account_10 = source_account_10.reset_index(drop=True)
            begin, end = source_account_1[t.effective_date].iat[0], source_account_1[t.effective_date].iat[-1]
            _EMV = np.sum(source_account_1[source_account_1[t.effective_date] == end][t.emv])
            _Manager_Expenses = np.sum(source_account_1[t.mgr_fees])

            _Account_period_ror_10, _Bench_period_ror = self.period_ror(source_account_10, t.ror), self.period_ror(
                source_account_1, t.index_ror)
            _Active_ror = _Account_period_ror_10 - _Bench_period_ror
            _Account_period_ror_1 = self.period_ror(source_account_1, t.ror)
            _BPS = (_Account_period_ror_1 - _Account_period_ror_10) * 10000
            _Active_gross = _Active_ror * 100 + _BPS / 100
            _Fee_divide_Active_gross = (_BPS / 100) / _Active_gross if _Active_ror > 0 else 1
            # format calc
            # graph of EMV&Fee/Active Gross
            _emv_and_fee_divide_active_gross['Account_Nm'].append(account)
            _emv_and_fee_divide_active_gross['EMV'].append(_EMV)
            _emv_and_fee_divide_active_gross['Fee/Active_Gross'].append(_Fee_divide_Active_gross)
            # graph of Watchlist
            _watchlist['Account_Nm'].append(account)
            _watchlist['EMV'].append(_EMV)
            # graph of Active Return & BPS by Account/Strategy
            # _active_return_and_bps_by_account_or_strategy.append({'Account_Nm':account,'Strategy':...})#TODO
            # graph of Table
            _table['Account'].append(account)
            _table['Ending_market_Value'].append(_EMV)
            _table['Fund_Return'].append(_Account_period_ror_10)
            _table['Bench_Return'].append(_Bench_period_ror)
            _table['Active_Return'].append(_Active_ror)
            _table['BPS'].append(_BPS)
        return _emv_and_fee_divide_active_gross, _watchlist, _table

    def _ret(self):
        pass

    def period_ror(self,source, col):  # source is full column filter by account by rates_rule
        ###delete following if data from database
        if source[col].min() > -99:
            source[col] = source[col]
        else:
            source[col] = np.where(source[col] > -99, source[col], -99)
        ###
        return np.prod(source[col] / 100 + 1) - 1


class CountryAnalysis(CalcBasic):
    def _parse(self,*args,**kwargs):
        pass

    def _calculate(self):
        pass

    def _ret(self):
        pass

    def country_map(self):
        pass

    def period_return(self):
        pass

    def top_5_holdings(self):
        pass

    def total_return(self):
        pass

    def total_ending_maket_value(self):
        pass


class FlowsByClassification(CalcBasic):
    def _parse(self,source_db,account=None,ClassificationOfFlows=None,MonthlySecurityReturnMethodology=None):
        self.source=source_db
        self.accounts=account
        self.classification_flows=tran_classification[ClassificationOfFlows]
        self.return_method=Configuration_Options[MonthlySecurityReturnMethodology]

    def _calculate(self):
        # get the left picture
        def total_monthly_net_cash_flows(source):
            source = source.loc[:, [t.effective_date, t.net_csh_flw]]
            source_grouped = source.groupby(t.effective_date).agg(sum)
            source_grouped = source_grouped.reset_index(drop=False)
            return source_grouped

        left = total_monthly_net_cash_flows(self.source)

        def flows_by_classification_by_manager(source,classificaiton):
            # without account_code
            source1 = source.loc[:, [t.effective_date, classificaiton, t.net_csh_flw]]
            source1 = source1.rename(columns={t.net_csh_flw: 'total_net_csh_flw'})
            source1_g = source1.groupby([t.effective_date, classificaiton]).agg(sum)
            source1_g = source1_g.reset_index(drop=False)
            # with account_code
            source2 = source.loc[:, [t.effective_date, classificaiton, t.net_csh_flw, t.account]]
            source2_g = source2.groupby([t.effective_date, classificaiton, t.account]).agg(sum)
            source2_g = source2_g.reset_index(drop=False)
            source_m = pd.merge(source2_g, source1_g, on=[t.effective_date, classificaiton], how='left')
            return source_m

        right=flows_by_classification_by_manager(self.source,self.classification_flows)

        def flows_by_manager_by_sec_id(source,ror_method):
            source = source.loc[:,[t.account, t.effective_date, t.sec_ssc_id, t.emv, t.bmv, t.net_csh_flw, t.value_add, ror_method]]
            source[t.period_return] = source[t.value_add] / source[ror_method] + 1
            source = source.loc[:,[t.account, t.effective_date, t.sec_ssc_id, t.emv, t.bmv, t.net_csh_flw, t.period_return]]
            source_g = source.groupby([t.account, t.sec_ssc_id])
            source_g = source_g.agg({t.emv: Aggregate_Plan_Overview.get_last_emv, t.net_csh_flw: sum,
                                     t.bmv: Aggregate_Plan_Overview.get_first_bmv, t.period_return: np.prod})
            source_g = source_g.reset_index(drop=False)
            source_g[t.period_return] = source_g[t.period_return] - 1
            source_g[t.period_return] = np.where(source_g[t.period_return] < -0.99, -0.99, source_g[t.period_return])
            return source_g

        third=flows_by_manager_by_sec_id(self.source,self.return_method)

        return left,right,third

    def _ret(self):
        pass


class PerformanceByClassification(CalcBasic):
    def _parse(self,source_db,level1=None,level2=None,level3=None,MonthlySecurityReturnMethodology=None):
        self.source=source_db
        self.level1=level1
        self.level2=level2
        self.level3=level3
        self.return_method=Configuration_Options(MonthlySecurityReturnMethodology)

    def _calculate(self):
        _Total_Return = ROR.total_return(self.return_method, self.source) - 1
        _Total_Ending_Market_Value = Aggregate_Plan_Overview.TotalEndingMarketValue(self.source)

    def _ret(self):
        pass


class ContributionToReturn(CalcBasic):
    def _parse(self,*args,**kwargs):
        pass

    def _calculate(self):
        pass

    def _ret(self):
        pass
