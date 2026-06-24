const assert = require("assert");
const Cards = require("./cards.js");

const DATA = {
  kind: "deepdive",
  slug: "demo",
  title: "标题示例",
  cover: null,
  cards: [
    { heading: "要点一", lines: ["第一行", "第二行"] },
    { heading: "要点二", lines: ["只有一行"] },
  ],
};

const deck = Cards.buildDeck(DATA);
// 封面 + 2 张知识卡 = 3
assert.strictEqual(deck.length, 3, "卡片数应为封面+2");
// 全部 1080×1440
deck.forEach((c) => {
  assert.strictEqual(c.w, 1080, "宽 1080");
  assert.strictEqual(c.h, 1440, "高 1440");
  assert.ok(/deepdive/.test(c.cls), "cls 含 deepdive");
  assert.ok(c.name, "有 name");
  assert.ok(/inner/.test(c.inner), "inner 含 .inner 容器");
});
// 封面卡含标题文字（无封面图时）
assert.ok(deck[0].inner.includes("标题示例"), "封面卡含标题");
// 知识卡含 heading 与某行
assert.ok(deck[1].inner.includes("要点一"), "知识卡含 heading");
assert.ok(deck[1].inner.includes("第二行"), "知识卡含行文本");
console.log("PASS deepdive cards");
