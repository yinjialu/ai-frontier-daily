---
type: Article
title: Government of Alberta uses Claude to find and fix cybersecurity vulnerabilities across government systems
source: anthropic-news
resource: https://www.anthropic.com/news/alberta-government-claude-cybersecurity
published: 2026-07-06
tags: [AI安全, 代码审计, 政府AI应用, Claude]
detected: 2026-07-07T03:58:07+08:00
---

加拿大阿尔伯塔省政府使用Claude Code（Opus与Sonnet模型）在20小时内扫描4.66亿行代码，发现并修复安全漏洞，比传统方法快数百倍。他们还构建了红蓝队AI代理进行持续安全审查，并公开技术白皮书供其他政府参考。

## Full Text

Government of Alberta uses Claude to find and fix cybersecurity vulnerabilities \ Anthropic
Skip to main content
Skip to footer
Research
Policy
Commitments
Learn
News
Try Claude
Case Study
Government of Alberta uses Claude to find and fix cybersecurity vulnerabilities across government systems
Jul 6, 2026
Since 2025, the Government of Alberta has been using Claude Code with both Opus and Sonnet models to review its systems, find vulnerabilities, and fix them. A team inside Alberta’s Ministry of Technology and Innovation scanned 466 million lines of code in 20 hours, remediated security gaps across its systems, and built new tools to make those systems safer.
We’re sharing details of their experience as an example of how government agencies can use Claude and Claude Code to secure their systems at a large scale. This is a critical challenge, as governments rely on these systems to deliver benefits and keep services running—yet the code is often old, insecure, and incompletely documented. Alberta has also published a collection of technical white papers documenting its efforts for other governments to learn from;
you can read them here.
“Albertans trust their government with some of the most sensitive information in their lives, and it is our responsibility to protect it,” said Nate Glubish, Alberta’s Minister of Technology and Innovation. “By using AI to find and fix vulnerabilities across our systems, we accomplished in hours what would have taken a traditional approach years to complete. This is what responsible government looks like in the AI era, and the best is still ahead of us.”
Alberta’s approach
Alberta’s Ministry of Technology and Innovation maintains the systems of all 27 provincial ministries, from social services to public safety to wildfire response. That includes roughly 1,280 applications and 3,400 code repositories. Most of it has never undergone a systematic security review, and the accumulated technical debt—insecure code, unaddressed bugs, outdated software—runs into the billions of dollars.
The Ministry’s systems hold highly sensitive information, including tax records, government procurement data, and social services case files. So in 2025, the Ministry set up an internal team with a mandate to make these systems more secure and easier to maintain over time, working with Claude to do so.
Already, the Ministry has used Claude to:
Assess 466 million lines of government code in 20 hours.
The team put Claude to work on the codebases it maintains, using Claude Code with Claude Opus and Sonnet models. Around 50 agents worked autonomously and in parallel to scan the systems for security vulnerabilities, weaknesses in underlying infrastructure and deployment processes, and gaps in technical documentation. Claude Code ran a two-stage routine, first scanning each repository with a rules engine to flag known patterns, then reviewing those flags and citing the exact file and line for each finding so developers could verify them. The scan covered every repository Alberta owns and identified issues that traditional automated scanning tools had missed. It took about 20 hours for Alberta’s implementation; the team estimates that that kind of review could otherwise have taken around 6.5 years.
Fix the vulnerabilities the scan found.
Where the scan identified a vulnerability, Claude Code could often generate a fix, test it, and build it. In cases where a system lacked the automated tests needed to confirm that a patch was safe, Claude wrote the tests first. Where the code was too outdated or too complex to patch efficiently in its existing form, Claude rebuilt it in a more modern and maintainable language. In some scenarios, these systems could be rebuilt in as little as four to five days, including a subsidy program portal that was originally hand-coded in Java roughly 25 years ago and took five months to build the first time. All of this was done in partnership with the Ministry’s engineers: before any patch shipped, it was reviewed and approved by the team.
Run continuous security review.
Alberta’s cybersecurity team also built a set of specialized Claude review agents that run throughout the development process. A “red team” agent probes an application from the outside, the way an attacker might, and maps how a vulnerability might be exploited. A “blue team” agent then assesses the application’s defenses against an international security standard, and writes a remediation plan that points to the exact files to fix. Additional agents check code quality and the clarity of the writing the public sees. Every application is checked against roughly 95 security controls on each pass. These agents are built on top of the
Claude Agent SDK
and run a robust series of checks and analysis for every application.
In addition to scanning, securing, and modernizing its own systems, Alberta is training both government workers and the public in the use of AI through the Alberta AI Academy. Thousands of government employees and more than 10,000 members of the public have used the platform to learn the essentials of effective AI use, from prompting through enterprise application delivery. Through the Academy, the Ministry of Technology and Innovation aims to extend its approach beyond a single team or project to every ministry that needs it.
Looking ahead
Today, Claude helps the Ministry write, review, and deploy code that aids in its modernization efforts. Next, it plans to expand that work with AI agents that can build entirely new software and tools alongside engineers.
The Government of Alberta also plans to continue its modernization work. One ministry, for example, has 185 legacy applications running in production, which are expensive to maintain and difficult to update. The Government plans to use Claude Code to analyze these systems, understand what they do, and consolidate them into 16 reusable applications built on modern coding languages and conventions. The goal is to reduce complexity, lower maintenance costs, and speed up modernization work that would otherwise take years to complete.
A case study for governments
The technical debt and security vulnerabilities the Government of Alberta is working to address are hardly unique. They exist in the systems of many provinces, states, and federal agencies across the world. The
technical white papers
Alberta has released give other governments a blueprint for addressing these same issues.
In addition to the white papers, Alberta is hosting
an industry day
in Edmonton in July to share what it has learned. And this fall, it will begin a program to scale its approach across the provincial government. We’ll keep working with Alberta as it expands these efforts, and we hope the approach it has documented can help other governments secure their own systems.
Related content
More details on Fable 5’s cyber safeguards and our jailbreak framework
Read more
Introducing Claude Sonnet 5
Sonnet 5 delivers frontier performance across coding, agents, and professional work at scale.
Read more
Redeploying Fable 5
Fable 5 returns globally July 1. We're also proposing an industry-wide framework for scoring jailbreak severity, together with Amazon, Microsoft, Google, and other Glasswing partners.
Read more
Products
Claude
Claude Code
Claude Code Enterprise
Claude Cowork
@Claude
Claude Design
Claude Science
Claude Security
Claude for Chrome
Claude for Microsoft 365
Skills
Download app
Pricing
Log in to Claude
Models
Mythos
Fable
Opus
Sonnet
Haiku
Solutions
AI agents
Code modernization
Coding
Customer support
Education
Enterprise
Financial services
Government
Healthcare
Legal
Life sciences
Nonprofits
Security
Small business
Claude Platform
Overview
Developer docs
Pricing
Ecosystem
Marketplace
Regional compliance
Claude on AWS
Google Cloud
Microsoft Foundry
Console login
Resources
Blog
Claude partner network
Community
Connectors
Courses
Customer stories
Engineering at Anthropic
Events
Inside Claude Code
Inside Claude Cowork
Inside Claude Enterprise
Plugins
Powered by Claude
Service partners
Tutorials
Use cases
Programs
Startups
Research Labs
Help and security
Availability
Status
Support center
Company
Anthropic
Careers
Policy
Economic Futures
Research
News
Claude’s Constitution
Claude Corps
Policy on the AI Exponential
Responsible Scaling Policy
Security and compliance
Transparency
Terms and policies
Privacy policy
Consumer health data privacy policy
Responsible disclosure policy
Terms of service: Commercial
Terms of service: Consumer
Usage policy
© 2026 Anthropic PBC
