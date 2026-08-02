---
type: Article
title: Vixen and Keyhole Panda: China-linked cyber operations
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-vixen-keyhole-panda
published: 2025-06-01
tags: [AI安全, 网络威胁, OpenAI, APT]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁了与PRC威胁组织Keyhole Panda和Vixen Panda相关的ChatGPT账户，这些账户利用AI辅助漏洞研究、脚本修改、翻译和运维，但未发现AI提供了无法从公开资源获取的新能力。

## Full Text

Vixen and Keyhole Panda: China-linked cyber operations | OpenAI
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
Vixen and Keyhole Panda: China-linked cyber operations
OpenAI banned accounts associated with threat actors publicly attributed to the PRC, using AI to support vulnerability research, scripting, translation, and operational troubleshooting.
Loading…
Share
This case study was originally published in OpenAI’s
June 2025
⁠
(opens in a new window)
report.
Actor
We banned ChatGPT accounts associated with multiple threat actors that have been publicly attributed to the People’s Republic of China (PRC). These accounts used infrastructure related to threat groups known as
KEYHOLE PANDA (AKA APT5)
⁠
(opens in a new window)
and
VIXEN PANDA (AKA APT15)
⁠
(opens in a new window)
.
Behavior
The threat actors engaged with our models in both Chinese and English. The activity we observed came from the same networks, but fell into separate subsets based on activity.
One subset used our models to assist with behaviors aligned with open-source research into various entities of interest and technical topics. For the model interactions that were technical in nature, the threat actors used our models to modify scripts or to troubleshoot system configurations. This activity included mention of reNgine, an automated reconnaissance framework for web applications, and Selenium automation, designed to bypass login mechanisms and capture authorization tokens.
Another subset appeared to be attempting to engage in development of support activities including Linux system administration, software development, and infrastructure setup. Their system administration work included advice on configured firewalls and nameservers, and building software packages for offline deployment. Their software development activity included web and Android app development, and both C-language and Golang software. Infrastructure setup included configuring VPNs, software installation, Docker container deployments, and local LLM deployments such as DeepSeek.
Completions
These threat actors generated content related to a number of topics:
Password bruteforcing: The threat actors sought help writing a script to try multiple username and password combinations against FTP servers.
Port scanning software: The threat actors used our models to modify and improve scripts to scan servers for specific ports.
AI-driven penetration testing: One threat actor researched how to use LLMs to automate penetration testing by analyzing Nmap scan output, building commands to run, and iteratively sending command output to the LLM to create new commands.
Social media automation: One threat actor worked on code designed to manage a fleet of Android devices to automate operations on social media platforms.
Research into US federal defense industry, military networks, and government technology: Multiple threat actors sought publicly available information on US Special Operations Command, satellite communications technologies, ground station terminal locations, government identity verification cards, and networking equipment.
Representative examples of these activities can be mapped to the LLM ATT&CK framework as follows:
Researching vulnerabilities and generating AI-assisted penetration testing scripts designed to be used with OpenAI API: LLM Assisted Vulnerability Research.
Automating IP range conversion and network reconnaissance scripting: LLM Enhanced Scripting Techniques.
Profiling network infrastructure by pasting text and using models to extract IPs and hostnames: LLM Guided Infrastructure Profiling.
Asking for details on government identity verification and telecom infrastructure analysis: LLM-Advised Strategic Planning.
Automating command and control for Android device social media manipulation: LLM Enhanced Scripting Techniques.
Using LLMs to analyze and summarize vulnerability reports and generate exploit payload ideas: LLM Assisted Vulnerability Research.
Generating code obfuscation and anti-reverse engineering techniques for malware development: LLM-Optimized Payload Crafting.
Impact
We disabled all accounts associated with this activity and shared relevant indicators with industry partners. While this investigation provided unusually broad visibility into a network of PRC-affiliated threat actors and their operational workflows, including tool development, open-source research, and infrastructure profiling, we found no evidence that access to our models provided these actors with novel capabilities or directions that they could not otherwise have obtained from multiple publicly available resources.
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
