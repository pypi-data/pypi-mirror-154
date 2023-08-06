import os
import subprocess
import pandas as pd 

from rrshare.rqUtil.rqDecorator import timer
from rrshare.rqUtil.rqDate_trade import rq_util_get_last_tradedate, rq_util_get_pre_trade_date
from rrshare.rqUtil.rqParameter import START_DATE_COUNT
from rrshare.rqUtil import client_pgsql


def read_daily_counts_from_pickle(table_name='stock_day_adj_fillna',N=START_DATE_COUNT):
    """  read large stockday N>250 need 10mins, cron read data save to pickle for speed"""
    USERPATH = os.path.expanduser('~')
    #print(USERPATH)
    file_path = f'{USERPATH}/.rrsdk/data'
    file_path_name = f"{file_path}/{table_name}_{N}.pkl"
    
    trade_date = rq_util_get_last_tradedate()
    start_date = rq_util_get_pre_trade_date(trade_date,N)
    if os.path.exists(file_path_name):
        try:
            df = pd.read_pickle(file_path_name)
            df = df.sort_values(by="trade_date")
            print(f"Read daily data from <{file_path_name}> \n {df}")
            return df
        except Exception as e:
            print(e)
            return pd.DataFrame()
    else:
        print(f"File <{file_path_name}> is not exists !")
        return 0
            


def is_daily_pickle_new(table_name='swl_day', N=START_DATE_COUNT):
    """check picle daily data is or not new! """
    USERPATH = os.path.expanduser('~')
    #print(USERPATH)
    file_path = f'{USERPATH}/.rrsdk/data'
    file_path_name = f"{file_path}/{table_name}_{N}.pkl"
    trade_date = rq_util_get_last_tradedate()
    start_date = rq_util_get_pre_trade_date(trade_date,N)
    if os.path.exists(file_path_name):
        try:
            df = pd.read_pickle(file_path_name)
            df = df.sort_values(by="trade_date")
            print(f"Read daily data from <{file_path_name}> \n {df}")
        except Exception as e:
            print(e)
    else:
        print(f"File <{file_path_name}> is not exists !")
        df = None
    if df is not None:
        print(df)
        df_last = df.copy()
        df_last_one = set(pd.to_datetime(df_last.trade_date.values, format='%Y-%m-%d'))
        last_date = str(max(df_last_one)).split(" ")[0]
        #print(last_date)
        flag = last_date == rq_util_get_last_tradedate()
        print(f" Daily data in <{file_path_name}> is New .") if flag else print("daily data in <{file_path_name}> not New, need update!")
        return flag
    else:
        return False
    

@timer
def save_daily_count_to_pickle(table_name='stock_day_adj_fillna', N=START_DATE_COUNT):
    """  read large stockday N>250 need 10mins, cron read data save to pickle for speed"""
    USERPATH = os.path.expanduser('~')
    #print(USERPATH)
    file_path = f'{USERPATH}/.rrsdk/data'
    if not os.path.exists(file_path):
        subprocess.run(['mkdir','-p', file_path])
    file_path_name = f"{file_path}/{table_name}_{N}.pkl"
    trade_date = rq_util_get_last_tradedate()
    start_date = rq_util_get_pre_trade_date(trade_date,N)
    print(f"You Input Daily counts is {N} > 250, Good!") if N > 250 else print(f"Ckeck Daily counts : {N} < 250")
    if N < 250  and (table_name.split("_")[0] == "stock"):
        print(" Warninng: Are you Check stock Daily counts , Sure > = 250 !")
    if N < 260 and (table_name.split("_")[0] == "swl"):
        print(" Warninng: Are you Check swl Daily counts , Sure > = 260 !")
        
    
    if not is_daily_pickle_new(table_name=table_name, N=N):
        sql = f"SELECT * FROM {table_name} WHERE trade_date >= '{start_date}'"
        df = pd.read_sql_query(sql, client_pgsql("rrshare"))
        df.to_pickle(file_path_name)
        print(f" Save  daily data: {len(df)}  to  pickle: {file_path_name}")
    else:
        print(f" Daily data in <{file_path_name}> is new , Needn't update ! ")
        

if  __name__ == "__main__":

    #read_daily_counts_from_pickle(table_name="swl_day") 
    #df = read_daily_counts_from_pickle(table_name="stock_day_adj_fillna")
    #print(df[df.ts_code=='600519.SH'])
    #is_daily_pickle_new(table_name="stock_day_adj_fillna", N=250)
    #is_daily_pickle_new(table_name='swl_day')
    save_daily_count_to_pickle(table_name='swl_day')
    #save_daily_count_to_pickle(table_name="stock_day_adj_fillna")
    
    
    