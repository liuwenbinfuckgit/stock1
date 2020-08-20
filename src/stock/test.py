import tushare as ts
import numpy as np
import pandas as pd
import datetime as date
matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

df = pd.DataFrame(matrix, columns=list('xyz'), index=list('abc'))
df['Col_sum'] = df.apply(lambda  x:x['y'],axis=1)
print(df)