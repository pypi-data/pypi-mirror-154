# -*- coding: utf-8 -*-

#init setting
from rrshare.RQSetting.rqLocalize import (cache_path, log_path, rq_path, setting_path, make_dir_path)

# rqUtil code , date, tradedate
from rrshare.rqUtil import (rq_util_if_trade, rq_util_if_tradetime, is_trade_time_secs_cn, rq_util_get_last_tradedate)

# api
from rrshare.rqFetch import pro

# sql-util
from rrshare.rqUtil.rqPgsql import (PgsqlClass, client_pgsql, read_data_from_pg, read_table_from_pg,       
                                    read_sql_from_pg, save_data_to_postgresql)

#rqFactor
from rrshare.rqFactor.stock_RS_OH_MA import update_stock_PRS_day, update_stock_PRS_new
from rrshare.rqFactor.swl_RS_OH_MA import update_swl_PRS_day, update_swl_PRS_new

# record data
from rrshare.rqUpdate.update_stock_day import record_stock_day
from rrshare.rqUpdate.update_swl_day import record_swl_day
from rrshare.rqUpdate.update_stock_RS_OH_MA import record_stock_PRS, record_stock_PRS_new
from rrshare.rqUpdate.update_swl_RS_OH_MA import record_swl_PRS, record_swl_PRS_new

# to streamlit
#from rrshare.rqWeb import main_st  #, main_echart


#record data all
#from rrshare.record_all_data import main_record

#cli
from rrshare.cmds import cli


def _get_version(default='4.2.0'):
    try:
        from pkg_resources import DistributionNotFound, get_distribution
    except ImportError:
        return default
    else:
        try:
            return get_distribution(__package__).version
        except DistributionNotFound:  # Run without install
            return default
        except ValueError:  # Python 3 setup
            return default
        except TypeError:  # Python 2 setup
            return default


__version__ = _get_version()


def entry_point():
    cli()


