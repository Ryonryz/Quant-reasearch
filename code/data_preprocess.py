# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 07:37:55 2020

@author: 15012
"""



import numpy as np 
import pandas as pd
import os
from utils import *


"""

market data

"""
dir_data_input = dir_data_raw_market
dir_data_output = dir_data_final



month_list_stock_df = pd.read_csv(dir_data_input + "MonthListStock.csv")
del month_list_stock_df["Unnamed: 0"]
month_list_stock_df.head()
month_list_stock_dict = {col: set(month_list_stock_df[col]) for col in month_list_stock_df.columns}



year = 2006
half_year = 1

cur_data = pd.read_csv(dir_data_input + "ALL_A_%dHY%d.CSV" %(year,half_year),encoding = "GBK")
cur_data.columns = ["stock_code","stock_name","date","open","high",\
                    "low","close","trading_volume","trading_amount","pct_chg",\
                    "cir_mv","total_mv","cir_share","total_share","delete"]

print(cur_data.shape)
cur_data["month"] = cur_data.date.apply(lambda x: x[:7])
cur_data["bool_in_HS"] = cur_data.apply(lambda x: x["stock_code"] in month_list_stock_dict[x["month"]] ,axis = 1)
cur_data = cur_data[cur_data.bool_in_HS]


#chosen_cols = ["stock_code","date","high","low","open","close","trading_volume","trading_amount","pct_chg"]
total_data = pd.DataFrame()
for year in np.arange(2006,2016):
    for half_year in np.arange(1,3):
        print("*"*30)
        print(year)
        print(half_year)
        cur_data = pd.read_csv(dir_data_input + "ALL_A_%dHY%d.CSV" %(year,half_year),encoding = "GBK")
        cur_data.columns = ["stock_code","stock_name","date","open","high",\
                            "low","close","trading_volume","trading_amount","pct_chg",\
                            "cir_mv","total_mv","cir_share","total_share","delete"]
        del cur_data["stock_name"]
        del cur_data["delete"]
        print(cur_data.shape)
        cur_data["month"] = cur_data.date.apply(lambda x: x[:7])
        cur_data["bool_in_HS"] = cur_data.apply(lambda x: x["stock_code"] in month_list_stock_dict[x["month"]] ,axis = 1)
        cur_data = cur_data[cur_data.bool_in_HS]
        print(cur_data.shape)
        del cur_data["bool_in_HS"]
        total_data = total_data.append(cur_data)

print(total_data.shape)
total_data.head()
total_data.columns

total_data.to_csv(dir_data_output + "trading_data_daily.csv",index = False)


trading_date = np.unique(total_data.date)
trading_date = sorted(trading_date)
trading_date = pd.DataFrame({"trading_date":trading_date})
trading_date.head()
trading_date.to_csv(dir_data_output + "trading_date_daily.csv", index=False)

trading_date["month"] = trading_date.trading_date.apply(lambda x:x[:7])
trading_date.head()
last_trading_date_per_month = trading_date.trading_date.groupby(trading_date.month).apply(lambda x:x.sort_values().iloc[-1])
last_trading_date_per_month.head()
last_trading_date_per_month.index = np.arange(len(last_trading_date_per_month))
pd.DataFrame({"last_trading_date_per_month":last_trading_date_per_month}).to_csv(dir_data_output + "last_trading_date_monthly.csv", index=False)


last_trading_date_per_month = set(last_trading_date_per_month)

print(total_data.shape)
total_data["bool_last_day"] = total_data.date.apply(lambda x: x in last_trading_date_per_month)
total_data = total_data[total_data.bool_last_day]
print(total_data.shape)

del total_data["bool_last_day"]
total_data.to_csv(dir_data_output + "trading_data_monthly.csv",index = False)


"""

