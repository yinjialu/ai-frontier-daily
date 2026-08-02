---
type: Article
title: Operation “ScopeCreep”: Russian-speaking malware development
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-scopecreep
published: 2025-06-01
tags: [AI安全, 恶意软件, 威胁情报, ChatGPT滥用]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁一批俄语恶意软件开发者账号，其利用ChatGPT辅助开发Windows恶意软件、调试代码及搭建C2，通过伪装游戏工具的仓库分发，并采用多种规避手段。OpenAI与平台合作下架恶意仓库并封禁相关账号，展现AI滥用监测与响应能力。

## Full Text

Operation “ScopeCreep”: Russian-speaking malware development | OpenAI
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
Operation “ScopeCreep”: Russian-speaking malware development
OpenAI banned Russian-language accounts using AI to build malware, refine loaders, and troubleshoot cyber tooling.
Loading…
Share
This case study was originally published in OpenAI’s
June 2025
⁠
(opens in a new window)
report.
Actor
We banned a cluster of ChatGPT accounts that appeared to be operated by a Russian-speaking threat actor. This actor used our models to assist with developing and refining Windows malware, debugging code across multiple languages, and setting up their command-and-control infrastructure.
The actor demonstrated knowledge of Windows internals and exhibited some operational security behaviors. Based on the operation’s focus on using a trojanized “crosshair” gaming tool and its stealthy tactics, we have dubbed it “ScopeCreep.”
Behavior
This threat actor had a notable approach to operational security. They utilized temporary email addresses to sign up for ChatGPT accounts, limiting each ChatGPT account to one conversation about making one incremental improvement to their code. They then abandoned the original account and created a new one.
The actor distributed the ScopeCreep malware through a publicly available code repository that impersonated a legitimate and popular crosshair overlay tool (Crosshair-X) for video games. Unsuspecting users who downloaded and ran the malicious version would initiate the malware loader on their system, resulting in additional malicious files being downloaded from attacker infrastructure and executed.
From there, the malware was designed to initiate a multi-stage process to escalate privileges, establish stealthy persistence, notify the threat actor, and exfiltrate sensitive data while evading detection.
The threat actor utilized our model to assist in developing the malware iteratively, by continually requesting ChatGPT to implement further specific features. ScopeCreep showcased a range of techniques across delivery, execution, evasion, and exfiltration, including:
C2 payloads designed to avoid signature-based detections.
Stealthy execution via DLL side-loading.
Obfuscation via custom packing with Themida.
Privilege escalation and evasion.
HTTPS over port 80.
Credential and session theft.
Attacker notifications via Telegram.
Proxy-based traffic obfuscation.
Despite the threat actor’s operational security efforts and detection evasion mechanisms in the malware itself, we were able to detect the activity due to our scaled cyber abuse detection process. We coordinated with the code hosting provider to take down the malicious repository and banned all ChatGPT accounts associated with this activity.
Completions
The model interactions from this cluster covered a wide range of development tasks. One included a snippet of Go code where the threat actor was struggling with an HTTPS request, and asked the model to debug it. In a separate instance, the threat actor asked for assistance in using PowerShell commands via Go to modify Windows Defender settings, looking for a way to programmatically add AV exclusions.
Representative examples of these activities can be mapped to the LLM ATT&CK framework as follows:
Using LLMs to compile a file, python310.dll, so that their code is executed whenever python.exe runs: LLM Aided Development.
Troubleshooting errors with SSL/TLS certificates designed to serve HTTPS traffic on port 80: LLM Aided Development.
Model-assisted migration of a Flask-based C2 server to a production-ready WSGI server: LLM Aided Development.
Developing PowerShell commands in Go to modify Windows Defender settings and add AV exclusions: LLM-Enhanced Anomaly Detection Evasion.
Debugging errors in code to notify an attacker-controlled Telegram channel when a new victim is compromised: LLM-Assisted Post-Compromise Activity.
Impact
At this stage, the impact of ScopeCreep may have been mitigated by quick reporting and close collaboration with industry partners who were able to take down the malicious repository. We banned the OpenAI accounts used by this adversary.
We assess this threat actor utilized our models in an attempt to speed up their malware development operations. Paradoxically, this also provided an opportunity for us to identify and disrupt the threat quickly and in what looked like its early stages.
While this malware’s capabilities include privilege escalation, persistence, credential harvesting, and remote access, these are not particularly novel. Although this malware was likely active in the wild, with some samples appearing on VirusTotal, we did not see evidence of any widespread interest or distribution.
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
