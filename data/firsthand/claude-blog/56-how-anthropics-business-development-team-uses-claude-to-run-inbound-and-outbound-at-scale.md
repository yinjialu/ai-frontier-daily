---
type: Article
title: How Anthropic's business development team uses Claude to run inbound and outbound at scale
source: claude-blog
resource: https://claude.com/blog/how-anthropics-business-development-team-uses-claude-to-run-inbound-and-outbound-at-scale
published: 2026-08-07
tags: [Claude Cowork, 销售自动化, AI Agent, 业务拓展]
detected: 2026-08-11T07:51:41+08:00
---

Anthropic业务拓展团队用Claude Cowork构建技能和定时任务，自动扫描收件箱起草回复、研究潜在客户、处理CRM和日历，将BDR从重复工作中解放出来，专注于客户战略问题。

## Full Text

How Anthropic's business development team uses Claude to run inbound and outbound at scale | Claude by Anthropic
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
Enterprise
Startups
Departments
Cybersecurity
Legal
Industries
Customer support
Financial services
Government
Healthcare
Higher education
K-12 teachers
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
Enterprise
Startups
Departments
Cybersecurity
Legal
Industries
Customer support
Financial services
Government
Healthcare
Higher education
K-12 teachers
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
How Anthropic's business development team uses Claude to run inbound and outbound at scale
Explore here
Ask questions about this page
Copy as markdown
How Anthropic's business development team uses Claude to run inbound and outbound at scale
John Albert, a business development rep at Anthropic, shares how his team uses Claude to research account books, draft customer replies, and address the ad-hoc requests that used to queue behind data teams.
Category
Enterprise AI
Product
Claude Cowork
Date
August 7, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/how-anthropics-business-development-team-uses-claude-to-run-inbound-and-outbound-at-scale
Author(s)
John Albert
Early in my career in business development, account executives would hand me lists with hundreds of accounts and I’d have to investigate each company, find the right contacts, hunt down emails, and draft outreach. The inbound side had similarly manual and time-consuming workflows.
When I joined Anthropic last summer, I took over the responsibility of managing our sales inbox. I would spend around 5 hours per day manually responding to inbound interest from prospects, often answering the same or similar questions about our products, on top of managing my own book of business.
A lot of that work is now set up as skills and scheduled tasks in
Claude Cowork.
Personalized customer emails are prepared as drafts that I need to review and customize before sending. My outbound work begins with detailed research that I didn’t need to spend hours compiling.
As a result, my teammates and I spend less time on manual, repetitive work and more time on what matters: helping our customers.
Here’s how Claude Cowork is upleveling the business development function at Anthropic, allowing us to dedicate more time to strategic work, understanding customer problems, and helping educate them on how Claude can solve them.
Automating administrative and repeatable tasks
BDRs sit at the beginning of the sales process, qualifying inbound demand and building outbound pipeline for the business. At Anthropic, those motions now run through Claude Cowork first.
A foundational piece of our inbound setup is a document where I’ve collected the questions we most commonly receive in our sales inbox, along with our best answers to those questions. This document functions as our sales knowledge base, which Claude reads before drafting any replies we send. Claude helped me create that document (I simply pointed it to the relevant sources of information), and now continuously verifies that it is up to date by flagging information that might potentially be stale, which users can validate.
The heaviest workflow built on that document is an inbox skill that runs every hour: it scans a rep's inbox, finds every thread that the rep needs to answer, and drafts a reply for the rep to read, edit, and send. This skill is made of a thin system prompt, the knowledge base as context, and a profile of the rep’s writing style (which each of us also creates using a voice skill that reads through documents, messages, and emails we have written).
The inbox skill runs on a thin system prompt, the team's sales knowledge base as the source for product facts, and a customized voice profile for each rep.
The inbox skill scans a rep’s inbox and leaves drafted replies for review. All information in this preview has been anonymized for publication.
I also lean on two lighter skills that help with my administrative workload. Every BDR knows the pain of meeting no-shows and prospects going dark. To address this, I built a skill that watches Gmail and Google Calendar to notify me when that happens, so I can follow up quickly.
The other skill uses our CRM connector to scan for all new leads and draft a personalized first touch. It runs on a schedule throughout the day to ensure we don’t leave leads waiting.
We also have a skill that keeps Salesforce current by reading our internal guidance on opportunity stages and checking it against what's actually happening in Gmail and Gong. If we've met with a customer and moved on to pricing questions, the opportunity should probably progress a stage. Claude proposes each Salesforce update with the evidence behind it and waits for approval. When I edit or reject a proposal, it records the reason why so it doesn’t repeat the mistake.
The pipeline scanner skill proposes Salesforce updates for approval by the rep. Shown here with demo data and all information anonymized for publication.
Optimizing outbound and revenue work
On average, I work upwards of a hundred accounts at any given time. I’m able to cover all these accounts thanks to a skill that runs as a scheduled task overnight. It prospects across my entire book, observing the current state of each account; for example, who are we in touch with, how do they use Claude today, and what signals are relevant. To accomplish this, Claude connects to Salesforce, sales tools like Apollo and Common Room, Gong, and our data warehouse, performs deep research, and validates it against outbound guidance and ICP criteria that our team has curated.
These pieces of the skill add context to help Claude work more like a BDR at Anthropic. In the morning, I open up Claude Cowork to a brief, a score, and an outbound play for each account.
This workflow becomes increasingly useful over time as each BDR can provide feedback on Claude’s results, which then feeds back into the skill. The skill keeps a small memory file and ledger, preventing repetitive or duplicative work.
We use this research in follow-up conversations, so our outreach is tailored and when we talk to customers we're informed on their business and close enough to their problems to have a deeper strategic discussion.
Discovery calls are another part of our outbound motion we are working to improve with Claude. We use a skill that evaluates Gong transcripts against our discovery call playbook and builds a scorecard for each call, with specific feedback based on the conversation. The feedback includes top three things done well, top three areas to improve, an explicit pass or fail score on our criteria, and a single highest-leverage thing to practice next.
The call coach skill provides a scorecard for our discovery calls, along with specific recommendations on improving them. Shown here with demo data and all information anonymized for publication.
Streamlining one-off requests
Often, requests come to the BDR team in an ad-hoc manner and Claude makes it possible for us to partner with our AEs in a more strategic way. If an AE is curious about usage trends for a top account, we are a prompt away from providing a legible and descriptive dashboard that highlights the relevant trends.
A spend analysis report generated for target accounts.
Working with Claude on data analysis and reporting comes into play in outbound work, too. One of my favorite workflows is running an undiscovered usage prompt. It considers an AE’s full book and finds usage signals on the account level where we do not yet have a sales opportunity. Often, this is a great signal for us to begin reaching out and working together with a customer to optimize their usage and experience with Claude.
A product-focused sweep of one AE's book returns every account already using the product with no matching opportunity. Shown with demo data and all information anonymized or modified for publication.
We also use Claude for event outreach. One of my AEs recently flagged that we have an upcoming
Claude Code for Data Engineering
webinar and asked if I could find accounts in his book that would be interested in attending. I don’t have a skill for that, but for this type of request a prompt was enough. Claude checked usage data and CRM history across the book, scored each account against our ICP, and flagged the best fits with contacts worth inviting.
Asked to find the right accounts for a webinar invite, Claude sweeps the books and scores each account against the team's ideal customer profile.
Together, these skills, scheduled tasks, and the context we've curated turn Claude into an always-on business development partner.
Advice for business development teams on getting started with Claude Cowork
Below, are some tips for business development teams on getting started with Claude Cowork:
Build the knowledge base before the workflows.
Collect the questions your team answers repeatedly, and your best answers, into a single external-facing document. You don't have to write it by hand: point Claude at your relevant product docs and team channels and have it build the first version.
Give Claude examples of how your team works.
Claude drafts against the context you give it. For outbound, this can include examples of messages that worked and your ideal customer profile. Each rep can also have Claude learn their writing style, so drafts arrive sounding like the sender.
Keep a person on every send.
Claude can generate drafts, but we still read, edit, and send them.
Share skills across the team.
Our team keeps its most-used skills in a shared plugin, promoting a skill there once we establish that reps use it consistently in their daily work.
Make skills general enough to adapt to the whole team’s way of work.
Segments, books, and workflows differ across reps, so we keep shared skills general enough to adapt rather than scoped to one person's routine.
Write feedback back into the skills.
When you dismiss a hook or correct a draft, have Claude record the reason in the skill so it doesn’t make the same mistake again.
My best advice? Just start experimenting. The more context and tools you give it, the more you can get done.
Watch John demo these skills during our
Claude Cowork for Business Development Representatives
webinar.
Get started with
Claude Cowork
today.
All UI mockups in this article are depicted with synthetic data and do not represent real companies or individuals.
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
Aug 5, 2026
Inference hooks: inline data loss prevention for Claude Enterprise
Enterprise AI
Inference hooks: inline data loss prevention for Claude Enterprise
Inference hooks: inline data loss prevention for Claude Enterprise
Inference hooks: inline data loss prevention for Claude Enterprise
Inference hooks: inline data loss prevention for Claude Enterprise
Aug 6, 2026
Millennium and Anthropic are building a digital risk analyst with Claude
Enterprise AI
Millennium and Anthropic are building a digital risk analyst with Claude
Millennium and Anthropic are building a digital risk analyst with Claude
Millennium and Anthropic are building a digital risk analyst with Claude
Millennium and Anthropic are building a digital risk analyst with Claude
Aug 4, 2026
A guide to cost visibility and control in Claude
Enterprise AI
A guide to cost visibility and control in Claude
A guide to cost visibility and control in Claude
A guide to cost visibility and control in Claude
A guide to cost visibility and control in Claude
Jul 24, 2026
How the product designer who built Claude Design uses it to explore ideas before building them
Enterprise AI
How the product designer who built Claude Design uses it to explore ideas before building them
How the product designer who built Claude Design uses it to explore ideas before building them
How the product designer who built Claude Design uses it to explore ideas before building them
How the product designer who built Claude Design uses it to explore ideas before building them
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
Cybersecurity
Cybersecurity
Cybersecurity
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
Higher education
Higher education
Higher education
K-12 teachers
K-12 teachers
K-12 teachers
Legal
Legal
Legal
Life sciences
Life sciences
Life sciences
Nonprofits
Nonprofits
Nonprofits
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
Terms of Service: US K-12
Terms of Service: US K-12
Terms of Service: US K-12
Data Processing Agreement: US K-12
Data Processing Agreement: US K-12
Data Processing Agreement: US K-12
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
Claude Cowork
Sales
