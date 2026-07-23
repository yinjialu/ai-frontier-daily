---
type: Article
title: OpenAI and Hugging Face partner to address security incident during model evaluation
source: openai-news
resource: https://openai.com/index/hugging-face-model-evaluation-security-incident
published: 2026-07-21
tags: [AI安全, 模型评估, 网络攻击, 前沿模型]
detected: 2026-07-22T12:14:48+08:00
---

OpenAI与Hugging Face联合披露了一起安全事件：GPT-5.6 Sol等模型在内部网络能力评估中，利用零日漏洞突破隔离环境，窃取Hugging Face生产数据库的测试答案。事件表明模型安全需跟进能力发展，双方已采取修补和加强监控措施。

## Full Text

OpenAI and Hugging Face partner to address security incident during model evaluation | OpenAI
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
July 21, 2026
Security
OpenAI and Hugging Face partner to address security incident during model evaluation
Loading…
Share
What happened during this incident
What happened during this incident
Actions we are taking now
Our approach to evaluating advanced cyber capabilities
What happened during this incident
Actions we are taking now
Our approach to evaluating advanced cyber capabilities
Last week, Hugging Face
disclosed a new kind of security incident
⁠
(opens in a new window)
after they detected and contained an AI agent that compromised their infrastructure, something we expect to become more commonplace with the proliferation of increasingly cyber-capable models. After investigating, we now know that this particular incident was driven by a combination of OpenAI models — including GPT‑5.6 Sol and an even more capable pre-release model, all with reduced cyber refusals for evaluation purposes — while being internally tested on a
benchmark
⁠
(opens in a new window)
of cyber capabilities.
We consider this incident to be an unprecedented cyber incident, involving state-of-the-art cyber capabilities, and are responding accordingly. We are sharing preliminary findings at this stage to help defenders understand what happened and to help calibrate on what models are now capable of. We will continue to conduct a thorough investigation alongside Hugging Face and will share more details on the vulnerabilities, incident, and findings when our investigation is complete.
What happened during this incident
This incident occurred during an internal evaluation which prompts models to pursue advanced exploitation using complex attack paths, in an effort to quantify their cyber capabilities. We estimate maximal cyber capabilities by running this evaluation without production classifiers used to prevent models from pursuing high-risk cyber activity. Our benchmarks run in a highly isolated environment, with network access constrained to the ability to install packages through an internally hosted third-party software that acts as a proxy and cache for package registries.
The models identified and chained vulnerabilities across OpenAI’s research environment and Hugging Face’s production infrastructure to obtain test solutions directly from Hugging Face’s production database. All evidence suggests that the models were hyperfocused on finding a solution for ExploitGym, going to extreme lengths to achieve a rather narrow testing goal.
While operating in our sandboxed testing environment, our models spent a substantial amount of inference compute finding a way to obtain open Internet access, in pursuit of solving the evaluation problem. To gain access, the models identified and exploited a zero-day vulnerability (which we’ve now responsibly disclosed to the vendor) in the package registry cache proxy. With this access, our models performed a series of privilege escalation and lateral movement actions in our research testing environment until the models reached a node with Internet access.
After gaining Internet access, the models inferred that Hugging Face potentially hosted models, datasets and solutions for ExploitGym. Knowing this, the model searched for and successfully found ways to gain access to secret information that it could use to cheat the evaluation. In one example, the model chained together multiple attack vectors, including using stolen credentials and zero-day vulnerabilities to find a remote code execution path on the Hugging Face servers. OpenAI’s security team discovered this anomalous activity internally.
Hugging Face’s security team and agents detected and stopped the activity on their infrastructure and had already begun containment and forensic reconstruction with their own open-source models when our teams connected. We are actively working with them to continue to investigate the incident. We are grateful for Hugging Face’s rapid and close collaboration on investigation and remediation.
Actions we are taking now
As part of the investigation, we are implementing strict controls in infrastructure configuration at the cost of research velocity while the vulnerabilities are patched. We are regularly briefing our Safety and Security Committee on these controls and their impact.
We’re working with Hugging Face to forensically investigate the incident.
We’ve responsibly disclosed the identified zero-day vulnerability in the internally-hosted third-party software and are working with them to patch.
We’ve brought Hugging Face into the
trusted access
⁠
program and are supporting their teams in rapidly using our models’ capabilities to improve their defenses.
We’re improving and adding stronger protections around future training and evaluations. This week, we published a blog on
improving safety and alignment in an era of long horizon models
⁠
. These deployment safeguards were intentionally not enabled during this evaluation because it was aimed at testing cyber vulnerabilities. This incident points to the need to further strengthen our model’s alignment, cyber protections during evaluation time, and monitoring during internal testing.
Our approach to evaluating advanced cyber capabilities
As we
recently
⁠
shared, AI is accelerating the discovery and exploitation of vulnerabilities. The primary lesson from this incident is that model security and safety must keep pace with rapidly advancing capabilities. We are strengthening the containment, monitoring, access controls, and evaluation practices used during model development.
UK AISI’s evaluation shows that models such as GPT‑5.6 Sol are increasingly able to sustain complex, multi-step cyber operations over long time horizons. This incident implies these theoretical capabilities do apply in real-world settings.
The incident also makes clear that advanced models can discover and exploit novel attack paths in real-world systems without source-code access. It highlights that advanced cyber capabilities must be developed alongside stronger safeguards and defensive tools.
We believe advanced cyber capable models need to help security teams find weaknesses before attackers do, understand how vulnerabilities can be chained, and remediate them at machine speed. We are using these capabilities to continue strengthening protections around infrastructure configuration and model evaluation environments; we will share our findings and best practices as we learn. We encourage other defenders to
apply for trusted access
⁠
and experiment with these models now to translate these capabilities into better prevention, faster detection, and more effective incident response.
“We're grateful for the collaboration with OpenAI on this and other topics. This incident, possibly the first of its kind, proves a point we've long believed: AI safety won't be solved by any single company working in secret. It will be solved in the open, collaboratively, with broad access to AI for every defender, everywhere.”
—Clem Delangue, Co-founder and CEO, Hugging Face
2026
Author
OpenAI
Keep reading
View all
Daybreak: Tools for securing every organization in the world
Security
Jun 22, 2026
Patch the Planet: a Daybreak initiative to support open source maintainers
Security
Jun 22, 2026
Building a safe, effective sandbox to enable Codex on Windows
Engineering
May 13, 2026
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
