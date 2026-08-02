---
type: Article
title: Advancing the price-performance frontier with GPT-5.6
source: openai-news
resource: https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6
published: 2026-07-30
tags: [GPT-5.6, 性价比, API定价, OpenAI]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI宣布GPT-5.6系列降价与提速：Luna降价80%，Terra降价20%，Sol在API中推出Fast mode，速度提升2.5倍。通过提升模型、推理及智能体效率，实现更强每美元性能，降低企业大规模AI应用成本。

## Full Text

Advancing the price-performance frontier with GPT-5.6 | OpenAI
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
July 30, 2026
Product
Advancing the price-performance frontier with GPT‑5.6
By making every layer more efficient, OpenAI is delivering stronger performance per dollar across more enterprise workloads.
Loading…
Share
Matching intelligence to the outcome
Matching intelligence to the outcome
How we advance the efficiency frontier
A compute strategy built for scale
Availability and pricing
Matching intelligence to the outcome
How we advance the efficiency frontier
A compute strategy built for scale
Availability and pricing
Yesterday, we shared how
GPT‑5.6
⁠
helped make itself
more efficient to run
⁠
. Today, we’re passing those gains on to customers with lower prices for GPT‑5.6
Luna
⁠
(opens in a new window)
and
Terra
⁠
(opens in a new window)
and faster performance with GPT‑5.6
Sol
⁠
in the API. Together, these updates help customers get more from every dollar they invest in AI and move faster when time matters.
Starting today, GPT‑5.6 Luna, our fastest and most affordable model, will cost 80% less, while GPT‑5.6 Terra, our balanced model for everyday work, will cost 20% less. These lower prices for Luna and Terra are also reflected in how usage is counted against paid subscriptions when using Codex and ChatGPT Work. Luna gives businesses a far more cost-effective way to handle high-volume work at very high levels of quality. It can use tools and complete multi-step workflows, making a broader range of AI applications practical to run at scale.
Making advanced intelligence more abundant and affordable is central to OpenAI’s mission to ensure AGI benefits all of humanity. These changes put that commitment into practice. They reflect years of improvements in how our models are built, served, and put to work.
We’re also introducing
Fast mode
in the API, which replaces our Priority Processing offering. For GPT‑5.6 Sol, Fast mode now delivers up to 2.5× faster speeds than Standard processing at twice the price, with no change in intelligence. Fast mode is backward compatible: requests tagged priority will automatically use Fast mode.
1 of 6
“
GPT‑5.6 Luna is the closest we’ve come to intelligence too cheap to meter. I’ve never seen a model this affordable be this powerful — it’s unlocking use cases for Replit we didn’t expect to build for a long time.
”
Michele Catasta, President & Head of AI, Replit
“
GPT‑5.6 Terra is a strong fit for everyday work in Notion’s personal agent, including workspace Q&A and scoped tasks where latency matters. In our evaluations, it delivered comparable quality to GPT‑5.5 at half the cost per task and in 60% less time.
”
Hoda Noorian, AI Product, Notion
“
We are focused on maximizing outcome per dollar in everything we do, and the GPT‑5.6 series has been a significant step forward in that regard. Terra and Luna lead on cost-efficiency across our internal coding benchmarks, and Luna is now our default model for background agent automations.
”
Shaiyon Hariri, Creator of Ramp SWE-Bench
“
GPT‑5.6 Luna is the biggest step change in agentic behavior we’ve seen since putting GPT‑4o mini into production. Luna moved us from a single structured-output call to a full tool-calling agent loop, increasing prompt-cache reuse from 24% to 90%. Across thousands of production calls, Luna handles 2.2× more context with 8.5× fewer output tokens—at 87% lower cost than GPT‑5.4 mini.
”
Sid Pardeshi, CTO + Co-Founder, Blitzy
“
GPT‑5.6 Luna is an ideal pair programmer for larger models, handling much of the routine work while striking an ideal balance between cost and intelligence. We’ve incorporated Luna into Devin Fusion to deliver significant cost savings for users without compromising quality.
”
Walden Yan, Co-Founder and Chief Product Officer, Cognition
“
We’ve seen meaningful operational improvements since adopting GPT‑5.6 Luna. Given the same agentic tasks, GPT‑5.6 Luna is 40% faster and 40% cheaper than our previous default model, leading to a more responsive experience for users. It delivers an excellent balance of quality, speed and efficiency.
”
Stanislas Polu, Co-Founder and CTO, Dust
Replit
Notion
Ramp
Blitzy
Cognition
Dust
Matching intelligence to the outcome
Using AI efficiently begins with the outcome. The stakes, cost of error, urgency, and scale determine the right balance of intelligence, speed, reliability, and cost. That balance can change from one step of a workflow to the next.
GPT‑5.6 gives businesses much more room to optimize that equation. Luna delivers performance comparable to models that were frontier-class a year ago at roughly 6 cents on the dollar per task, and at nearly nine times the speed. On professional work, as measured by Agents’ Last Exam, Luna outperforms Fable 5 at an estimated cost per task nearly 99% lower.
In practice, businesses can define the outcome and quality standard they need, then use evaluations to determine where additional intelligence materially improves the result and where faster, lower-cost processing can deliver the same quality. A coding workflow, for example, might use Sol to resolve uncertainty and define the plan, then use Luna to implement well-specified changes, write and run tests, and evaluate the results. Another workflow may call for a different balance.
The GPT‑5.6 family expands the range of those choices. Businesses can apply the maximum useful intelligence at every stage while paying the right price for the value it creates.
Delivering that flexibility starts with making every layer behind the models more efficient.
How we advance the efficiency frontier
Our efficiency edge comes from improving the models, the inference systems that run them, and the agentic harness that connects them to tools and context. GPT‑5.6 models take a more direct path through work. Better routing keeps hardware productive, optimized production software generates tokens more efficiently, and smarter context management helps agents avoid repeating completed work. Together, these improvements let us complete more useful work with the same compute, reducing the time, tokens, and cost required for each result.
GPT‑5.6 Sol is increasingly helping us find and deliver the next round of gains. Within a human-led process, Sol autonomously rewrote and optimized production kernels, designed and ran hundreds of experiments to improve token generation, and monitored training, intervening when problems arose. The kernel work helped reduce the end-to-end cost of serving the model by 20%, while its experiments increased token-generation efficiency by more than 15%. This work continues, creating a tighter feedback loop: as our models improve and are able to work more autonomously, our ability to improve efficiencies accelerates.
Read more
⁠
about the engineering behind GPT‑5.6.
A compute strategy built for scale
Meeting demand for abundant intelligence requires both more compute and more productive compute. We are building a resilient infrastructure portfolio and matching each workload to the systems best suited to run it. That approach supports both ends of the price-performance curve. At the lower-cost end, the new Luna and Terra prices make high-volume work economical at much greater scale. At the frontier end, Fast mode gives API customers faster access to Sol when response time is important.
Enterprises can move more AI into everyday operations without sacrificing speed on their most consequential work. Large-scale document analysis, customer-interaction classification, and routine implementation can become economical to run broadly, while complex Sol workloads can move faster when the premium is justified.
The gains can compound. Within a human-led process, more capable models help our technical team find the next generation of improvements, shortening the path to better performance and lower costs. Our strategy remains focused on advancing both capability and efficiency so each generation of intelligence can accomplish more work at a lower cost.
Availability and pricing
GPT‑5.6 Terra and Luna remain available in ChatGPT Work, Codex, and the OpenAI API. In ChatGPT Work and Codex, Free and Go users can access Terra, while Plus, Pro, Business, and Enterprise users can choose Terra and Luna.
Starting July 30, API pricing is $2 per million input tokens and $12 per million output tokens for Terra, and $0.20 per million input tokens and $1.20 per million output tokens for Luna. Sol pricing remains unchanged. ChatGPT and Codex subscription prices and quota budgets remain unchanged, while Terra and Luna usage now consumes fewer credits. Pricing changes will begin rolling out in AWS later today.
Fast mode for GPT‑5.6 Sol replaces Priority Processing in the API and aligns with /fast in Codex. Existing API requests tagged priority will continue to work.
View complete API pricing details.
⁠
2026
Author
OpenAI
Keep reading
View all
Launching Health in ChatGPT
Product
Jul 23, 2026
Introducing OpenAI Presence
Product
Jul 22, 2026
GPT-5.6 is now the preferred model in Microsoft 365 Copilot
Product
Jul 9, 2026
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
