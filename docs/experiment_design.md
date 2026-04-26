# Experiment Design

## 谱直方图与半圆律密度对比

生成 Wigner 矩阵，计算其全部特征值，绘制归一化谱直方图，并叠加标准半圆律密度：

```text
rho_sc(x) = 1/(2*pi) * sqrt(4 - x^2) * 1_{[-2,2]}(x)
```

## KS 距离收敛实验

计算经验谱分布函数 `F_N` 与半圆律理论分布函数 `F_sc` 之间的 KS 距离：

```text
D_KS(N) = sup_x |F_N(x) - F_sc(x)|
```

通过不同矩阵维数 `N` 下的平均 KS 距离观察经验谱分布向半圆律的收敛趋势。

## 矩量收敛与 Catalan 数验证

计算经验矩量：

```text
m_k^N = (1/N) * sum_i lambda_i^k
```

并与半圆律理论矩量比较。半圆分布奇数阶矩为 `0`，偶数阶矩为 Catalan 数。

## 数值普适性实验

在 `gaussian`、`rademacher`、`uniform` 三种矩阵条目分布下重复谱直方图实验，观察 Wigner 半圆律的数值普适性。

## 二维线性谱统计量 LSS-CLT 实验

本实验对应论文第 5 章“Wigner 矩阵线性谱统计量中心极限定理的二维数值实验设计”。

测试函数选为：

```text
f1(x) = x^2
f2(x) = x^4
```

对 Wigner 矩阵特征值 `lambda_i`，定义：

```text
L_N(f) = (1/N) sum_i f(lambda_i)
G_N(x^2) = N(L_N(x^2) - 1)
G_N(x^4) = N(L_N(x^4) - 2)
```

其中半圆律矩量满足：

```text
S(x^2) = 1
S(x^4) = 2
```

理论参考均值向量与协方差矩阵为：

```text
mu = (0, 1)^T
Sigma = [[4, 16],
         [16, 72]]
```

正式展示/复现命令：

```bash
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

参数含义：

- `--matrix-sizes 100,200,400` 表示矩阵维数 `N` 依次取 `100`、`200`、`400`。
- `--num-trials 2000` 表示每个 `N` 下独立重复模拟 `2000` 次。
- `--dist gaussian` 表示矩阵条目采用高斯分布。
- `--seed 0` 表示固定随机种子以便复现。

主要输出：

- `results/tables/lss_clt_summary.csv`
- `results/figures/lss_clt_scatter.png`
- `results/figures/lss_clt_mean_convergence.png`
- `results/figures/lss_clt_cov_convergence.png`

结果解释时应注意：样本均值不一定随 `N` 单调逼近理论值；有限样本下会受到 Monte Carlo 误差影响；`G_N(x^4)` 的波动通常比 `G_N(x^2)` 更明显。因此应关注整体稳定趋势，而不是要求每个点严格单调收敛。
