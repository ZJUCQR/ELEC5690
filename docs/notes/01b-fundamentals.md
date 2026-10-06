# 1b: Deep Learning Fundamentals

从医学回归任务出发，理解网络、损失与梯度，再掌握优化、正则化和调试方法。

## 1b.1 从医学回归任务开始

!!! definition "Regression（回归）"
    从输入 $x$ 预测连续数值 $\hat y$。模型不只回答“属于哪一类”，还要估计数值大小。

两个典型例子：

- **Bone Mineral Density（BMD，骨密度）**：输入 X-ray 图像，输出骨密度数值。
- **Left-Ventricular Ejection Fraction（LVEF，左心室射血分数）**：输入超声心动图视频，输出射血分数。

[[slide:01b:8|BMD 与 LVEF]]

二维图像可以写为 $x\in\mathbb R^{H\times W}$，视频增加时间维度 $T$。实际实现时还要明确通道和 batch 维度。

## 1b.2 定义网络：从单层到多层

### 单层全连接网络

对三维输入 $x=(x_1,x_2,x_3)^T$，一个标量输出可以写为：

$$
\hat y=w^Tx+b=w_1x_1+w_2x_2+w_3x_3+b.
$$

$w$ 是权重（weights），$b$ 是偏置（bias）。偏置允许输出整体平移，不必强制经过原点。

[[slide:01b:9|单层全连接网络：输入、权重与偏置]]

### 两层全连接网络

$$
z=W_1x+b_1,\qquad h=\phi(z),\qquad \hat y=W_2h+b_2.
$$

其中 $\phi$ 是激活函数。例如 ReLU：$\phi(z)=\max(0,z)$。

如果输入维数是 $d$，隐藏层宽度是 $m$，输出维数是 $k$，则：

| 参数或变量 | 形状 |
| --- | --- |
| $x$ | $d\times1$ |
| $W_1,b_1$ | $m\times d$，$m\times1$ |
| $h$ | $m\times1$ |
| $W_2,b_2$ | $k\times m$，$k\times1$ |

[[slide:01b:20|两层网络：仿射变换与激活函数交替出现]]

!!! tip "为什么需要非线性？"
    去掉激活函数后，$W_2(W_1x+b_1)+b_2=(W_2W_1)x+(W_2b_1+b_2)$，仍然只是一个仿射变换。单纯堆叠线性层不能得到新的非线性表达能力。

## 1b.3 定义损失：Mean Squared Error

损失函数衡量当前参数下预测与目标之间的差异。对 $M$ 个标量回归样本，采用：

$$
L=\frac1M\sum_{i=1}^{M}(\hat y_i-y_i)^2.
$$

有些教材在前面加 $\frac12$，方便求导；这会改变梯度的常数因子，不改变最优点的位置。本笔记使用上式的约定。

[[slide:01b:10|MSE：从单个样本的误差到整个数据集的平均损失]]

!!! example "补充算例：手算一次参数更新"
    取 $x=(1,2,3)^T$，$w=(0.1,0.2,0.3)^T$，$b=0$，$y=2$。

    预测 $\hat y=1.4$，损失 $L=(1.4-2)^2=0.36$。

    梯度为 $\nabla_wL=2(\hat y-y)x=(-1.2,-2.4,-3.6)^T$，$\partial L/\partial b=-1.2$。

    学习率 $\eta=0.01$ 时，更新得到 $w'=(0.112,0.224,0.336)^T$、$b'=0.012$。此时 $\hat y'=1.58$，损失降为 $0.1764$。

这个算例把网络、损失和优化连成一个完整步骤。

## 1b.4 梯度下降与反向传播

### Gradient Descent（梯度下降）

梯度指向函数局部上升最快的方向。为了减小损失，沿负梯度方向更新：

$$
\theta_{t+1}=\theta_t-\eta\nabla_\theta L(\theta_t).
$$

学习率（learning rate）$\eta$ 决定每次走多远：太大可能震荡甚至发散，太小则训练缓慢。

