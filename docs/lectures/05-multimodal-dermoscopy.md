# 5: Multi-modal Data & Dermoscopy

理解多模态融合，沿模型图判断融合位置，再比较皮肤镜分析中的分割、分类与多任务方法。

眼底与 OCT 的成像基础见[第 4 章](04-training-retina.md)。

## 5.1 Multimodal Data（多模态数据）

### “模态”可以相近，也可以差别很大

多模态学习把不同信息来源联合用于一个任务。这些来源既包括相近的图像采集方式，也包括结构完全不同的临床数据。

| 信息来源 | 示例 | 联合处理前需要明确什么 |
| --- | --- | --- |
| 不同 MRI 序列 | T1、T1C、T2、FLAIR | 同一位置是否对应同一组织，各序列突出什么 |
| 不同投照视图 | 左右乳腺的 CC、MLO | 侧别、视角与参数共享方式 |
| 图像与文本 | 胸片和放射学报告 | 是否属于同一次检查，文字在任务中起什么作用 |
| 不同临床记录 | p. 13 的检验、用药、诊断和病程记录 | 时间顺序、量纲、缺失项与预测时点 |

补充理解：多模态描述的是**输入来源**，多任务描述的是**输出目标**。四种 MRI 序列预测一个分割结果，是多模态单任务；一张皮肤镜图同时预测类别、框和 mask，是单模态多任务。

[[slide:05:13|临床多模态数据原例：检验、用药、诊断与病程记录]]

不同类型的临床记录也属于多模态来源。这张图展示的是数据，并未给出融合模型；只看输入种类，无法判断 early、joint 或 late fusion。

### MRI 原例：四个通道不是四个独立病例

[[slide:05:12|T1、增强 T1、T2、FLAIR 与脑肿瘤区域]]

| 序列 | 名称与特点 |
| --- | --- |
| T1 | T1-weighted，提供一种组织对比 |
| T1C / T1-enhanced | 使用钆对比剂的增强 T1，可显示增强区域 |
| T2 | T2-weighted，与 T1 形成不同的组织对比 |
| FLAIR | Fluid-Attenuated Inversion Recovery，液体衰减反转恢复序列 |

TR（repetition time）与 TE（echo time）是采集时序参数。补充澄清：FLAIR 的关键还在于利用反转恢复抑制脑脊液信号，不能只理解为“TR、TE 更长的 T2”。原页中的 `BRAST` 按常用数据集名称写作 **BraTS**。

同一肿瘤的增强区、周围水肿等结构在不同序列中并不同样显眼，因此把序列联合起来有意义。模型仍需学习它们和标注的关系，并非增加通道就必然提高效果。

[[slide:05:15|Havaei 等人的原例：把四种 MRI 序列堆叠到输入通道]]

图中输入是 $4\times33\times33$ 的局部图像块：4 表示模态数，两个 33 表示空间尺寸；输出为 $5\times1\times1$，表示该例中目标位置的五类预测。网络内部的双路径用于提取不同上下文，**模态在进入这些路径之前已经合并**。

补充实现对应：一批二维四序列输入可以表示为 `[B, 4, H, W]`，三维输入可以表示为 `[B, 4, D, H, W]`。堆叠前应完成空间对齐，并保持序列顺序一致；缺失序列需要单独约定处理方式。

## 5.2 Fusion（看模型图判断融合类型） {#52-fusion}

判断的关键是**合并什么、在哪里合并、融合后的 loss 是否更新模态分支**。输入有几种模态、网络有几条分支、是否出现 `concatenation`，都不能单独决定类型。

### 分类原图：五种结构，三类融合

[[slide:05:34|Early Type I / II、Joint Type I / II 与 Late Fusion：沿箭头寻找融合点]]

先读右上角图例：**圆形是 feature，带斜线的圆形是 extracted feature，方形是 prediction**；蓝色、绿色表示不同模态，橙色表示最终输出。中间图向下返回的 `Loss` 箭头表示模态特征提取器也接受训练信号。

