# Reproduction Guide

## 环境配置

建议使用独立 Python 虚拟环境，以保证依赖版本和实验环境可复现。

## 安装依赖

依赖项将在后续写入 `requirements.txt`。配置完成后可通过包管理工具安装项目所需依赖。

## 运行实验

实验入口将在 `src/experiments.py` 中组织，包括半圆律实验、矩量实验和线性谱统计量 CLT 实验。

## 生成图像

图像生成函数将在 `src/visualization.py` 中维护，输出文件建议统一保存到 `results/` 目录。
