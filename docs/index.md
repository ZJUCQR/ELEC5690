---
title: 医学影像分析
---

<div class="course-hero" markdown>
<p class="eyebrow">ELEC 5690 / COURSE NOTES / FALL 2026</p>
<a class="hero-visual" href="slides/generated/01a/#page=6" aria-label="查看首页眼底图像的原课件第 6 页"><img src="assets/retina.webp" width="299" height="299" alt="原课件中的眼底照片，显示视盘与视网膜血管"><span>FUNDUS / LECTURE 01a · 06 ↗</span></a>

# 医学影像分析

<p class="english-title">Advanced Topics in Artificial Intelligence<br>for Medical Image Analysis</p>
<p class="hero-description">从神经网络的基本原理，到分类、分割与视网膜影像。沿着课件的思路，把概念、公式和例子连起来。</p>
<div class="course-stats"><span><strong>05</strong> 份课程讲义</span><span><strong>504</strong> 页原始课件</span><span><strong>2026</strong> 秋季学期</span></div>
</div>

!!! info "课程基本信息"
    - 课程名称：Advanced Topics in Artificial Intelligence for Medical Image Analysis
    - 课程代码：`ELEC 5690`，香港科技大学（HKUST）
    - 授课老师：Xiaomeng Li；助教：Xinrui Zhou
    - 内容来源：2026 年 9 月的 Lecture 01a、01b、02、03、04，课程安排以原课件及最新教学通知为准。

## 笔记基本信息

本笔记以五份课程 PPT 的 PDF 版本为依据，按照“基础 → 分类 → 分割 → 训练策略与医学应用”的顺序整理。中文解释配合英文术语，公式单独排版；课件中的例子、网络结构和实验结果保留原页截图，并补充阅读说明。

