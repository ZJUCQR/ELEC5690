"""Exercise the reading paths in Chromium on desktop and mobile."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from decks import DECKS

BASE = os.environ.get('SITE_TEST_URL', 'http://127.0.0.1:8000/ELEC5690/').rstrip('/') + '/'
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.work/screenshots'
OUT.mkdir(parents=True, exist_ok=True)

def run():
    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}') if response.status >= 400 and response.url.startswith(BASE) else None)
        page.goto(BASE)
        expect(page.locator('.chapter-row')).to_have_count(len(DECKS))
        expect(page.locator('.md-tabs__link')).to_have_text(['学习笔记', '原 PPT'])
        page.screenshot(path=str(OUT / 'home-desktop.png'), full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Desktop overflow'

        for slug in [deck['note'] for deck in DECKS]:
            page.goto(BASE + 'lectures/' + slug + '/')
            expect(page.locator('h1')).to_be_visible()
            assert page.locator('.katex-error').count() == 0, f'Math error on {slug}'
            assert page.locator('.slide-figure').count() >= 7
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), slug + ' overflow'
        page.goto(BASE + 'lectures/02-classification/')
        assert page.locator('.katex').count() > 20
        first = page.locator('.slide-figure a[data-zoom]').first
        first.click()
        expect(page.locator('.image-dialog')).to_be_visible()
        page.locator('[data-size]').click()
        expect(page.locator('.image-dialog')).to_have_class('image-dialog is-zoomed')
        page.keyboard.press('Escape')
        expect(page.locator('.image-dialog')).not_to_be_visible()
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(OUT / 'classification-desktop.png'), full_page=False)

        search = page.locator('input[data-md-component="search-query"]')
        search.fill('视网膜')
        expect(page.locator('.md-search-result__item').first).to_be_visible(timeout=15000)
        chinese_results = page.locator('.md-search-result__item').count()
        assert '视网膜' in page.locator('.md-search-result__list').inner_text().replace('\u200b', '')
        search.fill('')
        expect(page.locator('.md-search-result__item')).to_have_count(0)
        search.fill('Dice')
        expect(page.locator('.md-search-result__item').first).to_be_visible(timeout=15000)
        assert 'dice' in page.locator('.md-search-result__list').inner_text().lower()
        search.fill('')
        expect(page.locator('.md-search-result__item')).to_have_count(0)
        search.fill('皮肤镜')
        expect(page.locator('.md-search-result__list a[href*="lectures/05-multimodal-dermoscopy/"]').first).to_be_visible(timeout=15000)
        search.fill('')
        expect(page.locator('.md-search-result__item')).to_have_count(0)
        search.fill('腺体')
        expect(page.locator('.md-search-result__list a[href*="lectures/06-ultrasound-pathology/"]').first).to_be_visible(timeout=15000)
        page.keyboard.press('Escape')

        page.goto(BASE + 'slides/generated/03/#page=33')
        expect(page.locator('[data-page]')).to_have_value('33')
        expect(page.locator('[data-viewer-image] img')).to_have_attribute('src', BASE + 'assets/slides/03/033.webp')
        page.locator('[data-next]').click()
        expect(page.locator('[data-page]')).to_have_value('34')
        page.go_back()
        expect(page.locator('[data-page]')).to_have_value('33')
        page.locator('[data-page]').select_option('139')
        expect(page.locator('[data-next]')).to_be_disabled()
        page.locator('[data-page]').select_option('1')
        expect(page.locator('[data-prev]')).to_be_disabled()
        page.locator('h1').click()
        page.keyboard.press('ArrowRight')
        expect(page.locator('[data-page]')).to_have_value('2')
        page.locator('[data-goto="30"]').click()
        expect(page.locator('[data-page]')).to_have_value('30')
        page.screenshot(path=str(OUT / 'slide-viewer.png'), full_page=False)

        page.goto(BASE + 'lectures/05-multimodal-dermoscopy/')
        expect(page.locator('[id="58-ultrasound"]')).to_have_count(0)
        expect(page.locator('[id="52-fusion"]')).to_be_visible()
        for slide in [34, 35, 36, 37, 38, 39, 40]:
            expect(page.locator(f'.slide-figure img[src$="/05/{slide:03}.webp"]')).to_have_count(1)
        for tab, quote in [('Early fusion', 'before any model processing'), ('Joint fusion', 'combined-modality components'), ('Late fusion', 'Individual modality outputs')]:
            page.locator('.tabbed-labels label').filter(has_text=tab).click()
            expect(page.locator('blockquote').filter(has_text=quote)).to_be_visible()
        expect(page.locator('.katex').first).to_be_attached()
        assert page.locator('.arithmatex').evaluate_all('els => els.every(el => el.querySelector(".katex"))')
        assert page.locator('.katex-error').count() == 0
        page.screenshot(path=str(OUT / 'lecture05-desktop.png'), full_page=False)
        page.locator('.slide-figure figcaption a[href$="/05/#page=12"]').click()
        expect(page.locator('[data-page]')).to_have_value('12')
        expect(page.locator('[data-viewer-image] img')).to_have_attribute('src', BASE + 'assets/slides/05/012.webp')
        page.locator('[data-page]').select_option('100')
        expect(page.locator('[data-next]')).to_be_disabled()
        expect(page.locator('[data-pdf-page]')).to_have_attribute('href', BASE + 'originals/lecture-05.pdf#page=100')

        page.goto(BASE)
        page.locator('.chapter-row[href="lectures/06-ultrasound-pathology/"]').click()
        expect(page.locator('h1')).to_contain_text('Ultrasound & Pathology')
        expect(page.locator('.katex').first).to_be_attached()
        assert page.locator('.arithmatex').evaluate_all('els => els.every(el => el.querySelector(".katex"))')
        assert page.locator('.katex-error').count() == 0
        for heading in ['EchoPrime', 'Attention MIL', 'MSSG', 'TITAN', 'QoQ-Med']:
            expect(page.locator('h2', has_text=heading)).to_have_count(1)
        for slide in [89, 94, 97, 98]:
            expect(page.locator(f'.slide-figure img[src$="/05/{slide:03}.webp"]')).to_have_count(1)
        expect(page.locator('h3', has_text='26 μs')).to_have_count(1)
        page.screenshot(path=str(OUT / 'lecture06-desktop.png'), full_page=False)
        page.locator('.slide-figure figcaption a[href$="/06/#page=5"]').click()
        expect(page.locator('[data-page]')).to_have_value('5')
        expect(page.locator('[data-viewer-image] img')).to_have_attribute('src', BASE + 'assets/slides/06/005.webp')
        page.locator('[data-page]').select_option('110')
        expect(page.locator('[data-next]')).to_be_disabled()
        expect(page.locator('[data-pdf-page]')).to_have_attribute('href', BASE + 'originals/lecture-06.pdf#page=110')
        page.goto(BASE + 'notes/05-multimodal-dermoscopy/#58-ultrasound')
        expect(page).to_have_url(BASE + 'lectures/06-ultrasound-pathology/#61-ultrasound-physics')
        page.goto(BASE + 'slides/')
        expect(page.locator('.md-content a[href="generated/06/"]')).to_be_visible()
        expect(page.locator('.md-content a[href="../originals/lecture-06.pdf"]')).to_have_count(1)

        page.goto(BASE)
        page.locator('label[for="__palette_1"]').click()
        expect(page.locator('body')).to_have_attribute('data-md-color-scheme', 'slate')
        page.screenshot(path=str(OUT / 'home-dark.png'), full_page=False)
        page.locator('label[for="__palette_0"]').click()

        mobile = browser.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, device_scale_factor=1)
        phone = mobile.new_page()
        phone.on('pageerror', lambda error: errors.append('mobile: ' + str(error)))
        for path in ['', 'slides/', *[f'lectures/{deck["note"]}/' for deck in DECKS], 'slides/generated/04/#page=108', 'slides/generated/05/#page=94', 'slides/generated/06/#page=110']:
            phone.goto(BASE + path)
            assert phone.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Mobile overflow: ' + path
            if not path:
                phone.screenshot(path=str(OUT / 'home-mobile.png'), full_page=True)
        phone.goto(BASE)
        phone.locator('.md-header label[for="__drawer"]').click()
        expect(phone.locator('#__drawer')).to_be_checked()
        phone.locator('.md-nav--primary a[href$="lectures/03-segmentation/"]').click()
        expect(phone.locator('h1')).to_contain_text('Segmentation')
        phone.screenshot(path=str(OUT / 'segmentation-mobile.png'), full_page=False)
        phone.goto(BASE + 'lectures/05-multimodal-dermoscopy/')
        phone.screenshot(path=str(OUT / 'lecture05-mobile.png'), full_page=False)
        phone.goto(BASE + 'lectures/06-ultrasound-pathology/')
        phone.screenshot(path=str(OUT / 'lecture06-mobile.png'), full_page=False)

        nojs = browser.new_context(java_script_enabled=False)
        static = nojs.new_page()
        static.goto(BASE + 'slides/generated/01a-001-020/')
        expect(static.locator('.slide-figure')).to_have_count(20)
        static.goto(BASE + 'slides/generated/05-081-100/')
        expect(static.locator('.slide-figure')).to_have_count(20)
        static.goto(BASE + 'slides/generated/06-101-110/')
        expect(static.locator('.slide-figure')).to_have_count(10)
        browser.close()
    assert not errors, errors
    print(json.dumps({'status':'PASS','chinese_search_results':chinese_results,'screenshots':str(OUT),'checks':['chapter content','local math','image enlargement','Chinese/English search','slide deep links','history','keyboard navigation','theme toggle','mobile navigation','responsive layout','no-JS gallery']},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    run()
