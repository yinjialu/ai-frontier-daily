---
type: Article
title: The builder’s guide to GPT‑5.6
source: openai-news
resource: https://openai.com/index/builders-guide-to-gpt-5-6
published: 2026-08-13
tags: [GPT-5.6, 模型选择, Responses API, 智能体]
detected: 2026-08-17T07:39:55+08:00
---

GPT-5.6以更低成本实现前沿智能，小模型Luna/Terra在低推理强度下性能媲美前代旗舰，成本大幅降低。Responses API新增推理持久化、原生压缩、多智能体编排与程序化工具调用，助力构建高效智能体。

## Full Text

The builder’s guide to GPT‑5.6 | OpenAI
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
August 13, 2026
Applied AI
The builder’s guide to GPT‑5.6
Technical lessons from startups in production
Loading…
Share
GPT-5.6 sets a new standard for price-performance
GPT-5.6 sets a new standard for price-performance
A better out-of-the-box experience
Model Selection
Evolving the Responses API to architect more efficient agents
Programmatic Tool Calling
Multi-agent
Prompt Caching
Conclusion
GPT-5.6 sets a new standard for price-performance
A better out-of-the-box experience
Model Selection
Evolving the Responses API to architect more efficient agents
Programmatic Tool Calling
Multi-agent
Prompt Caching
Conclusion
GPT‑5.6 sets a new standard for price-performance
The GPT‑5.6 model family makes frontier-level agent performance dramatically more affordable, while also advancing the frontier of what is possible.
In this guide, we show how startups are using smarter model selection and new API controls that help with reasoning continuity, multi-agent orchestration, and programmatic tool calling to build faster, more capable agents at a fraction of the cost.
A better out-of-the-box experience
Since GPT‑5, each model generation has sought to tackle longer-horizon tasks with fewer tokens. GPT‑5.6 continues that trajectory: stronger agent performance, lower costs, with minimal changes to the underlying harness.
The improvements in top-line cost efficiency are compounded with increased accuracy at lower reasoning efforts. For example, on Agents’ Last Exam, GPT‑5.6 Sol at “low” reasoning outperformed GPT‑5.5 at “high” reasoning when the harness was kept constant. We’ve seen similar success stories in production testing where startups report seeing significant cost improvements across a range of workflows by reducing the reasoning effort from the prior defaults.
“
We dropped GPT‑5.6 into our harness, and low reasoning effort gave us our best results. It knew when the data just wasn’t there, didn’t chase bad leads, and got to the right answer with fewer tokens.
”
— Izzy Miller, AI Research Lead,
Hex
⁠
(opens in a new window)
Model Selection
Historically, upgrading to a flagship model at the highest reasoning available has been the best option for long-horizon use cases. This has been in large part due to these models being significantly more capable than cost-optimized models at handling longer contexts and tool calling. This has changed with the 5.6-family: with more test-time compute, Luna and Terra can often perform similar to GPT‑5.4 and 5.5 while being significantly cheaper.
1 of 3
“
Luna keeps 98% of GPT‑5.5’s extraction accuracy at one-eighteenth the cost. That gives our agents high-quality document understanding at a price that makes it practical across many more workflows.
”
— Serhii Shchoholiev, Engineering Lead, Agents,
Hypha
⁠
(opens in a new window)
“
We ran Luna on 106 of our hardest browser tasks, and it completed 78% of them for about $14. The current SOTA model reached 80% for roughly $235. That combination of capability and cost is remarkable for browser agents.
”
— Gregor Zunic, Co-Founder,
Browser Use
⁠
(opens in a new window)
“
Luna is now our default model for a number of high-throughput code retrieval and decision modeling workloads. For a key code exploration task in our multi-agent engineering system, it lowered inference costs by 64%, cut response time by 90%, and improved F1 by five points.
”
— Animesh Koratana, Founder and CEO,
PlayerZero
⁠
(opens in a new window)
Hypha
Browser Use
PlayerZero
Consider tasks in BrowseComp: a search-based benchmark that tests a model’s ability to search for obscure facts. Three months ago, GPT‑5.5 (Extra High) scored 84.36% on this benchmark for a total cost of $33.27. At launch, GPT‑5.6 Luna (Extra High) delivers essentially the same performance, scoring 84.04% at a cost of $1.33. We’ve since reduced prices further.
Read more
on our latest price cuts.
The smaller 5.6-family models are a strong fit for high-volume workloads, latency-sensitive interactions, and repeated steps within agentic workflows. For example, if you’re operating a legal-tech startup that parses handwritten memos prior to agentic analysis, instead of using a frontier model for the entire use case, you can now use Terra or Luna for extraction and register significant cost savings.
Evolving the Responses API to architect more efficient agents
In addition to making GPT‑5.6 more performant out of the box, we also shipped new primitives to the Responses API to unlock further gains. We trained GPT‑5.6 end-to-end with three complementary architectural interventions that enable agents to operate more efficiently:
Reuse work already performed:
by allowing
reasoning to be persisted
⁠
(opens in a new window)
across model turns and using
native compaction
⁠
(opens in a new window)
to compress long-running conversations, the model can maintain coherence in its work across longer task horizons without getting confused or having to reconstruct prior context.
Parallel decomposition where appropriate:
using
native multi-agent orchestration
⁠
(opens in a new window)
allows coordinating multiple agents across parallel workstreams to finish complex tasks faster.
Move deterministic work into code:
using
programmatic tool calling
⁠
(opens in a new window)
to filter, aggregate, and orchestrate tool outputs outside the model’s context window, reserving model tokens for judgment and reducing cost, latency, and context rot.
Used together, the difference can be dramatic. For example, on ARC-AGI-3, GPT‑5.6 Sol scored 13.3% with the standard harness. After enabling retained reasoning and compaction, however, the score jumped to 38.3%—while using roughly 6× fewer output tokens. No changes to the model, but nearly three times the performance. You can read more on our
ARC-AGI-3 harness investigation
here.
Programmatic Tool Calling
Agentic workflows often involve two kinds of work:
Tasks that require judgment
Work that mostly requires moving, filtering, and combining data
When an agent retrieves 100 filings, filters them by date, and identifies relevant transactions, the model shouldn’t have to reason over every intermediate result in its context window. Programmatic Tool Calling lets GPT‑5.6 write JavaScript to orchestrate tools, run independent calls in parallel, and process their outputs outside the context window. The model is left to focus on what requires intelligence: applying judgment.
“
For financial research, the hard part is reliably pulling filings, coordinating tools, and working through the numbers. In our evaluations, GPT‑5.6 using Programmatic Tool Calling matched our rubric quality while using 21% fewer input tokens. That’s the difference between an agent that can discuss financial research and one that can actually carry it out.
”
— Alex Wang, Applied AI,
Rogo
⁠
(opens in a new window)
Multi-agent
On complex, parallelizable tasks, distributing actions and reasoning across multiple agent workstreams enables faster task completion as well as higher intelligence. In these setups, the primary agent is responsible for orchestrating the subagents and delegating tasks to them. The subagents pursue their objectives in parallel and finally pass back their output to the primary agent for final synthesis. Teams can start leveraging multi-agent natively by
enabling multi-agent
⁠
(opens in a new window)
in the Responses API. This is also how the ultra capability setting in ChatGPT works.
“
Qualia runs teams of agents on open-ended research problems, and GPT‑5.6 Sol just clicked. It showed a marked improvement over GPT‑5.5, finished faster than almost every other model we tested, and quickly became our go-to OpenAI model.
”
— E Chi, Founder,
Quadrillion
⁠
(opens in a new window)
“
GPT‑5.6 is the best orchestrator we’ve seen from OpenAI. We threw six specs at it at once (writing, building, and talking through all of them) and it kept track of everything without the quality falling apart.
”
— Jon Bell, Co-founder and CPO,
Obvious
⁠
(opens in a new window)
1 of 2
“
Qualia runs teams of agents on open-ended research problems, and GPT‑5.6 Sol just clicked. It showed a marked improvement over GPT‑5.5, finished faster than almost every other model we tested, and quickly became our go-to OpenAI model.
”
— E Chi, Founder,
Quadrillion
⁠
(opens in a new window)
“
GPT‑5.6 is the best orchestrator we’ve seen from OpenAI. We threw six specs at it at once (writing, building, and talking through all of them) and it kept track of everything without the quality falling apart.
”
— Jon Bell, Co-founder and CPO,
Obvious
⁠
(opens in a new window)
Quadrillion
Obvious
Although GPT‑5.6 has a strong sense of the appropriate number of subagents and when to spawn them, multi-agent behavior is very steerable. Instructing the model on when to invoke subagents can increase the likelihood of spawning agents only in situations where the additional token expenditures would result in better performance.
Prompt Caching
Across the entire family of models, the prompt cache TTL has been extended to a minimum of 30 minutes and cache breakpoints can now be set deterministically within a model’s context window. This has enabled startups to significantly improve their cache hit rate.
“
We added cache breakpoints and workspace-specific keys to a shared 29,000-token prompt and cut uncached input by 28%. The 30-minute cache window was a big unlock too: our agents could reuse the same context across runs instead of starting from scratch.
”
— Lorenzo Gentile, AI Engineer,
Ploy
⁠
(opens in a new window)
In addition to setting cache breakpoints, continuing to use an appropriate
prompt_cache_key
⁠
(opens in a new window)
increases the likelihood of requests landing on the same inference engine as one that previously served the same prefix, thereby reducing latency.
Conclusion
What stands out across these examples is how much the economics of building agents have changed.
Use cases that once required a frontier model at every step can now achieve comparable or better results at a fraction of the cost by using smaller models, tuning reasoning effort, and making efficient architectural choices.
We're excited to see what you all build!
2026
API Platform
About the authors
This guide was developed by
Samarth Madduru
⁠
(opens in a new window)
,
Prashant Mital
⁠
(opens in a new window)
,
Dave Leo
⁠
(opens in a new window)
, and
Julien Reiman
⁠
(opens in a new window)
, based on their experience working closely with startups building on GPT‑5.6 from early testing through production.
Keep reading
View all
How GPT-5 helped immunologist Derya Unutmaz solve a 3-year-old mystery
Applied AI
Jun 23, 2026
Using AI to help physicians diagnose rare genetic diseases affecting children
Applied AI
Jun 18, 2026
How an astrophysicist uses Codex to help simulate black holes
Applied AI
Jun 11, 2026
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
