import tushare as ts
import numpy as np
import pandas as pd
stocks=ts.get_stock_basics()
stocks.head()
df = pd.DataFrame(stocks)
stocksName = df.loc[:,['name']]
stocksName.head()
df.count()