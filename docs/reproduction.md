# 项目复现说明

## 1. 克隆或打开项目

用户可以从 GitHub 克隆本仓库，也可以直接在本地打开项目文件夹。后续命令均应在项目根目录下运行。

## 2. 创建 Python 虚拟环境

Windows PowerShell 命令：

```powershell
python -m venv .venv
.venv\Scripts\activate
```

激活成功后，终端命令行前面应出现 `(.venv)`。

## 3. 安装依赖

```powershell
pip install -r requirements.txt
```

主要依赖包括：

```text
numpy
scipy
pandas
matplotlib
jupyter
pytest
```

## 4. 运行测试

```powershell
pytest
```

测试用于检查：

- Wigner 矩阵生成；
- 半圆律密度函数；
- Catalan 数与矩量函数；
- 数值实验入口；
- LSS-CLT 相关函数。

## 5. 复现实验一：半圆律谱直方图

```powershell
python -m src.experiments --experiment semicircle --n 300 --dist gaussian --seed 42
```

输出：

```text
results/figures/semicircle_histogram.png
```

## 6. 复现实验二：KS 距离收敛

```powershell
python -m src.experiments --experiment ks --matrix-sizes 50,100,200 --num-trials 5 --dist gaussian --seed 42
```

输出：

```text
results/tables/ks_convergence.csv
```

## 7. 复现实验三：矩量收敛

```powershell
python -m src.experiments --experiment moments --matrix-sizes 50,100,200 --orders 2,4,6 --num-trials 5 --dist gaussian --seed 42
```

输出：

```text
results/tables/moment_convergence.csv
results/figures/moment_convergence.png
```

## 8. 复现实验四：数值普适性

```powershell
python -m src.experiments --experiment universality --n 300 --seed 42
```

输出：

```text
results/figures/universality_gaussian.png
results/figures/universality_rademacher.png
results/figures/universality_uniform.png
```

## 9. 复现实验五：LSS-CLT 二维数值实验

正式展示命令：

```powershell
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

输出：

```text
results/tables/lss_clt_summary.csv
results/figures/lss_clt_scatter.png
results/figures/lss_clt_mean_convergence.png
results/figures/lss_clt_cov_convergence.png
```

说明：

- 该实验计算量较大；
- `num-trials=2000` 表示每个矩阵维数下重复模拟 `2000` 次；
- 如果电脑运行较慢，可以先用较小参数测试：

```powershell
python -m src.experiments --experiment lss_clt --matrix-sizes 30,50,80 --num-trials 30 --dist gaussian --seed 42
```

## 10. 查看结果

- `results/figures` 保存图像；
- `results/tables` 保存 CSV 表格；
- `assets/` 中保存 README 展示用图片；
- `results/` 默认不提交到 GitHub。

## 11. 常见问题

### 1. `ModuleNotFoundError: No module named 'src'`

解决：请在项目根目录运行命令。

### 2. PowerShell 无法激活虚拟环境

解决：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

然后重新运行：

```powershell
.venv\Scripts\activate
```

### 3. LSS-CLT 运行较慢

解决：先降低 `matrix-sizes` 或 `num-trials`。

### 4. LSS-CLT 均值图不单调收敛

说明：有限样本下存在 Monte Carlo 误差，尤其 `G_N(x^4)` 波动较大，因此不应期待严格单调收敛。
