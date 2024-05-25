from __future__ import (absolute_import, division, print_function,unicode_literals)
import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] =False
matplotlib.rcParams['font.sans-serif'] = ['SimHei']

class TestStrategy(bt.Strategy):
    params = (
        ('idxperiod', 5),
        ('stop_loss', 0.3),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        """
        当访问一条Line 的数据时，会默认指向下标为0的数据。最后一个数据通过下标-1来访问，在-1之后是索引0，用于访问当前时刻。
        在回测过程中，无需知道已经处理了多少条|分钟/天/月，”o”一直指向当前值，下标-1来访问最后一个值。
        """
        self.init_cash = self.broker.get_cash()
        self.dataclose = self.datas[0].close
        # self.datas[0].close[0] 第一个0代表add数据集的位次，第二个0代表当前时间 # NOTICE!!! NOTICE!!! NOTICE!!!
        self.dataDecision = self.datas[0].openinterest

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add line
        self.high_ = bt.indicators.Highest(self.datas[0], period=self.params.idxperiod, subplot=False)
        self.low_ = bt.indicators.Lowest(self.datas[0], period=self.params.idxperiod, subplot=False)
        # self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.idxperiod)
        self.crossover = bt.indicators.CrossOver(self.dataDecision, 0)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %(trade.pnl, trade.pnlcomm))

    def next(self):

        if self.broker.getvalue() < self.init_cash * (1 - self.params.stop_loss):  # 账户价值亏损超过止损比例，退出整个策略
            self.sell()
            self.order = None
            self.log('亏损退出')
            self.env.runstop()

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataDecision[0] > 0:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('买入开仓, %.2f' % self.dataclose[0])
                self.order = self.buy()

            elif self.dataDecision[0] < 0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('卖出开仓, %.2f' % self.dataclose[0])
                self.order = self.sell()

        else:
            if self.dataDecision[0] > 0 and self.position.size >0:
                self.log('加仓 ADD BUY, %.2f' % self.dataclose[0])
                self.order = self.buy()

            if self.dataDecision[0] < 0 and self.position.size <0:
                self.log('加仓 ADD SELL, %.2f' % self.dataclose[0])
                self.order = self.sell()

            if self.dataDecision[0] > 0 and self.position.size <0: # NOTICE!!!
                self.log('买入平仓, %.2f' % self.dataclose[0])
                self.order = self.close()
                #self.order = self.buy()

            if self.dataDecision[0] < 0 and self.position.size >0:
                self.log('卖出平仓, %.2f' % self.dataclose[0])
                self.order = self.close()
                #self.order = self.sell()

def caculateBT(data):
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    dfPosition = data

    # 将 Pandas DataFrame 转换为 Backtrader 数据源
    dataPosition = bt.feeds.PandasData(dataname=dfPosition)

    # Add the Data Feed to Cerebro
    cerebro.adddata(dataPosition)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=5)

    # Set the commission
    cerebro.broker.setcommission(commission=0.01)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='myannualreturn')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrwadown')

    # Run over everything
    thestrats = cerebro.run()
    thestrat = thestrats[0]

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print("年化收益率：", thestrat.analyzers.myannualreturn.get_analysis())
    print('夏普率:', thestrat.analyzers.mysharpe.get_analysis())
    print("最大回撤：", thestrat.analyzers.mydrwadown.get_analysis()['max'])

    cerebro.plot()

    return