// Печать презентации в PDF: node _build/pdf.js  (нужен playwright)
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const root = path.resolve(__dirname, '..');
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'out', 'presentation.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(root, 'zptk-prezentaciya.pdf'), width: '297mm', height: '167mm', printBackground: true, preferCSSPageSize: true });
  await b.close();
  console.log('zptk-prezentaciya.pdf готов');
})();
