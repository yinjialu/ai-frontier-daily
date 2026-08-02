---
type: Article
title: Task scam: AI-assisted fake review jobs
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-task-scam
published: 2025-02-01
tags: [AI诈骗, 虚假评论, OpenAI, 网络安全]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁了一批疑似源于柬埔寨的ChatGPT账号，这些账号利用AI翻译进行“任务型”诈骗，通过招聘者与导师等角色诱导受害者做虚假评论并骗取激活费。OpenAI已与业界及当局共享信息，以打击此类滥用行为。

## Full Text

Task scam: AI-assisted fake review jobs | OpenAI
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
Task scam: AI-assisted fake review jobs
OpenAI banned accounts that appeared to originate in Cambodia and used AI to translate messages for fake-review job scams that asked victims to pay fees.
Loading…
Share
This case study was originally published in OpenAI’s
February 2025
⁠
(opens in a new window)
report.
Actor
We banned a cluster of ChatGPT accounts that were translating short comments between Urdu and English consistent with a “
task
⁠
(opens in a new window)
” scam, in which the victims are offered a highly-paid job, but then required to pay their own money into the system before they can access their supposed “earnings.” This activity appeared to originate in Cambodia. In these scams, victims generally lose both the “earnings” and their own money. We began investigating this activity following a tip from Meta.
Behavior
This network primarily used our models to translate short comments, consistent with chats between a scammer and their victims, between Urdu and English. We identified references to messaging on Telegram (apparently their primary platform), WhatsApp, SMS, and a range of employment forums and groups where job offers could be posted.
The scammers appeared to pose as two main types of persona. One was the “recruiter”: Their messages were a form of cold outreach, posting ads for well-paid remote work. The other, which generated a higher volume of activity, was the “mentor,” who would follow up on the “recruiter”’s outreach and teach the target how to do their job. The mentors very often referenced training sessions on Telegram.
Occasionally, the scammers also used our models to proofread the text of websites. These sites appear to have spoofed the names and appearance of luxury design, fashion, and travel brands. The “mentor” personas would claim to be recruiting on behalf of those brands, indicating that the websites were likely used to make the scam appear more credible.
Completions
Based on our limited visibility, the scammers appear to have followed a common workflow in moving their targets from engagement to scam:
Job posting: Based on their prompts and generations, the scammers appear to have started by posting job offers on various online forums. The recruitment efforts typically referenced remote work, and appear to have included salaries that were relatively high for a low amount of work, for example $300 a day plus bonuses for a few hours’ work. They were typically posted by the “recruiter” persona.
Recruit: The scammers would then generate comments using the “mentor” persona to contact potential employees using what they indicated may have been a range of messaging apps, and say they were working with the “recruiter.” The “mentor” would claim to work for one of the luxury brands for which the operation had set up a website. They would describe the task as submitting five-star reviews to the sites of those luxury brands, ostensibly to boost their customer ratings.
Reassure: Often, in generations, the scammers would reassure their targets that the work was legitimate because it was on behalf of a long-established company. If the target showed unease, the scammer would claim that they, too, had been scammed before, but that this opportunity was safe.
Train: If the target expressed continued interest, the generations suggested that the “mentor” would offer them training, usually on Telegram. The target would initially be given access to a “training account,” where they would be expected to file 25-35 review tasks per day. The “training account” would show the target’s “earnings” increasing rapidly.
Excite: Often, if the target continued their training, the generations indicated they would be offered a “special” or “ultimate” review task, which offered a higher bonus. The “mentor” would emphasize how rare it was, and how lucky the target was.
“Activation fee”: Once the target’s “earnings” reached a certain level, the generations included the “mentor” telling them that they need to pay an “activation fee” to be able to withdraw their “earnings.” If needed, the scammer would urge them to borrow the money from friends or family.
Pressurize: The generations showed that, if the target balked at paying money, the scammer would become increasingly aggressive, pressurizing them by comparing them with other, more efficient workers, and saying that they would lose their earnings if they did not pay in.
Make excuses: In generations, if there was an indication that the target paid money, the scammer would make a series of excuses as to why the target could not withdraw their earnings, often saying that they need to pay in more.
Impact
Some of the conversations showed that the targets were highly skeptical, and some of the comments generated by the scammers were in the voice of a mentor trying to ask why their target had stopped messaging, suggesting that this scam likely had a low overall conversion rate. However, some conversations and online reports suggest that at least some of the victims did indeed put money into these scams. We cannot independently verify activity that happens outside of our tools.
OpenAI’s policies strictly prohibit use of output from our tools for fraud or scams. We are dedicated to collaborating with industry peers and authorities to understand how AI is influencing adversarial behaviors and to actively disrupt scam activities abusing our services. In line with this commitment, we have shared information about the scam networks we disrupted with industry peers and the relevant authorities to enhance our shared safety.
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
