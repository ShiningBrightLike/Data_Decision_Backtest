import numpy as np
import warnings
import matplotlib
warnings.filterwarnings("ignore")
matplotlib.rcParams['axes.unicode_minus'] =False

def caculateSP(data):
    df = data
    window = 5
    df['max_high'] = df['high'].rolling(window=window).max() # 唐奇安通道
    df['min_low'] = df['low'].rolling(window=window).min()
    df['N'] = (df['high'] - df['low']).rolling(window=window).mean() # 价值波动N
    df['Signal'] = 0

    position = 0
    for i in range(len(df)):
        current_price = df['close'][i]
        upper_band = df['max_high'][i]
        lower_band = df['min_low'][i]
        current_N = df['N'][i] # 修正的价值波动

        # 建仓
        if position == 0:
            if current_price > upper_band:
                df['Signal'].iloc[i] = 1
                position = 1  # 多仓
            if current_price < lower_band:
                df['Signal'].iloc[i] = -1
                position = -1  # 空仓
            continue

        # 加仓
        if position > 0 and current_price > df['close'][i-1] + 0.5 * current_N:  # 加多仓
            df['Signal'].iloc[i] = 1
            position += 1
        elif position < 0 and current_price < df['close'][i-1] - 0.5 * current_N:  # 加空仓
            df['Signal'].iloc[i] = -1
            position -= 1

        # 止损
        if position > 0 and current_price < df['close'][i-1] - 1.5 * current_N:  # 止损多仓
            df['Signal'].iloc[i] = -1
            position = 0
        elif position < 0 and current_price > df['close'][i-1] + 1.5 * current_N:  # 止损空仓
            df['Signal'].iloc[i] = +1
            position = 0

        # 止盈
        if position >0 and current_price < lower_band:
            df['Signal'].iloc[i] = -1
            position = 0
        elif position <0 and current_price > upper_band:
            df['Signal'].iloc[i] = 1
            position = 0

    df['openinterest'] = df['Signal']
    # NOTICE!此框架中 openinterest 用于判断交易，并非未平仓量

    return df[['open', 'high', 'low', 'close', 'volume','openinterest']]