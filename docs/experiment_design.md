# 数值实验设计

## 1. 实验目标

本项目数值实验严格围绕论文《Wigner 矩阵谱分布性质的理论分析与数值研究》展开，用于验证：

- 经验谱分布向 Wigner 半圆律的收敛；
- 经验矩量向半圆分布矩量的收敛；
- 不同矩阵元素分布下半圆律的数值普适性；
- 二维线性谱统计量中心极限定理的数值表现。

## 2. Wigner 矩阵生成

实验中生成 `N x N` 实对称 Wigner 矩阵：

- 非对角元独立同分布；
- 均值为 `0`，方差为 `1`；
- 对角元独立生成；
- 矩阵整体按 `1/sqrt(N)` 标准化；
- 支持 Gaussian、Rademacher、Uniform `(-sqrt(3), sqrt(3))` 三类条目分布。

## 3. KS 距离收敛实验

对应论文第 4.2 节。对每个矩阵维数 `N` 重复生成 20 次 Wigner 矩阵，计算每次的 KS 距离：

```text
D_KS(N) = sup_x |F_N(x) - F_sc(x)|
```

论文正文参数：

```text
matrix_sizes = (50, 100, 200, 400, 800, 1600)
num_trials = 20
dist = "gaussian"
```

输出 `mean_ks_distance` 和 `std_ks_distance`，图像展示均值，并用误差棒表示标准差。`x` 轴使用 log scale，`y` 轴也使用 log scale，以对应论文中对数刻度下下降的展示方式。

复现命令：

```bash
python -m src.experiments --experiment ks --preset thesis
```

输出：

```text
results/tables/ks_convergence.csv
results/figures/ks_convergence.png
```

## 4. 矩量收敛实验

对应论文第 4.3 节。经验矩量为：

```text
m_k^N = (1/N) sum_i lambda_i^k
```

半圆分布理论矩量满足：奇数阶为 `0`，偶数阶为 Catalan 数：

```text
C_k = 1/(k+1) * binom(2k,k)
```

论文正文参数：

```text
matrix_sizes = (50, 100, 200, 400, 800, 1600)
orders = (2, 4, 6)
num_trials = 20
dist = "gaussian"
```

图像展示不同 `order` 下经验均值随 `N` 的变化，并叠加理论水平线。`x` 轴使用 log scale。

复现命令：

```bash
python -m src.experiments --experiment moments --preset thesis
```

输出：

```text
results/tables/moment_convergence.csv
results/figures/moment_convergence.png
```

## 5. Wigner 半圆律的数值普适性实验

对应论文第 4.4 节。分别使用 Gaussian、Rademacher、Uniform `(-sqrt(3), sqrt(3))` 三种条目分布，每种分布重复生成 10 个独立实对称 Wigner 矩阵，汇总特征值并绘制归一化直方图。

论文正文参数：

```text
n = 400
repeats = 10
distributions = ("gaussian", "rademacher", "uniform")
seed = 42
```

图像采用 `2 x 2` 子图：

- Gaussian entries；
- Rademacher entries；
- Uniform entries；
- Overlay comparison。

复现命令：

```bash
python -m src.experiments --experiment universality --preset thesis
```

输出：

```text
results/figures/universality_comparison.png
```

## 6. 二维线性谱统计量中心极限定理实验

对应论文第 5 章。测试函数为：

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

理论参考值：

```text
mean = [0, 1]
cov = [[4, 16], [16, 72]]
```

论文正文参数：

```text
matrix_sizes = (50, 100, 200, 400, 800)
num_trials = 1000
dist = "gaussian"
```

实验对每个 `N` 重复 1000 次，记录二维样本点 `(G_N(x^2), G_N(x^4))`。图像包括不同 `N` 下的二维散点图、样本均值点、协方差椭圆、样本均值向量变化和样本协方差矩阵三个独立分量变化。

复现命令：

```bash
python -m src.experiments --experiment lss_clt --preset thesis
```

输出：

```text
results/tables/lss_clt_summary.csv
results/figures/lss_clt_2d_scatter.png
results/figures/lss_clt_2d_mean.png
results/figures/lss_clt_2d_cov.png
```

## 7. 快速测试与自定义参数

pytest 不运行 thesis preset 的大规模实验。快速测试使用小规模参数，以检查函数和文件输出是否正常。

自定义参数示例：

```bash
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

## 8. 数值结果解释注意事项

- 数值实验用于有限维模拟验证理论趋势；
- 谱直方图不会完全等于半圆律密度；
- KS 距离和矩量误差不一定严格单调下降；
- LSS-CLT 中样本均值和协方差矩阵受 Monte Carlo 误差影响；
- `G_N(x^4)` 的波动通常比 `G_N(x^2)` 更明显；
- 不应把有限样本图像理解为严格数学证明。
