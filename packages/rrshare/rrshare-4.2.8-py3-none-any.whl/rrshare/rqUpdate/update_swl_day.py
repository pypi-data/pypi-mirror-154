from rrshare.rqUtil import rq_util_get_pre_trade_date

from rrshare.rqSU import  rq_save_swl_day_pg, rq_save_swl_day_valucation_pg
                

def record_swl_day():
    """ swl_day last 10 days data, N +10"""
    #rq_save_swl_industry_list_stock_belong()
    rq_save_swl_day_pg()
    rq_save_swl_day_valucation_pg()
    

if __name__ == '__main__':
    #print(rq_util_get_pre_trade_date(n=255))
    record_swl_day()