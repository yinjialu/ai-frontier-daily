---
type: Article
title: Scientific computing in the age of agentic AI
source: openai-news
resource: https://openai.com/index/scientific-computing-agentic-ai
published: 2026-07-28
tags: [智能体, 科学计算, 编码代理, 基因组学]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI发布实地报告，探讨编码智能体如何助力科学计算现代化。八个生命科学项目使用Codex和Claude Code，显著加速开发维护，但结果仍需人工验证，长期维护与人类判断力仍是关键。

## Full Text

Scientific computing in the age of agentic AI | OpenAI
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
July 28, 2026
Publication
Research
Scientific computing in the age of agentic AI
A field report shows how scientists are using coding agents to modernize scientific software for genomics and other data-rich fields.
Read the paper
(opens in a new window)
Loading…
Share
Case studies
Case studies
Recurring themes
Long-term stewardship remains essential
Toward more durable scientific software
Case studies
Recurring themes
Long-term stewardship remains essential
Toward more durable scientific software
Scientific computing is a core pillar of modern research across academia and industry. Yet the software needed to analyze scientific information has struggled to keep pace with the rapid rate of data generation. Many widely used research tools began as code accompanying a research paper, built by small academic teams with limited engineering experience and minimal time for packaging, testing, optimization, or long-term support. The result is scientific infrastructure that often depends on slow, fragile workflows requiring constant maintenance. These constraints impede the pace of discovery.
AI agents are beginning to change that equation. By lowering the costs of engineering work and taking on tedious implementation tasks, they can help researchers prototype ideas more quickly, pursue projects that were previously impractical, and more easily maintain software over the long term. As a result, scientific software becomes more efficient and better maintained, freeing researchers to spend more time on discovery.
We’re sharing an exploratory field report of eight agent-assisted scientific computing projects primarily in the life sciences; five using Codex alone, and three using a combination of Codex and Claude Code. The report brings together case studies written by the teams behind each project and identifies recurring themes. The projects range from routine maintenance and targeted optimization to large-scale language migrations and GPU-native redesigns. Contributors report that agents significantly accelerated software development and maintenance, in some cases helping small teams take on work that would otherwise have required far more time or specialized engineering support. But they also highlight the persistent challenge of establishing clear, long-term responsibility and stewardship of the resulting tools.
Contributors consistently describe a shift in the researchers’ role from implementation to verification and orchestration: specifying what to build, defining how to measure correctness, and deciding when a project is ready to ship. In this emerging model, the researchers remain in control of the scientific direction and quality bar, but with velocity uplift provided by agentic assistance
Case studies
cyvcf2
HI.SIM
hifiasm
MHCflurry
bayesm-rs
Rustar-aligner, svb, and kuva
RustQC, FastQC-Rust, and Trim Galore
HelixForge
Modernized a widely used library for parsing genomic data
cyvcf2 is a Python library for reading and writing genomic variant files. GPT‑5.5 replaced the library’s legacy build and packaging system with a modern, unified process designed to make the library easier to install, test, and release.
With coding agents, it’s quite easy to go fast; for now, to go far in science, there’s still a need for expert guidance, understanding, taste, and care.
—Brent Pedersen
Recurring themes
Though the projects varied widely in scope, they demonstrated that coding agents are making engineering labor and expertise less of a constraint in scientific computing. Now, the bottleneck is validating an AI agent’s output, which still depends on human judgement.
Across case studies, agents handled specific, well-scoped requests effectively but could not reliably judge whether their work was scientifically valid or met expectations. Indeed, agents often expressed confidence even when their work contained clear errors. Human reviewers therefore needed to find reliable ways to validate the results. The strongest approaches used an external reference or measurable acceptance target such as exact output agreement, parity with an existing tool, appropriate statistical behavior, or answers established in advance using simulated data.
Another recurring theme was that the projects generally proceeded in stages using feedback-driven iterations rather than as one-shot approaches. Contributors broke down broad goals into smaller changes, then used intermediate benchmarks and test systems to evaluate and refine the agents’ work. Agents often produced initial implementations quickly, but resolving edge cases and subtle numerical differences took much longer. Completing the “last mile” of an implementation often took the most work.
Overall, these case studies suggest that agents are enabling researchers to spend less time on implementation and more time directing the scientific work. People define the goal, break down complex projects into manageable chunks, and judge whether results are scientifically valid. By easing longstanding engineering constraints, agents expand what researchers can build while freeing them to focus on the scientific questions and decisions that matter most.
Long-term stewardship remains essential
The maintenance gap in research software has long slowed iteration and limited reproducibility and reliability. Published studies of “
research code
⁠
(opens in a new window)
” and
omics tools
⁠
(opens in a new window)
have found that published software often fails to properly install in a fresh computing setup or run as documented, forcing researchers to spend substantial time on configuration and debugging. Even routine improvements can save researchers time and reduce computing demands, while performance-based refactoring and rewrites can deliver larger gains.
But lower implementation costs also make it easier to produce many similar rewrites, fragmenting users and spreading the expert attention required to keep any one tool reliable. That makes long-term stewardship and attribution essential. Mature scientific software carries undocumented conventions, compatibility requirements, and user trust that translating the source code alone cannot reproduce.
The case studies illustrate several possible paths forward. Changes to MHCflurry and cyvcf2 were incorporated into their original upstream projects, while rustar-aligner moved under new community stewardship because the original project had been abandoned. Where coordination with existing maintainers is available, it should begin as early as possible. When a separate implementation is necessary, it needs a clear owner and a credible maintenance plan. Without that, today’s modern rewrite can become tomorrow’s abandoned code rather than reliable scientific infrastructure.
Toward more durable scientific software
This field report is retrospective and exploratory, but the case studies point to a practical shift in how scientific software is developed. Coding agents such as Codex can significantly lower the cost of maintenance, migration, optimization, and new implementations. Their long-term scientific value still depends on human decisions around what to build, how to verify it, and who will maintain it. The deeper change is not simply that researchers can produce more software, but that they can focus more of their effort on defining, validating, and stewarding the tools.
These case studies show that agents can already accelerate the pace of iteration in scientific computing. As coding agents improve, researchers will be able to spend less time keeping analysis pipelines running and more time advancing their fields.
2026
Software & Engineering
Author
OpenAI
Keep reading
View all
Ten advances in mathematics and theoretical computer science
Publication
Aug 1, 2026
How enabling two settings tripled our scores on the ARC-AGI-3 benchmark
Research
Jul 29, 2026
Accelerating scientific discovery with ChatGPT for Academic Researchers
Company
Jul 29, 2026
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
