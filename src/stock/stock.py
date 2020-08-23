import tushare as ts
import numpy as np
import pandas as pd
import datetime as date
import baostock as bs
lg = bs.login()

start_date_baostock = (date.datetime.now() + date.timedelta(days=-1)).strftime('%Y-%m-%d')
end_date_baostock = (date.datetime.now()).strftime('%Y-%m-%d')

#获取当日所有股票行情 code    name     changepercent  trade   open   high    low  settlement
today_price = ts.get_today_all()
today_price_columns= {'code':'代码',
'name':'名称',
'changepercent':'涨跌幅',
'trade':'现价',
'open':'开盘价',
'high':'最高价',
'low':'最低价',
'settlement':'昨日收盘价',
'volume':'成交量',
'turnoverratio':'换手率',
'amount':'成交金额',
'per':'市盈率',
'pb':'市净率',
'mktcap':'总市值',
'nmc':'流通市值'}
today_price.rename(columns=today_price_columns,inplace=True)
today_price['现价与市盈率、市净率之和'] = today_price.apply(lambda x: x['现价']+x['市盈率']+x['市净率'],
                                axis=1)
today_price = today_price.sort_values(by=['现价与市盈率、市净率之和'],ascending=[True])

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
k_lines_result_list =[]
k_lines_columns={'date':'交易所行情日期',
'code':'证券代码',
'open':'开盘价',
'high':'最高价',
'low':'最低价',
'close':'收盘价',
'preclose':'前收盘价:见表格下方详细说明',
'volume':'成交量（累计 单位：股）',
'amount':'成交额（单位：人民币元）',
'adjustflag':'复权状态(1：后复权， 2：前复权，3：不复权）',
'turn':'换手率:[指定交易日的成交量(股)/指定交易日的股票的流通股总股数(股)]*100%',
'tradestatus':'交易状态(1：正常交易 0：停牌）',
'pctChg':'涨跌幅（百分比）:日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%',
'peTTM':'滚动市盈率:(指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/归属母公司股东净利润TTM',
'pbMRQ':'市净率:(指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具)',
'psTTM':'滚动市销率:(指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价*截至当日公司总股本)/营业总收入TTM',
'pcfNcfTTM':'滚动市现率:(指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/现金以及现金等价物净增加额TTM',
'isST':'是否ST股，1是，0否'}
def k_lines(code):
    rs = bs.query_history_k_data_plus(code,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date=start_date_baostock, end_date=end_date_baostock,
                                      frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
    k_lines_result_list.append(data_list)

#### 估值信息 ####
# bs_result.columns=['交易日期','股票代码','今收盘价','滚动市盈率','市净率','滚动市销率','滚动市现率']
# bs_result_columns = {'code':'证券代码','dividPreNoticeDate':'预批露公告日','dividAgmPumDate':'股东大会公告日期','dividPlanAnnounceDate':'预案公告日','dividPlanDate':'分红实施公告日','dividRegistDate':'股权登记告日','dividOperateDate':'除权除息日期','dividPayDate':'派息日','dividStockMarketDate':'红股上市交易日','dividCashPsBeforeTax':'每股股利税前:派息比例分子(税前)/派息比例分母','dividCashPsAfterTax':'每股股利税后:派息比例分子(税后)/派息比例分母','dividStocksPs':'每股红股','dividCashStock':'分红送转:每股派息数(税前)+每股送股数+每股转增股本数','dividReserveToStockPs':'每股转增资本'}
# bs_result.rename(bs_result_columns,inplace=True)

stocks=ts.get_stock_basics()
stocks.head()
df = pd.DataFrame(stocks)
stocksName = df.loc[:,['name']]
# df.count()
ts.get_h_data('600726')
orgTrad = ts.inst_detail()
orgTrad = orgTrad.sort_values(by=['bamount','samount'],ascending=[False,True])
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
    # bs_result.to_excel(writer, sheet_name='估值信息')
    today_price.to_excel(writer, sheet_name='今日行情')
bs.logout()
