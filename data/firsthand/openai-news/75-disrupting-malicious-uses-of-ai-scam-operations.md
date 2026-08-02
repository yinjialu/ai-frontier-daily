---
type: Article
title: Scam operations: Online fraud networks
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-scam-operations
published: 2025-10-01
tags: [AI安全, 网络诈骗, OpenAI, 反欺诈]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI于2025年10月披露，已封禁疑似源自柬埔寨、缅甸和尼日利亚的在线诈骗网络。诈骗者利用ChatGPT生成翻译、撰写脚本、伪造身份及运营虚假投资平台，但ChatGPT也被用于识别诈骗，使用次数是滥用的三倍。报告展示了AI在欺诈与反欺诈中的双重角色。

## Full Text

Scam operations: Online fraud networks | OpenAI
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
October 1, 2025
Scam operations: Online fraud networks
OpenAI banned accounts tied to online fraud networks using AI to support scam scripts, impersonation, translation, and victim engagement.
Loading…
Share
This case study was originally published in OpenAI’s
October 2025
⁠
(opens in a new window)
report.
Networks likely originating in Cambodia, Myanmar, and Nigeria abusing ChatGPT in what appear to be attempts to defraud people online.
We are dedicated to identifying, preventing and disrupting attempts to abuse our models for harmful ends. Among those abuses are scams, where we detect and ban malicious actors attempting to misuse our models to deceive and defraud people. In the last three months, we’ve disrupted scam networks that likely originated in Cambodia, Myanmar and Nigeria. In an indication of the role AI can play in combating fraud, in the process of investigating these patterns of abuse, we’ve also seen many people using our models to help them identify scams. This report discusses both use cases.
Abuse of our models to support scams ranges from lone actors attempting fraud to scaled and persistent operations likely linked to organized crime groups. Regardless of their origins and precise tactics, the scam-related activity we’ve disrupted typically follows a common pattern, which we think of as the ping (cold outreach), the zing (trying to generate enthusiasm or panic), and the sting (extracting money or valuable information).
These scammers start out by scattering content, whether AI-generated or not, across messaging services and the internet, including by running social media ads. They then attempt to inspire anyone who replies with either enthusiasm for a lucrative opportunity or fear of some imminent financial loss, and leverage that emotion to convince the target to hand over money or sensitive information.
We’ve also observed many cases where our models have likely helped keep people safe from fraud. We have seen evidence of people using ChatGPT to help them identify and avoid online scams millions of times a month; in every scam operation in this report, we have seen the model help people correctly identify the scam and advise them on appropriate safety measures. Our current estimate is that ChatGPT is being used to identify scams up to three times more often than it is being used for scams.
Example of an OpenAI investigator pasting a screenshot of a scam SMS message they received into ChatGPT and successfully using the model to identify it as a scam. In this instance, the threat actors attempted to impersonate TikTok recruiters.
We’ve reinforced our own ability to detect and disrupt scams since our last report. We’ve disrupted further scam networks that appeared to originate from Cambodia, Myanmar and Nigeria. Together with our earlier disruptions, these takedowns allow us to identify some emerging trends across multiple scam operations from different countries.
Old tricks, AI tools
The majority of the scam activity we disrupted centered on fitting AI into existing scam playbooks, rather than creating new playbooks built around AI. All of the scam operations we have identified and banned this year primarily used AI as a scaling and efficiency tool. This typically included using our models for translation, to write messages, and to create content for social media.
For example, we recently banned scam operations likely originating in Cambodia and Nigeria that posed as “investment firms” in an attempt to defraud victims in multiple countries. The scammers created websites and online ads to promote the fake firms and used likely inauthentic social media accounts posing as trading experts to invite people to join private messaging groups. Promising lucrative and zero-risk earning opportunities, the threat actors then sought to entice potential victims to make payments into fictitious trading platforms. Across all of the scams, the scammers primarily used our models to generate and translate correspondence, create content for their websites and social media accounts, and conduct basic research.
In another case, we banned a scam center highly likely located in Myanmar that used our models both to generate content for its fraudulent schemes and to conduct day-to-day business tasks. This included organizing schedules, drafting internal announcements, assigning desk and dormitory allocations, and managing financial accounts. Some operators asked about the criminal penalties for people caught conducting online scams.
All scammers are equal, but some are more AI-qual than others
Not all scammers that we disrupted used our models in the same ways, or with the same degree of complexity. The majority of scammer interactions with ChatGPT featured relatively simple tasks like translation, but some scam operations were more ambitious and elaborate.
For instance, one likely Cambodia-origin scam operation we disrupted used our models to generate detailed biographies for fake investment experts and fictitious employees of fake trading firms. The scammers then asked ChatGPT to write social media messages in those characters’ voices. Often, the threat actors input to our model messages they appear to have received from their targets, and asked the model to continue the conversation as the fake persona.
A second scam operation, also likely originating in Cambodia, started out by using our models to generate cold-call SMS messages that were bulk-sent to U.S. phone numbers. One of these was sent to an OpenAI investigator, similar to the case that we reported in June. These SMS messages included invitations to join WhatsApp groups, subsequently banned, whose names resembled a legitimate investment firm.
Based on a series of WhatsApp messages sent to the OpenAI investigator, if a potential target joined one of these groups, they would quickly witness a “conversation” between half a dozen different accounts, all talking about investment. One of these posed as the “investment expert”, while the rest posed as investors with varying degrees of confidence and experience. Every part of this conversation was generated by the scammers, who translated it in a single block from Chinese – likely to create the impression of a vibrant group of keen and successful traders. Ultimately, the “investment expert” would suggest that the target try investing too.
Separately, an investment scam operation very likely originating in Nigeria asked the model for step-by-step advice on how to use social media ads to reach wealthy people in Latin America, how to mask their location, and how to avoid restrictions by social media platforms. This entailed directing the model to a platform’s public terms of service and asking it to review proposed ad content for compliance.
Obfuscation and excuses
Scammers, especially large-scale scam centers, are persistent. Very often, their response to disruption is to try to restart their violative activity, while changing some elements of their behavior, likely in an effort to evade further detection. This is one reason why it is important to share insights into their evolving activity across the industry, such as when OpenAI and Meta each shared information on threat actors that contributed to further investigation and enforcement.
Potentially in response to disruptions or to broader online conversations about signals that can betray AI usage, we have seen scammers attempt to disguise their use of AI in online content and communications with targets. This includes scam operations likely originating in Cambodia directing the model to remove em-dashes from outputs.
In one case, the scammers attempted to explain a large-scale disruption of their social media assets by making up an excuse for being banned. This concerned the likely Cambodia-origin scam center that operated on SMS and WhatsApp, described above. After WhatsApp banned “investment groups” linked to the operation, the operators started generating messages which claimed that those groups had been falsely reported by a competitor, likely to explain away the bans.
Screenshot of a WhatsApp message sent by the Cambodia-linked scam operation to an OpenAI investigator following WhatsApp’s takedown.
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
