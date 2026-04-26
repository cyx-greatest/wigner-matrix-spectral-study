# Wigner Matrix Spectral Distribution: Theory and Numerical Experiments

## 项目简介

本项目基于本科毕业论文《Wigner 矩阵谱分布性质的理论分析与数值研究》，围绕 Wigner 随机矩阵的谱分布性质展开。项目主要研究 Wigner 矩阵的经验谱分布，并通过 Python 数值实验验证 Wigner 半圆律、矩量收敛、数值普适性以及二维线性谱统计量中心极限定理的渐近正态性。

## 研究内容

- Wigner 矩阵与经验谱分布
- Wigner 半圆律
- Catalan 数与矩量收敛
- 谱直方图与半圆律密度对比
- KS 距离收敛实验
- 数值普适性实验
- 二维线性谱统计量中心极限定理实验

## 数学定义

设 `lambda_i` 为 Wigner 矩阵的特征值。经验谱分布定义为：

```text
L_N = (1/N) sum_i delta_{lambda_i}
```

标准半圆律密度为：

```text
rho_sc(x) = 1/(2*pi) * sqrt(4 - x^2) * 1_{[-2,2]}(x)
```

经验矩量定义为：

```text
m_k^N = (1/N) sum_i lambda_i^k
```

半圆分布的奇数阶矩为 `0`，偶数阶矩为 Catalan 数。

二维 LSS-CLT 实验选取测试函数：

```text
f1(x) = x^2
f2(x) = x^4
```

并计算：

```text
G_N(x^2) = N(L_N(x^2) - 1)
G_N(x^4) = N(L_N(x^4) - 2)
```

## 项目结构

```text
src/
tests/
docs/
paper/
notebooks/
assets/
results/
```

## 环境配置

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 实验复现命令

半圆律谱直方图：

```bash
python -m src.experiments --experiment semicircle --n 300 --dist gaussian --seed 42
```

KS 距离收敛实验：

```bash
python -m src.experiments --experiment ks --matrix-sizes 50,100,200 --num-trials 5 --dist gaussian --seed 42
```

矩量收敛实验：

```bash
python -m src.experiments --experiment moments --matrix-sizes 50,100,200 --orders 2,4,6 --num-trials 5 --dist gaussian --seed 42
```

数值普适性实验：

```bash
python -m src.experiments --experiment universality --n 300 --seed 42
```

LSS-CLT 正式展示实验：

```bash
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

## 实验图像展示

![Semicircle Histogram](assets/semicircle_histogram.png)

![Moment Convergence](assets/moment_convergence.png)

![LSS CLT Scatter](assets/lss_clt_scatter.png)

![LSS CLT Mean Convergence](assets/lss_clt_mean_convergence.png)

![LSS CLT Covariance Convergence](assets/lss_clt_cov_convergence.png)

## 结果解释

谱直方图应随矩阵维数增大逐渐接近半圆律密度。经验矩量应向理论半圆律矩量靠近，其中奇数阶矩为 `0`，偶数阶矩由 Catalan 数给出。不同矩阵条目分布下的谱分布应表现出 Wigner 半圆律的数值普适性。

在 LSS-CLT 实验中，样本均值向量和样本协方差矩阵会受到有限样本 Monte Carlo 误差影响。`G_N(x^4)` 的波动通常比 `G_N(x^2)` 更明显。因此，数值结果不应理解为严格单调收敛，而应关注整体稳定趋势。

## 测试

```bash
pytest
```

## 论文说明

`paper/thesis_summary.md` 是论文摘要式说明，不包含个人隐私信息。项目暂不上传含姓名、学号、导师信息的原始论文 PDF。

## 免责声明

本项目用于数学科研学习与数值实验复现，不构成其他用途。