# account data
import copy
"""
dir_data_input = dir_data_raw_account
dir_data_output = dir_data_output

import copy

file_names_orig = os.listdir(dir_data_input)
file_names_orig
file_names = copy.deepcopy(file_names_orig)

def chg_delist_file_name(x):
    if x[0] == "~":
        return None
    if len(x) > 12:
        if x[-12:-5] == "_delist":
            result = x[:-12]
            result = result + x[-5:]
            return result
    return x




file_names = [chg_delist_file_name(file_name) for file_name in file_names]
file_names
file_names = file_names[:-3]
file_names

file_names = np.unique(file_names)


total_factor_df = pd.DataFrame()

file_name = file_names[0]

factor_name = file_name[:-5]
cur_file = pd.read_excel(dir_data_input + file_name)
cur_file.head()
del cur_file["name"]
cur_file.index = cur_file.id
del cur_file["id"]
cur_file.head()

cur_factor_df = cur_file.stack()
cur_factor_df.index
cur_factor_df = cur_factor_df.reset_index()
cur_factor_df.head()
cur_factor_df = cur_factor_df.rename(columns = {"level_1":"quarter",0:factor_name})
cur_factor_df["quarter"] = cur_factor_df.quarter.apply(lambda x:x[-6:])
cur_factor_df.head()

file_name = factor_name + "_delist.xlsx"

if file_name in file_names_orig:
    cur_file = pd.read_excel(dir_data_input + file_name)
    cur_file.head()
    del cur_file["name"]
    cur_file.index = cur_file.id
    del cur_file["id"]
    cur_file.head()

    cur_factor_delist_df = cur_file.stack()
    cur_factor_delist_df.index
    cur_factor_delist_df = cur_factor_delist_df.reset_index()
    cur_factor_delist_df.head()
    cur_factor_delist_df = cur_factor_delist_df.rename(columns = {"level_1":"quarter",0:factor_name})
    cur_factor_delist_df["quarter"] = cur_factor_delist_df.quarter.apply(lambda x:x[-6:])
    cur_factor_delist_df.head()
    cur_factor_df = cur_factor_df.append(cur_factor_delist_df)

if len(total_factor_df) == 0:
    total_factor_df = cur_factor_df
else:
    total_factor_df = pd.merge(total_factor_df,cur_factor_df,how = "outer")


file_name = file_names[1]

factor_name = file_name[:-5]
cur_file = pd.read_excel(dir_data_input + file_name)
cur_file.head()
del cur_file["name"]
cur_file.index = cur_file.id
del cur_file["id"]
cur_file.head()

cur_factor_df = cur_file.stack()
cur_factor_df.index
cur_factor_df = cur_factor_df.reset_index()
cur_factor_df.head()
cur_factor_df = cur_factor_df.rename(columns = {"level_1":"quarter",0:factor_name})
cur_factor_df["quarter"] = cur_factor_df.quarter.apply(lambda x:x[-6:])
cur_factor_df.head()

file_name = factor_name + "_delist.xlsx"

if file_name in file_names_orig:
    cur_file = pd.read_excel(dir_data_input + file_name)
    cur_file.head()
    del cur_file["name"]
    cur_file.index = cur_file.id
    del cur_file["id"]
    cur_file.head()

    cur_factor_delist_df = cur_file.stack()
    cur_factor_delist_df.index
    cur_factor_delist_df = cur_factor_delist_df.reset_index()
    cur_factor_delist_df.head()
    cur_factor_delist_df = cur_factor_delist_df.rename(columns = {"level_1":"quarter",0:factor_name})
    cur_factor_delist_df["quarter"] = cur_factor_delist_df.quarter.apply(lambda x:x[-6:])
    cur_factor_delist_df.head()
    cur_factor_df = cur_factor_df.append(cur_factor_delist_df)

if len(total_factor_df) == 0:
    total_factor_df = cur_factor_df
else:
    total_factor_df = pd.merge(total_factor_df,cur_factor_df,how = "outer")



total_factor_df.head()



total_factor_df = pd.DataFrame()
for file_name in file_names:
    factor_name = file_name[:-5]
    print("*"*30)
    print(factor_name)
    cur_file = pd.read_excel(dir_data_input + file_name)
    del cur_file["name"]
    cur_file.index = cur_file.id
    del cur_file["id"]

    cur_factor_df = cur_file.stack()
    cur_factor_df.index
    cur_factor_df = cur_factor_df.reset_index()
    cur_factor_df = cur_factor_df.rename(columns = {"level_1":"quarter",0:factor_name})
    cur_factor_df["quarter"] = cur_factor_df.quarter.apply(lambda x:x[-6:])

    file_name = factor_name + "_delist.xlsx"

    if file_name in file_names_orig:
        cur_file = pd.read_excel(dir_data_input + file_name)
        cur_file.head()
        del cur_file["name"]
        cur_file.index = cur_file.id
        del cur_file["id"]
        cur_file.head()
        cur_factor_delist_df = cur_file.stack()
        cur_factor_delist_df.index
        cur_factor_delist_df = cur_factor_delist_df.reset_index()
        cur_factor_delist_df.head()
        cur_factor_delist_df = cur_factor_delist_df.rename(columns = {"level_1":"quarter",0:factor_name})
        cur_factor_delist_df["quarter"] = cur_factor_delist_df.quarter.apply(lambda x:x[-6:])
        cur_factor_df = cur_factor_df.append(cur_factor_delist_df)

    if len(total_factor_df) == 0:
        total_factor_df = cur_factor_df
    else:
        total_factor_df = pd.merge(total_factor_df,cur_factor_df,how = "outer")

    print(total_factor_df.columns)

total_factor_df.columns
total_factor_df.shape
total_factor_df.head()


np.unique(total_factor_df.quarter)


total_factor_df = total_factor_df.rename(columns = {"id":"stock_code"})
total_factor_df.to_csv(dir_data_output + "account_data_quarterly.csv",index = False)



"""

merge trading date and account date daily

