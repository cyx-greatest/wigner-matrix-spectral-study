# Reproduction Guide

## 环境配置

建议使用独立 Python 虚拟环境，以保证依赖版本和实验环境可复现。

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 安装依赖

在虚拟环境中安装项目依赖：

```powershell
pip install -r requirements.txt
```

## 运行测试

```powershell
python -m pytest tests
```

## 运行 LSS-CLT 实验

论文第 5 章对应“Wigner 矩阵线性谱统计量中心极限定理的二维数值实验设计”。正式复现命令为：

```bash
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

实验设定为：

```text
f1(x) = x^2
f2(x) = x^4
L_N(f) = (1/N) sum_i f(lambda_i)
G_N(x^2) = N(L_N(x^2) - 1)
G_N(x^4) = N(L_N(x^4) - 2)
```

其中半圆律矩量满足 `S(x^2)=1`、`S(x^4)=2`。理论参考均值向量和协方差矩阵为：

```text
mu = (0, 1)^T
Sigma = [[4, 16],
         [16, 72]]
```

参数含义：

- `--matrix-sizes 100,200,400` 表示矩阵维数 `N`。
- `--num-trials 2000` 表示每个 `N` 下独立重复模拟 `2000` 次。
- `--dist gaussian` 表示矩阵条目采用高斯分布。
- `--seed 0` 表示固定随机种子以便复现。

## 输出文件

LSS-CLT 实验会生成：

- `results/tables/lss_clt_summary.csv`
- `results/figures/lss_clt_scatter.png`
- `results/figures/lss_clt_mean_convergence.png`
- `results/figures/lss_clt_cov_convergence.png`

## 结果解释

样本均值不一定随 `N` 单调逼近理论值。有限样本下会受到 Monte Carlo 误差影响，且 `G_N(x^4)` 的波动通常比 `G_N(x^2)` 更明显。因此应关注样本均值向量和样本协方差矩阵的整体稳定趋势，而不是要求每个点严格单调收敛。
