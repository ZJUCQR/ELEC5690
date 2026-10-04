"""Reproducibly render every original slide and build accessible slide indexes."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import sys
import pymupdf as fitz
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from decks import DECKS, topic

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
VERSION = 'webp-1600-q88-v1'

def prepare():
    output = DOCS / 'slides/generated'
    output.mkdir(parents=True, exist_ok=True)
    (DOCS / 'originals').mkdir(exist_ok=True)
    manifest = []
    for deck in DECKS:
        source = ROOT / deck['file']
        checksum = hashlib.sha256(source.read_bytes()).hexdigest()
        folder = DOCS / 'assets/slides' / deck['id']
        folder.mkdir(parents=True, exist_ok=True)
        stamp = folder / '.fingerprint'
        fingerprint = checksum + VERSION
        ready = stamp.exists() and stamp.read_text() == fingerprint
        pdf = fitz.open(source)
        assert len(pdf) == deck['pages'], f'Unexpected page count: {source.name}'
        for i, page in enumerate(pdf, 1):
            target = folder / f'{i:03}.webp'
            if ready and target.exists():
                continue
            pix = page.get_pixmap(matrix=fitz.Matrix(1600 / page.rect.width, 1600 / page.rect.width), alpha=False)
            img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
            img.save(target, 'WEBP', quality=88, method=4)
        pdf.close()
        stamp.write_text(fingerprint)
        dest = DOCS / 'originals' / f'lecture-{deck["id"]}.pdf'
        if not dest.exists() or hashlib.sha256(dest.read_bytes()).hexdigest() != checksum:
            shutil.copyfile(source, dest)
        count = deck['pages']
        options = ''.join(f'<option value="{p}">p. {p} · {html.escape(topic(deck, p))}</option>' for p in range(1, count + 1))
        lines = [f'# Lecture {deck["id"]} · {deck["zh"]}', '',
            f'{deck["title"]} · **{count} 页** · [阅读中文笔记](../../notes/{deck["note"]}.md) · [下载完整 PDF](../../originals/lecture-{deck["id"]}.pdf)', '',
            '使用下方页码选择原页。左右方向键可以翻页，点击图像可放大；每一页都有可分享的链接。', '',
            f'<div class="slide-viewer" data-deck="{deck["id"]}" data-count="{count}">',
            '<div class="viewer-toolbar"><button type="button" data-prev aria-label="上一页">← 上一页</button>',
            f'<label>页码 <select data-page aria-label="选择课件页码">{options}</select></label>',
            '<button type="button" data-next aria-label="下一页">下一页 →</button></div>',
            f'<a data-zoom data-viewer-image href="../../../assets/slides/{deck["id"]}/001.webp"><img src="../../../assets/slides/{deck["id"]}/001.webp" width="1600" height="900" alt="Lecture {deck["id"]} 第 1 页" fetchpriority="high"></a>',
            '<div class="viewer-footer"><span data-counter aria-live="polite"></span><a data-pdf-page href="../../../originals/lecture-'+deck['id']+'.pdf#page=1">在 PDF 中查看此页 ↗</a></div>',
            '</div>', '', '## 主题定位', '', '| 主题 | 起始页 |', '| --- | --- |']
        for start, title in deck['sections']:
            lines.append(f'| {title} | <a href="#page={start}" data-goto="{start}">p. {start}</a> |')
        lines += ['', '## 全部原页', '', '下列静态图集保留全部页面，也可在不启用 JavaScript 时阅读。', '']
        for start in range(1, count + 1, 20):
            end = min(start + 19, count)
            name = f'{deck["id"]}-{start:03}-{end:03}.md'
            lines.append(f'- [第 {start}–{end} 页]({name})')
            gallery = ['---', 'search:', '  exclude: true', '---', '', f'# Lecture {deck["id"]} · 第 {start}–{end} 页', '',
                       f'[← 返回课件浏览器]({deck["id"]}.md) · [中文笔记](../../notes/{deck["note"]}.md)', '']
            for p in range(start, end + 1):
                gallery += [f'## 第 {p} 页 · {topic(deck, p)}', '', f'[[slide:{deck["id"]}:{p}|{topic(deck, p)}]]', '']
            if end < count:
                gallery.append(f'[下一组原页 →]({deck["id"]}-{end+1:03}-{min(end+20,count):03}.md)')
            (output / name).write_text('\n'.join(gallery), encoding='utf-8')
        (output / f'{deck["id"]}.md').write_text('\n'.join(lines), encoding='utf-8')
        manifest.append({**deck, 'sha256': checksum})
        print(f'Prepared Lecture {deck["id"]}: {count} pages', flush=True)
    (DOCS / 'assets/slide-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    prepare()
