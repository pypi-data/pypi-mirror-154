import pandas as pd 
from rrshare.rqUtil import rq_util_get_last_tradedate, client_pgsql

lastTD = rq_util_get_last_tradedate()

df_v = pd.read_sql(f"SELECT DISTINCT * FROM swl_day_valuation WHERE trade_date = '{lastTD}'", con=client_pgsql('rrshare'))

print(df_v)