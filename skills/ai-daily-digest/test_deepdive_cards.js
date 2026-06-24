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

const EDITORIAL = {
  kind: "deepdive",
  slug: "demo",
  title: "Claude Tag\n给 AI 发工牌",
  cover: "data:image/png;base64,eA==",
  style: "editorial",
  cards: [
    {
      kind: "quote",
      heading: "真正变化\n不是进 Slack",
      quote: "不是 Claude 进了 Slack，而是它换了一套身份模型。",
      notes: [
        ["01", "过去：AI 借你的账号和权限干活。"],
        ["02", "现在：AI 需要自己的身份和审计记录。"],
      ],
      footer: ["核心判断", "Swipe"],
    },
    {
      kind: "image",
      heading: "从个人钥匙\n到频道身份",
      image: "data:image/png;base64,eA==",
      caption: ["权限从 per-user 搬到 per-channel。"],
      footer: ["Agent Identity", "02 / 03"],
    },
    {
      kind: "closing",
      heading: "AI 当同事\n先要有身份",
      quote: "“代表你”是工具逻辑；“成为它自己”才是同事逻辑。",
      notes: [["READ", "完整长文已发公众号：变量生活"]],
      footer: ["变量生活", "完整长文见公众号"],
    },
  ],
};

const editorialDeck = Cards.buildDeck(EDITORIAL);
assert.ok(/xhs-card/.test(editorialDeck[0].cls), "editorial 封面使用杂志卡 class");
assert.ok(editorialDeck[1].inner.includes("quote-shot"), "quote 卡含引用版式");
assert.ok(editorialDeck[2].inner.includes("image-page-img"), "image 卡含插画版式");
assert.ok(editorialDeck[3].inner.includes("完整长文已发公众号"), "closing 卡含收束信息");
console.log("PASS deepdive cards");
