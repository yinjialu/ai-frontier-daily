#!/usr/bin/env node
/* 渲染器：DATA(json) -> 每张卡片一个 PNG。
   用法：node render.js <data.json> <outDir> [--engine wkhtml|playwright|auto] [--only N]
   - wkhtml 后端：每张卡片生成独立 HTML，wkhtmltoimage 渲染（无需联网/浏览器下载）
   - playwright 后端：加载 cards.html 注入 DATA，对每个 .card 元素截图（字体保真度更高，推荐生产用）
*/
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const Cards = require("./cards.js");

const CSS = fs.readFileSync(path.join(__dirname, "cards.css"), "utf8");
const FONTS = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,900;1,9..144,500&family=Noto+Serif+SC:wght@500;700;900&family=Noto+Sans+SC:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">';

// 移动端优先：默认 1 倍渲染（卡片本就 1080 宽=小红书推荐尺寸）+ JPEG，
// 一张约 200–400KB，天然低于公众号在文图 1MB 上限，省去后压缩。
// 可用环境变量覆盖：CARD_FORMAT=png|jpeg、CARD_QUALITY=1..100、CARD_SCALE=1|2。
const FMT = (process.env.CARD_FORMAT || "jpeg").toLowerCase();
const EXT = FMT === "png" ? "png" : "jpg";
const QUALITY = parseInt(process.env.CARD_QUALITY || "86", 10);
const SCALE = parseInt(process.env.CARD_SCALE || "1", 10);

function cardPage(card, withFonts){
  return `<!doctype html><html><head><meta charset="utf-8">${withFonts?FONTS:""}
<style>${CSS}</style>
<style>html,body{margin:0;padding:0;background:#fff}.stage{display:inline-block}</style>
</head><body><div class="stage"><div class="card ${card.cls}"${card.h?` style="width:${card.w}px;height:${card.h}px"`:` style="width:${card.w}px"`}>${card.inner}</div></div></body></html>`;
}

function renderWkhtml(card, outFile, tmpDir){
  const htmlFile = path.join(tmpDir, card.name.replace(/[^\w\u4e00-\u9fa5]+/g,"_") + ".html");
  fs.writeFileSync(htmlFile, cardPage(card, false));
  const args = ["--enable-local-file-access","--encoding","utf-8",
                "--format", EXT === "jpg" ? "jpg" : "png", "--quality", String(QUALITY),
                "--load-error-handling","ignore","--load-media-error-handling","ignore",
                "--width", String(card.w)];
  if (card.h) args.push("--height", String(card.h));
  args.push(htmlFile, outFile);
  execFileSync("wkhtmltoimage", args, {stdio:"pipe"});
}

async function renderPlaywright(cards, outDir){
  const { chromium } = require("playwright");           // 生产环境：npm i playwright && npx playwright install chromium
  const launchOpts = process.env.PLAYWRIGHT_EXECUTABLE_PATH
    ? { executablePath: process.env.PLAYWRIGHT_EXECUTABLE_PATH }
    : {};
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage({deviceScaleFactor:SCALE});
  const fileUrl = "file://" + path.join(__dirname, "cards.html");
  for (const card of cards){
    const html = cardPage(card, true);
    await page.setContent(html, {waitUntil:"networkidle"});
    const el = await page.$(".card");
    const shot = {path: path.join(outDir, card.name + "." + EXT)};
    if (EXT === "jpg") { shot.type = "jpeg"; shot.quality = QUALITY; }
    await el.screenshot(shot);
    console.log("  ✓", card.name + "." + EXT);
  }
  await browser.close();
}

(async function main(){
  const [,, dataPath, outDir, ...rest] = process.argv;
  if (!dataPath || !outDir){ console.error("usage: node render.js <data.json> <outDir> [--engine ...] [--only N]"); process.exit(1); }
  let engine = "auto"; let only = null;
  for (let i=0;i<rest.length;i++){ if(rest[i]==="--engine") engine=rest[++i]; if(rest[i]==="--only") only=parseInt(rest[++i],10); }

  const DATA = JSON.parse(fs.readFileSync(dataPath,"utf8"));
  if (process.env.CARD_STYLE) DATA.style = process.env.CARD_STYLE;   // 覆盖/启用风格层（如 glass）
  let cards = Cards.buildDeck(DATA);
  if (only!=null) cards = [cards[only]];
  fs.mkdirSync(outDir, {recursive:true});

  if (engine==="auto"){ try{ require.resolve("playwright"); engine="playwright"; }catch(e){ engine="wkhtml"; } }
  console.log(`engine=${engine}, ${cards.length} cards -> ${outDir}`);

  if (engine==="playwright"){ await renderPlaywright(cards, outDir); }
  else {
    const tmpDir = fs.mkdtempSync("/tmp/cards-");
    for (const card of cards){
      renderWkhtml(card, path.join(outDir, card.name + "." + EXT), tmpDir);
      console.log("  ✓", card.name + "." + EXT);
    }
  }
  fs.writeFileSync(path.join(outDir,"manifest.json"),
    JSON.stringify({date:DATA.date, cnDate:DATA.cnDate, files:cards.map(c=>c.name+"."+EXT)}, null, 2));
})();
