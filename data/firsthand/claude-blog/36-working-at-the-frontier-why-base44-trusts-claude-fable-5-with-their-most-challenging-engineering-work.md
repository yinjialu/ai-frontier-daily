---
type: Article
title: Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
source: claude-blog
resource: https://claude.com/blog/working-at-the-frontier-why-base44-trusts-claude-fable-5-with-their-most-challenging-engineering-work
published: 2026-07-15
tags: [Claude Fable 5, Base44, vibe-coding, 工程效率]
detected: 2026-07-16T15:29:42+08:00
---

Base44团队发现Claude Fable 5是首个能像资深工程师一样推理的模型，成功将其用于重写系统提示等核心复杂任务，独立完成90%-95%工作，并发现评估中缓存测试缺失的盲点，大幅提升开发效率。

## Full Text

Working at the frontier: How Base44 trusts Claude Fable 5 with their most challenging engineering work | Claude by Anthropic
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
Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
Explore here
Ask questions about this page
Copy as markdown
Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
Yoav Orlev, Head of Product at Base44, joined the vibe coding platform as its first employee and has seen his team build on every Claude model since Sonnet 4. Here's why he thinks Claude Fable 5 is the first model that reasons about software the way a senior engineer would, and what that frees the rest of his team to build.
Category
Enterprise AI
Product
Claude Platform
Date
July 15, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/working-at-the-frontier-why-base44-trusts-claude-fable-5-with-their-most-challenging-engineering-work
Base44 is a vibe-coding platform that allows anyone, regardless of technical ability, to build full stack applications and websites. Its customers range from small businesses with no developers to companies using it to build full SaaS products.
Yoav Orlev, who joined Base44 as its first employee and now runs product, says one of the most satisfying parts of his work is seeing what small businesses can do with the platform for which they otherwise lacked the time, budget, or knowhow, whether that’s building a digital storefront or a shift-management application for restaurant staff. His team’s mission is to keep widening their product’s capabilities while keeping it usable for everyone.
The Base44 product and engineering teams have always moved quickly, especially when shipping small or medium-scope features. But any changes to the platform’s core that touch multiple interdependent parts could only be entrusted to the most senior engineers.
One such bottleneck was Base44's system prompt and its hundreds of permutations, which vary by whether someone is on their first app or their fifth, a free user or a subscriber, and by the category and features of the app being built. Another was changing the native mobile infrastructure, which only engineers with mobile expertise could do.
Earlier Claude models, which have powered Base44’s app generation engine since it launched in early 2025, couldn't be trusted with that work, Orlev suggests. When a model got stuck on an error, for example, it would keep working the spot in front of it instead of recognizing the fix probably already existed elsewhere in the code and searching for it.
“The decision on what to do next is a crucial one and most of the time [earlier] models would take, I would say, a naive approach,” he says.
Claude Fable 5 was the first model the team tested that could reason as if it had an understanding of how software is built, Orlev says.
Trusting Fable 5 with the most complex product and engineering jobs
Base44 runs each new Claude model through evals across different app types, measuring latency, cost, and build errors. The team also runs tests like building a Minecraft clone to see how a model handles game physics and mechanics.
With Claude Fable 5, two things stood out: it finished tasks in far fewer turns, and it built more complete apps from the first prompt, including the edge cases that earlier models skipped.
So the team pointed it at a task they had previously reserved only for the most senior engineers: rebuilding the Base44 system prompt. After about an hour of back-and-forth questions, Claude Fable 5 ran on its own for four hours and returned 90% to 95% of what they needed. Using its A/B testing infrastructure, the team was then able to measure and ship these changes that afternoon. And while Claude Fable 5 worked, it even flagged a gap in Base44's own evals: the team wasn't testing for cache hits, even though a prompt change can break the cache, and at the scale of millions of users that drives up cost. The model raised a blind spot and corrected it.
When Claude Fable 5 got stuck on a change to the harness behind Base44's in-app agent, it reasoned that the same problem had probably been solved elsewhere in the codebase, went to investigate that part, and came back with the fix. "This reasoning of 'this probably has been solved somewhere else, so I should go there to investigate' is something we haven't seen so often in other models," Orlev says.
Orlev compares working with Claude Fable 5 to working with a senior engineer. While a junior engineer needs every step specified and constant checking, you only need to brief a senior one on the goal and the why.
This type of work extends beyond the engineering team, too. When a product manager wanted to bring native mobile app building inside Base44, he pointed Claude Fable 5 at the job and after roughly two and a half hours had a working environment that was about 90% of what the team needed to move to production.
Before Claude Fable 5, this type of work had to wait for Base44's top three engineers or a specialist to free up. Now, the model executes tasks while Orlev's team reviews, tests, and approves the code before shipping it.
Claude Fable 5 gives Base44's product, engineering, and design teams confidence to build more ambitious parts of their Sugeragents platform.
What’s next
As Claude model capabilities advance, so do the Base44 team’s goals for the platform. The team aims to turn Base44 from a tool that builds apps into one that also helps people manage and grow what they've built. Base44 Superagents, now public, run workflows around those apps.
Knowing that they can trust Fable 5 with complex tasks, Orlev now encourages product managers and designers to build in parts of the platform they were previously not willing to touch for fear of breaking anything.
“Fable has given us the confidence to make bolder moves with the business,” Orlev says. “It’s bringing the product to a whole new area and possibilities that before that we were, I would say, scared to do.”
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
Jun 24, 2026
Building effective human-agent teams
Enterprise AI
Building effective human-agent teams
Building effective human-agent teams
Building effective human-agent teams
Building effective human-agent teams
Jun 5, 2026
The Claude Cowork product guide
Enterprise AI
The Claude Cowork product guide
The Claude Cowork product guide
The Claude Cowork product guide
The Claude Cowork product guide
Jul 13, 2026
Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
Enterprise AI
Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
Jul 10, 2026
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Enterprise AI
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night
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
