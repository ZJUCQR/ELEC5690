DECKS = [
    dict(id='01a', title='Course Introduction', zh='课程介绍', file='Lecture01a-Course Introduction.pdf', pages=56, note='01a-introduction', sections=[(1, '课程信息与医学影像'), (8, 'AI、ML 与 DL'), (9, '人工智能的发展'), (26, '学习任务与特征'), (35, 'CNN 与训练'), (45, '课程安排与考核')]),
    dict(id='01b', title='Deep Learning Fundamentals', zh='深度学习基础', file='Lecture01b-Deep Learning Fundamentals.pdf', pages=76, note='01b-fundamentals', sections=[(1, '机器学习与深度学习'), (8, '回归、损失与梯度'), (18, '多层网络与反向传播'), (30, '课堂问答'), (35, '框架实现'), (39, '优化与学习率'), (43, '学习曲线与调试'), (55, '正则化与泛化'), (66, '推理与模型设计')]),
    dict(id='02', title='Basic Vision Models · Classification', zh='图像分类', file='Lecture02-Basic Vision Models (Classification).pdf', pages=120, note='02-classification', sections=[(1, '卷积与池化回顾'), (23, '优化方法'), (30, '分类网络与损失'), (54, '数据划分与迁移学习'), (72, '评价指标'), (84, 'DR/DME 与 CANet'), (101, '胸片迁移学习'), (104, '肺结节多视图'), (106, '糖尿病视网膜病变检测'), (112, '皮肤病变与胸片筛查'), (119, '乳腺筛查')]),
    dict(id='03', title='Basic Vision Models · Segmentation', zh='分割、三维与视频', file='Lecture03-Basic Vision Models (Segmentation).pdf', pages=139, note='03-segmentation', sections=[(1, '分类回顾'), (15, '分割与 U-Net'), (19, '上采样'), (30, '分割指标与损失'), (43, '三维卷积'), (51, '3D U-Net'), (61, '脑微出血与肝脏分割'), (72, '多尺度椎间盘分割'), (82, 'H-DenseUNet'), (111, '视频模型与循环网络')]),
    dict(id='04', title='Training Strategies & Retinal Images', zh='训练策略与视网膜影像', file='Lecture04 - Trainnig Strategies and Medical Images (Retinal Images).pdf', pages=113, note='04-training-retina', sections=[(1, '三维与视频回顾'), (17, '数据预处理'), (27, '数据增强'), (30, '损失函数'), (36, '影像分析工具'), (44, '眼部生理与疾病'), (54, 'Fundus 与 OCT'), (71, 'RETFound'), (80, 'DeepDR Plus'), (89, 'DeepDR-LLM'), (98, '儿童视力筛查'), (107, 'SLIViT')]),
]

def topic(deck, page):
    return next(title for start, title in reversed(deck['sections']) if page >= start)