| 名称 | 一次更新使用的数据 | 特点 |
| --- | --- | --- |
| Full-batch GD | 全部训练样本 | 梯度稳定，单次更新开销大 |
| SGD（严格定义） | 一个样本 | 更新频繁，随机性较强 |
| Mini-batch SGD | 一小批样本 | 实践中常简称 SGD |

**Epoch** 表示遍历一次训练集；**iteration / step** 表示一次参数更新。二者不能混用。

### Backpropagation（反向传播）

反向传播利用链式法则，在计算图上从输出向输入传播梯度。它负责“算梯度”；优化器负责“按梯度更新参数”。

对前面的两层网络，标量输出、单样本 MSE 有：

$$
\delta_2=2(\hat y-y),\qquad
\delta_1=(W_2^T\delta_2)\odot\phi'(z).
$$

$$
\frac{\partial L}{\partial W_2}=\delta_2h^T,\quad
\frac{\partial L}{\partial b_2}=\delta_2,\quad
\frac{\partial L}{\partial W_1}=\delta_1x^T,\quad
\frac{\partial L}{\partial b_1}=\delta_1.
$$

这里 $\odot$ 是逐元素乘法。批量训练还需要按所采用的损失约定汇总各样本梯度。

[[slide:01b:23|把上游梯度与局部梯度连接起来]]

[[slide:01b:29|手写前向传播、反向传播与梯度更新]]

读计算图时先做一遍前向计算，把中间值记下来，再从最终损失向前计算局部导数。遇到分叉，一个变量影响损失的各条路径贡献需要相加。

!!! note "原图代码的实现澄清"
    上图按行存放 batch，与前文按列书写的单样本公式转置约定不同。真正实现时，第一层权重梯度应为 `X.T @ d_Z`，偏置梯度应沿 batch 维求和；不要将截图中的 `d_X.T` 或未归约的偏置梯度直接照抄。正文公式与下面的自动微分示例采用一致的计算定义。

## 1b.5 用深度学习框架实现

TensorFlow 和 PyTorch 提供张量运算、自动微分、数据批处理和优化器。自动微分仍然是在执行链式法则；框架不会自动替我们选择正确的标签、损失和数据划分。

[[slide:01b:36|TensorFlow 2.0 的 GradientTape 与参数更新]]

下面用**补充的 PyTorch 示例**实现两层回归网络，展示完整训练步骤。

```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(3, 16), nn.ReLU(), nn.Linear(16, 1))
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def train_step(x, y):
    model.train()
    optimizer.zero_grad()
    prediction = model(x)           # [batch_size, 1]
    loss = criterion(prediction, y) # y 也应为 [batch_size, 1]
    loss.backward()
    optimizer.step()
    return loss.item()
```

!!! tip "实现时先检查形状"
    如果预测是 `[B, 1]`，标签却是 `[B]`，广播可能产生不符合预期的计算。另一个常见问题是忘记清空梯度：PyTorch 默认会累加梯度。

## 1b.6 优化器、学习率与学习曲线

### 优化器与学习率衰减

常见优化器包括 SGD、Momentum、RMSProp 和 Adam。Momentum 累积更新方向，RMSProp 用梯度平方的移动平均调节各参数的步长，Adam 同时使用一阶和二阶矩估计。

学习率通常随训练逐渐降低。例如在第 30、60、90 个 epoch 将学习率乘以 0.1，或采用 cosine、linear 等计划。这些是策略示例，不是所有数据集的固定答案。

[[slide:01b:42|学习率衰减：分段下降及其他调度方式]]

### Overfitting / Underfitting

| 现象 | 可能的问题 | 优先考虑 |
| --- | --- | --- |
| 训练损失低，验证损失高 | Overfitting（过拟合） | 更多有效数据、增强、正则化、降低容量 |
| 训练和验证表现都差 | Underfitting（欠拟合）或训练故障 | 先检查实现与优化，再考虑增加容量 |
| 损失缓慢下降 | 学习率偏小等 | 结合曲线尝试调整学习率 |
| 损失震荡或发散 | 学习率过大、数值问题等 | 检查尺度、梯度和学习率 |

