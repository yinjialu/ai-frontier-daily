---
type: Article
title: Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders
source: claude-blog
resource: https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders
published: 2026-08-21
tags: [Claude Mythos 5, 网络安全, AI安全, 开源安全]
detected: 2026-08-23T17:00:52+08:00
---

Anthropic宣布将Claude Mythos 5集成至Claude Security及合作伙伴防御工具，推出3500万美元基金资助开源安全，并扩展网络验证计划以安全分发强模型防御能力。

## Full Text

Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders | Claude by Anthropic
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
Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders
Explore here
Ask questions about this page
Copy as markdown
Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders
Category
Product announcements
Product
No items found.
Date
August 21, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders
We're sharing an update on our efforts to help more teams use frontier capabilities for cyber defense.
Claude Mythos 5
is now available in
Claude Security
, and coming soon to partners' cyber defense tools. We're also launching a $35M fund to help secure open-source software and sharing plans to expand our
Cyber Verification Program
.
In April, we launched
Project Glasswing
to put our most capable frontier model, Claude Mythos Preview (and its successor, Claude Mythos 5), in the hands of a small group of organizations securing the world’s most critical software. This gave defenders a window of time to find and fix vulnerabilities ahead of models with similar capabilities becoming generally available or reaching malicious actors.
Our goal has always been to expand Mythos-level defense to as many defenders as we safely can. To do that, we've been working on
safety classifiers
and safeguards that let us expand access to Mythos-class models without putting their offensive cyber capabilities in the wrong hands.
Claude Fable 5
was the first step: it made the model broadly available while blocking dual-use cyber work.
Today, we’re taking the next steps. The riskiest behavior occurs when a user has direct access to a model, where a malicious actor can try to steer it toward harmful uses. But if users can only receive specific outputs, such as a patch for a vulnerability or a security alert, that risk is much lower. The changes we’re announcing give users greater access to the defensive results, while maintaining appropriate guardrails around direct access to the model:
Claude Mythos 5 integration into the tools defenders rely on.
We’re working with our cybersecurity technology and services partners to integrate Claude Mythos 5 into the products and services defenders already use to secure their software.
Claude Security scans can now run on Claude Mythos 5.
Customers on Claude Enterprise plans can now run our most capable model in Claude Security, using it to scan their codebases for security vulnerabilities and suggest patches.
$35 million in credits for open-source security.
Our new Defender Advantage Fund (0xDAF) will provide $35 million in credits to organizations working to patch vulnerabilities in open-source projects, automate parts of the process of scanning and patching open-source software, and experiment with new security approaches.
Expanding our Cyber Verification Program.
The program already gives vetted defenders reduced safeguards on Opus and Sonnet models. In the coming weeks, we will expand this program to include broader dual-use capabilities on Opus and Sonnet, with Mythos-class access to follow.
Our aim remains to help organizations adapt to the pace and demands of cybersecurity as AI models become increasingly powerful. We will continue to develop safeguards, access programs, and community support to make our most capable models safely available to a wide range of people and organizations.
Integrating Mythos into existing cyberdefensive tools
The teams defending hospitals, utilities, financial systems, and the software supply chain already rely on a suite of products and services for security operations, incident response, threat intelligence, and detection engineering. The fastest way to make frontier capabilities available to those defenders is to integrate Mythos-class models into the tools they already run.
Many of our partners have already
built cyber products on Claude Opus
that help security teams triage alerts, identify threats, and remediate vulnerabilities faster. We’re now working with these partners and more to build Claude Mythos 5 into their products and services, so they can deliver Mythos-level defensive outcomes to their customers.
When an end user uses one of these products, they’re not interacting with Mythos directly. Instead, they work through a purpose-built interface that runs Mythos in the background for a defined task and only receive the specific artifact the product is intended to provide. For example, a tool to remediate vulnerabilities might provide a list of suggested patches as its output. This output would be generated by Mythos, but the user would not have a way to prompt the model to, say, develop an exploit for a vulnerability. We and our partners also have abuse prevention measures in place to verify the model stays within its intended scope.
We're early in this work and expect it to expand over time. If you build security products or services and want to bring Claude Mythos 5 to your customers, you can
register your interest here
.
Making Claude Security available with Claude Mythos 5 for Enterprise customers
Starting today,
Claude Security
scans now run on Claude Mythos 5. Claude Security scans codebases for vulnerabilities and suggests patches for human review; it’s currently in public beta for Claude Enterprise customers, and scans with Mythos 5 are billed as standard token usage under your existing plan, with no separate add-on.
Enterprise admins can enable Claude Security in the
admin console
. From
claude.ai/security
, users can select a repository to scan using Claude Mythos 5. Claude then scans the codebase for vulnerabilities, and returns each finding with a
CWE
(Common Weakness Enumeration) category, confidence and severity ratings, and a suggested fix.
Users can then open Claude Code on the web to implement the fix. Interactive patching uses the models your organization has access to in Claude Code. The Mythos scan itself does not extend Mythos access to other surfaces. Every patch must be reviewed and approved by a human before it can be implemented.
Claude Security uses Mythos 5 to scan code you own, and returns detailed findings rather than raw outputs without exposing the model itself. This means defenders can access the capabilities of Claude Mythos 5 without the model becoming accessible to those who might misuse it.
For more about Claude Security, see our
guide to getting started
.
Launching the Defender Advantage Fund to secure open-source software
Some of the world’s most widely used programs run on open-source software. Yet these projects are often maintained by volunteers or nonprofit foundations, who may lack the resources or personnel to comprehensively defend their projects against attack. Through Project Glasswing, we made $4M in direct donations to open-source security organizations, provided credits to the open-source security foundations in the program, helped scan and patch widely used projects, and support coordinated vulnerability-fixing efforts like
Akrites
and
Gold Eagle
.
Our new Defender Advantage Fund (0xDAF) builds on that work with $35 million in Claude credits for organizations helping open-source maintainers secure their software. Grants will focus on three areas: patching live vulnerabilities in widely used projects, automating scanning and patching in ways other projects can replicate, and helping projects pursue more ambitious security approaches that make them resistant to whole classes of attack.
We're starting with a small number of larger, pilot grants to learn what works and scales best. We will share details on initial recipients in the coming weeks.
Expanding our Cyber Verification Program
To date, our Cyber Verification Program has provided organizations with access to dual-use capabilities when using Claude Opus and Sonnet models. Organizations in the program experience reduced safeguards, minimizing interruptions for accepted teams doing legitimate cybersecurity work on systems they’re authorized to protect.
Over the coming weeks, we are evolving the program to expand safeguarded access to Claude Mythos. As part of this, access to defensive capabilities like vulnerability triaging and validation will expand to Mythos-class models, and cyber defenders will see reduced blocks on Claude Opus and Sonnet-class models. Additionally, we are continuing to expand access to Claude Mythos through Project Glasswing in collaboration with our partners in the U.S. Government, focused on protectors of critically important infrastructure that meet strict security control requirements.
We'll share more details about the Cyber Verification Program expansion in the coming weeks. In the meantime, we encourage all security teams performing legitimate cybersecurity work to apply for the program for reduced safeguards on Claude Opus and Sonnet models. If you are already enrolled and accepted, no action is needed; we’ll reach out with updates.
What’s next
These initiatives are a continuation of our efforts to make the defensive capabilities of frontier models available to more people and organizations, and to support the open-source community in hardening their projects against attack. We will continue to work with government partners, organizations, open-source maintainers, and the broader industry to build the resilient cyber infrastructure today’s highly capable AI models demand.
Apply for the
Cyber Verification Program
.
Register your interest
in building cyber products and offerings with Mythos.
Claude Security is available in public beta for Enterprise customers. Admins can enable Claude Security in the
admin console
. For a full walkthrough, see our
guide to getting started
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
Aug 13, 2026
Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions
Agents
Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions
Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions
Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions
Self-service data analytics in Slack: how Anthropic deploys Claude Tag for ad-hoc questions
Aug 20, 2026
Build production agents with computer use, the Skills API, and the Files API
Product announcements
Build production agents with computer use, the Skills API, and the Files API
Build production agents with computer use, the Skills API, and the Files API
Build production agents with computer use, the Skills API, and the Files API
Build production agents with computer use, the Skills API, and the Files API
Aug 20, 2026
Anthropic’s approach to teaching and learning AI
Product announcements
Anthropic’s approach to teaching and learning AI
Anthropic’s approach to teaching and learning AI
Anthropic’s approach to teaching and learning AI
Anthropic’s approach to teaching and learning AI
May 19, 2026
New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels
Product announcements
New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels
New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels
New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels
New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels
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
Report abuse
Report abuse
Report abuse
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
