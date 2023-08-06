from rrshare.rqFactor.swl_RS_OH_MA import update_swl_PRS_day, update_swl_PRS_new

def record_swl_PRS():
    try:
        update_swl_PRS_day()
    except Exception as e:
        print(e)

def record_swl_PRS_new():
    try:
        update_swl_PRS_new()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    record_swl_PRS()
    record_swl_PRS_new()

