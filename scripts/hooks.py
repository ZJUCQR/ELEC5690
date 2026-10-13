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

def on_post_build(config):
    """Keep existing chapter bookmarks without duplicating chapter content."""
    site = Path(config['site_dir'])
    for deck in DECKS:
        legacy = f'notes/{deck["note"]}/'
        target = get_relative_url(f'lectures/{deck["note"]}/', legacy)
        canonical = config['site_url'].rstrip('/') + f'/lectures/{deck["note"]}/'
        folder = site / legacy
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'index.html').write_text(
            '<!doctype html><html lang="zh"><head><meta charset="utf-8">'
            '<meta name="robots" content="noindex">'
            f'<link rel="canonical" href="{html.escape(canonical)}">'
            f'<meta http-equiv="refresh" content="0;url={html.escape(target)}">'
            '<title>课程章节</title></head><body>'
            f'<p><a href="{html.escape(target)}">前往课程章节</a></p>'
            f'<script>location.replace("{target}" + location.search + location.hash)</script>'
            '</body></html>', encoding='utf-8')

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
    if page.file.src_uri.startswith('lectures/'):
        words = len(re.findall(r'[\u4e00-\u9fff]|\b[a-zA-Z]+\b', markdown))
        minutes = max(1, round(words / 300))
        markdown = re.sub(r'(^# .+\n)', rf'\1\n<div class="reading-meta">ELEC 5690 <span>约 {minutes} 分钟阅读</span></div>\n', markdown, count=1)
    return markdown
