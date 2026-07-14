---
type: Article
title: Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
source: claude-blog
resource: https://claude.com/blog/working-at-the-frontier-how-hebbia-builds-ai-for-financial-diligence-that-cant-miss-a-detail
published: 2026-07-13
tags: [金融AI, 大模型评测, Claude应用, AI Agent]
detected: 2026-07-14T08:23:12+08:00
---

Hebbia为金融机构构建AI尽职调查平台，使用Claude Fable 5在自有金融评测中取得最大准确率提升（约20%相对增益），通过元提示和矩阵网格实现透明可追溯的分析，满足高精度投资决策需求。

## Full Text

Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail | Claude by Anthropic
Meet Claude
Products
Claude
Claude Code
Claude Cowork
@Claude
Features
Claude for Chrome
Claude for Microsoft 365
Skills
Claude apps built for
Design
Science
Security
Models
Mythos
Fable
Opus
Sonnet
Haiku
Platform
Build on Claude
Overview
Pricing
Developer docs
Console login
Works with Claude
Ecosystem
Marketplace
Connectors
Plugins
Solutions
Use cases
AI agents
Coding
Company size
Startups
Enterprise
Departments
Legal
Security
Industries
Customer support
Education
Financial services
Government
Healthcare
Life sciences
Nonprofits
Pricing
Overview
API
Resources
Insights
Blog
Customer stories
Anthropic news
Learn
Anthropic Academy
Courses
Tutorials
Use cases
Connect
Events
Community
Login
Contact sales
Contact sales
Contact sales
Try Claude
Try Claude
Try Claude
Contact sales
Contact sales
Contact sales
Try Claude
Try Claude
Try Claude
Contact sales
Contact sales
Contact sales
Try Claude
Try Claude
Try Claude
Contact sales
Contact sales
Contact sales
Try Claude
Try Claude
Try Claude
Meet Claude
Products
Claude
Claude Code
Claude Cowork
@Claude
Features
Claude for Chrome
Claude for Microsoft 365
Skills
Claude apps built for
Design
Science
Security
Models
Mythos
Fable
Opus
Sonnet
Haiku
Platform
Build on Claude
Overview
Pricing
Developer docs
Console login
Works with Claude
Ecosystem
Marketplace
Connectors
Plugins
Solutions
Use cases
AI agents
Coding
Company size
Startups
Enterprise
Departments
Legal
Security
Industries
Customer support
Education
Financial services
Government
Healthcare
Life sciences
Nonprofits
Pricing
Overview
API
Resources
Insights
Blog
Customer stories
Anthropic news
Learn
Anthropic Academy
Courses
Tutorials
Use cases
Connect
Events
Community
Login
Contact sales
Contact sales
Contact sales
Try Claude
Try Claude
Try Claude
Contact sales
Contact sales
Contact sales
Try Claude
Try Claude
Try Claude
Blog
Blog
/
Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
Explore here
Ask questions about this page
Copy as markdown
Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
Hebbia builds research and diligence software for financial professionals, and tests every new model against finance evals tied to expert outcomes. In testing, Claude Fable 5 posted the biggest accuracy gain its research team has recorded, and tracked complex queries that prior models kept dropping.
Category
Enterprise AI
Product
No items found.
Date
July 13, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/working-at-the-frontier-how-hebbia-builds-ai-for-financial-diligence-that-cant-miss-a-detail
Hebbia is an AI platform built for the rigor of  institutional finance, serving more than a third of the top 50 asset managers along with tier-1 investment banks and law firms. Divya Mehta, the company's founding product manager, spends roughly half her time with its largest investment banking, private equity, and credit customers.
Those customers make decisions based on analyses that span thousands of dense documents, where a wrong number can change the outcome of an entire deal.
How Hebbia holds the line on accuracy
A banker or investor weighing an opportunity has to work through all the data that could impact the decision, including the company's public filings, its credit agreements, internal documents, and structured data like information from a CRM. Hebbia's meta-prompting turns plain-language requests into prompts, and then Claude runs each step of the analysis across hundreds of documents. Each answer lands in its own cell on a grid in Hebbia's Matrix, enabling full transparency, traceability, and steerability.
Keeping those answers accurate at scale is the work of Hebbia's applied AI research team, led by Adithya Ramanathan. For Ramanathan, the point of that work is finding signals: getting a model to draw on the right data, in the right context, and surface what a customer wants to know.
"When you're connecting it to the right data and putting it in the right ecosystem," Ramanathan says, "that's when you get the alpha that finance professionals actually chase."
Getting there means running every new model through Hebbia's finance-specific benchmark, head to head against the model it would replace, and expanding what the benchmark measures with each release to keep pace as models improve. The benchmark is built to be hard on purpose.
"The bar is extremely high, and our customers hold us to that extremely high bar—and rightfully so," Mehta says. "At the end of the day, they're making investment decisions at a very large scale based on the analysis and final work product built in Hebbia."
The team at Hebbia runs every new Claude model through finance-specific benchmarks that run head-to-head against the model it would replace.
Clearing Hebbia's evals by the widest margin yet
Joe Renner, a researcher on the applied AI team, runs each new Claude model against that benchmark, with a battery of tests replicating key finance knowledge worker use cases. One such test covers question answering and citation finding over financial documents. Another test runs through Hebbia's agent system, with the tools its chat product uses, on the kind of open-ended, multi-source analysis a customer actually does.
Claude Fable 5 cleared both by the widest margin Renner had measured. On the question-answering and citation test, it posted about a 20% relative gain in accuracy over financial documents, the best he had seen from any new model. Citation match held roughly steady—Renner believes the gain comes from the model better understanding the evidence it finds.
"It comes down to two seemingly fundamental qualities: the ability to find the right information from a dense data set, and then synthesize it correctly," Divya says. "These seem like fundamental model capabilities, but they have massive impact when we think about finance and research workflows." On the agent run, it held every part of a multi-part request at once, answering all of them and citing each answer back to its source.
Claude Fable 5 also showed more reach. On open-ended analysis, it reasoned from a wider cross-section of the data and arrived at conclusions the team thought were worth a closer look. Renner traces that to how the model holds a long task together: it keeps every part of a request in view, prompts its own sub-agents and tools so the right facts come back, and grounds each claim in the source rather than inferring it.
Setting a new standard for deal diligence with Claude Fable 5
The information that gives customers  an edge usually sits in unstructured, proprietary documents.
Those have been harder to analyze at scale than the structured, quantitative data finance already models well. Hebbia built Matrix to make that qualitative work systematic, and every model generation widens what it can take on.
That might be a data room with thousands of documents, where the work is finding the relevant signal, citing it, and drafting each section of an investment memo. Or it might be analyzing every document tied to a credit deal (the credit agreement, amendments, side letters, each running hundreds of dense technical pages) and extracting the full covenant package, financial terms and operating restrictions alike, from that unstructured mass.
"These are actually the types of documents that Anthropic models have always done really well at," Mehta says.
With earlier Sonnet and Opus models, Matrix could already pull out and synthesize a credit agreement's covenants—the dense protections a lender writes in for itself. With Claude Fable 5, Hebbia is reaching for the rest of the job: the multi-step analysis on top of those covenants, comparing them against live monitoring data, flagging risks, all the way to a first draft of the covenant review and an internal memo. That review is something credit firms used to pay outside teams a great deal to produce by hand.
Claude Fable 5 enables Matrix, Hebbia's AI platform built for financial professionals, to take on longer-running, multi-step tasks like synthesizing credit agreement coven
What's next
Now that models like Claude Fable 5 can carry this work end to end, the comparison is the specialist hours it replaces.
Before AI, when a managing director needed a deck to pitch a CEO, it would take a junior banker 2-3 days to learn the company, pull financials, and build slides. In the pre-Opus days, the timeline to produce a first draft compressed by 12 to 24 hours, and with earlier Opus models on Hebbia, Mehta says, it dropped even further, taking about a day to run end-to-end. Hebbia has since codified the whole job into a Matrix that gathers the data across sources in a set of deterministic agentic steps, does the analysis, and builds the final deck, financial model, and internal research in a couple of minutes, so the banker can spend the time on which buyers to pursue and how to position them. Claude Fable 5 tightens it further, she says.
Decomposing the work into steps still matters, "no matter how brilliant the model is," because firms want control over which documents feed the analysis and how each step is built. So Hebbia is adopting the Claude Agent SDK to compose these jobs as smaller, repeatable, checked steps rather than a single model run.
"Compressing the deal lifecycle has a massive impact on a firm's ability to compete for those investments," Mehta says. She hears it in customer conversations. Two or three years ago the questions were defensive, about hallucinations and whether the math was right. "Today, those conversations have changed completely. They're: how can I automate more of my workflow? How do I sequence more steps together? How can I generate ten, fifteen, twenty slide decks in one click with high fidelity and consistency?"
Get started with
Claude Fable 5.
No items found.
Prev
Prev
0
/
5
Next
Next
eBook
FAQ
No items found.
Related posts
Explore more product news and best practices for teams building with Claude.
Jun 5, 2026
The Claude Cowork product guide
Enterprise AI
The Claude Cowork product guide
The Claude Cowork product guide
The Claude Cowork product guide
The Claude Cowork product guide
Jun 24, 2026
Building effective human-agent teams
Enterprise AI
Building effective human-agent teams
Building effective human-agent teams
Building effective human-agent teams
Building effective human-agent teams
Jul 10, 2026
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Enterprise AI
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Jul 7, 2026
How people are using Claude Cowork
Enterprise AI
How people are using Claude Cowork
How people are using Claude Cowork
How people are using Claude Cowork
How people are using Claude Cowork
Transform how your organization operates with Claude
See pricing
See pricing
See pricing
Contact sales
Contact sales
Contact sales
Get the developer newsletter
Product updates, how-tos, community spotlights, and more. Delivered monthly to your inbox.
Subscribe
Subscribe
Please provide your email address if you'd like to receive our monthly developer newsletter. You can unsubscribe at any time.
Thank you! You’re subscribed.
Sorry, there was a problem with your submission, please try again later.
Homepage
Homepage
Next
Next
Thank you! Your submission has been received!
Oops! Something went wrong while submitting the form.
Write
Button Text
Button Text
Learn
Button Text
Button Text
Code
Button Text
Button Text
Write
Help me develop a unique voice for an audience
Hi Claude! Could you help me develop a unique voice for an audience? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Improve my writing style
Hi Claude! Could you improve my writing style? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Brainstorm creative ideas
Hi Claude! Could you brainstorm creative ideas? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Learn
Explain a complex topic simply
Hi Claude! Could you explain a complex topic simply? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Help me make sense of these ideas
Hi Claude! Could you help me make sense of these ideas? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Prepare for an exam or interview
Hi Claude! Could you prepare for an exam or interview? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Code
Explain a programming concept
Hi Claude! Could you explain a programming concept? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Look over my code and give me tips
Hi Claude! Could you look over my code and give me tips? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Vibe code with me
Hi Claude! Could you vibe code with me? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to— like Google Drive, web search, etc.—if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can—an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
More
Write case studies
This is another test
Write grant proposals
Hi Claude! Could you write grant proposals? If you need more information from me, ask me 1-2 key questions right away. If you think I should upload any documents that would help you do a better job, let me know. You can use the tools you have access to — like Google Drive, web search, etc. — if they’ll help you better accomplish this task. Do not use analysis tool. Please keep your responses friendly, brief and conversational.
Please execute the task as soon as you can - an artifact would be great if it makes sense. If using an artifact, consider what kind of artifact (interactive, visual, checklist, etc.) might be most helpful for this specific task. Thanks for your help!
Write video scripts
this is a test
Anthropic
Anthropic
©
[year]
Anthropic PBC
Products
Claude
Claude
Claude
Claude Code
Claude Code
Claude Code
Claude Code for Enterprise
Claude Code for Enterprise
Claude Code for Enterprise
Claude Cowork
Claude Cowork
Claude Cowork
@Claude
@Claude
@Claude
Claude Design
Claude Design
Claude Design
Claude Science
Claude Science
Claude Science
Claude Security
Claude Security
Claude Security
Download app
Download app
Download app
Pricing
Pricing
Pricing
Log in
Log in
Log in
Features
Claude for Chrome
Claude for Chrome
Claude for Chrome
Claude for Microsoft 365
Claude for Microsoft 365
Claude for Microsoft 365
Skills
Skills
Skills
Models
Mythos
Mythos
Mythos
Fable
Fable
Fable
Opus
Opus
Opus
Sonnet
Sonnet
Sonnet
Haiku
Haiku
Haiku
Solutions
AI agents
AI agents
AI agents
Code modernization
Code modernization
Code modernization
Coding
Coding
Coding
Customer support
Customer support
Customer support
Education
Education
Education
Enterprise
Enterprise
Enterprise
Financial services
Financial services
Financial services
Government
Government
Government
Healthcare
Healthcare
Healthcare
Legal
Legal
Legal
Life sciences
Life sciences
Life sciences
Nonprofits
Nonprofits
Nonprofits
Security
Security
Security
Small business
Small business
Small business
Claude Platform
Overview
Overview
Overview
Developer docs
Developer docs
Developer docs
Pricing
Pricing
Pricing
Ecosystem
Ecosystem
Ecosystem
Marketplace
Marketplace
Marketplace
Claude on AWS
Claude on AWS
Claude on AWS
Google Cloud
Google Cloud
Google Cloud
Microsoft Foundry
Microsoft Foundry
Microsoft Foundry
Regional compliance
Regional compliance
Regional compliance
Console login
Console login
Console login
Resources
Blog
Blog
Blog
Claude partner network
Claude partner network
Claude partner network
Community
Community
Community
Connectors
Connectors
Connectors
Courses
Courses
Courses
Customer stories
Customer stories
Customer stories
Engineering at Anthropic
Engineering at Anthropic
Engineering at Anthropic
Events
Events
Events
Plugins
Plugins
Plugins
Powered by Claude
Powered by Claude
Powered by Claude
Service partners
Service partners
Service partners
Tutorials
Tutorials
Tutorials
Use cases
Use cases
Use cases
Company
Anthropic
Anthropic
Anthropic
Careers
Careers
Careers
Policy
Policy
Policy
Economic Futures
Economic Futures
Economic Futures
Research
Research
Research
News
News
News
Policy on the AI Exponential
Policy on the AI Exponential
Policy on the AI Exponential
Responsible Scaling Policy
Responsible Scaling Policy
Responsible Scaling Policy
Security and compliance
Security and compliance
Security and compliance
Transparency
Transparency
Transparency
Programs
Startups
Startups
Startups
Research Labs
Research Labs
Research Labs
Help and security
Availability
Availability
Availability
Status
Status
Status
Support center
Support center
Support center
Terms and policies
Privacy choices
Cookie settings
We use cookies to deliver and improve our services, analyze site usage, and if you agree, to customize or personalize your experience and market our services to you. You can read our Cookie Policy
here
.
Customize
cookie settings
Reject
all cookies
Accept
all cookies
Necessary
Enables security and basic functionality.
Required
Analytics
Enables tracking of site performance.
Off
Marketing
Enables ads personalization and tracking.
Off
Save preferences
Privacy policy
Privacy policy
Privacy policy
Responsible disclosure policy
Responsible disclosure policy
Responsible disclosure policy
Terms of service: Commercial
Terms of service: Commercial
Terms of service: Commercial
Terms of service: Consumer
Terms of service: Consumer
Terms of service: Consumer
Usage policy
Usage policy
Usage policy
x.com
x.com
LinkedIn
LinkedIn
YouTube
YouTube
Instagram
Instagram
English (US)
English (US)
日本語 (Japan)
Deutsch (Germany)
Français (France)
한국어 (South Korea)
Italian (Italy)
Financial services
