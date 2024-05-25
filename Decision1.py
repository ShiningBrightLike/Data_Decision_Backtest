import numpy as np
import warnings
import matplotlib
warnings.filterwarnings("ignore")
matplotlib.rcParams['axes.unicode_minus'] =False

def caculateSP(data):
    df = data
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['Signal'] = 0
    df['Signal'][10:] = np.where(df['MA5'][10:] > df['MA10'][10:], 1, -1)
    df['openinterest'] = df['Signal'].diff()
    df['openinterest'] = df['openinterest'].fillna(0)
    # NOTICE!此框架中 openinterest 用于判断交易，并非未平仓量

    return df[['open', 'high', 'low', 'close', 'volume','openinterest']]