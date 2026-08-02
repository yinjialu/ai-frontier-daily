---
type: Article
title: Operation “Peer Review”: AI-assisted surveillance planning
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-peer-review
published: 2025-02-01
tags: [AI安全, 滥用, 网络监控, OpenAI]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁了一批疑似来自中国的ChatGPT账户，这些账户利用AI辅助生成社交媒体监控工具的宣传材料、调试相关代码，并分析政治人物及文档，涉及网络监控与情报支持。

## Full Text

Operation “Peer Review”: AI-assisted surveillance planning | OpenAI
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
Operation “Peer Review”: AI-assisted surveillance planning
OpenAI banned likely China-origin accounts using AI to draft surveillance-tool pitches, analyze documents, and debug code.
Loading…
Share
This case study was originally published in OpenAI’s
February 2025
⁠
(opens in a new window)
report.
Summary
Actor
We banned a cluster of ChatGPT accounts that, based on behavioral patterns and other findings, likely originated in China. They were using our models to assist with analyzing documents, generating sales pitches and descriptions of tools for monitoring social media activity powered by non-OpenAI models, editing and debugging code for those tools, and researching political actors and topics. Based on this network’s behavior in promoting and reviewing surveillance tooling, we have dubbed it “Peer Review.”
Behavior
This network consisted of ChatGPT accounts that operated in a time pattern consistent with mainland Chinese business hours, prompted our models in Chinese, and used our tools with a volume and variety consistent with manual prompting, rather than automation. In one instance, we believe the same account may have been used by multiple operators.
Within the cluster, the operators performed a number of primary tasks. One was to use the model as a basic research tool, in a way similar to which earlier generations would have used search engines. This included, for example, searching for publicly available information about think tanks in the United States, and politicians and government officials in countries including Australia, Cambodia, and the United States.
Another workstream consisted of using our models to read, translate, and analyze screenshots of English-language documents. Some of these images were announcements of Uyghur rights protests in a range of Western cities, and were potentially copied from social media. Others appeared to concern diplomatic and government topics in the Indo-Pacific region. There is insufficient evidence to determine whether these documents were authentic, or to show how the operators obtained them.
A third workstream consisted of using ChatGPT to generate short- to medium-length comments about Chinese dissident organizations, notably the Falun Gong, and about US policies and politics. Occasionally, the actors asked the model to assume the persona of an English-speaker called “Thompson.” We were not able to identify these comments posted online.
Fourth, the operators used our model to edit and debug code and generate promotional materials for what appeared to be an AI-powered social media listening tool. We did not see evidence of this tool being run on our models. The details of this activity are described below.
Completions
One of this operation’s main activities was generating detailed descriptions, consistent with sales pitches, for what they described as the “Qianyue Overseas Public Opinion AI Assistant” (“千阅境外舆情AI助手”). According to the descriptions, which we cannot independently verify, this was designed to ingest and analyze posts and comments from platforms such as X, Facebook, YouTube, Instagram, Telegram, and Reddit.
Again according to the descriptions, one purpose of this tooling was to identify social media conversations related to Chinese political and social topics, especially any online calls to attend demonstrations about human rights in China, and to feed the resulting insights to Chinese authorities. The operators used our models to proofread claims that their insights had been sent to Chinese embassies abroad, and to intelligence agents monitoring protests in countries including the United States, Germany, and the United Kingdom.
A separate account in the same cluster also referenced the social-media monitoring tool, but in the context of editing and debugging code. This operator used ChatGPT to debug and modify code that appeared designed to run the social-media monitoring tool. This code most frequently named Meta’s llama3.1:8b deployed via Ollama as the driver of the tool’s analysis and generation. We do not have visibility into whether, how, or where this code may have been deployed.
The same account debugged code apparently intended for malware analysis, and referred to other models like Qwen (built by Alibaba Cloud) and an unspecified model by DeepSeek. It also used our models to generate what appeared to be an end-of-year performance review, which claimed that the actor had generated phishing emails on behalf of unspecified clients in China. We did not see evidence or claims that this email-related activity had been powered by AI.
Impact
Very little of this operation’s activity appeared to be designed for publication on social media or other distribution platforms. A few generations did resemble social media comments, but we were not able to identify them being posted online. Significantly more content appeared to be for capability development, such as code debugging, or for internal purposes, such as image analysis and the development of promotional materials.
Assessing the impact of this activity would require inputs from multiple stakeholders, including operators of any open-source models who can shed a light on this activity.
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