| 图中结构 | 数据流与识别线索 | 判定依据 |
| --- | --- | --- |
| **Early Fusion — Type I** | 原始特征先拼接 → 一个模型 → 输出 | 模型处理前已经合并输入 |
| **Early Fusion — Type II** | 原始 / 预提取特征先拼接 → 一个模型 → 输出 | 预提取特征可以作为输入；下游梯度不更新其提取器 |
| **Joint Fusion — Type I** | 两个模态分别经过可学习网络 → 中间特征合并 → 联合预测 | 联合训练更新模态专属网络与融合后的模型 |
| **Joint Fusion — Type II** | 一个模态先经过可学习网络，再与另一模态的原始 / 已有特征合并 | 不要求每种模态都有一个可训练编码器；图中的模态网络仍由联合 loss 更新 |
| **Late Fusion** | 各模态模型分别输出预测 → aggregation → 最终预测 | 合并的是预测结果，而非中间表示 |

### 英文定义摘录与看图要点

以下英文摘录自 p. 35–37，合并了原页换行；中文用于解释判定方法。

=== "Early fusion"

    [[slide:05:35|Early fusion 原页：输入拼接，以及不回传梯度的预提取特征]]

    > Early fusion: concatenate / combine data before any model processing. Includes using extracted features as input, if model gradients are not backpropagated to update feature extractor parameters

    **先合并输入，再交给模型。** 即使输入来自预训练 CNN，只要作为固定特征使用、下游梯度不更新提取器，仍可按本章约定归入 early fusion。不要把“经过 CNN 的特征”直接等同于 joint fusion。

=== "Joint fusion"

    [[slide:05:36|Joint fusion 原页：模态专属组件与融合组件共同更新]]

    > Joint fusion: Both modality-specific components (with learnable parameters) and combined-modality components within the model, that are updated during model training

    **先做模态专属处理，在中间表示处融合，再共同训练。** 看融合后的 loss 是否能更新模态分支。Type II 表明：一个分支是可训练网络、另一个是已有特征，也可以构成 joint fusion。

=== "Late fusion"

    [[slide:05:37|Late fusion 原页：先各自预测，再聚合预测结果]]

    > Late fusion: Main learnable model components are only model specific. Individual modality outputs are then aggregated.

    **各自预测，再合并答案。** 原文的 `model specific` 沿用原页措辞，这里对应各模态自己的模型。平均、加权、投票可以实现预测聚合；应先确认被聚合的是预测，而不是 feature map。

### 考试看图：先找融合点，再解释训练关系

1. **从输入沿箭头走**，找不同模态第一次相遇的位置；有多个融合点时分别判断。
2. **相遇时已经各自预测了吗？** 若已经有类别概率、分数或预测值，再平均 / 投票，属于 late fusion。
3. **若合并的是输入或特征，看训练关系。** 原始 / 固定特征在模型前合并 → early；模态网络产生中间表示，并接受联合 loss 更新 → joint。
4. **用图中的模块说明理由。** 回答包含“类型＋融合的对象＋融合位置”，不要只写类型名称。若图中没有冻结 / 梯度信息，就注明判断所需的训练条件。

| 可以直接用于简答的句式 | 需要在图中指出什么 |
| --- | --- |
| **Early fusion:** The modalities are concatenated at the input level before model processing. | 输入通道 / 特征向量先拼接 |
| **Early fusion with fixed features:** The extracted features are combined as inputs, and the feature extractors are not updated by the downstream loss. | 固定提取器、无回传更新 |
| **Joint fusion:** Modality-specific features are fused inside the network, and the modality-specific and fusion components are trained jointly. | 中间特征、联合训练路径 |
| **Late fusion:** Each modality produces its own prediction, and these predictions are aggregated to obtain the final output. | 各自预测头、末端聚合 |

