---
title: Advanced Topics in Artificial Intelligence for Medical Image Analysis
---

<div class="course-hero" markdown>
<p class="eyebrow">MEDICAL IMAGE ANALYSIS</p>
<a class="hero-visual" href="slides/generated/01a/#page=6" aria-label="查看眼底影像原图"><img src="assets/retina.webp" width="299" height="299" alt="眼底照片，显示视盘与视网膜血管"><span>FUNDUS / RETINAL IMAGING ↗</span></a>

# Advanced Topics in Artificial Intelligence for Medical Image Analysis

<p class="course-meta"><span>ELEC 5690</span><span>授课教师 · Xiaomeng Li</span></p>
<p class="hero-description">从深度学习基础到分类、分割与多模态分析，结合医学影像案例理解方法。</p>
</div>

<nav class="study-paths" aria-label="阅读入口">
<a class="study-path" href="#topics"><strong>学习笔记 <span aria-hidden="true">↘</span></strong><small>按主题理解概念、公式与案例</small></a>
<a class="study-path" href="slides/#browse"><strong>原页浏览 <span aria-hidden="true">↗</span></strong><small>逐页翻阅，放大查看原图</small></a>
<a class="study-path" href="slides/#originals"><strong>原始 PPT <span aria-hidden="true">↗</span></strong><small>打开或保存完整 PDF</small></a>
</nav>

## 主题导航 {#topics}

<div class="chapter-list">
<a class="chapter-row" href="notes/01a-introduction/"><span class="chapter-number">01a</span><span><strong>Medical Imaging & AI · 医学影像入门</strong><small>成像方式、AI / ML / DL、视觉任务与卷积网络</small></span><span class="chapter-end">阅读 ↗</span></a>
<a class="chapter-row" href="notes/01b-fundamentals/"><span class="chapter-number">01b</span><span><strong>Deep Learning Fundamentals · 深度学习基础</strong><small>回归、损失函数、反向传播、优化与泛化</small></span><span class="chapter-end">阅读 ↗</span></a>
<a class="chapter-row" href="notes/02-classification/"><span class="chapter-number">02</span><span><strong>Classification · 图像分类</strong><small>经典网络、迁移学习、评价指标与疾病筛查</small></span><span class="chapter-end">阅读 ↗</span></a>
<a class="chapter-row" href="notes/03-segmentation/"><span class="chapter-number">03</span><span><strong>Segmentation · 分割、三维与视频</strong><small>U-Net、Dice、三维卷积与视频建模</small></span><span class="chapter-end">阅读 ↗</span></a>
<a class="chapter-row" href="notes/04-training-retina/"><span class="chapter-number">04</span><span><strong>Training & Retinal Images · 训练策略与视网膜影像</strong><small>预处理、增强、眼底与 OCT、视网膜研究</small></span><span class="chapter-end">阅读 ↗</span></a>
<a class="chapter-row" href="notes/05-multimodal-dermoscopy/"><span class="chapter-number">05</span><span><strong>Multi-modal Data & Dermoscopy · 多模态、皮肤镜与超声</strong><small>融合、皮损分析、旋转等变与超声成像</small></span><span class="chapter-end">阅读 ↗</span></a>
</div>

## 术语与指标速查 {#quick-reference}

??? note "任务与数据"

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
    | Multimodal learning | 多模态学习 | 联合不同输入来源，例如 MRI 序列或图像与报告 | [5](notes/05-multimodal-dermoscopy.md) |
    | Multi-task learning | 多任务学习 | 联合多个输出目标，例如分类、检测与分割 | [5](notes/05-multimodal-dermoscopy.md) |

??? note "训练与网络"

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
    | Early / Joint / Late fusion | 早期 / 联合 / 后期融合 | 分别在输入、可联合训练的特征、预测结果处合并 |
    | FPN / RPN | 特征金字塔 / 区域建议网络 | 分别组织多尺度特征、产生候选区域 |
    | Focal loss | 焦点损失 | 用难易调制因子降低容易样本的相对贡献 |
    | Equivariance | 等变性 | 输入变换后，输出按对应方式变换 |
    | Deep supervision | 深监督 | 中间输出也参与损失计算 |

??? note "评价指标"

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

    第 5 章结果表中的 AP 为 Average Precision，用于概括 precision–recall 表现；JA 为 Jaccard / IoU，DI 为 Dice。AP 不等于 Accuracy，分类指标与像素级分割指标应分别解读。
