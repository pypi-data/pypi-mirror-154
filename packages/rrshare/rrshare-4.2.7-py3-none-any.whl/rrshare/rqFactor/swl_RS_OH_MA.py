import time
import datetime
import os
import pickle
import pandas as pd
import numpy as np
from decimal import Decimal
import warnings
warnings.filterwarnings("ignore")
import logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s- %(levelname)s-%(message)s')

from rrshare.rqUtil import (rq_util_log_debug, rq_util_log_expection,
                                                     rq_util_log_info)
from rrshare.rqUtil import (rq_util_date_today, rq_util_get_trade_range, rq_util_get_last_tradedate, rq_util_get_pre_trade_date)
from rrshare.rqUtil import (PERIODS, is_trade_time_secs_cn, is_tradeday_and_market_opened)
from rrshare.rqUtil import (client_pgsql, read_data_from_pg, read_sql_from_pg)
from rrshare.rqFetch import Swsindex
from rrshare.rqUtil.rqParameter import START_DATE_COUNT

N = START_DATE_COUNT
NList = PERIODS().PERIODS
N1List = list(map(lambda x: x-1,NList))
client_rrshare = client_pgsql('rrshare')
client_rrfactor = client_pgsql('rrfactor')


USERPATH = os.path.expanduser('~')
#print(USERPATH)
file_path = f'{USERPATH}/.rrsdk/data'
#file_path_name = f"{file_path}/{table_name}_{N}.pkl"

def swl_RT_HH_MA_pre(table_name='swl_day', N=N, level="L2"):
    """caculate i-1 swl_day rt_ma
       prepare to next day  day rs_OH_ma
       swl_day has last some data N = 250 + 10
       迭代， 只算一次， 速度快。
    """
    trade_date = rq_util_get_last_tradedate()
    start_date = rq_util_get_pre_trade_date(trade_date,N)
    #print(start_date, trade_date, level)
    '''
    sql = f"SELECT * FROM {table_name} WHERE level='{level}' AND trade_date >= '{start_date}'"
    print(sql)
    df = pd.read_sql_query(sql,con=client_rrshare)
    print(df)
    df.to_pickle(f"~/.rrsdk/data/sw_{level}_day_250.pkl")
    '''
    file_path_name = f"{file_path}/{table_name}_{N}.pkl"
    df = pd.read_pickle(file_path_name)
    #print(df)
    #print(df.columns)
    df = df[['trade_date','name_level', 'open', 'high', 'low', 'close',
       'change_pct', 'vol', 'amount', 'index_code','level' ]]
    df = df[df['level'] == level]
    cols = ['open', 'high', 'low', 'close','change_pct', 'vol', 'amount']
    for i in cols:
        df[i] = pd.to_numeric(df[i], errors='coerce')
    df_i = df.set_index(['trade_date','index_code'])
    df_i.drop_duplicates(keep='last',inplace=True)
    df_un = df_i.unstack()
    vol_chg = 100*(df_un['vol'] / df_un['vol'].rolling(49).mean() - 1).unstack()
    df_fill = df_un.stack().reset_index()
    #print(df_fill)
    ma=dict()
    rt=dict()
    for i in N1List:
        ma[i] = (df_un['close'].rolling(i).mean()).unstack()
        rt[i] = df_un['change_pct'].rolling(i).sum().unstack()
    H = (df_un['high']).expanding().max()
    HH = H.unstack()
    L = df_un['low'].expanding().min()
    LL = L.unstack()
    close = df_un['close'].unstack()
    pct_chg = df_un['change_pct'].unstack()
    name_level = df_un['name_level'].unstack()
    pct_ma_rs = pd.DataFrame({
    'close_pre':close,'name_level':name_level, 'pct_chg_pre': pct_chg, 
    'ma4':ma[4],'ma9':ma[9],'ma19':ma[19], 'ma59':ma[59],'ma119':ma[119],'ma249':ma[249],
    'rt4':rt[4],'rt9':rt[9],'rt19':rt[19],'rt59':rt[59],'rt119':rt[119], 'rt249': rt[249], 
    'vol_chg_pre': vol_chg,'H':HH,'L':LL, 
    })
    data = pct_ma_rs.reset_index()
    df= data[data['trade_date'] == trade_date]
    table_name_L = f"swl_{level}_RT_HH_MA_pre"
    #print(table_name_L)
    df.to_sql(table_name_L,con=client_rrfactor, if_exists='replace')
    return df


