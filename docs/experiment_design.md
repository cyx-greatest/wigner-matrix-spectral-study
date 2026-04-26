# 数值实验设计

## 1. 实验目标

本项目的数值实验用于验证 Wigner 矩阵谱分布的典型性质，包括：

- 经验谱分布向半圆律的收敛；
- 经验矩量向半圆分布矩量的收敛；
- 不同矩阵元素分布下半圆律的数值普适性；
- 二维线性谱统计量中心极限定理的数值表现。

## 2. Wigner 矩阵生成

实验中生成 `N x N` 实对称 Wigner 矩阵。其设置为：

- 非对角元独立同分布；
- 均值为 `0`，方差为 `1`；
- 对角元独立生成；
- 整体按 `1/sqrt(N)` 标准化；
- 支持 Gaussian、Rademacher、Uniform 三类条目分布。

## 3. 实验一：谱直方图与半圆律密度对比

该实验步骤为：

- 生成一个 `N x N` Wigner 矩阵；
- 计算全部特征值；
- 绘制归一化谱直方图；
- 在同一图中叠加半圆律密度：

```text
rho_sc(x) = 1/(2*pi) * sqrt(4 - x^2) * 1_{[-2,2]}(x)
```

对应命令：

```bash
python -m src.experiments --experiment semicircle --n 300 --dist gaussian --seed 42
```

## 4. 实验二：KS 距离收敛实验

该实验步骤为：

- 对不同矩阵维数 `N` 重复生成 Wigner 矩阵；
- 计算经验谱分布函数 `F_N`；
- 与半圆律理论分布函数 `F_sc` 比较；
- 使用 KS 距离作为收敛误差指标：

```text
D_KS(N) = sup_x |F_N(x) - F_sc(x)|
```

对应命令：

```bash
python -m src.experiments --experiment ks --matrix-sizes 50,100,200 --num-trials 5 --dist gaussian --seed 42
```

## 5. 实验三：矩量收敛与 Catalan 数验证

对每个矩阵维数 `N`，计算经验矩量：

```text
m_k^N = (1/N) sum_i lambda_i^k
```

半圆分布理论矩量满足：

- 奇数阶矩为 `0`；
- 偶数阶矩 `m_{2k}=C_k`。

Catalan 数为：

```text
C_k = 1/(k+1) * binom(2k,k)
```

对应命令：

```bash
python -m src.experiments --experiment moments --matrix-sizes 50,100,200 --orders 2,4,6 --num-trials 5 --dist gaussian --seed 42
```

## 6. 实验四：Wigner 半圆律的数值普适性

该实验步骤为：

- 分别使用 Gaussian、Rademacher、Uniform 三种条目分布；
- 生成 Wigner 矩阵并计算特征值；
- 比较不同条目分布下谱直方图与半圆律密度的接近情况；
- 用于展示半圆律对具体条目分布的数值普适性。

对应命令：

```bash
python -m src.experiments --experiment universality --n 300 --seed 42
```

## 7. 实验五：二维线性谱统计量中心极限定理实验

严格使用论文中的设定。

测试函数：

```text
f1(x) = x^2
f2(x) = x^4
```

线性谱统计量：

```text
L_N(f) = (1/N) sum_i f(lambda_i)
```

中心化二维向量：

```text
G_N(x^2) = N(L_N(x^2) - 1)
G_N(x^4) = N(L_N(x^4) - 2)
```

理论参考均值向量：

```text
mu = (0,1)^T
```

理论参考协方差矩阵：

```text
Sigma = [[4,16],
         [16,72]]
```

实验考察：

- 二维样本散点图；
- 样本均值向量随 `N` 的变化；
- 样本协方差矩阵随 `N` 的变化；
- 有限样本下 `G_N(x^4)` 波动通常比 `G_N(x^2)` 更明显。

正式展示命令：

```bash
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

## 8. 输出文件说明

主要输出文件包括：

```text
results/figures/semicircle_histogram.png
results/tables/ks_convergence.csv
results/tables/moment_convergence.csv
results/figures/moment_convergence.png
results/figures/universality_gaussian.png
results/figures/universality_rademacher.png
results/figures/universality_uniform.png
results/tables/lss_clt_summary.csv
results/figures/lss_clt_scatter.png
results/figures/lss_clt_mean_convergence.png
results/figures/lss_clt_cov_convergence.png
```

## 9. 数值结果解释注意事项

- 数值实验用于有限维模拟验证理论趋势；
- 谱直方图不会完全等于半圆律密度；
- KS 距离和矩量误差不一定严格单调下降；
- LSS-CLT 中样本均值和协方差矩阵受 Monte Carlo 误差影响；
- 不应把有限样本图像理解为严格数学证明。
