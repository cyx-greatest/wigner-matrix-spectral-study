# 理论说明

## 1. Wigner 矩阵

论文中考虑的 Wigner 矩阵是随矩阵维数 `N` 变化的一列随机矩阵 `X_N`。其基本构造为：

- 构造 `N x N` 矩阵 `X_N`；
- 非对角元由独立同分布随机变量 `Z_ij` 构成；
- 对角元由随机变量 `Y_i` 构成；
- 矩阵元素按 `1/sqrt(N)` 标准化；
- 实值情形下 `X_N` 为实对称矩阵，复值情形下为复厄米矩阵。

## 2. 经验谱分布

设 `X_N` 的特征值为：

```text
lambda_1^(N), ..., lambda_N^(N)
```

经验谱分布定义为：

```text
L_N = (1/N) sum_{i=1}^N delta_{lambda_i^(N)}
```

经验谱分布用于描述随机矩阵特征值的整体分布。

## 3. Wigner 半圆律

标准半圆律密度为：

```text
rho_sigma(x) = 1/(2*pi) * sqrt(4 - x^2) * 1_{[-2,2]}(x)
```

Wigner 半圆律表明，适当归一化的 Wigner 矩阵经验谱分布 `L_N` 在弱收敛意义下收敛到半圆分布 `sigma`。

## 4. 组合式矩量法

论文中半圆律证明的主要思路是组合式矩量法：

- 将经验谱分布的收敛问题转化为矩量收敛；
- 计算 `E tr(X_N^k)`；
- 用 closed words、Wigner words 和关联图进行组合计数；
- 主导贡献来自与树结构对应的 Wigner words；
- 最终偶数阶矩对应 Catalan 数，奇数阶矩为 `0`。

## 5. Catalan 数与 Dyck 路

Catalan 数定义为：

```text
C_k = 1/(k+1) * binom(2k,k)
```

半圆分布矩量满足：

```text
m_{2k} = C_k
m_{2k+1} = 0
```

论文中通过 Dyck 路与 Wigner word 的对应关系解释 Catalan 数在半圆律矩量中的出现。

## 6. 线性谱统计量

对测试函数 `f`，线性谱统计量定义为：

```text
<L_N, f> = integral f dL_N = (1/N) sum_i f(lambda_i)
```

线性谱统计量用于研究经验谱分布在测试函数下的平均行为及其波动。

## 7. 线性谱统计量中心极限定理

为了研究谱分布围绕半圆律的二阶波动，论文中考察：

```text
G_N(f) = N(<L_N, f> - <sigma, f>)
```

在适当矩条件和光滑性条件下，线性谱统计量的有限维分布收敛为高斯向量。

## 8. 本项目数值实验对应关系

本项目代码与理论内容的对应关系如下：

- `src/wigner_matrix.py`：Wigner 矩阵生成与特征值计算；
- `src/semicircle_law.py`：半圆律密度、分布函数与 KS 距离；
- `src/moments.py`：Catalan 数与矩量收敛；
- `src/lss_clt.py`：二维线性谱统计量 CLT 实验；
- `src/experiments.py`：统一实验入口。