def swl_RS_OH_MA_last(table_name='swl_day', N=N, level="L2"):
    """caculate i swl_day rt_ma
       prepare to next day  day rs_OH_ma
       swl_day has last some data N = 250 + 10
       pd.to_numeric()  !!!
       迭代， 只算一次， 速度快。
    """
    trade_date = rq_util_get_last_tradedate()
    start_date = rq_util_get_pre_trade_date(trade_date,N)
    #print(start_date, trade_date)
    '''
    sql = f"SELECT * FROM {table_name} WHERE level='{level}' AND trade_date >= '{start_date}'"
    print(sql)
    df = pd.read_sql_query(sql,con=client_rrshare)
    print(df)
    #df.to_pickle(f"~/.rrsdk/data/sw_{level}_day_250.pkl")
    '''
    file_path_name = f"{file_path}/{table_name}_{N}.pkl"
    df = pd.read_pickle(file_path_name)
    #print(df)
    #print(df.columns)
    df = df[['trade_date','name_level', 'open', 'high', 'low', 'close',
       'change_pct', 'vol', 'amount', 'index_code','level' ]]
    df = df[df['level'] == level]
    cols = ['open', 'high', 'low', 'close','change_pct', 'vol', 'amount']
    for i in cols:
        df[i] = pd.to_numeric(df[i], errors='coerce')
    df_i = df.set_index(['trade_date','index_code'])
    df_i.drop_duplicates(keep='last',inplace=True)
    df_un = df_i.unstack()
    vol_chg = 100*(df_un['vol'] / df_un['vol'].rolling(50).mean() - 1).unstack()
    df_fill = df_un.stack().reset_index()
    #print(df_fill)
    ma=dict()
    rt=dict()
    rs=dict()
    for i in NList:
        ma[i] = (df_un['close'].rolling(i).mean()).unstack()
        rt[i] = df_un['change_pct'].rolling(i).sum().unstack()
        rs[i]= 100*rt[i].unstack(0).rank(axis=1,ascending=True, pct=True).unstack()
    H = (df_un['high']).expanding().max()
    HH = H.unstack()
    L = df_un['low'].expanding().min()
    LL = L.unstack()
    OH = 100*(df_un['close']/H).unstack()
    OL = 100*(df_un['close']/L - 1).unstack()
    close = df_un['close'].unstack()
    pct_chg = df_un['change_pct'].unstack()
   
    name_level = df_un['name_level'].unstack()
    pct_ma_rs = pd.DataFrame({
    'close':close,'name_level':name_level, 'pct_chg': pct_chg, 
    'ma5':ma[5],'ma10':ma[10],'ma20':ma[20], 'ma60':ma[60],'ma120':ma[120],'ma250':ma[250],
    'rt5':rt[5],'rt10':rt[10],'rt20':rt[20],'rt60':rt[60],'rt120':rt[120], 'rt250': rt[250],
    'rs5':rs[5],'rs10':rs[10],'rs20':rs[20],'rs60':rt[60],'rs120':rs[120], 'rs250': rt[250],
    'vol_chg':vol_chg,'OH':OH,'OL':OL,'H':HH,'L':LL, 
    })
    data = pct_ma_rs.reset_index()
    #print(data)
    df = data[data['trade_date'] == trade_date]
    #print(df)
    table_name_L=f"swl_{level}_RS_OH_MA_last"
    df.to_sql(table_name_L,con=client_rrfactor, if_exists='replace')
    return df


def swl_RS_OH_MA(level="L2"):
    df = read_data_from_pg(table_name=f'swl_{level}_RS_OH_MA_last',client=client_rrfactor)
    logging.info(f'\n {df.head()}')
    df.rename(columns={'close_pre':'close','pct_chg_pre':'pct_chg'}, inplace=True)
    df['OH'] = 100*(df['close']/df['H'])
    #df['OH'] = df['OH'].apply(lambda x: Decimal(x).quantize(Decimal((0.00))))
    df['OL'] = 100*(df['close']/df['L'] - 1)
    #df['OL'] = df['OL'].apply(lambda x: Decimal(x).quantize(Decimal((0.00))))
    col_rt =['rt5', 'rt10', 'rt20', 'rt60','rt120', 'rt250']
    col_rs = ['rs_5','rs_10','rs_20','rs_60','rs_120', 'rs_250']
    col_rs_dict = dict(zip(col_rs,col_rt))
    for k, v in col_rs_dict.items():
        df[k] = 100*df[v].rank(axis=0,ascending=True, pct=True)
        cols = ['trade_date', 'code','close', 'pct_chg',\
                'ma5','ma10','ma20', 'ma60', 'ma120','ma250',\
                'rs_5','rs_10','rs_20','rs_60','rs_120', 'rs_250',\
                'rt5', 'rt10', 'rt20', 'rt60','rt120', 'rt250',\
                'H','L','OH','OL']
        #print(cols)
        #df = df[cols].round(2)
        print(df)
        print(df.columns)
        table_name_L = f"swl_{level}_RS_OH_MA"
        print(table_name_L)
        df.to_sql(table_name_L, con=client_pgsql('rrfactor'), if_exists='replace')
        logging.info(f'\n {df.head()}')
        return df