补充数学表达，设 $x_m$ 为模态输入、$f_m$ 为其编码器：

$$
\begin{aligned}
\text{Early:}\quad &\hat y=h([x_1;x_2]),\\
\text{Joint:}\quad &\hat y=h([f_1(x_1);f_2(x_2)]),\\
\text{Late:}\quad &p(y)=\sum_m\alpha_m p_m(y),\qquad \alpha_m\geq0,\quad\sum_m\alpha_m=1.
\end{aligned}
$$

方括号表示拼接。第二式只有在模态分支按联合目标更新时才体现这里的 joint fusion；若 $f_m$ 固定，其输出只是预提取输入特征，就要按 early fusion 的约定判断。

### 原题 1：MRI 脑肿瘤分割 — Early fusion

[[slide:05:38|原题：What kind of fusion was this model? 四种 MRI 序列的脑肿瘤分割]]

**答案：Early fusion（输入级融合）。** T1、T1C、T2、FLAIR 在进入卷积网络前已堆叠成通道。图中输入是 $4\times33\times33$：4 是模态数，33 是 patch 边长；输出 $5\times1\times1$ 是目标位置的五类预测。

图内上下两条路径从**同一个四通道输入**提取不同尺度的上下文，后面再拼接它们。它们不是四个 MRI 模态分别训练的分支，因此内部的双路径 / `Concatenation` 不改变输入级 early fusion 的判断。

!!! example "英文作答"
    **This is early fusion. The four MRI modalities are stacked as input channels before convolutional processing. The two internal paths extract features from the already fused input.**

### 原题 2：乳腺四视图 — Joint + Late fusion

[[slide:05:39|原题：What kind of fusion was this model? 左右乳腺 CC / MLO 四视图]]

**答案：同时包含 Joint fusion 和 Late fusion。** 需要指出两个不同的融合位置；只写其中一种不足以描述整张图。

| 从下到上的位置 | 原图在做什么 | 应怎样解释 |
| --- | --- | --- |
| 四个输入 | L-CC、R-CC、L-MLO、R-MLO | L/R 为左/右；CC 为头尾位；MLO 为内外斜位 |
| ResNet-22 | 各视图分别提特征 | 同一投照方向的左右分支共享参数；CC 与 MLO 的参数分别学习 |
| Average pooling | 每条分支压缩空间特征 | 这里尚未合并不同模态的预测，不能因 `average` 就叫 late fusion |
| Concatenation → fully connected layer | 同一投照方向的左右特征拼接，再预测 | **Joint fusion**：中间特征融合，分支与融合部分共同训练 |
| 各方向的预测头 | 左/右乳腺的良性、恶性标签，各为二元判断 | 四个独立标签，不是四类互斥的一个 softmax |
| 顶部 average | CC 与 MLO 对同一标签的预测平均 | **Late fusion**：合并已经产生的预测 |

=== "中间特征融合：p. 20"

    [[slide:05:20|标注原图：拼接 modality-specific processing 的输出，再进行联合预测]]

    先有模态专属表示，再把左右特征拼起来。`Fully connected layer` 位于特征合并之后，不代表这里是在融合两个最终预测。

=== "预测融合：p. 23"

    [[slide:05:23|标注原图：CC 与 MLO 的预测平均，是第二处融合]]

    先分别得到 CC、MLO 的二元预测，再逐标签平均。参数共享是编码器的设计，不能替代对融合位置的判断。

!!! example "英文作答"
    **The model uses both joint and late fusion. Left and right features are concatenated within each projection branch and jointly processed. The CC and MLO predictions are then averaged, which is late fusion.**

### 原题 3：TieNet 胸片＋报告 — Joint fusion

[[slide:05:40|原题：What kind of fusion was this model? 胸片 CNN 与报告 LSTM]]

