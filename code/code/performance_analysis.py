# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt

from back_test import *

# 作收益折线图

x = trade_date
y = funds

df = pd.DataFrame({'Month': trade_date, 'Values': funds})

df['Month'] = pd.to_datetime(df['Month'])
df.set_index('Month', inplace=True)

plt.plot(df.index, df['Values'], linestyle='-')
plt.xticks(rotation=45)

plt.title('start funds : 10000')
plt.ylabel('rate of return')


# 计算波动率 因为是十年内每个月的收益率，所以是12
Volatility = np.std(monthly_rtn) * np.sqrt(12)
print("volatility:", Volatility)
# 简化模型，假设无风险利率 计算夏普比率
risk_free_rate = 0.017

sharpe_ratio = (annual_rtn - risk_free_rate) / Volatility
print("sharpe ratio:", sharpe_ratio)


# 最大回撤
def max_drawdown(returns):
    max_dd = 0
    peak = returns[0]
    for r in returns:
        if r > peak:
            peak = r
        dd = (peak - r) / peak
        if dd > max_dd:
            max_dd = dd
    return max_dd


dd = max_drawdown(monthly_rtn)
print("max drawdown: ", dd)

plt.show()
