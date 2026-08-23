---
type: Article
title: Offering Zero Data Retention for frontier models
source: openai-news
resource: https://openai.com/index/offering-zero-data-retention-for-frontier-models
published: 2026-08-19
tags: [OpenAI, 零数据保留, 私有安全处理, AI安全]
detected: 2026-08-23T17:00:52+08:00
---

OpenAI预览私有安全处理，使零数据保留（ZDR）兼容的安全系统能跨相关交互识别风险，同时不向OpenAI人员暴露客户内容，以兼顾隐私与安全。

## Full Text

Offering Zero Data Retention for frontier models | OpenAI
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
August 19, 2026
Company
Safety
Offering Zero Data Retention for frontier models
Previewing Private Safety Processing, which strengthens safeguards across interactions while remaining compatible with ZDR.
Loading…
Share
Why safety systems need to evolve
Why safety systems need to evolve
How Private Safety Processing works
Privacy and safety built with and for our customers
Why safety systems need to evolve
How Private Safety Processing works
Privacy and safety built with and for our customers
Zero Data Retention gives eligible API customers a clear promise: OpenAI does not retain their prompts or model responses after a request is processed. Customer content is not available to OpenAI personnel for review
1
, and enterprise customer data is not used to train our models unless customers explicitly opt-in.
As models take on longer, more complex tasks, some serious risks may only become visible across multiple interactions. Existing ZDR-compatible safety systems evaluate each interaction individually. Today, we’re previewing Private Safety Processing, which is designed to identify patterns across related interactions without giving OpenAI personnel access to the underlying content.
For ZDR deployments, customer content remains on infrastructure the customer controls. We are also developing an option in which content is stored on OpenAI infrastructure, encrypted with keys controlled by the customer. In both cases, automated systems can identify potential misuse and return limited safety signals without exposing the underlying prompts or responses to OpenAI personnel.
Why safety systems need to evolve
The most serious AI safety risks are not always visible in a single interaction. Often, potentially harmful intentions become clear only when multiple interactions are viewed together. Similar risks can arise when bad actors repeatedly probe safeguards, coordinate across accounts, or disguise threats as routine research. Risks can also develop over the course of an agentic task—for example, if a system becomes misaligned with the user’s intent by continuing to act after being told to stop.
As AI systems take on longer and more complex tasks, this broader context becomes increasingly important for distinguishing legitimate activity from misuse and ensuring that AI agents remain within the bounds of their intended authority.
Some recent frontier-model deployments have required customers to allow their AI provider to retain sensitive content for safety monitoring. For many organizations, such requirements conflict with their security obligations or commitments to the people they serve.
Private Safety Processing is designed so we can continue to offer ZDR.
How Private Safety Processing works
Private Safety Processing builds on the automated protections already used in ZDR and other deployments. Existing ZDR-compatible safety systems evaluate interactions individually. Private Safety Processing extends those protections across related interactions, allowing automated systems to identify patterns without OpenAI personnel having access to retained customer content.
Private Safety Processing utilizes customer content regardless of where it is stored—whether in infrastructure customers control (ZDR deployments) or in storage provided by OpenAI. With OpenAI-provided storage, customer content is encrypted using keys controlled by the customer. OpenAI personnel do not have a copy of those keys, so they cannot access the underlying content.
When a risk is identified, OpenAI receives a narrowly defined signal indicating the type of activity involved, similar to our existing safety systems today. That signal can be used to determine whether enforcement is necessary. OpenAI personnel do not receive access to the customer content even when it is flagged.
Customers can investigate alerts and enforcement decisions using information available in their own systems. If they want to appeal, clarify legitimate activity, or support an investigation into verified abuse, they can choose to share relevant information with OpenAI.
Private Safety Processing is currently being tested with early customers. We are sharing this preview now because we’ve heard our customers loud and clear that they need predictability about how their content will be protected as AI systems become more capable.
Privacy and safety built
with
and
for
our customers
Our mission is to ensure that artificial general intelligence benefits all of humanity. Collaboration with customers and partners is essential to how we build effective safeguards. As
our principles
make clear, no AI lab can address emerging risks alone. Private Safety Processing reflects that approach and is being shaped by customers across industries, regions, and company sizes.
The organizations we work with handle some of the most sensitive information in their sectors, including financial records, health data, confidential business plans, and proprietary research. Protecting that information is essential to meeting regulatory obligations, maintaining customer trust, and preserving their competitive advantage.
Their feedback is helping us build stronger safeguards while keeping their information under their control.
Glean
Databricks
Abridge
Microsoft
“Enterprise AI adoption depends solely on customer control of data, with no direct or derivative use beyond the chosen service. OpenAI’s no-training commitment and ZDR give Glean confidence to build with OpenAI. As models become more capable, OpenAI shows safety can advance without compromising the privacy and control that sustain enterprise trust.”
—Sunil Agrawal, Chief Information Security Officer, Glean
We will continue working with customers on the technical and operational details of our approach. We plan to start rolling out Private Safety Processing, and share a technical white paper, in September. We’ll keep customers informed every step of the way, sharing updates early, explaining what they mean for existing commitments, and providing the time and support customers need to plan ahead.
2026
API Platform
Author
OpenAI
1
Like other frontier model providers, OpenAI is
required by law
⁠
(opens in a new window)
to report apparent child sexual abuse material (CSAM). Images flagged for potential CSAM will continue to be retained for manual review and reporting purposes, even in Zero Data Retention deployments, as they are today.
Keep reading
View all
ChatGPT Ads expands across Europe
Product
Aug 18, 2026
Partnering with CodeAI to prepare the first AI generation
Company
Aug 18, 2026
Pacing model development in an era of cyber-critical capabilities
Company
Aug 18, 2026
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
