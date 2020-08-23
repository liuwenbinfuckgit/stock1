import tushare as ts
import numpy as np
import pandas as pd
import datetime as date
import baostock as bs
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)
rs = bs.query_history_k_data_plus("sh.600000",
    "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
    start_date='2019-01-01', end_date='2019-12-31',
    frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
#### 打印结果集 ####
result_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    result_list.append(rs.get_row_data())
bs_result = pd.DataFrame(result_list, columns=rs.fields)

stocks=ts.get_stock_basics()
stocks.head()
df = pd.DataFrame(stocks)

stocksName = df.loc[:,['name']]
# df.count()
print(stocksName.head())
ts.get_h_data('600726')
orgTrad = ts.inst_detail()
orgTrad = orgTrad.sort_values(by=['bamount','samount'],ascending=[False,True])
print(orgTrad)
#一次性获取全部日k线数据  42a02c36c41bd06d0365c2ad7de7d1b78427cc58329372f9d480a4d1
try:
    orgTrad['open'] = orgTrad.apply(lambda x: ts.get_hist_data(x['code'], start=(
            date.datetime.now() + date.timedelta(days=-1)).strftime('%Y-%m-%d')).reset_index()['open'],
                                    axis=1)
    # orgTrad.rename(columns={'code':'股票代码'},inplace=True)
    orgTrad.columns=['股票代码','股票名字','交易日期','机构席位买入额(万)','机构席位卖出额(万)','类型','当日开盘价']
except Exception as result:
    print(result)
# print(ts.get_today_all())
with pd.ExcelWriter(r'G:\stock\today_market_price.xlsx') as writer:
    orgTrad.to_excel(writer, sheet_name='今日机构增减持')
    bs_result.to_excel(writer, sheet_name='baostock测试数据')



bs.logout()
