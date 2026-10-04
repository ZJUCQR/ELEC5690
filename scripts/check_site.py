"""Check the published tree: local links, assets, slide coverage, original PDFs."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser
import hashlib
import sys

sys.path.insert(0, str(Path(__file__).parent))
from decks import DECKS

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])

def main():
    errors = []
    pages = {}
    for file in SITE.rglob('*.html'):
        parser = Links()
        parser.feed(file.read_text())
        pages[file.resolve()] = parser
    for file, parser in pages.items():
        if file.name == '404.html':
            continue  # Root-relative fallback has a different URL context.
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if path.startswith('/ELEC5690/'):
                target = SITE / path.removeprefix('/ELEC5690/')
            elif path.startswith('/'):
                target = SITE / path.lstrip('/')
            else:
                target = file.parent / path if path else file
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            if not target.exists():
                errors.append(f'Missing target: {file.relative_to(SITE)} -> {link}')
            elif url.fragment and target in pages and not url.fragment.startswith('page='):
                fragment = unquote(url.fragment)
                if fragment not in pages[target].ids:
                    errors.append(f'Missing anchor: {file.relative_to(SITE)} -> {link}')
    total = 0
    for deck in DECKS:
        folder = SITE / 'assets/slides' / deck['id']
        expected = {f'{n:03}.webp' for n in range(1, deck['pages'] + 1)}
        actual = {f.name for f in folder.glob('*.webp')}
        if actual != expected:
            errors.append(f'Slide coverage mismatch: {deck["id"]}')
        original = hashlib.sha256((ROOT / deck['file']).read_bytes()).hexdigest()
        copied = hashlib.sha256((SITE / 'originals' / f'lecture-{deck["id"]}.pdf').read_bytes()).hexdigest()
        if original != copied:
            errors.append(f'PDF checksum mismatch: {deck["id"]}')
        total += len(actual)
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'PASS: {len(pages)} HTML pages; all local links and anchors resolve; {total} slide images; 5 byte-identical PDFs.')

if __name__ == '__main__':
    main()
