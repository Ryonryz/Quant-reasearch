# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 07:38:07 2020

@author: 15012
"""
import pandas as pd# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 07:38:07 2020

@author: 15012
"""
import pandas as pd
import numpy as np
from utils import *

dir_data_input = dir_data_final
dir_data_output = dir_result

total_df = pd.read_csv(dir_data_input + "total_df_monthly.csv")



"""

monthly rtn

"""


print(total_df.head())
print(total_df.columns)

data_df = total_df
rtn_name = "monthly_next_rtn"
date_name = "date"

factor_name = "ratio_ROA"

def anal_ICs(data_df,factor_name,rtn_name,date_name):
    ICs = []
    dates = np.unique(data_df[date_name])
    dates = sorted(dates)

    for date in dates:
        cur_df = data_df[data_df.date == date]
        cur_bool1 = pd.notna(cur_df[factor_name])
        cur_bool2 = pd.notna(cur_df[rtn_name])
        cur_bool = cur_bool1 & cur_bool2

        if sum(cur_bool) > 0:
            cur_df = cur_df[cur_bool]
            ICs.append(np.corrcoef(cur_df[factor_name],cur_df[rtn_name])[0,1])

    ICs = pd.Series(ICs)
    IC_mean = np.mean(ICs)
    IC_abs_mean = np.mean(abs(ICs))
    IC_std = np.std(ICs)
    IC_greater_zero = (sum(ICs > 0)/len(ICs) - 0.5)
    IC_t = IC_mean/IC_std * np.sqrt(len(ICs) - 1)

    return {"ICs":ICs,"IC_mean":IC_mean,"IC_abs_mean":IC_abs_mean,"IC_std":IC_std,\
            "IC_greater_zero":IC_greater_zero,"IC_t":IC_t}

# define get_rank function
def get_rank(series):
    return series.rank()

def anal_rankICs(data_df,factor_name,rtn_name,date_name):
    ICs = []
    dates = np.unique(data_df[date_name])
    dates = sorted(dates)
    for date in dates:
        cur_df = data_df[data_df.date == date]
        cur_bool1 = pd.notna(cur_df[factor_name])
        cur_bool2 = pd.notna(cur_df[rtn_name])
        cur_bool = cur_bool1 & cur_bool2
        if sum(cur_bool) > 0:
            cur_df = cur_df[cur_bool]
            s1 = get_rank(cur_df[factor_name])
            s2 = get_rank(cur_df[rtn_name])
            ICs.append(np.corrcoef(s1,s2)[0,1])

    ICs = pd.Series(ICs)
    IC_mean = np.mean(ICs)
    IC_abs_mean = np.mean(abs(ICs))
    IC_std = np.std(ICs)
    IC_greater_zero = (sum(ICs > 0)/len(ICs) - 0.5)
    IC_t = IC_mean/IC_std * np.sqrt(len(ICs))

    return {"rankICs":ICs,"rankIC_mean":IC_mean,"rankIC_abs_mean":IC_abs_mean,"rankIC_std":IC_std,\
            "rankIC_greater_zero":IC_greater_zero,"rankIC_t":IC_t}


#anal_ICs(data_df,factor_name,rtn_name,date_name)

"""
get_rank function

analyze each factor
"""

#anal_rankICs(data_df,factor_name,rtn_name,date_name)





# 假设你有一个因子名称的列表
factor_names = ['pct_chg', 'cir_mv', 'total_mv', 'cir_share',
       'total_share', 'bs_equity_belong_parent_film',
       'bs_fixed_asset', 'bs_illiquid_liability', 'bs_liquid_liability',
       'bs_total_asset', 'bs_total_equity','bs_total_liability',
       'cfs_operating_cashflow', 'is_net_profit',
       'is_operating_income', 'is_operating_profit',
       'ratio_ROA', 'ratio_ROE', 'ratio_net_asset_growth',
       'ratio_net_profit_growth', 'ratio_net_profit_margin',
       'ratio_operating_cashflow_growth',
       'ratio_operating_cashflow_to_total_operating_income',
       'ratio_operating_income_growth', 'ratio_total_asset_growth']


import pandas as pd

# 创建一个空的DataFrame，用于存储结果
columns = ['Factor', 'ICs', 'IC_mean', 'IC_abs_mean', 'IC_std', 'IC_greater_zero', 'IC_t',
           'rankICs', 'rankIC_mean', 'rankIC_abs_mean', 'rankIC_std', 'rankIC_greater_zero', 'rankIC_t']
result_df = pd.DataFrame(columns=columns)

for factor_name in factor_names:
    # 分析因子与收益率的相关性
    result_ICs = anal_ICs(data_df, factor_name, rtn_name, date_name)

    # 分析因子的 rank IC
    result_rankICs = anal_rankICs(data_df, factor_name, rtn_name, date_name)

    # 计算IR
    IR = result_ICs["IC_mean"] / result_ICs["IC_std"]

    # 如果IR的绝对值大于等于0.1，则将结果添加到DataFrame中
    if abs(IR) >= 0.1:
        result_df = result_df._append({
            'Factor': factor_name,
            'ICs': result_ICs["ICs"],
            'IC_mean': result_ICs["IC_mean"],
            'IC_abs_mean': result_ICs["IC_abs_mean"],
            'IC_std': result_ICs["IC_std"],
            'IC_greater_zero': result_ICs["IC_greater_zero"],
            'IC_t': result_ICs["IC_t"],
            'rankICs': result_rankICs["rankICs"],
            'rankIC_mean': result_rankICs["rankIC_mean"],
            'rankIC_abs_mean': result_rankICs["rankIC_abs_mean"],
            'rankIC_std': result_rankICs["rankIC_std"],
            'rankIC_greater_zero': result_rankICs["rankIC_greater_zero"],
            'rankIC_t': result_rankICs["rankIC_t"],
            'IR': IR
        }, ignore_index=True)

# 保存DataFrame到CSV文件
result_df.to_csv(dir_data_output + 'sgl_factor_result.csv', index=False)