正文中的 **Lecture / p.** 链接可以定位到对应原页。连续动画页和重复回顾在笔记中合并说明，全部 504 页仍保留在[课件资料库](slides/index.md)中。复习时可直接查看本页的[术语与公式速查](#quick-reference)。

## 章节目录

<div class="chapter-list">
<a class="chapter-row" href="notes/01a-introduction/"><span class="chapter-number">01a</span><span><strong>Course Introduction · 课程介绍</strong><small>医学影像、AI / ML / DL、卷积网络直觉、课程安排与考核</small></span><span class="chapter-end">56 PAGES ↗</span></a>
<a class="chapter-row" href="notes/01b-fundamentals/"><span class="chapter-number">01b</span><span><strong>Deep Learning Fundamentals · 深度学习基础</strong><small>回归例子、损失函数、反向传播、优化与泛化</small></span><span class="chapter-end">76 PAGES ↗</span></a>
<a class="chapter-row" href="notes/02-classification/"><span class="chapter-number">02</span><span><strong>Classification · 图像分类</strong><small>卷积、经典网络、迁移学习、评价指标、DR / DME 与多类筛查</small></span><span class="chapter-end">120 PAGES ↗</span></a>
<a class="chapter-row" href="notes/03-segmentation/"><span class="chapter-number">03</span><span><strong>Segmentation · 分割、三维与视频</strong><small>U-Net、Dice、三维卷积、H-DenseUNet、循环与视频模型</small></span><span class="chapter-end">139 PAGES ↗</span></a>
<a class="chapter-row" href="notes/04-training-retina/"><span class="chapter-number">04</span><span><strong>Training & Retinal Images · 训练策略与视网膜影像</strong><small>预处理、增强、损失、眼底与 OCT、五组研究案例</small></span><span class="chapter-end">113 PAGES ↗</span></a>
</div>

## 建议阅读顺序

1. **第一次学习**：先看 1a 的任务和数据，再用 1b 的回归例子理解“网络—损失—优化”。
2. **实现分类模型**：阅读第 2 章。先明确数据划分和评价指标，再选择网络。
3. **实现分割模型**：阅读第 3 章。重点核对输入输出尺寸、跳跃连接和 Dice / IoU。
4. **阅读医学研究**：结合第 4 章的成像知识，按“问题—输入输出—方法—证据”的顺序看案例。

!!! tip "复习时关注什么？"
    能说明模型的输入和输出，能解释损失为什么这样定义，能读懂原图中的数据流，并知道指标没有反映什么。每章末尾的自测可以用来检查这些问题。

## 术语与公式速查 {#quick-reference}

按任务与方法归类。完整解释和课件示例见对应章节。

### 任务与数据

| 英文 | 中文 | 要点 | 章节 |
| --- | --- | --- | --- |
| Classification | 分类 | 输出类别或类别分数 | [2](notes/02-classification.md) |
| Regression | 回归 | 输出连续数值 | [1b](notes/01b-fundamentals.md) |
| Semantic segmentation | 语义分割 | 每个像素 / 体素一个类别 | [3](notes/03-segmentation.md) |
| Instance segmentation | 实例分割 | 类别之外，还区分目标个体 | [3](notes/03-segmentation.md) |
| Ground truth | 参考真值 / 标注 | 指评价协议中的参考标签，不意味着绝对无误 | [2](notes/02-classification.md) |
| Voxel | 体素 | 三维数据的基本单元 | [3](notes/03-segmentation.md) |
| Spacing | 像素 / 体素间距 | 数组坐标与物理尺度的联系 | [4](notes/04-training-retina.md) |
| ROI | 感兴趣区域 | Region of interest | [3](notes/03-segmentation.md) |
| Data leakage | 数据泄漏 | 评价数据的信息进入训练或选参 | [2](notes/02-classification.md) |

### 训练与网络

| 英文 | 中文 | 要点 |
| --- | --- | --- |
| Epoch | 训练轮次 | 遍历一次训练数据 |
| Mini-batch | 小批量 | 一次更新使用的样本集合 |
| Backpropagation | 反向传播 | 用链式法则计算梯度 |
| Learning rate | 学习率 | 参数更新步长 |
| Logits | 未归一化分数 | softmax / sigmoid 之前的输出 |
| Regularization | 正则化 | 约束拟合，改善泛化的措施 |
| Overfitting | 过拟合 | 拟合训练数据但泛化不足 |
| Transfer learning | 迁移学习 | 复用已有模型或表示 |
| Fine-tuning | 微调 | 从预训练权重继续更新参数 |
| Receptive field | 感受野 | 一个特征对应的输入区域 |
| Residual connection | 残差连接 | 常见形式是 $F(x)+x$ |
| Skip connection | 跳跃连接 | U-Net 通常沿通道拼接特征 |
| Transposed convolution | 转置卷积 | 可学习的尺寸扩张操作，不是数学逆卷积 |
| Self-supervised learning | 自监督学习 | 从数据本身构造训练目标 |
| MAE | 掩码自编码器 | Masked autoencoder，通过重建遮挡部分学习 |

### 评价指标

| 指标 | 公式 | 分母对应什么 |
| --- | --- | --- |
| Accuracy | $(TP+TN)/(TP+TN+FP+FN)$ | 所有样本 |
| Precision | $TP/(TP+FP)$ | 预测阳性 |
| Recall / Sensitivity | $TP/(TP+FN)$ | 实际阳性 |
| Specificity | $TN/(TN+FP)$ | 实际阴性 |
| F1 | $2TP/(2TP+FP+FN)$ | Precision 与 Recall 的调和平均 |
| IoU / Jaccard | $TP/(TP+FP+FN)$ | 两个 mask 的并集 |
| Dice / DSC | $2TP/(2TP+FP+FN)$ | 两个 mask 大小之和 |
| Youden index | $\mathrm{Sensitivity}+\mathrm{Specificity}-1$ | ROC 操作点的一种选择准则 |

ROC 是 TPR 对 FPR 的曲线；AUC 是其曲线下面积。分割的 Dice 与二分类 F1 形式相同，但实际评价还涉及图像、类别和数据集层面的归约方式。

### 常用公式

单层回归与梯度更新：

$$
\hat y=w^Tx+b,\qquad L_{\mathrm{MSE}}=\frac1M\sum_i(\hat y_i-y_i)^2,
\qquad \theta\leftarrow\theta-\eta\nabla_\theta L.
$$

互斥多分类：

$$
p_k=\frac{e^{z_k}}{\sum_j e^{z_j}},\qquad L_{\mathrm{CE}}=-\log p_y.
$$

普通卷积输出尺寸（含 dilation）：

$$
W_{\mathrm{out}}=\left\lfloor\frac{W+2P-D(K-1)-1}{S}\right\rfloor+1.
$$

转置卷积输出尺寸：

$$
W_{\mathrm{out}}=(W-1)S-2P+D(K-1)+O+1.
$$

$W$ 为输入尺寸，$P$ 为 padding，$D$ 为 dilation，$K$ 为核大小，$S$ 为 stride，$O$ 为 output padding。

### 医学影像与眼科

| 缩写 / 英文 | 中文 | 出现位置 |
| --- | --- | --- |
| CT | 计算机断层成像 | [1a](notes/01a-introduction.md)、[3](notes/03-segmentation.md) |
| MRI | 磁共振成像 | [1a](notes/01a-introduction.md)、[3](notes/03-segmentation.md) |
| PET | 正电子发射断层成像 | [3](notes/03-segmentation.md) |
| Fundus photography | 眼底照相 | [2](notes/02-classification.md)、[4](notes/04-training-retina.md) |
| OCT | 光学相干断层成像 | [4](notes/04-training-retina.md) |
| OCTA | OCT 血管成像 | [4](notes/04-training-retina.md) |
| FAF | 眼底自发荧光 | [4](notes/04-training-retina.md) |
| BMD | 骨密度 | [1b](notes/01b-fundamentals.md) |
| LVEF | 左心室射血分数 | [1b](notes/01b-fundamentals.md)、[3](notes/03-segmentation.md) |
| DR | 糖尿病视网膜病变 | [2](notes/02-classification.md)、[4](notes/04-training-retina.md) |
| DME | 糖尿病黄斑水肿 | [2](notes/02-classification.md) |
| AMD | 年龄相关性黄斑变性 | [4](notes/04-training-retina.md) |
| IVD | 椎间盘 | [3](notes/03-segmentation.md) |

### 模型选用时的输入输出

| 情况 | 典型输入形状（PyTorch） | 典型输出 |
| --- | --- | --- |
| 图像分类 | `[B, C, H, W]` | `[B, K]` logits |
| 二维互斥分割 | `[B, C, H, W]` | `[B, K, H, W]` logits |
| 三维互斥分割 | `[B, C, D, H, W]` | `[B, K, D, H, W]` logits |
| 标量回归 | 取决于输入模态 | `[B, 1]` |
| 3D 卷积视频模型 | `[B, C, T, H, W]` | 视频级或逐时间步输出 |

这里仅列常见约定，实际模型可能裁剪或降采样输出。数据读取、模型、损失和评价代码中的形状要保持一致。

## 编写进度

- [x] Lecture 01a：课程介绍与 CNN 入门
- [x] Lecture 01b：基础概念、公式与训练方法
- [x] Lecture 02：分类、评价与医学案例
- [x] Lecture 03：分割、三维与视频
- [x] Lecture 04：训练策略与视网膜研究
- [x] 全部原页、PDF 下载、[术语与公式速查](#quick-reference)

!!! note "资料说明"
    这是一份学习整理，不是课程官方讲义。正文中另行推导的算例和代码会标注为补充；课件原图保留其引用。详见[资料与编写说明](reference/sources.md)。
