# -*- coding: utf-8 -*-


from utils import *

dir_data_result = dir_main + "result\\"

total_df = pd.read_csv(dir_data_result + "factor_scores.csv")
# 换手交易的时间
trade_date = list(set(total_df['month']))
trade_date.sort()

# 初始资金
start_funds = 10000

high_scores = start_funds
low_scores = start_funds

monthly_rtn = []
funds = []

for date in trade_date:
    stocks = total_df[total_df['month'] == date]
    stocks = stocks.sort_values(by="score", ascending=False)

    score_top30 = stocks.head(30)
    score_last30 = stocks.tail(30)

    rtn = (low_scores / 30 * (1 + score_last30["monthly_rtn"]).sum()) / low_scores - 1
    monthly_rtn.append(rtn)

    high_scores = high_scores / 30 * (1 + score_top30["monthly_rtn"]).sum()
    low_scores = low_scores / 30 * (1 + score_last30["monthly_rtn"]).sum()

    funds.append(low_scores)


print(high_scores / start_funds, low_scores / start_funds)

annual_rtn = pow(low_scores / start_funds, 0.1) - 1

print(f"Annualized Return : {annual_rtn}")