"""


market_df = pd.read_csv(dir_data_output + "trading_data_daily.csv")
account_df = pd.read_csv(dir_data_output + "account_data_quarterly.csv")
account_df = account_df.rename(columns = {"report_date":"date"})

account_df.columns
market_df.columns

print(market_df.shape)
total_df = pd.merge(market_df,account_df,how = "left")
print(total_df.shape)
total_df.head()
total_df = total_df.groupby("stock_code").apply(lambda x:x.sort_values("date").fillna(method = "ffill"))
total_df.index = np.arange(len(total_df))
total_df.columns
total_df.head()
total_df.to_csv(dir_data_output + "total_df_daily.csv",index=False)


last_trading_date_per_month = pd.read_csv(dir_data_output + "last_trading_date_monthly.csv")
last_trading_date_per_month = set(last_trading_date_per_month.last_trading_date_per_month)

cur_last_day_per_month = total_df.date.apply(lambda x: x in last_trading_date_per_month)
print(total_df.shape)
total_df = total_df[cur_last_day_per_month]
print(total_df.shape)

total_df.to_csv(dir_data_output + "total_df_monthly.csv",index=False)



"""
get monthly rtn

"""

total_df = pd.read_csv(dir_data_output + "total_df_monthly.csv")

def get_rtn_for_sgl_stock(x,price_name = "close",date_name = "date"):
    x = copy.deepcopy(x[[price_name,date_name]])
    x = x.sort_values(date_name)
    x["rtn"] = x[price_name].pct_change()
    return x

monthly_rtn = total_df.groupby("stock_code").apply(lambda x: get_rtn_for_sgl_stock(x))
monthly_rtn.head()
monthly_rtn = monthly_rtn.reset_index()
monthly_rtn.head()

monthly_rtn = monthly_rtn[["stock_code","date","rtn"]]
monthly_rtn = monthly_rtn.rename(columns = {"rtn":"monthly_rtn"})
monthly_rtn.head()

total_df = pd.merge(total_df,monthly_rtn,how = "left")
total_df.columns
total_df.to_csv(dir_data_output + "total_df_monthly.csv",index=False)


"""

1. add more factor, total number of factors should be greater than 40, trading related factors should be more than 10

2. dealing with abnormal value

3. industry standardization
"""
# total_df = pd.read_csv(dir_data_output + 'total_df_monthly.csv')
#
# industry_df = pd.read_excel(dir_data_raw_market + 'industry.xlsx')
# industry_df.index = industry_df.id
# del industry_df['name']
# del industry_df['id']
#
# industry_df = industry_df.stack()
# industry_df = industry_df.reset_index()
# industry_df = industry_df.rename(columns = {'id': 'stock_code', 'level_1': 'month', 0: 'industry'})
#
# industry_df['month'] = industry_df['month'].apply(lambda x:x[8:12] + '-' + x[13:15] )
#
# total_df = pd.merge(total_df, industry_df, how = 'left')
#
# fct_name = 'ratio_total_asset_growth'
# tmp_df = total_df[[fct_name, 'month', 'industry']]
#
# tmp_df = tmp_df.groupby(['month', 'industry']).apply(lambda x: (x[fct_name].mean(), x[fct_name].std()))
# tmp_df = tmp_df.reset_index()
# tmp_df = tmp_df.rename(columns = {0: '%s_mean_std'%fct_name})
# total_df = pd.merge(total_df, tmp_df, how = 'left')
#
# # total_df = total_df.fillna(int(0))
# #
# # print(total_df[fct_name])
# # print(total_df['%s_mean_std'%fct_name][0])
# # print(total_df['%s_mean_std'%fct_name][1])
# # def get_standardization(x):
# #     return (x[fct_name] - x['%s_mean_std'%fct_name][0])/x['%s_mean_std'%fct_name][1]
#
#
#
# total_df['%s_scaled'%fct_name] = total_df.apply(lambda x: (x[fct_name] - x['%s_mean_std'%fct_name][0])/x['%s_mean_std'%fct_name][1])
#
# fct_names = ['ratio_ROA', 'ratio_ROE']
#
# for fct_name in fct_names:
#     tmp_df = total_df[[fct_name, 'month', 'industry']]
#     tmp_df = tmp_df.groupby(['month', 'industry']).apply(lambda x: (x[fct_name].mean(), x[fct_name].std()))
#     tmp_df = tmp_df.reset_index()
#     tmp_df = tmp_df.rename(columns = {0: '%s_mean_std'%fct_name})
#     total_df = pd.merge(total_df, tmp_df, how='left')
#     total_df['%s_scaled'%fct_name] = total_df.apply(lambda x: (x[fct_name] - x['%s_mean_std'%fct_name][0])/x['%s_mean_std'%fct_name][1])
"""
4. next_rtn
"""


total_df["monthly_next_rtn"] = total_df.groupby("stock_code").monthly_rtn.shift(-1)
total_df.to_csv(dir_data_output + "total_df_monthly.csv",index=False)


"""
test
"""

print(total_df.head())
print(total_df.columns)
print(total_df['monthly_next_rtn'])
# mean,std
# single stock:
# fct - mean / std
# industry ,industry mean,industtry std
