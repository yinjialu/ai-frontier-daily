---
type: Article
title: CyberAv3ngers: Iran-linked cyber research activity
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-cyberav3ngers
published: 2024-10-01
tags: [AI安全, 网络攻击, 工业控制系统, 伊朗]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁疑似伊朗背景黑客组织CyberAv3ngers的账户，该组织利用ChatGPT研究工业控制系统漏洞、默认凭证，并调试攻击脚本，但未获得新颖能力。

## Full Text

CyberAv3ngers: Iran-linked cyber research activity | OpenAI
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
October 1, 2024
CyberAv3ngers: Iran-linked cyber research activity
OpenAI banned accounts that appeared to belong to CyberAv3ngers using AI to research industrial control systems, default credentials, and targets.
Loading…
Share
This case study was originally published in OpenAI’s
October 2024
⁠
(opens in a new window)
report.
Actor
We banned accounts, which based on an assessment from a credible source, appear to belong to an adversary known as CyberAv3ngers that has been publicly reported as affiliated with Iran’s IRGC. Accounts operated by this threat actor used our models to research vulnerabilities, debug code, and ask for scripting advice.
Behavior
Based on open-source information, the CyberAv3ngers group is known for its disruptive attacks against industrial control systems (ICS) and programmable logic controllers (PLCs) used in water systems, manufacturing, and energy systems. Infrastructure targeted by this group is typically associated with Israel, the United States, or Ireland.
Recent attacks have included compromise of PLCs at the Municipal Water Authority of Aliquippa in Pennsylvania (November 2023) and a two-day disruption of water services in County Mayo, Ireland (December 2023). These campaigns often take advantage of default / weak passwords or well documented vulnerabilities in PLCs in combination with open-source tools for scanning and exploiting industrial control systems.
Much of the behavior observed on ChatGPT consisted of reconnaissance activity, asking our models for information about various known companies or services and vulnerabilities that an attacker would have historically retrieved via a search engine. We also observed these actors using the model to help debug code.
Completions
The tasks the CyberAv3ngers asked our models in some cases focused on asking for default username and password combinations for various PLCs. In some cases, the details of these requests suggested an interest in, or targeting of, Jordan and Central Europe.
The operators also sought support in creating and refining bash and python scripts. These scripts sometimes leveraged publicly available pentesting tools and security services to programmatically find vulnerable infrastructure. CyberAv3nger accounts also asked our models high-level questions about how to obfuscate malicious code, how to use various security tools often associated with post-compromise activity, and for information on both recently disclosed and older vulnerabilities from a range of products. While previous public reporting on this threat actor focused on their targeting of ICS and PLCs, from these prompts we were able to identify additional technologies and software that they may seek to exploit, which can be found in the table below.
Activity
LLM ATT&CK Framework Category
Asking to list commonly used industrial routers in Jordan.
LLM-informed reconnaissance
Asking to list industrial protocols and ports that can connect to the Internet.
LLM-informed reconnaissance
Asking for the default password for a Tridium Niagara device.
LLM-informed reconnaissance
Asking for the default user and password of a Hirschmann RS Series Industrial Router.
LLM-informed reconnaissance
Asking for recently disclosed vulnerabilities in CrushFTP and the Cisco Integrated Management Controller as well as older vulnerabilities in the Asterisk Voice over IP software.
LLM-informed reconnaissance
Asking for lists of electricity companies, contractors and common PLCs in Jordan.
LLM-informed reconnaissance
Asking why a bash code snippet returns an error.
LLM enhanced scripting techniques
Asking to create a Modbus TCP/IP client.
LLM enhanced scripting techniques
Asking to scan a network for exploitable vulnerabilities.
LLM assisted vulnerability research
Asking to scan zip files for exploitable vulnerabilities.
LLM assisted vulnerability research
Asking for a process hollowing C source code example.
LLM assisted vulnerability research
Asking how to obfuscate vba script writing in excel.
LLM-enhanced anomaly detection evasion
Asking the model to obfuscate code (and providing the code).
LLM-enhanced anomaly detection evasion
Asking how to copy a SAM file.
LLM-assisted post compromise activity
Asking for an alternative application to mimikatz.
LLM-assisted post compromise activity
Asking how to use pwdump to export a password.
LLM-assisted post compromise activity
Asking how to access user passwords in MacOS.
LLM-assisted post compromise activity
Impact
In line with our findings from other investigations into state-sponsored threat actors using our models, we believe that these interactions did not provide CyberAv3ngers with any novel capability, resource, or information, and only offered limited, incremental capabilities that are already achievable with publicly available, non-AI powered tools.
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
