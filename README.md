# Wigner Matrix Spectral Study

本项目用于整理本科毕业论文《Wigner 矩阵谱分布性质的理论分析与数值研究》中的理论内容与数值实验，目标是形成一个可复现的 Python 科研项目。

## 项目简介

项目围绕 Wigner 矩阵的谱分布性质展开，关注经验谱分布、Wigner 半圆律、组合式矩量法、Catalan 数、Dyck 路、线性谱统计量及其中心极限定理，并为后续数值实验复现预留代码结构。

## 研究内容

- Wigner 矩阵与经验谱分布
- Wigner 半圆律及其数值验证
- 组合式矩量法、Catalan 数与 Dyck 路
- 线性谱统计量与 LSS-CLT
- 谱分布、矩量收敛和数值普适性实验

## 项目结构

```text
src/        Python 源代码骨架
tests/      pytest 测试骨架
docs/       理论说明、实验设计与复现说明
paper/      论文相关摘要与说明
notebooks/  交互式实验笔记
assets/     图像或静态资源
results/    实验输出结果
```

## 后续计划

- 配置 Python 科研计算环境
- 实现 Wigner 矩阵生成与谱计算函数
- 实现半圆律、矩量和 LSS-CLT 数值实验
- 补充测试、图像生成脚本与复现实验说明
