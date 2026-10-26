// Рендер картинки-превью для соцсетей: node _build/og/render.js -> og-zptk.jpg
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(__dirname, 'og.html'));
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname, '..', '..', 'og-zptk.jpg'), type: 'jpeg', quality: 90 });
  await b.close();
})();
