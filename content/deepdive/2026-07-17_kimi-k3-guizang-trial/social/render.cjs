const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const root = __dirname;
const targets = [
  ['#xhs-01', 'xhs-01-cover.png'],
  ['#xhs-02', 'xhs-02-model.png'],
  ['#xhs-03', 'xhs-03-workflow.png'],
  ['#xhs-04', 'xhs-04-vision-loop.png'],
  ['#xhs-05', 'xhs-05-guardrails.png'],
  ['#xhs-06', 'xhs-06-takeaway.png'],
  ['#wechat-21x9', 'wechat-21x9-cover.png'],
  ['#wechat-1x1', 'wechat-1x1-cover.png'],
  ['#wechat-pair-preview', 'wechat-cover-pair-preview.png'],
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 2600, height: 1500 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(root, 'index.html')).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  for (const [selector, file] of targets) {
    const node = page.locator(selector);
    await node.screenshot({ path: path.join(root, 'output', file) });
  }
  await browser.close();
})().catch((error) => { console.error(error); process.exit(1); });
