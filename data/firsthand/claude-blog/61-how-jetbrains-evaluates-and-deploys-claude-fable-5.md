---
type: Article
title: Securing the frontier: How JetBrains evaluates and deploys Claude Fable 5
source: claude-blog
resource: https://claude.com/blog/how-jetbrains-evaluates-and-deploys-claude-fable-5
published: 2026-08-13
tags: [Claude Fable 5, JetBrains, 模型评估, AI编程]
detected: 2026-08-17T07:39:55+08:00
---

JetBrains CTO Vladislav Tankov 分享评估与部署 Claude Fable 5 的经验：基于私有仓库和真实任务评测，模型在 Python 任务通过率上较 Opus 4.8 大幅提升（44.3% vs 28.2%），且步骤更少、更高效。Fable 5 适合复杂推理和长时 agentic 编码，虽单 token 更贵但单位任务成本更低。

## Full Text

Securing the frontier: How JetBrains evaluates and deploys Claude Fable 5 | Claude by Anthropic
Meet Claude
Products
Claude
Claude Code
Claude Cowork
@Claude
Features
Claude in Chrome
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
Claude in Chrome
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
Securing the frontier: How JetBrains evaluates and deploys Claude Fable 5
Explore here
Ask questions about this page
Copy as markdown
Securing the frontier: How JetBrains evaluates and deploys Claude Fable 5
JetBrains Agent Systems CTO Vladislav Tankov on how the company evaluates frontier models against its private repositories, when his team reaches for Claude Fable 5, and why he treats safeguards and data retention as central to working with them.
‍
Category
Enterprise AI
Product
No items found.
Date
August 13, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/how-jetbrains-evaluates-and-deploys-claude-fable-5
JetBrains builds the tools developers use worldwide, from IntelliJ IDEA and PyCharm to the Kotlin programming language, serving more than 12.5 million active users and 88 of the Fortune Global 100. Vladislav Tankov, CTO at JetBrains, spoke with Anthropic about how his team evaluates new models, decides when to use Claude Fable 5, and thinks about data retention and safeguards when working with frontier models.
How has frontier AI changed for JetBrains in 2026?
I've been with JetBrains for 10 years, and we were among the very first customers of LLM providers. Over the last year, we moved from having AI skeptics among our customers and inside the company to seeing that AI is here to stay. It's a big and foundational change in the technology industry. Literally every skeptic in the company has changed.
How do you evaluate new models and decide when to use them?
We're a coding company, so we have a big evaluation pipeline: large eval sets on private repositories, including our monorepo. We take a close look at whether a model lives up to its benchmark scores on real work—some models are tuned to score well on public benchmarks but fall down on actual tasks. With a private repository, that's a lot easier to check. We also keep leaderboards for best quality, best cost per task, and fastest model. While Claude Fable 5 is more expensive per token, its cost per task is lower in some cases, particularly for more complicated, long-running work.
How did Claude Fable 5 score on your evals relative to previous models?
Claude Fable 5 is both more accurate and more efficient than prior models. It posted the best Python pass rate in our suite at 44.3%, against 28.2% for Opus 4.8, a 16-point jump. In a head-to-head comparison, Claude Fable 5 solved 18 Python tasks that Opus 4.8 missed and lost only 2. Its answers are also more trustworthy: when its code ran, it passed our tests far more often than either Opus model. That matters because code that runs but produces wrong answers is the most expensive kind of failure to catch.
The efficiency story is just as interesting. Claude Fable 5 needed about 22% fewer steps than Opus 4.8 to reach a solution, so it gets to working code with less trial and error. It also spends its effort in the right places. On Java tasks, Opus 4.8 repeatedly tried to pull in outside resources that almost never help in our environment, while Claude Fable 5 skipped that entirely and worked with the code in front of it. It shows better engineering habits more generally.
When do you use Claude Fable 5 over other models?
Opus is seen as a workhorse: you can be very sure it will do the work. You go to Claude Fable 5 when you really need good reasoning, when you almost need a partner, and you're not sure yourself how to do the thing. For example, one of our tech leads decided to implement a rich text editor component we had attempted a few times over the years, and Claude Fable 5 almost one-shotted it.
Another popular Claude Fable 5 use case is long-running agentic-coding experimentation. We provide an agent running Claude Fable 5 with specifications (in the form of text and images) and make it implement sophisticated IDE-like apps. The interesting thing here is that specifications can also be generated by the agent, based on the existing app. Joining these two components allows us to rewrite the app from one runtime, framework, or language to another in a nearly black-box setup.
How are you thinking about safety and data retention with today's frontier models?
We're not a company trying to create the safest model ourselves. We expect that the red teaming and everything else done on Anthropic's side is enough to believe the model is safe. Then we take a systematic approach to deployment, where we can guarantee safety: creating the infrastructure and the safety net around the model and the harness, rather than tweaking the model itself.
Security is also one of our biggest Claude Fable 5 uses. We run white-box testing against our own products to find vulnerabilities, and our security team is preparing for the fact that not only are we running the model—people outside the company will be running Claude Fable 5, or similar-class models, to probe for vulnerabilities across all of our products. Since we serve large enterprises in regulated industries, it's important for us to be prepared. Claude Fable 5 supports our work rather than blocking.
So it's a tight balance: the less aggressive the classifier is on your side, the more vulnerabilities someone will find in our products—including ones nobody knew about.
And it's no secret: we'd prefer zero data retention. But I don't see any other way for you to understand what was asked and where a classifier may have worked incorrectly. As long as reviews are only to investigate the most serious cases flagged , I'm okay with it. I think it's a fair tradeoff for access to frontier intelligence that allows my team to do their best work.
What's next on JetBrains's AI roadmap?
We expect the underlying models built by the LLM providers to keep getting more capable. What matters now is a kind of cockpit for software development: a space in which agents and people collaborate, and where people can manage the development process.
For JetBrains, it’s a big transformation. We see an opportunity to build the next generation of products across the agentic software development lifecycle that powers that cockpit. Developers will get more and better code shipped with agents, non-technical roles will have a larger role in software creation, and organisations will get the governance and clarity on the return on investment they need.
Get started with
Claude Fable
.
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
Aug 14, 2026
Maximizing the value of your Claude Code sessions
Claude Code
Maximizing the value of your Claude Code sessions
Maximizing the value of your Claude Code sessions
Maximizing the value of your Claude Code sessions
Maximizing the value of your Claude Code sessions
Oct 30, 2025
How Brex improves code quality and productivity with Claude Code
Enterprise AI
How Brex improves code quality and productivity with Claude Code
How Brex improves code quality and productivity with Claude Code
How Brex improves code quality and productivity with Claude Code
How Brex improves code quality and productivity with Claude Code
Jan 26, 2026
How Anthropic's Growth Marketing team cut ad creation time from 30 minutes to 30 seconds with Claude Code
Enterprise AI
How Anthropic's Growth Marketing team cut ad creation time from 30 minutes to 30 seconds with Claude Code
How Anthropic's Growth Marketing team cut ad creation time from 30 minutes to 30 seconds with Claude Code
How Anthropic's Growth Marketing team cut ad creation time from 30 minutes to 30 seconds with Claude Code
How Anthropic's Growth Marketing team cut ad creation time from 30 minutes to 30 seconds with Claude Code
Jul 24, 2025
How Anthropic teams use Claude Code
Enterprise AI
How Anthropic teams use Claude Code
How Anthropic teams use Claude Code
How Anthropic teams use Claude Code
How Anthropic teams use Claude Code
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
Claude in Chrome
Claude in Chrome
Claude in Chrome
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
Italiano (Italy)
