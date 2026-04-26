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

主要依赖包括 `numpy`、`scipy`、`pandas`、`matplotlib`、`jupyter` 和 `pytest`。

## 4. 运行测试

```powershell
pytest
```

测试使用小规模参数，不运行论文正文 thesis preset 的大规模实验。

## 5. 复现论文正文实验

### KS 距离收敛实验

对应论文第 4.2 节：

```powershell
python -m src.experiments --experiment ks --preset thesis
```

输出：

```text
results/tables/ks_convergence.csv
results/figures/ks_convergence.png
```

### 矩量收敛实验

对应论文第 4.3 节：

```powershell
python -m src.experiments --experiment moments --preset thesis
```

输出：

```text
results/tables/moment_convergence.csv
results/figures/moment_convergence.png
```

### 数值普适性实验

对应论文第 4.4 节：

```powershell
python -m src.experiments --experiment universality --preset thesis
```

输出：

```text
results/figures/universality_comparison.png
```

### LSS-CLT 二维数值实验

对应论文第 5 章：

```powershell
python -m src.experiments --experiment lss_clt --preset thesis
```

输出：

```text
results/tables/lss_clt_summary.csv
results/figures/lss_clt_2d_scatter.png
results/figures/lss_clt_2d_mean.png
results/figures/lss_clt_2d_cov.png
```

说明：LSS-CLT thesis preset 计算量较大，其中 `num_trials=1000` 表示每个矩阵维数下重复模拟 1000 次。

## 6. 自定义参数运行

仍可使用自定义参数进行较小规模测试，例如：

```powershell
python -m src.experiments --experiment lss_clt --matrix-sizes 30,50,80 --num-trials 30 --dist gaussian --seed 42
```

也可以使用指定参数复现某次展示实验：

```powershell
python -m src.experiments --experiment lss_clt --matrix-sizes 100,200,400 --num-trials 2000 --dist gaussian --seed 0
```

## 7. 查看结果

- `results/figures` 保存图像；
- `results/tables` 保存 CSV 表格；
- `assets/` 中保存 README 展示用图片；
- `results/` 默认不提交到 GitHub。

## 8. 常见问题

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