**答案：Joint fusion。** CNN 提取胸片特征，word embedding / LSTM 处理报告；图像特征通过注意力参与文本序列处理，再将学习到的图文表示融合进行疾病预测。交互发生在中间表示层，模态专属组件和融合组件共同训练。

不要因为融合处有一个最终 fully connected layer 就答 late fusion：图中没有“胸片独立诊断＋报告独立诊断，再平均两个答案”的过程。具体注意力数据流见下一节。

!!! example "英文作答"
    **This is joint fusion. Image and text representations interact within the network through attention and are fused for disease prediction; the modality-specific and fusion components are trained jointly.**

!!! warning "看图判断的易错点"
    `Concatenation` 不必然是 joint；`average pooling` 不必然是 late；两个分支不必然是两个模态。先看分支处理什么，再看合并的是输入、可共同训练的特征，还是预测。`Joint embedding space` 的名字也不能代替融合结构与训练关系的证据。

## 5.3 Image–Text Learning（胸片与报告）

### TieNet：沿文本序列关注图像区域

[[slide:05:28|TieNet 原图：词语、LSTM、空间注意力与图像特征的联系]]

Wang 等人的 TieNet（CVPR 2018）将胸片和对应报告用于联合学习。图中存在两条不同的数据处理路径：

- **图像路径**：CNN 提取空间特征图；空间注意力给不同位置分配权重。
- **文本路径**：词先变为 embedding，再由 LSTM 处理序列，形成文本表示。
- **交互与输出**：每个时间步结合图像信息；词语显著性用于加权空间注意力图，再由联合表示预测疾病标签。

[[slide:05:29|TieNet 最终融合位置：图文表示进入 fully connected layer，再输出疾病标签]]

两种表示在中间计算中已经发生交互，再由联合全连接部分产生预测。p. 25–27 分别标出 word embedding、CNN 与 LSTM；p. 28 的词语 saliency 用于加权空间 attention maps，p. 29 才是最终图文表示的融合。因此，整个方法属于 joint fusion。

补充阅读建议：区分报告用于训练监督、联合输入或生成目标的设置，并单独核对推理时实际可用的输入。特别是当报告本身写有目标疾病时，不能把“读到报告后分类”的结果直接解释为“只看胸片”的能力。

### 共同嵌入空间：让图像和报告能够互相检索

[[slide:05:32|Hsu 等人的原例：图像和文本映射到共同的 embedding 空间]]

这一例的目标是学习跨模态表示：图像和对应报告在空间中接近，其他不相关报告相对更远。图像由 DenseNet121 提取特征，文本使用自己的特征表示，再映射到共同空间。它可以用于 image-to-text 或 text-to-image retrieval，而不只是输出固定类别。

[[slide:05:33|Hsu 等人的完整原例：图像 / 文本处理、共同嵌入空间与三种对齐目标]]

> Learn mapping from images and text to vectors in the same embedding space, such that images are embedded closer to their corresponding reports than other reports, and vice versa.

**读图区别：** 胸片经 DenseNet121、平均池化和 PCA；报告经 TF-IDF / distributed embeddings，再用映射 $W$ 对齐。共同空间中保留图像、文本各自的向量，用于跨模态匹配，并不是两个疾病预测的平均。图中的 `Joint Embedding Space` 表示共同嵌入空间；它本身不能证明所有编码器接受同一个 loss 的端到端更新，不能仅凭名称将其等同于前面定义的 joint fusion 分类网络。

该方法比较三种训练设置：

| 设置 | 原页标记 | 约束的内容 |
| --- | --- | --- |
| 有配对信息的对齐 | EA，Embedding Alignment | 让已匹配的图像与报告表示接近 |
| 对抗式对齐 | Adv，Adversarial Domain Adaptation | 判别器区分模态，映射学习使模态难以区分 |
| 半监督组合 | EA + Adv | 同时使用配对约束和分布对齐 |

原页给出的线性对齐目标可写为：

