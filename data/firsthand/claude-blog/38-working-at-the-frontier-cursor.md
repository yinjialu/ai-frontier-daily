---
type: Article
title: Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
source: claude-blog
resource: https://claude.com/blog/working-at-the-frontier-cursor
published: 2026-07-17
tags: [Claude Fable 5, CursorBench, AI编码代理, 模型评估]
detected: 2026-07-18T07:31:58+08:00
---

Cursor工程师Nate Schmidt通过自建基准CursorBench评估Claude Fable 5，发现其在模糊、需理解全局的工程任务中达72.9%准确率，且能自主推理，减少人工引导，标志着AI编码代理能力的重大突破。

## Full Text

How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems | Claude by Anthropic
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
Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
Explore here
Ask questions about this page
Copy as markdown
Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems
Nate Schmidt's job at Cursor is to evaluate frontier models against their ability to tackle long-running, real-world engineering problems. Here’s why–and how–Claude Fable 5 changed the calculus on what coding agents are capable of.
Category
Enterprise AI
Product
Claude Platform
Date
July 17, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/working-at-the-frontier-cursor
Cursor is an AI coding agent for building professional software. It supports every major frontier model alongside Cursor's own, which makes the company an unusually neutral judge of how each one actually performs.
Nate Schmidt is the engineer who maintains that scorecard. He works on evals and model behavior at Cursor: studying how models succeed, how they fail, and what makes a developer quietly switch away from one mid-task. When colleagues and customers want a read on a new release, they come to him.
Over time, Schmidt's team noticed that public benchmark scores and real developer reception to these models had stopped lining up, so they built their own: CursorBench.
CursorBench was built to capture the messy, underspecified ways engineers actually prompt their models. One eval task is just a stack trace pasted in with the single word "fix," and the model has to infer the intent, find the root cause, and validate the change on its own. Another tells the model the wrong module is broken, to see whether it challenges the user's assumption or follows it into a dead end.
When Claude Fable 5 ran the eval, the model achieved 72.9% at Max effort, setting a new high, and capturing what agentic coding tools were capable of when paired with the right models.
Claude Fable 5 achieved achieved 72.9% at Max effort, setting a new high.
But when Schmidt was using the model on his own engineering workflows and personal tests, he'd stopped having to repeat his goals. The constant babysitting—reminding the model of context, spelling out the solution, auditing the results—wasn't necessary anymore. He could hand over a problem, from the gnarly refactor he was putting off to reasoning about nuanced edge cases, and Claude Fable 5 could solve it.
"I don't feel like I have to bootstrap Claude Fable 5 to understand the world I exist in and the problem I'm trying to solve," Schmidt says. "The model just has a sense of it out-of-the-box."
Reasoning about the entire mission
When Schmidt's team runs a new model through CursorBench, the right answer is table stakes. What they're scoring is whether the model understood what it was being asked.
"Many evals look like this: here's a well-defined problem, here are the constraints, go fix it. But the prompts we get from real users don't really look like that," Schmidt says. "The model has to infer that the user has a problem and what they're trying to convey, identify the root cause, fix it, validate the fix, and report back."
Claude Fable 5 scored so well on these ambiguous tasks, the Cursor team started to feel suspicious.
"One of two things is happening: either the model's very smart, or the model is cheating," he says. So the team looked into the traces, reading the model's actual reasoning on the hardest tasks, the ones where the prompt looks simple but cracking it requires understanding the whole system.
"We just kept seeing the model dig out wins that no other model was doing previously," he says. It was also getting there with fewer operations: token-efficient relative to the work it completed.
Then Schmidt put Claude Fable 5 on one of his favorite personal tests: landing on the moon.
A few weeks earlier he'd wired Claude Opus into a programmable space-flight simulator with a one-line prompt—build a rocket and land it on the moon—and let it run on a second monitor for twelve to sixteen hours. The model would launch, run out of fuel in orbit, add a lot more fuel, then fail to clear the atmosphere because the rocket was now too heavy.
He re-ran the experiment with the same blank-slate prompt, this time using Claude Fable 5. A few minutes in, the rocket went up, parked in low orbit, and came back down. Same failure as before. Then Schmidt read the transcript.
"Fable decided it wouldn’t go to the moon on its first attempt. It wanted to do an initial mission just to go into orbit and collect telemetry, then use that to inform the next trip." A few attempts later, the engine noise on his second monitor stopped. There was a lander on the moon. The whole run took a couple of hours, against Opus's twelve-plus with no result.
"With Opus, it was doing local reasoning—thinking about what just happened and what's immediately about to happen," Schmidt says. "With Fable it's global reasoning. It's thinking about the entire mission."
Cursor runs all models through CursorBench, their internal benchmark for evaluating models on tasks that simulate real developer work.
When to reach for the global optimum
Schmidt has settled on a simple rule for when to use Claude Fable 5 over cheaper, less intelligent models.
"If you have a good sense of what the path from A to B looks like, you might not need Fable. If you're at A and you have no idea where B is, Fable is an excellent choice,” he says. "When I want to build something the right way, Fable is the first model I think of."
Claude Fable 5 has also allowed his team to focus on projects the team had previously shelved—rewrites everyone agreed would be better but nobody could justify spending weeks on—because the model can carry enough of the skeleton. "It lowers the activation energy to work on these types of tasks," Schmidt says. "It lets us move in search of a global optimum rather than a local one."
It also changes how the team coordinates. Cursor runs lean, with intense individual ownership and few standups. Now, before touching shared code, Schmidt has an agent read his teammate's recent commits and flag conflicts, so neither of them has to stop what they’re doing to check in.
To balance cost and performance, his team pairs Claude Fable 5 with faster, lighter models for routine work and brings it in for the problems where capability is the constraint. In that configuration, he says, the combination is the most effective setup they've run.
“If I'm getting into a really gnarly problem–the p99 of problems–the thing I'm trying to optimize for is time to solution,” he says. “And I think Fable is the best model for solving our hardest problems.”
Nate Schmidt tests new models across various evaluations, including putting it through the paces in a space-flight simulator.
What's next
Despite putting the model through its paces on CursorBench and sending it to the moon, Schmidt is still looking for Claude Fable 5’s limits. Next, he wants to see how long the model can manage a back-end system unattended; days-to-weeks runs are his next experiment. Inside Cursor, the team is using the model to hunt performance bottlenecks and user pain points proactively rather than waiting for reports, and to build the more sophisticated, closer-to-reality eval environments that will measure whatever comes next.
"There's a class of problems people weren't even thinking about because it didn't seem approachable," he says. "With Fable, I'm excited to push at that."
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
Jul 15, 2026
Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
Enterprise AI
Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
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
Claude Platform
