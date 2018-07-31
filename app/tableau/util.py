import numpy as np
import pandas as pd
from .config import t
from enum import Enum

Configuration_Options = {'Beginning of Month': t.abal_full,
                         'Mid Month': t.abal_mid,
                         'End of Month': t.abal_zero,
                         'Inflows': t.inflws,
                         'Modified Dietz': t.abal}


class ROR:
    @staticmethod
    def ror_cum(arr):
        arr = (arr/100.0).add(1).prod()-1
        return arr

    @staticmethod
    def ror_ann(arr):
        pass

    @staticmethod
    def return_flows_by_classification(df_g,ror_method):
        return (df_g[t.value_add]/df_g[ror_method]).add(1).prod()-1

    @staticmethod
    def total_return(methodology: str, source: pd.DataFrame)->float:#methodology is ``abal,abal_zero...``
        denominator = methodology
        source = source.loc[:, [t.effective_date, denominator, t.value_add]]
        grouped = source.groupby(t.effective_date).agg(sum)#sort=False
        ror_monthly = grouped.loc[:, t.value_add] / grouped.loc[:, denominator]
        #ror_monthly=ror_monthly.fillna(0)
        #ror_monthly=ror_monthly.replace([np.inf,-np.inf,np.nan],0)
        if ror_monthly.min() < -0.99:
            ror_monthly = np.where(ror_monthly < -0.99, -0.99, ror_monthly)
        ror_monthly += 1.0
        total_ror = ror_monthly.prod()#-1
        return total_ror

    @staticmethod
    def ror_cum_ann(source_account, annualized):
        # column of effective_date
        effed_col = source_account.loc[:, t.effective_date]
        source_account = source_account.loc[:, [t.ror, t.index_ror]]
        source_account_cum = (source_account / 100).add(1).cumprod()
        if len(source_account[t.ror]) <= 12:
            pass
        else:
            if annualized:
                piece_top = source_account_cum.loc[0:11, :]
                effed_col = (effed_col.sub(
                    effed_col.iat[0]))/np.timedelta64(1, 'D')
                power = (365.25/effed_col)[12:]
                source_account_cum = np.power(source_account_cum.loc[12:, :],pd.DataFrame(power))
                piece_bottom = source_account_cum
                source_account_cum = piece_top.append(piece_bottom)
        source_account_cum = source_account_cum - 1
        return source_account_cum


MappingAccountBenchmark = {'DEMOA': 'EQUITY MARKET NEUTRAL FUND',
                           'DEMOAG1': 'TOTAL PORTFOLIO',
                           'DEMOAG11': 'TOTAL SHORT TERM',
                           'DEMOAG12': 'TOTAL REAL ESTATE',
                           'DEMOAG13': 'TOTAL PRIVATE EQUITY',
                           'DEMOAG2': 'US EQUITY',
                           'DEMOAG3': 'INTERNATIONAL EQUITY',
                           'DEMOAG4': 'FIXED INCOME',
                           'DEMOAG5': 'FIXED INCOME',
                           'DEMOAG7': 'TOTAL INVESTMENTS - DC',
                           'DEMOAG8': 'INVESTMENT OPTIONS AGGREGATE',
                           'DEMOAG9': 'TOTAL HEDGE FUNDS',
                           'DEMOB': 'CREDIT ARBITRAGE MANAGER',
                           'DEMOXY11': 'SHORT TERM',
                           'DEMOXY12': 'US TREASURIES',
                           'DEMOXY13': 'LARGE CAP - PASSIVE',
                           'DEMOXY14': 'GLOBAL INFLATION LINKED',
                           'DEMOXY15': 'INFRASTRUCTURE',
                           'DEMOXY16': 'US EQUITY FUND',
                           'DEMOXY17': 'INTL EQUITY FUND',
                           'DEMOXY20': '2040 FUND',
                           'DEMOXY21': '2030 FUND',
                           'DEMOXY22': '2020 FUND',
                           'DEMOXY6J': 'BANK LOAN',
                           'DEMOXYZ1': 'SMALL/MIDCAP ACTIVE',
                           'DEMOXYZ2': 'CORE PLUS',
                           'DEMOXYZ3': 'HIGH YIELD',
                           'DEMOXYZ4': 'PRIVATE EQUITY',
                           'DEMOXYZ5': 'REAL ESTATE',
                           'DEMOXYZ6': 'INTL DEVELOPED PASSIVE',
                           'DEMOXYZ7': 'LARGE CAP GROWTH - ACTIVE',
                           'DEMOXYZ8': 'SMALL CAP - PASSIVE',
                           'DEMOXYZ9': 'INTL EMERGING - ACTIVE'}

class Tag(Enum):
    FUNDTREE = ['BG TREE',
                'DC - INVESTMENT FUNDS',
                'DC - PARTICIPANT FUNDS',
                'MONTHLY PLAN ATTRIBUTION',
                'TOTAL PLAN',
                'TOTAL PLAN W/ HF'
                ]
    STRATEGY = ['INVESTMENT OPTIONS AGGREGATE',
                'TOTAL INVESTMENTS - DC',
                'TOTAL INVESTMENTS - DC / FIXED INCOME',
                'TOTAL INVESTMENTS - DC / INTERNATIONAL EQUITY',
                'TOTAL INVESTMENTS - DC / US EQUITY',
                'TOTAL PORTFOLIO',
                'TOTAL PORTFOLIO / FIXED INCOME',
                'TOTAL PORTFOLIO / INFLATION LINKED',
                'TOTAL PORTFOLIO / INTERNATIONAL EQUITY',
                'TOTAL PORTFOLIO / TOTAL HEDGE FUNDS',
                'TOTAL PORTFOLIO / TOTAL PRIVATE EQUITY',
                'TOTAL PORTFOLIO / TOTAL REAL ESTATE',
                'TOTAL PORTFOLIO / TOTAL SHORT TERM',
                'TOTAL PORTFOLIO / US EQUITY'
                ]

    ACCOUNTCODE = ['DEMOA',
                   'DEMOAG1',
                   'DEMOAG11',
                   'DEMOAG12',
                   'DEMOAG13',
                   'DEMOAG2',
                   'DEMOAG3',
                   'DEMOAG4',
                   'DEMOAG5',
                   'DEMOAG7',
                   'DEMOAG8',
                   'DEMOAG9',
                   'DEMOB',
                   'DEMOXY11',
                   'DEMOXY12',
                   'DEMOXY13',
                   'DEMOXY14',
                   'DEMOXY15',
                   'DEMOXY16',
                   'DEMOXY17',
                   'DEMOXY20',
                   'DEMOXY21',
                   'DEMOXY22',
                   'DEMOXY6J',
                   'DEMOXYZ1',
                   'DEMOXYZ2',
                   'DEMOXYZ3',
                   'DEMOXYZ4',
                   'DEMOXYZ5',
                   'DEMOXYZ6',
                   'DEMOXYZ7',
                   'DEMOXYZ8',
                   'DEMOXYZ9'
                   ]

    PERIOD = ['1 Month',
              'Quarter to Date',
              '3 Months',
              '6 Months',
              'Year to Date',
              '1 Year',
              '3 Years',
              '5 Years',
              '10 Years',
              'Inception to Date'
              ]

    RETURNTYPE = ['Net All',
                  'Net Manager',
                  'Total Gross',
                  'Total Invested'
                  ]

    CumulativeOrAnnualized = ['Cumulative',
                              'Annualized'
                              ]
