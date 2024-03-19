# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 07:38:07 2020

@author: 15012
"""
import pandas as pd
from utils import *

dir_data_input = dir_data_final
dir_data_output = dir_result

total_df = pd.read_csv(dir_data_input + "total_df_monthly.csv")


"""

monthly rtn

"""


# print(total_df.head())
# print(total_df.columns)
# print(total_df['monthly_rtn'])

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
            # print(cur_df[factor_name])
            # print(cur_df[rtn_name])
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
    

anal_ICs(data_df,factor_name,rtn_name,date_name)

"""
get_rank function
"""
def get_rank(x):
    return x.rank()



"""
analyze each factor



"""

print(anal_rankICs(data_df,factor_name,rtn_name,date_name))
