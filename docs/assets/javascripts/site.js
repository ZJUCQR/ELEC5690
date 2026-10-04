/* Local-only mathematics, accessible image enlargement, and slide navigation. */
(() => {
  'use strict';
  // Material listens for keyup. Also refresh for paste, mobile keyboards, and IME.
  const searchInput = document.querySelector('input[data-md-component="search-query"]');
  if (searchInput) {
    const refreshSearch = () => searchInput.dispatchEvent(new Event('keyup', {bubbles: true}));
    searchInput.addEventListener('input', event => { if (!event.isComposing) refreshSearch(); });
    searchInput.addEventListener('compositionend', refreshSearch);
    searchInput.form.addEventListener('reset', () => queueMicrotask(refreshSearch));
  }
  document.querySelectorAll('.arithmatex').forEach(element => {
    const text = element.textContent;
    const display = text.startsWith('\\[');
    const formula = text.replace(/^\\\(|\\\)$/g, '').replace(/^\\\[|\\\]$/g, '');
    if (window.katex) window.katex.render(formula, element, {displayMode: display, throwOnError: false, strict: 'ignore'});
  });

  const dialog = document.createElement('dialog');
  dialog.className = 'image-dialog';
  dialog.setAttribute('aria-label', '课件图片放大预览');
  dialog.innerHTML = '<div class="dialog-controls"><button type="button" data-size>原始尺寸</button><button type="button" data-close aria-label="关闭图片预览">关闭 ×</button></div><div class="dialog-image"><img alt=""></div><p></p>';
  document.body.append(dialog);
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-size]').addEventListener('click', event => {
    const zoomed = dialog.classList.toggle('is-zoomed');
    event.target.textContent = zoomed ? '适应窗口' : '原始尺寸';
  });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  document.querySelectorAll('a[data-zoom]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const source = link.querySelector('img');
      const image = dialog.querySelector('img');
      image.src = link.href;
      image.alt = source?.alt || '课件原图';
      dialog.querySelector('p').textContent = image.alt + ' · Esc 关闭';
      dialog.classList.remove('is-zoomed');
      dialog.querySelector('[data-size]').textContent = '原始尺寸';
      dialog.showModal();
    });
  });

  const viewer = document.querySelector('.slide-viewer');
  if (!viewer) return;
  const count = Number(viewer.dataset.count);
  const select = viewer.querySelector('[data-page]');
  const imageLink = viewer.querySelector('[data-viewer-image]');
  const image = imageLink.querySelector('img');
  const imageBase = new URL('.', image.src);
  const pdfLink = viewer.querySelector('[data-pdf-page]');
  const pdfBase = pdfLink.href.split('#')[0];
  let current = 1;
  function show(number, updateURL = false) {
    const n = Number(number);
    current = Math.max(1, Math.min(count, Number.isFinite(n) ? Math.trunc(n) : 1));
    select.value = String(current);
    image.src = new URL(String(current).padStart(3, '0') + '.webp', imageBase).href;
    image.alt = `Lecture ${viewer.dataset.deck} 第 ${current} 页 · ${select.selectedOptions[0].textContent.split(' · ').slice(1).join(' · ')}`;
    imageLink.href = image.src;
    pdfLink.href = pdfBase + '#page=' + current;
    viewer.querySelector('[data-counter]').textContent = `${current} / ${count} 页`;
    viewer.querySelector('[data-prev]').disabled = current === 1;
    viewer.querySelector('[data-next]').disabled = current === count;
    if (updateURL) history.pushState(null, '', '#page=' + current);
  }
  function fromHash() { show(location.hash.match(/^#page=(\d+)$/)?.[1] || 1); }
  select.addEventListener('change', () => show(select.value, true));
  viewer.querySelector('[data-prev]').addEventListener('click', () => show(current - 1, true));
  viewer.querySelector('[data-next]').addEventListener('click', () => show(current + 1, true));
  document.querySelectorAll('[data-goto]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    show(link.dataset.goto, true);
    viewer.scrollIntoView({block: 'center'});
  }));
  document.addEventListener('keydown', event => {
    if (dialog.open || document.querySelector('#__search')?.checked || /INPUT|SELECT|TEXTAREA|BUTTON/.test(event.target.tagName) || event.target.isContentEditable) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); show(current + (event.key === 'ArrowLeft' ? -1 : 1), true);
    }
  });
  window.addEventListener('hashchange', fromHash);
  window.addEventListener('popstate', fromHash);
  fromHash();
})();
