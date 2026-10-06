# ELEC 5690 · 医学影像分析课程笔记

**网站：https://zjucqr.github.io/ELEC5690/**

将六份 2026 秋季课程 PDF 整理为中文笔记，覆盖课程介绍、深度学习基础、分类、分割、训练策略、视网膜、多模态数据、皮肤镜与超声。保留全部 **604 页**原课件、**109 张正文例图**及原始 PDF 下载。

包含章节导航、页内目录、中英文搜索、本地公式排版、图片放大、原页跳转、深色模式与移动端布局。

## 本地预览

要求 Python 3.12 或更新版本。原始 PDF 必须保留在仓库根目录。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

访问终端显示的本地 URL。首次构建会逐页渲染课件，此后根据 PDF 内容指纹复用截图。

## 构建与验证

```sh
python -m mkdocs build --strict
python scripts/check_site.py
```

`site/` 为完整静态站点，可放在 GitHub Pages 项目子路径下。数学字体、KaTeX、页面样式及课件图片随站点发布，不使用字体或公式 CDN。

浏览器验证需要额外依赖：

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
mkdir -p .work/preview
ln -s ../../site .work/preview/ELEC5690
python -m http.server 8000 --bind 127.0.0.1 --directory .work/preview
```

在另一终端运行：

```sh
.venv/bin/python scripts/browser_check.py
```

已有预览链接时无需重复运行 `ln -s`。截图保存于 `.work/screenshots/`。检查其他站点地址时，可通过 `SITE_TEST_URL` 设置测试入口。

## GitHub Pages

仓库使用 GitHub Actions 发布，工作流在推送 `main` 或手动运行时构建、校验、上传并部署。仓库 **Settings → Pages → Source** 应为 **GitHub Actions**。

若 fork 到其他仓库，修改 `mkdocs.yml` 的 `site_url`、`repo_url`、`repo_name`，以及首页/资料说明中的仓库链接和 README 中的网站地址。浏览器验证默认使用 `/ELEC5690/`；测试其他路径时设置 `SITE_TEST_URL`。

## 文件组织

```text
Lecture*.pdf                 原始课件，不修改
PLAN.md                      实施规划与验收范围
mkdocs.yml                   站点导航、主题及插件
docs/notes/                  六章人工整理的 Markdown
docs/index.md                课程首页与术语、公式速查
docs/reference/              资料说明与旧速查入口
docs/assets/stylesheets/     页面样式
docs/assets/javascripts/     图片放大、课件浏览、数学排版
docs/assets/vendor/katex/    本地数学排版资源及许可证
scripts/decks.py             课件、页数与主题定位映射
scripts/prepare.py           渲染图片、复制 PDF、生成静态图集
scripts/hooks.py             构建钩子、正文截图及阅读时间
scripts/check_site.py        链接、页数与 PDF 内容验证
scripts/browser_check.py     真实浏览器阅读路径验证
.github/workflows/pages.yml  自动构建和发布
```

`docs/assets/slides/`、`docs/originals/`、`docs/slides/generated/` 与 `site/` 均在构建时生成，不需要提交。原始 PDF、人工笔记和构建代码提交即可。

正文插图用以下形式引用，构建时生成带原页链接的图片：

```text
[[slide:03:33|课件原例：IoU 与 Dice]]
```

增加或替换课件时，应同时更新 `scripts/decks.py` 中的页数、主题映射、笔记及相关来源说明。首页眼底图来自 Lecture 01a p. 6 的原图节选。

Lecture 05 文件共 100 页，封面编号为 Lecture 06；站点按文件名接续第 5 章，并保留封面与 PDF 原貌。内容还包含超声成像，已纳入笔记和首页速查。

## 资料归属

课程课件及其中论文、教学材料的图示归原作者。本项目保留原页引用，不对这些材料另行授予开源许可。中文笔记中的补充推导和实现说明已作标注；内容纠正与页码对应见网站的“资料与编写说明”。

技术依赖：MkDocs / Material for MkDocs、PyMuPDF、Pillow、jieba 与 KaTeX；第三方资源遵循各自许可证。