[[slide:01b:49|过拟合与欠拟合的学习曲线]]

[[slide:01b:52|平台期、下降过慢与过早降低学习率]]

训练损失与最终评价指标不同，应该同时监控。损失仍在变化但指标不动，或反过来，都是可能的。

**Early stopping（早停）** 根据验证集表现选取 checkpoint。不能用测试集寻找最佳 epoch，否则测试结果不再独立。

## 1b.7 正则化与泛化

### 显式正则化

$$
L_{\mathrm{total}}=L_{\mathrm{data}}+\lambda\lVert W\rVert_2^2.
$$

L2 正则化惩罚过大的权重；L1 使用 $\lVert W\rVert_1$，常产生更稀疏的解。$\lambda$ 控制约束强度。现代优化器中的 decoupled weight decay 与直接向损失加 L2 项需要区分，尤其是 Adam 一类自适应方法。

### 隐式正则化与数据增强

| 方法 | 训练时做什么 | 推理时注意什么 |
| --- | --- | --- |
| Dropout | 随机丢弃一部分激活，降低共同依赖 | 普通推理关闭随机丢弃 |
| Batch Normalization | 用 batch 统计量标准化并学习缩放和平移 | 通常使用训练累计的统计量 |
| Data augmentation | 对输入做符合任务语义的随机变换 | 验证/测试通常使用确定性预处理 |
| Ensemble | 训练多个模型 | 聚合预测，增加计算开销 |

[[slide:01b:57|Dropout：训练时随机丢弃神经元的示意]]

Dropout 的概率必须明确是“丢弃率”还是“保留率”，不同资料的符号约定可能不同。Batch Normalization 有时带来正则化效应，但它的作用不能简单等同于 Dropout。

医学增强还需要考虑标签是否保持不变：左右翻转可能改变解剖侧别，裁剪可能移除病灶。更多例子见[第 4 章](04-training-retina.md)。

## 1b.8 调参、推理与网络设计

### 调试顺序

1. 查看输入图像、标签和数据归一化结果。
2. 用 1–2 个 mini-batch 训练，确认网络可以在少量样本上明显过拟合。
3. 扩展到完整训练集，观察训练与验证曲线。
4. 在验证集上调整学习率、层数、隐藏层宽度和正则化强度。
5. 保存表现最好的 checkpoint，再进行独立测试。

[[slide:01b:64|先过拟合小数据，再在较宽范围内搜索超参数]]

!!! note "学习率的对数尺度搜索"
    例如想覆盖 $10^{-5}$ 到 $10^0$，可取 $u\sim U[-5,0]$，再令 $\eta=10^u$。若使用 $e^u$，则指数区间也应相应改变。

### 推理与激活函数

推理时切换到 evaluation mode，并关闭不必要的梯度记录。回归最后一层通常是线性输出；多分类输出 logits 后通过 softmax 得到概率；多标签任务的各类别可分别使用 sigmoid。

| 激活 | 表达式 | 常见位置 |
| --- | --- | --- |
| ReLU | $\max(0,z)$ | CNN / MLP 隐藏层 |
| Sigmoid | $1/(1+e^{-z})$ | 二分类、多标签概率或门控 |
| Tanh | $\tanh z$ | 部分循环网络与隐藏状态 |

模型集成通常能改善稳定性，但不能保证固定的提升比例。

## 1b.9 自测

??? question "反向传播和梯度下降是一回事吗？"
    不是。反向传播计算梯度，梯度下降使用梯度更新参数。相同的反向传播结果也可以交给 Momentum 或 Adam 等优化器。

??? question "训练集上表现很好，是否说明模型可以用于新病人？"
    不能。还需要独立验证、测试和合适的数据划分。训练数据上的表现只说明模型拟合了已见样本。

??? question "数据增强、集成、Dropout、正则项，哪些可能改善泛化？"
    四者都有可能，但效果依赖任务与超参数。应使用验证集判断，不能把某种技巧视为必然有效。

---

[原文与图示](../slides/generated/01b.md) · [PDF](../originals/lecture-01b.pdf)