$$
L_{\mathrm{EA}}=\|W^TX-Y\|_F^2.
$$

$X$ 与 $Y$ 的列表示配对样本；$W$ 把一种表示映射到另一种表示的维度。分布难以区分，并不自动保证每一对语义都匹配，因此还需要通过检索或下游任务检验。

## 5.4 Dermoscopy（皮肤镜与原图观察）

皮肤镜图像呈现皮肤病变的颜色、边界与内部结构。阅读本节时，先区分“病变在哪里”的分割问题和“属于什么病变”的分类问题，再观察背景、毛发、反光与低对比度会怎样影响这两个任务。

### 三个观察例子

[[slide:05:48|黑色素瘤原例：用轮廓、横线与遮盖标记比较病变形状]]

**Melanoma（黑色素瘤）**：沿轮廓、横线和遮盖标记，比较病变两侧的形状、边缘和颜色分布。病变名称沿用来源标注。

[[slide:05:49|Nevus：整体轮廓与局部结构]]

**Nevus（痣）**：结合整体轮廓与局部细节，观察对称性、边界和颜色分布。示例中列举的颜色较均匀、直径小于 5 mm 等特征是观察线索，不能单独作为良恶性的判定条件，也不等同于完整的皮肤镜评分规则。

[[slide:05:55|Basal cell carcinoma 原例：浅色病变也属于皮肤镜分析对象]]

**Basal cell carcinoma（基底细胞癌）**：这一例与前面的色素性病变外观不同，观察时需要关注浅色区域及局部结构，不能把“颜色深”作为所有病变的共同前提。

### 类别与数据集

[[slide:05:56|痣、皮肤纤维瘤、黑色素瘤及其他皮损]]

| 原图名称 | 中文理解 |
| --- | --- |
| Nevus | 痣 |
| Dermatofibroma | 皮肤纤维瘤 |
| Melanoma | 黑色素瘤 |
| Pigmented Bowen's | 色素性 Bowen 病 |
| Pigmented Benign Keratoses | 色素性良性角化性病变 |
| Basal Cell Carcinoma | 基底细胞癌 |
| Vascular | 血管性病变 |

