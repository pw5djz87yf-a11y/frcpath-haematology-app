// Screenshot each HTML frame to PNG at 1920x1080. Usage: node shoot.js '<json [{html,png}]>'
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  for (const j of jobs) {
    await page.goto('file://' + j.html);
    await page.screenshot({ path: j.png });
  }
  await browser.close();
})();
