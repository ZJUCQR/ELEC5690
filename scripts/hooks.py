import html
import re
import sys
from pathlib import Path
from mkdocs.utils import get_relative_url

sys.path.insert(0, str(Path(__file__).parent))
from prepare import prepare
from decks import DECKS

def on_pre_build(config):
    prepare()

def on_page_markdown(markdown, page, config, files):
    def figure(match):
        deck, number, caption = match.groups()
        spec = next(d for d in DECKS if d['id'] == deck)
        number = int(number)
        if not 1 <= number <= spec['pages']:
            raise ValueError(f'Invalid slide: {deck}/{number}')
        src = get_relative_url(f'assets/slides/{deck}/{number:03}.webp', page.url)
        viewer = get_relative_url(f'slides/generated/{deck}/', page.url) + f'#page={number}'
        label = html.escape(caption)
        return f'<figure class="slide-figure"><a href="{src}" data-zoom aria-label="放大：{label}"><img src="{src}" alt="{label}，Lecture {deck} 第 {number} 页" width="1600" height="900" loading="lazy" decoding="async"></a><figcaption><span>{label}</span><a href="{viewer}">Lecture {deck} · p. {number} ↗</a></figcaption></figure>'
    markdown = re.sub(r'\[\[slide:([\da-z]+):(\d+)\|([^\]]+)\]\]', figure, markdown)
    if page.file.src_uri.startswith('notes/'):
        words = len(re.findall(r'[\u4e00-\u9fff]|\b[a-zA-Z]+\b', markdown))
        minutes = max(1, round(words / 300))
        markdown = re.sub(r'(^# .+\n)', rf'\1\n<div class="reading-meta">ELEC 5690 <span>约 {minutes} 分钟阅读</span></div>\n', markdown, count=1)
    return markdown
