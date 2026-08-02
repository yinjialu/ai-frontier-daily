---
type: Article
title: Deceptive Employment Scheme: IT worker activity
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-it-workers
published: 2025-06-01
tags: [AI安全, 威胁情报, 朝鲜, 滥用]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁了疑似朝鲜IT工作者利用AI进行欺骗性远程求职的账户。攻击者用ChatGPT批量生成定制简历、完成编码任务、规避身份验证，并招募美国人员接收笔记本以便远程操控。OpenAI已分享情报以提升安全防护。

## Full Text

Deceptive Employment Scheme: IT worker activity | OpenAI
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
June 1, 2025
Deceptive Employment Scheme: IT worker activity
OpenAI banned accounts associated with suspected deceptive employment campaigns that used AI to develop materials for potentially fraudulent remote-job applications.
Loading…
Share
This case study was originally published in OpenAI’s
June 2025
⁠
(opens in a new window)
report.
Actor
We identified and banned ChatGPT accounts associated with what appeared to be multiple suspected deceptive employment campaigns. These threat actors used OpenAI’s models to develop materials supporting what may be fraudulent attempts to apply for IT, software engineering and other remote jobs around the world.
While we cannot determine the locations or nationalities of the threat actors, their behaviors were consistent with activity publicly attributed to IT worker
schemes connected to North Korea (DPRK)
⁠
(opens in a new window)
. Some of the actors linked to these recent campaigns may have been employed as contractors by the core group of potential DPRK-linked threat actors to perform application tasks and operate hardware, including within the US.
Behavior
Similar to the threat actors we disrupted and wrote about in
February
⁠
(opens in a new window)
, the latest campaigns attempted to use AI at each step of the employment process. Previously, we observed these actors using AI to manually generate credible, often U.S.-based personas with fabricated employment histories at prominent companies. This time, they attempted some degree of automated generation of resumes, and some indicators suggest operators in Africa posing as job applicants, in addition to recruiting people in North America to run laptops on their behalf.
We detected two distinct strands of activity, likely representing two types of operator: core operators, and contractors.
The core operators attempted to automate résumé creation based on specific job descriptions, skill templates, and persona profiles, and sought information about building tools to manage and track job applications. They also used our models to generate content that resembled job postings aimed at recruiting contractors in different parts of the world.
The core operators used ChatGPT as a research tool to help inform remote-work setups. They also engaged our models to generate text concerning the recruitment of real people in the US to take delivery of company laptops, which would then be remotely accessed by the core threat actors or their contractors.
The threat actors researched using tools such as Tailscale peer-to-peer VPN, OBS Studio, vdo.ninja live-feed injection, and HDMI capture loops as part of their operations. These tools have the potential to be used to circumvent corporate security measures, and if successful, they would allow someone to maintain a persistent, undetected remote presence, as well as attempt to bypass some identity verification processes that rely on live video meetings.
Meanwhile, the possible contractor operators used ChatGPT to help complete job application tasks. They also used it to generate content that resembled messages to the core operators inquiring about payments and about the personas used to apply for remote jobs.
Completions
We determined that these threat actors attempted to use our models for a deceptive operation. Specifically, they used detailed prompts, instructions, and automation loops to generate tailored, credible résumés at scale.
Automating detailed résumés aligned to various tech job descriptions, personas, and industry norms: LLM Supported Social Engineering.
Answering employment-related application questions, coding assignments, and real-time interview questions based on uploaded resumes: LLM Supported Social Engineering.
Seeking guidance for remotely configuring corporate-issued laptops to appear domestically located, including geolocation masking and endpoint security evasion methods: LLM-Enhanced Anomaly Detection Evasion.
Assisting coding of tools to move the mouse automatically, or keep a computer awake remotely, possibly to assist in remote working infrastructure setups: LLM Aided Development.
Impact
We cannot independently assess the success of these operations, as assessing impact would require inputs from multiple stakeholders.
While the threat actors likely built AI into every step of their process to increase their efficiency, it also increased their exposure. By giving us insights across their workflows, they enabled us to share insights about these campaigns with relevant industry peers and authorities for each stage of their activity, enhancing our collective ability to detect, prevent, and respond to such threats while advancing our shared safety.
Author
OpenAI
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
