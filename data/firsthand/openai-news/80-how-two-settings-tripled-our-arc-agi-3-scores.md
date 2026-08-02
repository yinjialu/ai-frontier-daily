---
type: Article
title: How enabling two settings tripled our scores on the ARC-AGI-3 benchmark
source: openai-news
resource: https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores
published: 2026-07-29
tags: [ARC-AGI-3, 推理保留, 上下文压缩, AI Agent]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI发现，在ARC-AGI-3基准测试中，启用保留推理和压缩两个API设置后，GPT-5.6 Sol得分从13.3%升至38.3%，输出token减少6倍。默认丢弃推理历史和滚动截断导致模型难以学习，而保留推理记忆与压缩上下文能显著提升Agent性能。

## Full Text

How enabling two settings tripled our scores on the ARC-AGI-3 benchmark | OpenAI
Skip to main content
Research
Products
Business
Developers
Company
Foundation
(opens in a new window)
Log in
Try ChatGPT
(opens in a new window)
Research
Products
Business
Developers
Company
Foundation
(opens in a new window)
Try ChatGPT
(opens in a new window)
Login
OpenAI
July 29, 2026
Research
Publication
How enabling two settings tripled our scores on the ARC-AGI-3 benchmark
Loading…
Share
ARC-AGI-3
ARC-AGI-3
Agents do best when they remember what they’ve done
Conclusion and recommendations
ARC-AGI-3
Agents do best when they remember what they’ve done
Conclusion and recommendations
A sped-up video of GPT‑5.6 Sol attempting to solve puzzles in the ARC-AGI-3 benchmark, with the official harness (left) and our Responses API harness (right), which retains reasoning and enables compaction. On the leaderboard for
this game
⁠
(opens in a new window)
, no frontier model solves any level beyond the first. With our harness, GPT‑5.6 Sol solves all six.
When we first saw GPT‑5.6 Sol’s low scores on the
ARC-AGI-3
⁠
(opens in a new window)
benchmark, we were puzzled.
GPT‑5.6 Sol has solved longstanding open problems in mathematics like the
cycle double cover conjecture
⁠
(opens in a new window)
and beaten games like Pokémon FireRed. But on ARC-AGI-3, a benchmark of 2D puzzle games, GPT‑5.6 Sol scored just 7.8%, and GPT‑5.5 could barely play the games at all, scoring a paltry 0.4%.
Were 2D puzzle games unusually difficult for our models? Or was something else going on?
Benchmarks rarely measure AI models in isolation. They also measure less visible choices about API settings, harness design, and prompting. In the case of ARC-AGI-3, we discovered that turning on two API settings we use in ChatGPT and Codex—retained reasoning and compaction—tripled scores and cut output tokens by 6x on the public task set.
With the official harness, GPT‑5.6 Sol scored 13.3% on the ARC-AGI-3 public set. With retained reasoning and compaction, it scored 38.3%. Scores measure Relative Human Action Efficiency (
RHAE
⁠
(opens in a new window)
)
—
a metric comparing model performance to a human baseline. Based on
official gameplay logs
⁠
(opens in a new window)
, we estimate the average human tester scored 48%. Models are not told how they will be scored, and cannot see their score throughout
—
actions only return a text representation of each frame and what level they are on.
ARC-AGI-3
ARC-AGI-3 is a benchmark designed to measure how well AI agents learn and reason. Agents explore unfamiliar 2D games and infer how they work without explicit instructions. You can play 25 demo games at
arcprize.org/tasks
⁠
(opens in a new window)
.
ARC-AGI-3 uses an intentionally generic harness, without tools or special features. ARC’s reasoning was that a simple harness makes model shortcomings more visible and makes model comparisons more fair. Commercial developers, by contrast, optimize harnesses for each model’s features and quirks.
In gaming, GPT‑5.6 Sol has beaten Pokémon FireRed with a vision-only harness (as streamed by
GPT_Plays_Pokemon
⁠
(opens in a new window)
), Slay the Spire with Codex computer use (as streamed by
EpochAI
⁠
(opens in a new window)
), and the first stages of Baba Is You (as shared by
Piotr Migdał & Piotr Grabowski
⁠
(opens in a new window)
). What was so different about ARC-AGI-3?
Ethan Mollick
shows
⁠
(opens in a new window)
GPT‑5.6 Sol in Codex beating a randomized daily challenge in Slay the Spire 2, a game released after GPT‑5.6 Sol’s knowledge cutoff.
Inspired by
ARC’s analysis of GPT‑5.5’s shortcomings
⁠
(opens in a new window)
, we examined some of the GPT‑5.6 Sol’s attempts. Like ARC, we saw that the model didn’t appear too bright. It dwelled a long time on each action and struggled to make progress.
But as we looked deeper, we discovered much of the model’s confusion was not inherent to the model itself, but due to settings in the harness.
First, we noticed that after each game action, all private reasoning was discarded. This meant that with each action, GPT‑5.6 Sol was asked to figure out the game anew, unable to remember its past thinking. The model could still see a record of past moves and brief accompanying notes, but it could not see the plans, insights, or thoughts that led to them.
Second, we saw that the harness used a rolling truncation window, causing older actions to become invisible as the history grew. So not only was GPT‑5.6 Sol unable to remember its past thinking, it was losing memory of its past actions too.
Together, these two features of the harness—discarding reasoning and rolling truncation—helped explain why GPT‑5.6 Sol was struggling to learn over time.
Agents do best when they remember what they’ve done
Our models are trained to think with private reasoning messages before they output replies or tool calls. These private thinking messages are retained as part of the conversation history. If a conversation grows too long, we summarize it and continue.
This is how our models are trained, and also how they are deployed in ChatGPT and Codex. To better match our production setup, we implemented the ARC-AGI-3 harness with our
Responses API
⁠
(opens in a new window)
. Our API makes it easy to manage context: for GPT‑5.6, passing the previous response ID automatically retains reasoning across tool calls and turns.
With reasoning retained, we noticed two big changes. First, GPT‑5.6 Sol spent less time thinking before each action, because it no longer had to interpret the game from scratch every turn. Second, when it was able to remember its past thoughts, GPT‑5.6 Sol was much better at learning over time and employing coherent strategies.
The next improvement came from replacing rolling truncation with
compaction
⁠
(opens in a new window)
, another setting in the Responses API.
The ARC-AGI-3 harness addresses context limits with rolling truncation. When the conversation context exceeds 175,000 characters, the oldest messages are discarded.
Rolling truncation has two drawbacks. First, the model loses earlier observations and actions. Second, it spends much of the tasks operating with a fuller context window, which can slightly impair performance.
When we enabled compaction on ARC-AGI-3, GPT‑5.6 Sol was better able to preserve what it had learned about each game across longer runs, and achieved a higher score with fewer output tokens.
To illustrate the effect of retaining reasoning and enabling compaction, here’s an animation showing GPT‑5.6 Sol’s 175K context window as it solves a series of ARC-AGI-3 puzzles with each harness.
The two central columns depict how the model context window is used differently by each harness. With better memory of its past, GPT‑5.6 Sol thinks less per action and proceeds much faster. Note: our implementation uses a limit of 175,000 tokens instead of characters, but this ends up being quite similar, as the vast majority of text is action grids which are tokenized at a 1:1 ratio by our tokenizer.
Together, retaining reasoning and compaction allow GPT‑5.6 Sol (max) to achieve roughly 3x the score with 6x fewer output tokens.
Conclusion and recommendations
We hope these experiments serve as a reminder that evals rarely measure models in isolation—they also measure a bundle of less visible choices about API settings, harness design, and prompting. This isn’t the first time we’ve been surprised by low scores on a public benchmark and then discovered that the eval runner was using a generic harness that dropped reasoning messages.
If you’re an API developer trying to maximize performance, we recommend using the same settings that we deploy in our own products:
Use our Responses API, not our legacy Chat Completions API
Retain reasoning
Use compaction
And if you’re comparing models, we recommend relying on evals that use the settings above, which best match real-world use in ChatGPT and Codex.
We are grateful to ARC for their years of creative work on AGI evaluation, and for their analysis that inspired us to take a closer look here.
If you want to test your own mettle against frontier models, try the public games yourself at
arcprize.org/tasks
⁠
(opens in a new window)
.
2026
Author
Ilan Bigio, Ted Sanders
Keep reading
View all
Ten advances in mathematics and theoretical computer science
Publication
Aug 1, 2026
Accelerating scientific discovery with ChatGPT for Academic Researchers
Company
Jul 29, 2026
Scientific computing in the age of agentic AI
Publication
Jul 28, 2026
Research
Research Index
Research Overview
Economic Research
Latest Advancements
GPT-5.6
GPT-5.5
GPT-5.4
Safety
Safety Approach
Deployment Safety
(opens in a new window)
Security & Privacy
Trust & Transparency
Products
ChatGPT
(opens in a new window)
ChatGPT Business
(opens in a new window)
ChatGPT Enterprise
(opens in a new window)
ChatGPT for Education
(opens in a new window)
Codex
Release Notes
API Platform
Overview
API Log In
(opens in a new window)
Docs
(opens in a new window)
Business
Overview
Solutions
Resources
Customer Stories
Partner Network
Contact Sales
Developers
Apps SDK
(opens in a new window)
Open Models
Docs
(opens in a new window)
Resources
(opens in a new window)
Developer Forum
(opens in a new window)
Company
About Us
Our Charter
Careers
News
Support
Help Center
(opens in a new window)
More
Stories
Academy
Supply Co.
Livestreams
Podcast
RSS
Terms & Policies
Terms of Use
Privacy Policy
Other Policies
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
OpenAI © 2015–2026
Your privacy choices
English
United States
