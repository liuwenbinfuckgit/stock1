import tushare as ts
import numpy as np
import pandas as pd
import datetime as date
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
#一次性获取全部日k线数据
try:
    orgTrad['open'] = orgTrad.apply(lambda x: ts.get_hist_data(x['code'], start=(
            date.datetime.now() + date.timedelta(days=-1)).strftime('%Y-%m-%d')).reset_index()['open'],
                                    axis=1)
except Exception as result:
    print(result)
# print(ts.get_today_all())
print()
with pd.ExcelWriter(r'G:\stock\today_market_price.xlsx') as writer:
    orgTrad.to_excel(writer, sheet_name='今日机构增减持')