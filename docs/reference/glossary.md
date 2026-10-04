# 术语与公式速查

按任务与方法归类。完整解释和课件示例见对应章节。

## 任务与数据

| 英文 | 中文 | 要点 | 章节 |
| --- | --- | --- | --- |
| Classification | 分类 | 输出类别或类别分数 | [2](../notes/02-classification.md) |
| Regression | 回归 | 输出连续数值 | [1b](../notes/01b-fundamentals.md) |
| Semantic segmentation | 语义分割 | 每个像素 / 体素一个类别 | [3](../notes/03-segmentation.md) |
| Instance segmentation | 实例分割 | 类别之外，还区分目标个体 | [3](../notes/03-segmentation.md) |
| Ground truth | 参考真值 / 标注 | 指评价协议中的参考标签，不意味着绝对无误 | [2](../notes/02-classification.md) |
| Voxel | 体素 | 三维数据的基本单元 | [3](../notes/03-segmentation.md) |
| Spacing | 像素 / 体素间距 | 数组坐标与物理尺度的联系 | [4](../notes/04-training-retina.md) |
| ROI | 感兴趣区域 | Region of interest | [3](../notes/03-segmentation.md) |
| Data leakage | 数据泄漏 | 评价数据的信息进入训练或选参 | [2](../notes/02-classification.md) |

## 训练与网络

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

## 评价指标

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

## 常用公式

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

## 医学影像与眼科

| 缩写 / 英文 | 中文 | 出现位置 |
| --- | --- | --- |
| CT | 计算机断层成像 | [1a](../notes/01a-introduction.md)、[3](../notes/03-segmentation.md) |
| MRI | 磁共振成像 | [1a](../notes/01a-introduction.md)、[3](../notes/03-segmentation.md) |
| PET | 正电子发射断层成像 | [3](../notes/03-segmentation.md) |
| Fundus photography | 眼底照相 | [2](../notes/02-classification.md)、[4](../notes/04-training-retina.md) |
| OCT | 光学相干断层成像 | [4](../notes/04-training-retina.md) |
| OCTA | OCT 血管成像 | [4](../notes/04-training-retina.md) |
| FAF | 眼底自发荧光 | [4](../notes/04-training-retina.md) |
| BMD | 骨密度 | [1b](../notes/01b-fundamentals.md) |
| LVEF | 左心室射血分数 | [1b](../notes/01b-fundamentals.md)、[3](../notes/03-segmentation.md) |
| DR | 糖尿病视网膜病变 | [2](../notes/02-classification.md)、[4](../notes/04-training-retina.md) |
| DME | 糖尿病黄斑水肿 | [2](../notes/02-classification.md) |
| AMD | 年龄相关性黄斑变性 | [4](../notes/04-training-retina.md) |
| IVD | 椎间盘 | [3](../notes/03-segmentation.md) |

## 模型选用时的输入输出

| 情况 | 典型输入形状（PyTorch） | 典型输出 |
| --- | --- | --- |
| 图像分类 | `[B, C, H, W]` | `[B, K]` logits |
| 二维互斥分割 | `[B, C, H, W]` | `[B, K, H, W]` logits |
| 三维互斥分割 | `[B, C, D, H, W]` | `[B, K, D, H, W]` logits |
| 标量回归 | 取决于输入模态 | `[B, 1]` |
| 3D 卷积视频模型 | `[B, C, T, H, W]` | 视频级或逐时间步输出 |

这里仅列常见约定，实际模型可能裁剪或降采样输出。数据读取、模型、损失和评价代码中的形状要保持一致。
