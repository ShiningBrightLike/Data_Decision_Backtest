# Data_Decision_Backtest
A simple quantitative trading system

**1.Data acquisition**

*rqdatac* framework is mainly used for data call, and the types of financial data include: all basic information and daily market data/minute data of China A-shares, ETFs, and China futures (stock index, national debt, and commodity futures), financial data of A-shares listing, in-exchange fund data, and macro data.

**2.Strategy construction**

Strategy function, high degree of freedom, the only requirement: return the decision column [-1, 0, 1] indicates [sell, unchanged, buy].

**3.Backtest evaluation**

Mainly using the *backtrader* framework, Backtrader provides powerful backtest capabilities to evaluate and optimize trading strategies: trade fee and slip point simulation, money management, trade records and statistical indicators, visual analysis, parameter optimization and strategy comparison.
