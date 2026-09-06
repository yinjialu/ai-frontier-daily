// Browser fallback for official sites whose article links appear after hydration.
const { chromium } = require('playwright');
(async () => {
  const [url, pattern] = process.argv.slice(2);
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.route('**/*', route => ['image', 'font', 'media'].includes(route.request().resourceType()) ? route.abort() : route.continue());
    await page.goto(url, {waitUntil:'domcontentloaded', timeout:30000});
    await page.waitForFunction(pattern => [...document.querySelectorAll('a[href]')].filter(a => new RegExp(pattern).test(new URL(a.href).pathname)).length >= 3, pattern, {timeout:20000});
    process.stdout.write(await page.content());
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error.name + ': browser source failed'); process.exit(1); });
