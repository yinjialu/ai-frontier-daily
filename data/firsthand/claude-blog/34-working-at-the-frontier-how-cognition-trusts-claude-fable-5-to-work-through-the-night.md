---
type: Article
title: Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
source: claude-blog
resource: https://claude.com/blog/working-at-the-frontier-how-cognition-trusts-claude-fable-5-to-work-through-the-night
published: 2026-07-10
tags: [Claude Fable 5, 自主AI编码, Cognition Devin, AI代理]
detected: 2026-07-11T06:22:56+08:00
---

Cognition在Devin中使用Claude Fable 5，首次信任其通宵自主编程。Fable 5在Frontier Code基准上得分约30%（上一代仅10%），并可连续工作8小时，显著提升代码质量和自主性。

## Full Text

Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night | Claude by Anthropic
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
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Explore here
Ask questions about this page
Copy as markdown
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Silas Alberti, SVP of Research at Cognition, has tested nearly every Claude model inside Devin, the company's AI software engineer. Claude Fable 5 is the first he'd trust to leave running overnight.
Category
Enterprise AI
Product
No items found.
Date
July 10, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/working-at-the-frontier-how-cognition-trusts-claude-fable-5-to-work-through-the-night
Cognition is young, even by Silicon Valley standards. It built Devin, its autonomous AI software engineer, in early 2024, at a time when the basic mechanics of an agent barely held together.
Devin takes on the work engineers never quite get to: codebase migrations, the backlog of bugs, the features that keep slipping. With customers ranging from high-growth startups to Fortune 500 companies, the bar is high. Code written by Devin has to be reliable and production-ready; a small bug introduced quietly can cause real problems downstream.
Alberti’s team trains and tests the models behind Devin and has run nearly every Claude generation since the start. He traces the first real jump to Claude 3.6 Sonnet in late 2024. It was the first model that could reliably chain tools and hold a multi-step task. When the team plugged it into Devin, internal usage tripled.
That history is what makes him hard to impress. Cognition has watched models ace a benchmark and then fall apart the moment its engineers tried to use them. "We've been burned like this a bunch of times," Alberti says. So the team trusts its own engineers over any score. Its highest-taste developers put each new model through a real day of work, and the bar is whether the code is something they’d actually keep.
As Alberti puts it, "we trust no eval."
Where earlier models hit their limit
For all that progress, one ceiling remained: how long an agent could run before it lost the thread?
"Before Fable, you could delegate agents that could stay on-task for a couple of minutes, maybe an hour," Alberti says. After that, sessions drifted. Give an earlier model five ideas to weigh at once, and it would lose track and get confused. On one database migration, a prior Opus model technically finished the job but introduced a series of subtle bugs along the way.
Incident triage showed the same shape. Earlier models tended to stay at the surface of the logs instead of digging for the relevant line, and they were trained to give an answer no matter what—so they'd "confidently claim the first plausible thing they discover and then stop." Engineers learned to tune them out.
Cognition evaluates frontier models against a series of benchmarks, including Frontier Code.
Claude Fable 5 clears Cognition's own bar
Cognition grades models on Frontier Code, a benchmark it built because existing ones kept rewarding code that passed tests but wouldn't survive a real codebase. Alberti calls it an "anti-slop" standard. On its hardest subset, the prior Opus model scored around 10%. Claude Fable 5 scored about 30%.
The team's first reaction was suspicion. "Is there a bug? This can't be true." Usually a benchmark jump comes with engineers arguing for weeks over whether the model is actually better in practice. This time the dogfooding agreed with the numbers. "It was kind of a shocker, honestly," Alberti says.
"The biggest thing we noticed was the horizon, how long it can be self-sufficient," he says. "There have been tasks where I was about to go to bed and I was like, 'Okay, just please keep working on this and don't stop until I wake up.' And then I wake up, and it's been working for eight hours straight and actually making real progress. I hadn't seen that before."
The horizon held because Claude Fable 5 stayed clear-headed in messy context. It was the first model to properly use Cognition's internal debugging tools, paging through logs in the browser and drawing conclusions despite the noise. On a migration that had tripped up earlier models, it stated the invariants it would hold itself to, then executed against them. On triage, it pinned down the root cause and said what it didn't know, which Alberti says is what actually rebuilds trust.
He puts the jump in a small class of true step changes, the kind that come roughly once a year.
Silas and his team are building Devin, powered by models like Claude, to tackle more complex, longer running workloads.
What’s next
Cognition's founding bet was that agents should run in the cloud for hours at a time. For the company's first year, the models weren't there yet.
Alberti says Claude Fable 5 makes the full version of that bet viable, and some of it is already in the product. Devin can watch a Slack channel and jump into an issue without being tagged, or monitor production and triage a spike on its own. When it gets one of those right, he says, it feels "like a real engineer on the team."
He expects this to become the default for engineering teams. In a year or two, he says, 90% of agent sessions will be proactive ones that find a problem, scan the codebase, and message you with the fix.
"A lot of these things we've always wanted to build at the company are now possible," Alberti says.
Get started with
Claude Fable 5
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
Jul 8, 2026
How Anthropic's marketing operations team uses Claude Cowork to automate reporting and campaign builds
Enterprise AI
How Anthropic's marketing operations team uses Claude Cowork to automate reporting and campaign builds
How Anthropic's marketing operations team uses Claude Cowork to automate reporting and campaign builds
How Anthropic's marketing operations team uses Claude Cowork to automate reporting and campaign builds
How Anthropic's marketing operations team uses Claude Cowork to automate reporting and campaign builds
Jul 8, 2026
Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work
Enterprise AI
Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work
Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work
Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work
Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work
Jul 7, 2026
How people are using Claude Cowork
Enterprise AI
How people are using Claude Cowork
How people are using Claude Cowork
How people are using Claude Cowork
How people are using Claude Cowork
Jun 3, 2026
How Anthropic enables self-service data analytics with Claude
Enterprise AI
How Anthropic enables self-service data analytics with Claude
How Anthropic enables self-service data analytics with Claude
How Anthropic enables self-service data analytics with Claude
How Anthropic enables self-service data analytics with Claude
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
Coding
