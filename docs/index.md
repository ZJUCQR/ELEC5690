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

正文中的 **Lecture / p.** 链接可以定位到对应原页。连续动画页和重复回顾在笔记中合并说明，全部 504 页仍保留在[课件资料库](slides/index.md)中。

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

## 编写进度

- [x] Lecture 01a：课程介绍与 CNN 入门
- [x] Lecture 01b：基础概念、公式与训练方法
- [x] Lecture 02：分类、评价与医学案例
- [x] Lecture 03：分割、三维与视频
- [x] Lecture 04：训练策略与视网膜研究
- [x] 全部原页、PDF 下载、[术语与公式速查](reference/glossary.md)

!!! note "资料说明"
    这是一份学习整理，不是课程官方讲义。正文中另行推导的算例和代码会标注为补充；课件原图保留其引用。页面组织与语言写法参考 [T-ComputerNetworks](https://zhengliangduanfang.github.io/T-ComputerNetworks/)，视觉设计为本课程单独调整。详见[资料与编写说明](reference/sources.md)。
