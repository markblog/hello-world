
class t(object):
    fundtree='fund_tree_name'
    strategy='concat_all'
    effective_date='effective_date'
    account='account_code'
    return_type='rates_rule'
    emv='emv'
    bmv='bmv'

    abal='abal'
    abal_zero='abal_zero'
    abal_mid='abal_mid'
    abal_full='abal_full'
    base_flows='base_flows'
    value_add='value_add'
    gain_loss='gain_loss'
    inc='inc'
    inflws='inflws'
    otflw_val='otflw_val'
    net_csh_flw = 'net_csh_flw'
    ror='ror'
    mgr_fees='mgr_fees'

    index_code='index_code'
    index_ror='index_ror'

    #security level
    security_name='security_name'
    sec_ssc_id='sec_ssc_id'
    asset_class='classification_1'
    country='classification_2'
    sector='classification_3'
    industry='classification_4'

    period_return='period_return'
    ror_cum='cumulative account ror'
    ror_index_cum='cumulative benchmark ror'
    ror_ann='annualized account ror'

tran_classification={'country':'classification_2',
                     'asset_class':'classification_1',
                     'sector':'classification_3',
                     'industry':'classification_4'}

#This dict build relationship between ``account_code``,``account_name_long``,``index_code``,``index_short_name``.
#Account_Benchmark dictionaty's structure is {account_code:{account_name_long:str,index_code:str,index_short_name:str}}
