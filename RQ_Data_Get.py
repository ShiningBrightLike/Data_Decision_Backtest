import rqdatac

def acquire_code(codename,t_a,t_b):   #下载一只股票数据

    rqdatac.init()
    rqID = rqdatac.id_convert(codename)
    datatest = rqdatac.get_price(rqID, t_a, t_b, fields=['open', 'high', 'low', 'close', 'volume'],expect_df=False)
    print(rqID)
    print(datatest.tail())
    print("—" * 50)

    return datatest


"""
在我国，期货代码主要是由字母和数字共同组成，而字母指的是期货品种的交易代码，而数字代表期货合约的到期年份和月份
比如AU2301合约，意思就是2023年1月份到期的黄金期货合约，这的2301就是该合约到期的时间，到期年月的意思

获取目标数据
金融数据类型包括：中国A股、ETF、中国期货（股指、国债、商品期货）的所有基本信息和每日市场数据/分钟数据，A股上市的财务数据和场内基金数据，宏观数据。
get_price(order_book_ids, start_date='2013-01-04', end_date='2014-01-04', frequency='1d',
adjust_type='pre', skip_suspended =False, market='cn', expect_df=True,time_slice=None)

格式描述   格式示例
数字      YYYYDDMM       20150101
字符串    "YYYY-DD-MM"   "2015-01-01"
datetime 对象	        datetime.datetime (2015, 1, 3)
date     对象	        datetime.date (2015, 1, 3)
Pandas   Timestamp	    pandas.Timestamp ('20150103')

PS:tick数据、实时数据 无权限
"""