def swl_RS_OH_MA_new(level="L2"):
    """ fast and right pkl or h5 or sql
    """
    #df = pd.read_pickle('/home/rome/.rrshare/data/stock_RT_HH_MA_pre.pkl')
    df = pd.read_sql_table(f"swl_{level}_RT_HH_MA_pre", client_rrfactor)
    logging.info(df.head())
    df_last_date =str( max(set(list(df['trade_date'].values))))[0:10]
    #print(df_last_date)
    today_ = rq_util_date_today().strftime('%Y-%m-%d') 
    trade_date = today_  if is_tradeday_and_market_opened() else rq_util_get_last_tradedate()
    #print(trade_date)

    if (trade_date == df_last_date): 
        #fetch_realtime_price from rqFetch
        df_p = Swsindex().fetch_swsindex_L1_L2_realtime(level)
        print(df_p)
        df_p = df_p.drop(columns =['trade_date','amount','open'], axis=1)
        
        df = pd.merge(df,df_p, how='left', on='index_code')
        #print(df)
        #vol_chg = 100*((df['vol']*df['adj_factor']) / (df['vol']*df['adj_factor']).rolling(50).mean() - 1)
        col_ma_pre = ['ma4','ma9', 'ma19', 'ma59', 'ma119', 'ma249']
        col_ma = ['ma5','ma10','ma20', 'ma60','ma120','ma250']
        col_rt_pre =['rt4', 'rt9', 'rt19', 'rt59','rt119', 'rt249']
        col_rt =['rt5', 'rt10', 'rt20', 'rt60','rt120', 'rt250']
        col_ma_dict = dict(zip(col_ma,col_ma_pre))
        #print(col_ma_dict)
        col_rt_dict = dict(zip(col_rt, col_rt_pre))
        for  k, v in col_ma_dict.items():
            n = int(k[2:])
            #print(n)
            df[k] = ((n-1)*df[v] + df['close']) / n
            #print(df[k])
            df[k] = df[k].apply(lambda x: Decimal(x).quantize(Decimal(('0.00'))))
        for  k, v in col_rt_dict.items():
            n = int(k[2:])
            df[k] = df[v] + df['change_pct']
        df.dropna(subset=['H','L','name'],inplace=True)   # TODO ???
        #print(df)
        vol_chg = 100*(df['vol']/(df['vol']).rolling(50).mean() - 1)  # TODO
       
        df['H'] = df.apply(lambda x: max(x.H, x.high), axis=1) 
       
        df['L'] = df.apply(lambda x: min(x.L, x.low), axis=1)
        df['OH'] = 100*(df['close']/df['H'])
        #df['OH'] = df['OH'].apply(lambda x: Decimal(x).quantize(Decimal((0.00))))
        df['OL'] = 100*(df['close']/df['L'] - 1)
        #df['OL'] = df['OL'].apply(lambda x: Decimal(x).quantize(Decimal((0.00))))

        #rsi= 100*rt[i].unstack(0).rank(axis=1,ascending=True, pct=True).unstack()
        col_rs = ['rs_5','rs_10','rs_20','rs_60','rs_120', 'rs_250']
        col_rs_dict = dict(zip(col_rs,col_rt))
        for k, v in col_rs_dict.items():
            df[k] = 100*df[v].rank(axis=0,ascending=True, pct=True)

        cols = ['index_code', 'name',  'change_pct',\
                'ma5','ma10','ma20', 'ma60', 'ma120','ma250',\
                'rs_5','rs_10','rs_20','rs_60','rs_120', 'rs_250',\
                'rt5', 'rt10', 'rt20', 'rt60','rt120', 'rt250',\
                'H','L',
                'OH','OL'
                ]

        #print(cols)
        df = df[cols].round(2)
        print(df)
        #df.rename(columns={'date':'trade_date'}, inplace=True)
        table_name_L = f"swl_{level}_RS_OH_MA_new"
        #print(table_name_L)
        df.to_sql(table_name_L, con=client_rrfactor, if_exists='replace')
        logging.info(f"\n {df.head()}")
        return df
    else:
        return read_data_from_pg(table_name=f'swl_{level}_RS_OH_MA',client=client_rrfactor)


def update_swl_PRS_day():
    for l in ["L1","L2"]:
        swl_RT_HH_MA_pre(level=l)
        swl_RS_OH_MA_last(level=l)
        swl_RS_OH_MA(level=l)


def update_swl_PRS_new():
    for l in ["L1","L2"]:
        swl_RS_OH_MA_new(level=l)
    

if  __name__  == "__main__":
    update_swl_PRS_day()
    update_swl_PRS_new()