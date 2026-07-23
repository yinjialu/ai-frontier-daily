---
type: Article
title: Working at the frontier: How Rakuten builds agents overnight with Claude Fable 5
source: claude-blog
resource: https://claude.com/blog/working-at-the-frontier-rakuten
published: 2026-07-20
tags: [Claude Fable 5, AI代理, 企业AI, Rakuten]
detected: 2026-07-21T09:08:30+08:00
---

Rakuten使用Claude Fable 5构建可通宵运行的自主AI代理，覆盖多部门，速度提升10倍。新模型能长时间独立工作并自我校验，减少人工干预，推动企业AI自动化升级。

## Full Text

How Rakuten builds agents overnight with Claude Fable 5 | Claude by Anthropic
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
Working at the frontier: How Rakuten builds agents overnight with Claude Fable 5
Explore here
Ask questions about this page
Copy as markdown
Working at the frontier: How Rakuten builds agents overnight with Claude Fable 5
Yusuke Kaji, General Manager of AI for Business at Rakuten, has been testing Claude models since Sep 2024. Here’s why he thinks Claude Fable 5 is a step change for long-running enterprise agents.
Category
Enterprise AI
Product
Claude Code
Claude Cowork
Claude Platform
Date
July 20, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/working-at-the-frontier-rakuten
As General Manager of AI for Business at Rakuten, Yusuke Kaji’s job is to “find the seeds of transformative innovation and scale them across the company.”
One of those seeds was Claude.
Since March 2025, Rakuten has used Claude to speed up software development with Claude Code, stand up agents across its business functions, and power AI features for millions of customers. According to Kaji, Rakuten chose to partner with Anthropic for its enterprise focus, leadership, and product taste.
Across nearly a dozen model launches, he's watched the work he can hand to an agent keep growing: first using Claude Code to
ship production software
, then building custom
Claude Managed Agents
for teams across the company. He likens testing out new models with embarking on a “new quest.”
“The way a good leader prepares stretch goals for their people, we prepare stretch tasks for a new Claude,” he adds. “Maybe Claude is nudging us to stretch, too."
When he tested Claude Fable 5, he knew something felt different. The model could run on its own for far longer than its predecessors, and for the first time, checking its own work and completing nuanced tasks overnight while Kaji slept.
That extra autonomy is what lets Rakuten hand its agents bigger, longer-running jobs, and transform the way they work.
Building an AI-native workforce
Rakuten is remaking itself around AI, a project it calls AI-nization – their company-wide effort to infuse AI into everything we do for customers, business partners, and employees.. When Claude Managed Agents arrived, Rakuten deployed agents across product, sales, marketing, and finance inside a week, plugged into Slack, Microsoft Teams, and the company's own task system.
For Kaji and his team, the constraint about building agents used to be who could write code; now, it's who understands the business problem.
"The modern corporation is designed to minimize the cost of communication," he says. "I believe agents like Claude Code can shine when we work with them to minimize the cost of new innovation as well, like a quick transition from idea to production." Give a capable person agents that hold context and taste, and "it allows the hidden talent to unlock their potential and scale their potential 100 times more."
But running agents in every function around the clock surfaces a new constraint: human judgment. While Rakuten's agents close issues roughly 10x faster across every domain, the number of tasks the organization takes on keeps rising. Adding more agents doesn't add judgment. So the faster the agents run, the more the organization's progress depends on a person closing the loop.
Powering agents that run for hours, unattended
For most builders, the hardest part of building long-running agents is setting them up to succeed with minimal oversight. Connecting it to the right tools and context is one thing, but in Kaji’s experience, there were always limits to how long an agent could go without needing a human in the loop to validate its work.
Before Claude Fable 5, setting an agent loose on a multi-hour task without human oversight was always a gamble. "If they choose the right path in the first step, everything is fine," Kaji says. "But if they choose the wrong direction in the first pass, the agent spends significant time to fix the path, or even fails to reach the destination." On a job meant to run five hours or a full day, one early wrong assumption could burn the entire run, and the only way to catch it was a person checking in.
The failure mode was a lack of self-verification. Any model can take a wrong first step. The problem with earlier models was that they didn't check their own work as they went, so an early wrong turn went unnoticed. It compounded over the run and produced a suboptimal result hours later.
According to Kaji, Claude Fable 5 changes the calculus for days-long agentic runs because it checks its own work as it goes, far more often than any prior model.
"We tested Fable, and we love its capability for self-reflection and self-verification," Kaji says. "Compared with previous models, it understands its mistake before I point it out at 2 a.m. or 3 a.m.—so that I can sleep."
What sets Claude Fable 5 apart
Kaji’s team cite three behaviors that distinguish Claude Fable 5 from its predecessors, and signal a step-change in frontier intelligence:
It re-checks its own assumptions.
When the state of the task changes midway, Fable 5 notices and corrects a wrong assumption before acting on it, rather than committing to a bad path and discovering it hours later.
It returns to first principles at each step.
It re-validates against the original intent without being told, the course-correction Kaji used to have to make himself when a run started down the wrong path..
It matches the team's taste.
Even with minimal guidance, its judgment on ambiguous calls lines up with theirs. Kaji has a name for this, a term he coined: taste alignment. "Taste alignment is smoother with Fable than any previous model from your company, or any other model we’ve used."
Most importantly, longer autonomy changes the unit of work Kaji can delegate.
“Before Fable, we had to break work into well-defined chunks for the agent to execute," he says. Now he can hand over a whole task and run several at once.
Claude Fable 5 changes what happens in between. It reflects at each step, catches a bad early assumption, and finds its own way back to first principles — re-navigating to the right outcome without anyone steering it. Because the model self-corrects mid-run, sign-off becomes feasible for the first time, and the unit of work Kaji delegates shifts from the task to the decision. The agents also carry memory between runs: "Our agents with memory remember what went wrong in past sessions and avoid repeating those mistakes."
As a result, the absolute number of tasks keeps climbing, but the ones that truly need a human stay at a focusable level. Not having to jump in and steer mid-run is, he says, is the biggest productivity win of all—it lets his team spend its time on the decisions only people should make, and keeps an AI-native organization accelerating instead of stalling on human course-correction.
Balancing cost and efficiency
Frontier capability comes at a frontier price, and Kaji is direct that cost decides how widely he can deploy.
"As a large enterprise, we want to balance intelligence and cost," he says. His team measures task completion ratio alongside cost per task, then sends Fable 5 the work where the extra capability changes the outcome and lets smaller models keep the rest.
For Kaji, two things make the math work in Fable 5's favor: it gets more done with fewer tokens and fewer wrong turns, and it needs less hand-holding.
What’s next
The frontier Kaji is testing now isn't individual speed. It's getting agents to coordinate people. Claude Code has sped up his own work and his colleagues', but the hard part of any organization is the alignment between people, matching one person's context and taste to another's. He's exploring agents that "coordinate or organize, more like a manager," holding the nuance that usually gets lost between team members.
"We do not see AI agents as future colleagues or competitors. They are systems around us." And he holds Anthropic to its own advice, that you should build for the model coming in three or six months rather than the one in front of you.
"I think we as a society still haven't found the model–task fit yet for Claude Fable 5," he says, "but it already stands out as a model that crossed the line and came over to our world.
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
Jul 17, 2026
Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
Enterprise AI
Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
Jul 17, 2026
Zero risk isn't the job: a CISO's guide to agentic AI
Enterprise AI
Zero risk isn't the job: a CISO's guide to agentic AI
Zero risk isn't the job: a CISO's guide to agentic AI
Zero risk isn't the job: a CISO's guide to agentic AI
Zero risk isn't the job: a CISO's guide to agentic AI
Jul 16, 2026
How Anthropic runs large-scale code migrations with Claude Code
Claude Code
How Anthropic runs large-scale code migrations with Claude Code
How Anthropic runs large-scale code migrations with Claude Code
How Anthropic runs large-scale code migrations with Claude Code
How Anthropic runs large-scale code migrations with Claude Code
Jul 16, 2026
Working with Claude Fable 5 in Claude Cowork
Enterprise AI
Working with Claude Fable 5 in Claude Cowork
Working with Claude Fable 5 in Claude Cowork
Working with Claude Fable 5 in Claude Cowork
Working with Claude Fable 5 in Claude Cowork
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
Claude Code
Claude Cowork
Claude Platform
Coding
Agents
