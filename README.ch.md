# 算法简介

竞争性自适应重加权采样法（competitive adapative reweighted sampling， CARS）是一种结合蒙特卡洛采样与PLS模型回归系数的特征变量选择方法，模仿达尔文理论中的 ”适者生存“ 的原则（Li et al., 2009）。CARS 算法中，每次通过自适应加权采样（adapative reweighted sampling， ARS）保留PLS模型中 回归系数绝对值权重较大的点作为新的子集，去掉权值较小的点，然后基于新的子集建立PLS模型，经过多次计算，选择PLS模型交互验证均方根误差（RMSECV）最小的子集中的波长作为特征波长。

CARS算法的具体过程如下。

1. 采用 蒙特卡洛采样法，每次随机从校正集中选择一定数量（一般为80%）的样本进入建模集，剩余的20%作为预测集建立PLS模型。蒙特卡洛的采样次数（N）需要提前设定。记录每一次采样过程PLS模型中的回归系数的绝对值权重，$|b_i|$为第i个变量的回归系数绝对值，$w_i$为第i个变量的回归系数绝对值权重

   $$
   w_i=|b_i|/\sum_{i=1}^m|b_i|
   $$
   m为每次采样中剩余的变量数。
   
2. 利用指数衰减函数（exponentially decreasing function， EDF）强行去除回归系数绝对值权重相对较小的波长。在第i次基于MC采样建立PLS模型时，根据EDF得到保留的波长点的比例$R_i$为

   $$
   R_i=\mu e^{-k_i}
   $$
   式中，$\mu$和k是常数，可以按照以下两种情况计算。
   
   1. 在一次采样并进行相应计算时，所有的波长都参与了建模分析，因此此时保留的波长点的比例为1。
   
   2. 在最后一次采样在（第N次）完成并进行相应计算时，只剩下两个波长参与PLS建模，此时保留的波长点的比例为 $2/n$，其中$n$是原始波长点数。
      由以上最初及最后一次采样的情况可知，$\mu$和k的计算公式为
      $$
      \mu=(\cfrac{n}{2})^{\cfrac{1}{N-1}},k=\cfrac{ln(\cfrac{n}{n})}{N-1}
      $$
      
   
3. 在每次采样时，都从上一次采样时的变量数中采用自适应加权采样（ARS）选择数量为$R_i * n$个的波长变量，进行PLS建模，计算RMSECV。

4. 在N次采样完成之后，CARS 算法得到了N组候选的特征波长子集，以及对应的RMSECV值，选择RMSECV最小值所对应的波长变量子集为特征波长。
   

说明： 竞争性自适应重加权算法（CARS）是通过自适应重加权采样（ARS）技术选择出PLS模型中回归系数绝对值大的波长点，去掉权重小的波长点，利用交互验证选出RMSECV指最低的子集，可有效寻出最优变量组合。

# 快速使用

## 1.读取数据

```python 
# 导入 pandas 读取数据
import pandas as pd
import numpy as np

# 读取数据
data = pd.read_csv("./data/peach_spectra_brix.csv")
```

## 2. 数据处理

```python
# m * n 
print("数据矩阵 data.shape：",data.shape)

# 50个样本， 600个 波段 第一列是 桃子糖度值 需要分离开
X = data.values[:,1:] 
# 等同操作
#X = data.drop(['Brix'], axis=1)

y = data.values[:,0]
# 等同操作
# y = data.loc[:,'Brix'].values

print(f"X.shape:{X.shape}, y.shape:{y.shape}")
```

## 3. 工具导入

```python
import CARS
```

## 4. 建模筛选

```python
lis = CARS.CARS_Cloud(X,y)
print("获取波段数：",len(lis))
print(lis)
```

## 5. 数据导出

```python 
X_ = X[:,lis]
```

# 注意事项

**cars具有随机性，建议运行五次选取最佳rmsecv及波段数。**

CARS开发使用的PLS 是基于 sklearn 的 NIPALS  并非 MATLAB 的 SIMPLS， 因此 系数趋势图 绘制不理想，暂时砍掉了。除此之外，该版本全部基于python开发完成，与MATLAB存在较大差异在所难免，核心算法思想一致，请自行选择，后续会上传 MATLAB版本 CARS。

示例数据来源：[nirpyresearch.com](https://nirpyresearch.com/)
