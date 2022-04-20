# # 1. 读取数据
# 导入 pandas 读取数据
import pandas as pd
import numpy as np

# 读取数据
data = pd.read_csv("./data/peach_spectra_brix.csv")
data[:5]

# # 2. 数据处理
# m * n 
print("数据矩阵 data.shape:",data.shape)

# 50个样本， 600个 波段 第一列是 桃子糖度值 需要分离开
X = data.values[:,1:] 
# 等同操作
# X = data.drop(['Brix'], axis=1)

y = data.values[:,0]
# 等同操作
# y = data.loc[:,'Brix'].values
print(f"X.shape:{X.shape}, y.shape:{y.shape}")

# # 3. 工具导入
import CARS

# # 4. 建模筛选
lis = CARS.CARS_Cloud(X,y)
print("获取波段数:",len(lis))
print(lis)


# # 5. 导出数据
X_ = X[:,lis]
X_.shape

