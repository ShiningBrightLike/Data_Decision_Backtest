import numpy as np

def calculate_rsi(prices):
    n = 10 # 可调参数
    overbought = 70
    oversold = 30
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    signals = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)

        if rsi[i] > overbought:
            signals[i] = -1
        elif rsi[i] < oversold:
            signals[i] = 1

    return rsi,signals

def caculateSP(data):
    df = data
    prices = df['close']
    v1, v2 = calculate_rsi(prices)
    df['openinterest'] = v2
    """ NOTICE!!!并非交叉点
    df['Signal'] = v2
    for i in range(1,len(prices)):
        if df['Signal'].iloc[i] == df['Signal'].iloc[i-1]:
            df['openinterest'].iloc[i] = 0
    """

    # NOTICE!此框架中 openinterest 用于判断交易，并非未平仓量
    return df[['open', 'high', 'low', 'close', 'volume','openinterest']]
