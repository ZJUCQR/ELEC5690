# 资料与编写说明

## 原始课件

本网站整理以下五份 PDF，原文件保留在仓库根目录。站点下载文件仅使用较短的文件名，内容与原文件一致。

| 原始文件 | 页数 | 课件封面日期 |
| --- | ---: | --- |
| Lecture01a-Course Introduction.pdf | 56 | 2026-09-01 |
| Lecture01b-Deep Learning Fundamentals.pdf | 76 | 2026-09-01 |
| Lecture02-Basic Vision Models (Classification).pdf | 120 | 2026-09-15 |
| Lecture03-Basic Vision Models (Segmentation).pdf | 139 | 2026-09-22 |
| Lecture04 - Trainnig Strategies and Medical Images (Retinal Images).pdf | 113 | 2026-09-28 |

封面和页内信息用于识别课程内容；PDF 属性中的通用模板标题不作为课程名称。Lecture 04 原文件名中的 `Trainnig` 拼写予以保留，站内显示为 `Training`。

## 笔记怎样对应课件？

- 每章对应一份 PDF，页码均为 PDF 从 1 开始的物理页码。
- 核心概念、例子、网络图和研究案例写入正文，截图下方可跳转原页。
- 连续动画步骤、重复回顾、行政信息与原有图示均完整保留在[课件资料库](../slides/index.md)。
- 正文中的补充公式、算例、实现建议和 PyTorch 对照代码属于学习整理，未假称为课件原文。
- 论文结果按课件中的研究设置解释，不把特定实验的表现泛化为所有人群、设备或任务的结论。

## 已澄清的原页细节

| 位置 | 整理说明 |
| --- | --- |
| Lecture 01a p. 44 | 原图 error 未完整定义，作为训练趋势示意保留 |
| Lecture 01b p. 25–29 | 手写反向传播示意中的权重梯度与偏置归约需按形状核对，正文补充正确关系 |
| Lecture 01b p. 64 | 区分 $10^u$ 与 $e^u$ 的学习率对数尺度采样区间 |
| Lecture 02 p. 73 / 77 | Accuracy 和 Specificity 的 1 是近似值，正文按整数重算 |
| Lecture 02 p. 85 | DME 距离标签按正式数据集协议核对，原图不作为临床分级标准 |
| Lecture 03 p. 22–26 | 转置卷积的输出尺寸还取决于 output padding / 目标尺寸约定 |
| Lecture 03 p. 38 | 类别频率与其倒数权重明确区分 |
| Lecture 04 p. 33 | 显示后的概率精度会影响手算交叉熵的末位数字 |
| Lecture 04 p. 50 / 72 | 青光眼不都伴随高眼压；AMD 预后不解释成“高眼压变成 AMD” |

## 引用与来源

课件包含 Stanford BIODS 220、CS231n、Justin Johnson 的教学材料及多篇论文图示。原截图保留课件上的来源、作者、论文题目和图注。查找研究原文时，应以对应原页的完整引用为准。

课程建议教材包括：

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [*Deep Learning*](https://www.deeplearningbook.org/).
- Jerry L. Prince, Jonathan M. Links, *Medical Imaging Signals and Systems*.
- Kevin Zhou, Hayit Greenspan, Dinggang Shen, *Deep Learning for Medical Image Analysis*.

本网站采用暖白与深绿色视觉，使用 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 构建，并使用 [KaTeX](https://katex.org/) 排版公式。

## 使用与维护

本站不是课程官方发布渠道。课程时间、考核与作业要求以老师最新通知为准。课件与所引用图片、论文的权利归原作者，本项目不对其另行授予开源许可。

如需反馈笔记中的错误，可在[项目仓库](https://github.com/ZJUCQR/ELEC5690)提出 Issue，附上章节与原课件页码，便于核对。
