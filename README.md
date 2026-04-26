# Wigner Matrix Spectral Study

本项目用于整理本科毕业论文《Wigner 矩阵谱分布性质的理论分析与数值研究》中的理论内容与数值实验，目标是形成一个可复现的 Python 科研项目。

## 项目简介

项目围绕 Wigner 矩阵的谱分布性质展开，关注经验谱分布、Wigner 半圆律、组合式矩量法、Catalan 数、Dyck 路、线性谱统计量及其中心极限定理。

## 研究内容

- Wigner 矩阵与经验谱分布
- Wigner 半圆律及其数值验证
- 组合式矩量法、Catalan 数与 Dyck 路
- 矩量收敛与 Catalan 数理论值对比
- 线性谱统计量与二维 LSS-CLT 数值实验

## LSS-CLT 实验

论文第 5 章对应“Wigner 矩阵线性谱统计量中心极限定理的二维数值实验设计”。实验选取测试函数：

```text
f1(x) = x^2
f2(x) = x^4
```

线性谱统计量为：

```text
L_N(f) = (1/N) sum_i f(lambda_i)
G_N(x^2) = N(L_N(x^2) - 1)
G_N(x^4) = N(L_N(x^4) - 2)
```

其中半圆律矩量满足 `S(x^2)=1`、`S(x^4)=2`。理论参考均值和协方差矩阵为：

```text
mu = (0, 1)^T
Sigma = [[4, 16],
         [16, 72]]
```

正式复现命令：

```bash
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

主要输出：

- `results/tables/lss_clt_summary.csv`
- `results/figures/lss_clt_scatter.png`
- `results/figures/lss_clt_mean_convergence.png`
- `results/figures/lss_clt_cov_convergence.png`

## 项目结构

```text
src/        Python 源代码
tests/      pytest 测试
docs/       理论说明、实验设计与复现说明
paper/      论文相关摘要与说明
notebooks/  交互式实验笔记
assets/     图像或静态资源
results/    实验输出结果
```