[ISIC 2018 Task 3：Lesion Diagnosis](https://challenge.isic-archive.com/landing/2018/47/) 是皮损分类的一个任务示例。不同年份和任务的标签定义、训练数据与评价协议需要分别核对；皮损分割、二分类识别和多类别诊断不能直接共用一张排行榜。

## 5.5 Residual Networks（先分割，再分类）

### 为什么要先找病变区域？

[[slide:05:59|Yu 等人的原例：类别外观相似、低对比度、伪影与病变尺寸差异]]

*Automated Melanoma Recognition in Dermoscopy Images via Very Deep Residual Networks*（Yu 等，TMI 2017）研究如何定位并识别皮损。困难包括：不同类别外观相似、病变与皮肤对比度低、毛发等伪影，以及病变在整张图中占比变化大。

[[slide:05:60|两阶段框架：FCRN 分割病变，再用 DRN 分类裁剪区域]]

数据流是：

1. **FCRN**（Fully Convolutional Residual Network）输出皮损 mask。
2. 利用分割结果定位并裁剪病变区域。
3. **DRN**（Deep Residual Network）对裁剪图进行分类。

分割帮助分类器关注病变，残差连接则帮助训练较深网络。两者解决的是不同问题。p. 61 同时比较网络深度和多尺度特征整合；表中 FCRN-50 的 JA 高于 FCRN-101，说明“更深”本身不能保证更好。

### 结果怎样读：不同指标不一定一起提高

[[slide:05:62|原始结果表：有无分割的分类对照，以及不同任务的评价指标]]

直接摘录原页 Table V：

| 设置 | Accuracy | AUC | AP | Sensitivity | Specificity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Without segmentation | 0.828 | 0.782 | 0.560 | 0.427 | 0.927 |
| With segmentation | 0.855 | 0.783 | 0.624 | 0.547 | 0.931 |

加入分割后，AP 从 0.560 增至 0.624，Sensitivity 从 0.427 增至 0.547，但 AUC 只从 0.782 变为 0.783。因此这里应分别描述各指标，而不能笼统地说“所有评价都显著提升”。AP（Average Precision）概括 precision–recall 表现，也不是 Accuracy 的另一种写法。

p. 62 的分割挑战表按 JA（Jaccard / IoU）排序；p. 64 的分类挑战表按 AP 排序。第一名依赖任务与指标，不能跨表直接比较名次。p. 74 转引 CUMED 时，SE/SP 的数值位置与 p. 62 不同；本文保留原表，并按上述 Table V 解读该对照。

[[slide:05:65|分割轮廓偏差与漏识别的黑色素瘤]]

两阶段系统会传递误差：若第一阶段没有准确定位病变，裁剪后的分类输入也会受到影响。图中上排是分割失败，下排是该框架漏识别的黑色素瘤，可以据此分析误差如何传递。

## 5.6 Multi-task Learning（分类、检测与分割）

### 三个输出怎样合作？

[[slide:05:67|Song 等人的多任务框架：FPN、RPN 与分类、检测、分割分支]]

Song 等人的 *An End-to-End Multi-Task Deep Learning Framework for Skin Lesion Analysis*（JBHI 2020）联合学习三种任务。框架通过 FPN（Feature Pyramid Network）提供多尺度特征，通过 RPN（Region Proposal Network）产生候选区域，再由三个子网络输出类别、位置和 mask，并组合结果。

| 分支 | 回答的问题 | 监督信号 |
| --- | --- | --- |
| Classification | 病变属于什么类别？ | 类别标签 |
| Detection | 病变在哪里？ | 边界框、前景/背景 |
| Segmentation | 哪些像素属于病变？ | 像素级 mask |

训练图像的高宽与颜色分布可能不同。进入网络前要统一处理尺寸，并同步变换框与 mask；数据统计也能帮助判断是否存在明显的采集差异。

补充理解：多任务总损失可抽象写为 $L=\lambda_cL_c+\lambda_dL_d+\lambda_sL_s$，但这只是解释各任务共同训练的示意，不是对原论文全部损失项的复写。各项尺度、样本数与权重会影响共享特征最终偏向哪个任务。

### Focal Loss 为什么压低容易样本的贡献？

RPN 需要从大量 anchors 中区分前景与背景，并回归位置。大量容易判断的背景会影响分类损失的构成，focal loss 用于降低这些容易样本的相对贡献。

[[slide:05:71|Focal Loss 原图：不同 γ 下，易分类样本的损失受到不同程度抑制]]

设 $p_t$ 是模型分配给**真实类别**的概率，原图采用不含类别权重项的形式：

$$
L_{\mathrm{CE}}=-\log p_t,\qquad
L_{\mathrm{FL}}=-(1-p_t)^\gamma\log p_t.
$$

- $\gamma=0$ 时恢复普通交叉熵。
- $p_t$ 接近 1 时，$(1-p_t)^\gamma$ 很小，容易样本的损失贡献被压低。
- $p_t$ 较小时，调制因子相对较大，使困难样本在总损失中的相对作用增加。

!!! example "补充算例：取 γ = 2"
    对 $p_t=0.9$ 的样本，CE 约为 0.1054，乘以 $0.1^2$ 后，FL 约为 0.001054。

    对 $p_t=0.2$ 的样本，CE 约为 1.6094，乘以 $0.8^2$ 后，FL 约为 1.0300。

    两个样本的损失都下降，但容易样本下降得更多。这是相对重加权，而不是把困难样本的损失一律放大。

原始 focal loss 论文入口见 [Lin 等，Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002)。类别平衡权重 $\alpha_t$ 可以另行加入，不应与难易调制参数 $\gamma$ 混为一谈。

### 消融实验：增加任务是否有帮助？

[[slide:05:76|单任务、双任务与三任务的消融比较]]

在原页 Table IX 和 Table X 的固定设置下：

| 任务组合 | 分类 AP | 分割 JA |
| --- | ---: | ---: |
| 仅对应单任务 | 0.787（Cls） | 0.760（Seg） |
| Cls + Seg | 0.815 | 0.782 |
| Cls + Dec + Seg | 0.823 | 0.799 |

这里的 `Dec` 沿用原表，表示检测分支。单任务一行来自两个各自独立的单任务基线，不是同一个模型同时产生两项结果。对照支持任务间在该设置下有帮助；它不保证任意任务组合都能改善性能。

[[slide:05:74|损失对照原表：分类结果与分割结果需要分别阅读]]

还有一个值得比较的细节：p. 72 分类表中 FL + JL 的 AP 为 0.823；但 p. 74 的分割表中，标为 JL（Jaccard loss）的一行 JA 为 0.813，高于 FL + JL 的 0.799。**某个损失组合对分类较好，不代表它对分割的每个指标也最好**。p. 73、75 的初始化、backbone 和 batch size 变化，应与同一配置下的消融分开分析。

## 5.7 Rotation Equivariance（旋转等变性）

### 分类希望“不变”，分割希望“跟着变”

[[slide:05:77|普通卷积的平移等变性与旋转后的特征差异]]

Li 等人的 *Deeply Supervised Rotation Equivariant Network for Lesion Segmentation in Dermoscopy Images*（MICCAI Workshop 2018）将旋转关系引入分割网络。皮肤镜图像可以有不同拍摄方向，因此希望网络正确处理旋转。

设 $T_g$ 表示一种旋转或其他空间变换，补充定义如下：

$$
\begin{aligned}
\text{不变性（invariance）：}\quad &f(T_gx)=f(x),\\
\text{等变性（equivariance）：}\quad &f(T_gx)=T_gf(x).
\end{aligned}
$$

病变旋转后，分类标签通常应保持一致；分割 mask 则应该随着病变一起旋转。如果输出 mask 完全不动，空间位置反而错了。

普通卷积具有平移等变的结构，但固定卷积核一般不保证旋转等变。实际网络中的边界处理、步幅和池化还会影响严格的平移等变关系。

### G-convolution 与 Deep Supervision

[[slide:05:80|G-convolution 原图：方向通道、群上的计算与投影]]

这里使用两种离散变换群：**p4** 包含平移与 90° 的整数倍旋转；**p4m** 还加入镜像反射。G-convolution 在这些变换之间安排共享关系，使旋转输入与相应的特征变换相对应。

与“训练时随机旋转几张图”相比，数据增强从样本变化中学习，等变网络则把指定变换关系放进运算结构。对 p4 的设计不等于对任意角度旋转都作出同样的严格保证。

[[slide:05:81|完整分割网络：G-upsampling、G-projection 与多个预测分支]]

网络使用群卷积、上采样和投影，并在不同层次产生预测。Deep supervision（深监督）通过中间输出参与训练，给较早层提供监督信号。补充示意为 $L=\sum_s\lambda_sL_s$，各 $s$ 对应一个受监督的输出；应将它与“网络更深”区分开。

[[slide:05:82|旋转等变与深监督的消融表：比较结构变化及参数量]]

原页中，ResnetFCN34* 与 (RE)-ResnetFCN34* 均列为 22.8M 参数，JA 从 71.27 增至 74.54。这组结果是在参数量相同的对照下观察到的改进。表中的数值采用百分数尺度，而 p. 83 的比较表采用 0–1 尺度，阅读时先统一单位。

---

[原文与图示](../slides/generated/05.md) · [PDF](../originals/lecture-05.pdf)
