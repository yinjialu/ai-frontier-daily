---
type: Article
title: Cyber threat actors: AI-assisted intrusion research
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-cyber-threat-actors
published: 2025-02-01
tags: [AI安全, 网络威胁, 朝鲜APT, LLM滥用]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁了疑似朝鲜关联威胁行为者的账户，其利用AI辅助研究入侵工具、调试RDP暴力破解代码、规避检测并策划钓鱼攻击，主要针对加密货币。OpenAI已分享恶意载荷并与安全社区协作应对，但未发现AI提供了全新能力。

## Full Text

Cyber threat actors: AI-assisted intrusion research | OpenAI
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
February 1, 2025
Cyber threat actors: AI-assisted intrusion research
OpenAI banned accounts potentially associated with publicly reported DPRK-affiliated threat actors using AI to research intrusion tooling, phishing, malware, and cryptocurrency targeting.
Loading…
Share
This case study was originally published in OpenAI’s
February 2025
⁠
(opens in a new window)
report.
Actor
We banned accounts demonstrating activity potentially associated with publicly reported Democratic People’s Republic of Korea (DPRK)-affiliated threat actors. Some of these accounts engaged in activity involving TTPs consistent with a threat group known as
VELVET CHOLLIMA (AKA Kimsuky, Emerald Sleet)
⁠
(opens in a new window)
, while other accounts were potentially related to an actor that was assessed by a credible source to be linked to
STARDUST CHOLLIMA (AKA APT38, Sapphire Sleet)
⁠
(opens in a new window)
. We detected these accounts following a tip from a trusted industry partner.
Behaviour
The banned accounts primarily used our tools to pursue information likely related to cyber intrusion tools or operations. They also demonstrated interest in cryptocurrency-related topics, likely in relation to financially motivated activities. This blend of financial and cyber-related activity is typical for DPRK-associated threat groups.
Completions
The actors used our models for coding assistance and debugging, along with researching security-related open-source code. This included debugging and development assistance for publicly available tools and code that could be used for Remote Desktop Protocol (RDP) brute force attacks, as well as assistance on the use of open-source Remote Administration Tools (RAT).
While debugging auto-start extensibility point (ASEP) locations and techniques for MacOS, the actor revealed staging URLs for binaries (compiled executable files) that appeared to be unknown to security vendors at the time. We submitted the staging URLs to an online scanning service to facilitate sharing with the security community, and the binaries are now reliably detected by a number of vendors, providing protection for potential victims.
A sample of activity mapped into previously proposed LLM-themed extensions to the
MITRE ATT&CK
®
Framework
⁠
(opens in a new window)
is shown below:
Asking about vulnerabilities in various applications: LLM-informed reconnaissance.
Developing and troubleshooting a C#-based RDP client to enable brute-force attacks: LLM-Aided Development.
Requesting code to bypass security warnings for unauthorized RDP access: LLM-Aided Development.
Requesting numerous PowerShell scripts for RDP connections, file upload/download, executing code from memory, and obfuscating HTML content: LLM-Enhanced Scripting Techniques; LLM-Enhanced Anomaly Detection Evasion.
Discussing creating and deploying obfuscated payloads for execution: LLM-Optimized Payload Crafting.
Seeking methods to conduct targeted phishing and social engineering against cryptocurrency investors and traders, as well as more generic phishing content: LLM-Supported Social Engineering.
Crafting phishing emails and notifications to manipulate users into revealing sensitive information: LLM-Supported Social Engineering.
Researching open-source Remote Administration Tools (RATs): LLM-Assisted Post-Compromise Activity.
Impact
Prompts and queries from the actor were primarily based on existing open-source information and the provided model generations either did not offer any novel capability or were refusals to respond. We banned the accounts associated with the threat actor, and shared their payloads with the security community to further disrupt their operations.
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
