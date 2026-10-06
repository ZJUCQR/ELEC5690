# 资料与编写说明

## 原始课件

内容整理自香港科技大学 ELEC 5690（2026 秋季），授课教师为 Xiaomeng Li。原始资料列于下表，下载文件与原文件内容一致。

| 原始文件 | 页数 | 课件封面日期 |
| --- | ---: | --- |
| Lecture01a-Course Introduction.pdf | 56 | 2026-09-01 |
| Lecture01b-Deep Learning Fundamentals.pdf | 76 | 2026-09-01 |
| Lecture02-Basic Vision Models (Classification).pdf | 120 | 2026-09-15 |
| Lecture03-Basic Vision Models (Segmentation).pdf | 139 | 2026-09-22 |
| Lecture04 - Trainnig Strategies and Medical Images (Retinal Images).pdf | 113 | 2026-09-28 |
| Lecture05-Medical Images (Multi-modal Data and Dermoscopy).pdf | 100 | 2026-10-06 |

封面和页内信息用于识别课程内容；PDF 属性中的通用模板标题不作为课程名称。Lecture 04 原文件名中的 `Trainnig` 拼写予以保留，站内显示为 `Training`。

新增文件名为 `Lecture05`，但封面印有 `Lecture 06`。本站按文件名编为第 5 章和 Lecture 05，截图与下载文件保留原貌。文件末段还包含超声成像原理，已一并纳入该章。

## 笔记怎样对应课件？

- 每章对应一份 PDF，页码均为 PDF 从 1 开始的物理页码。
- 核心概念、例子、网络图和研究案例写入正文，图注与章末链接可查阅原文。
- 连续动画步骤、重复回顾、行政信息与原有图示均完整保留在[原始资料](../slides/index.md)。
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
| Lecture 05 p. 12 | `BRAST` 按常用名称写作 BraTS；FLAIR 的解释补充反转恢复与脑脊液信号抑制 |
| Lecture 05 p. 51 | 良性痣特征是课件观察线索，不等同于完整评分体系或单项诊断条件 |
| Lecture 05 p. 62 / 74 | CUMED 的 SE/SP 数值位置不同；保留原表，正文按 p. 62 Table V 解读有无分割的对照 |
| Lecture 05 p. 82 / 83 | 指标分别以百分数和 0–1 尺度呈现，比较前需统一尺度 |
| Lecture 05 p. 90–98 | 超声测深使用往返时间；衰减中的传播路径长度也需区分单程与往返 |

## 引用与来源

课件包含 Stanford BIODS 220、CS231n、Justin Johnson 的教学材料及多篇论文图示。Lecture 05 另引用多模态融合、皮肤镜研究与 Alfred ICU 的超声教学材料。原截图保留课件上的来源、作者、论文题目和图注。查找研究原文时，应以对应原页的完整引用为准。

课程建议教材包括：

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [*Deep Learning*](https://www.deeplearningbook.org/).
- Jerry L. Prince, Jonathan M. Links, *Medical Imaging Signals and Systems*.
- Kevin Zhou, Hayit Greenspan, Dinggang Shen, *Deep Learning for Medical Image Analysis*.

本网站使用 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 构建，并使用 [KaTeX](https://katex.org/) 排版公式。

??? info "课程安排存档（2026 秋季）"

    以下按 Lecture 01a p. 45–48 整理，时间为课件中的安排或暂定日期。

    | 项目 | 比例 | 课件要求 |
    | --- | ---: | --- |
    | Programming Assignment | 20% | 分类、分割两个编程任务，提交定量和定性结果；暂定 9 月 20 日至 10 月 16 日 |
    | Paper Reading & Sharing | 20% | 10 分钟讲解 + 5 分钟问答；计划从 9 月 22 日开始 |
    | Midterm Exam | 30% | 深度学习与医学影像基础；闭卷，可带一张 A4 笔记 |
    | Final Project & Presentation | 25% | 1–2 人小组；调研、基线、改进、报告及展示；暂定 12 月第 2 周 |
    | Class Attendance | 5% | 课堂出勤 |

    课件列出的上课时间为周二 09:00–11:50，地点 Rm 2610（Lift 31–32）。迟交政策为共 3 天免费迟交额度，耗尽后每天扣 25%；实际执行以课程最新通知为准。

    可选教材包括 [Deep Learning](https://www.deeplearningbook.org/)、*Medical Imaging Signals and Systems*、*Deep Learning for Medical Image Analysis*。完整书目见原课件 p. 46。

    !!! note "课程强调的学习方式"
        理解模型如何从头实现、如何训练和调试，能把方法用于真实医学任务。课件鼓励讨论思路，同时要求提交自己的工作、注明合作者，并遵守课程的合作政策（p. 53）。

## 使用与维护

本站不是课程官方发布渠道。课程时间、考核与作业要求以老师最新通知为准。课件与所引用图片、论文的权利归原作者，本项目不对其另行授予开源许可。

如需反馈笔记中的错误，可在[项目仓库](https://github.com/ZJUCQR/ELEC5690)提出 Issue，附上章节与原课件页码，便于核对。
