import Decision1 # 均线交叉策略
import Decision3 # 海龟交易策略
import Decision4 # 相对强弱指标
import RQ_Data_Get
import Backtest
import rqdatac
import pandas as pd

rqdatac.init()
codeList = pd.read_excel('FUTURE_CODE.xlsx', header = None) # 早上09：00-11：30 下午13:30-15:00 夜间：21：00-02：30(某些品种无夜盘)
rank = 31  # 0~70
idMain = rqdatac.futures.get_dominant(codeList.iloc[rank,1], '20240430') # NOTICE!!! 主力合约随时间变化
codename0 = idMain[0] # 股票/期货代码 600095.SH/AU2301

# 历史数据获取
data1 = RQ_Data_Get.acquire_code(codename0,"20230401","20241001")
# 执行策略
dataSP = Decision4.caculateSP(data1)
# 回测
Backtest.caculateBT(dataSP)

# dataSP.to_excel("test0.xlsx")
