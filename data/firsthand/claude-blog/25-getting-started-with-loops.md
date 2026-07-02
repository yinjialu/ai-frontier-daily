---
type: Article
title: Getting started with loops
source: claude-blog
resource: https://claude.com/blog/getting-started-with-loops
published: 2026-06-30
tags: [agentic loops, Claude Code, coding agent, loop design]
detected: 2026-07-01T01:06:02+08:00
---

本文介绍了Claude Code团队对agentic loops的定义与分类，包括turn-based和goal-based等循环模式，并提供了从简单到复杂的实践指南，帮助开发者根据任务类型选择合适的循环策略，同时管理token消耗。

## Full Text

Getting started with loops | Claude by Anthropic
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
Security
Science
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
Security
Science
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
Getting started with loops
Explore here
Ask questions about this page
Copy as markdown
Getting started with loops
Learn how the Claude Code team defines agentic loops, with practical guidance on progressing from turn-based to goal-based, time-based, and proactive loops—and when to use each.
Category
Claude Code
Product
Claude Code
Date
June 30, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/getting-started-with-loops
There’s a lot of talk right now about "designing loops" instead of prompting your coding agent. If you spend some time on X trying to pin down what a loop actually is, you'll come across multiple different answers.
On the Claude Code team, we define
loops as agents repeating cycles of work until a stop condition is met
. We categorize a few different types of loops based on:
How they are triggered
How they are stopped
What Claude Code primitive is used
What type of task is most appropriate for each.
We’ll cover the main loop types, when to use each, and how to maintain code quality while managing token usage. Not all tasks require complex loops; start with the simplest solution and use these patterns selectively.
No items found.
Prev
Prev
0
/
5
Next
Next
Get Claude Code
Desktop
VS Code
JetBrains
On the web
Slack
curl -fsSL
https://claude.ai/install.sh
| bash
Copy command to clipboard
irm
https://claude.ai/install.ps1
| iex
Copy command to clipboard
Or read the
documentation
Try Claude Code
Try Claude Code
Try Claude Code
Developer docs
Developer docs
Developer docs
eBook
Turn-based loops
Triggered by
: A user prompt.
Stop criteria
: Claude judges it has completed the task or needs additional context.
Best used for:
Shorter tasks that are not part of a regular process or schedule.
Managed usage by:
Write specific prompts and improve verification using skills to reduce the number of turns.
‍
Every prompt you send starts a manual loop with you directing each turn. Claude gathers context, takes action, checks its work, repeats if needed, and responds. We call this the agentic loop.
For example, ask Claude to create a like button. It reads your code, makes the edit, runs the tests, and hands back something it
believes
works. You then manually check the work, and write the next prompt.
You can improve the verification step by encoding your manual steps as a SKILL.md so Claude can check more of its own work, end-to-end. This should include tools or connectors to allow Claude to
see
,
measure
or
interact
with the result. The more quantitative the checks are, the easier it is for Claude to self-verify.
For example, in your SKILL.md file you may specify:
---
name: verify-frontend-change
description: Verify any UI change end-to-end before declaring it done.
---
# Verifying frontend changes
Never report a UI change as complete based on a successful edit alone. Verify it the way a human reviewer would:
1. Start the dev server and open the edited page in the browser.
2. Interact with the change directly. For a new control (button, input, toggle): click it, confirm the expected state change, and screenshot before/after.
3. Check the browser console: zero new errors or warnings.
4. Use the Chrome Devtools MCP, run a performance trace and audit Core Web Vitals.
If any step fails, fix the issue and rerun from step 1 — do not hand back partially verified work.
Goal-based loop (/goal)
Triggered by
: A manual prompt in real-time.
Stop criteria
: Goal achieved OR maximum number of turns reached.
Best used for:
Tasks that have verifiable exit criteria.
Managed usage by:
Setting a specific completion criteria and explicit turn caps, “stop after 5 tries.”
Sometimes, a single turn is not enough, especially for more complex tasks. Agents do better when they can iterate. You can extend how long Claude keeps iterating by defining what done looks like with /goal.
When you define the success criteria, Claude doesn’t have to make a determination on what is “good enough” and end the loop early. Each time Claude tries to stop, an evaluator model checks your condition and sends it back to work until the goal is met or a number of turns you define is reached.
This is why deterministic criteria, such as number of tests passed or clearing a certain score threshold, are so effective.
For example:
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
Time-based loop (/loop and /schedule)
Triggered by
: A specified time interval.
Stop criteria
: You cancel it, or the work completes (the PR merges, the queue is empty).
Best used for:
For recurring work, or interfacing with external environments / systems.
Managed usage by:
Set longer intervals or react based on events rather than time.
Some agentic work is recurring: the task stays the same and only the inputs change. For example, summarizing Slack messages every morning. Other work depends on external systems, and a simple way to interface with one is to check it on an interval and react to what changed. For example, a PR which may receive code reviews or fail CI.
For these, you can trigger when Claude runs with `/loop` which re-runs a prompt on an interval. For example:
/loop 5m check my PR, address review comments, and fix failing CI
`/loop` runs on your computer, so if you turn it off, it stops. You can move the loop to the cloud by creating a routine with  `/schedule`.
Proactive loops
Triggered by
: An event or schedule, with no human in real time.
Stop criteria
: Each task exits when its goal is met. The routine itself runs until you turn it off.
Best used for:
Recurring streams of well-defined work: bug reports, issue triage, migrations, dependency upgrades, etc.
Managed usage by:
Routing routines to smaller, faster models and using the most capable model for judgment calls.
The primitives above, along with other Claude Code features like
auto mode
and
dynamic workflows
(research preview) can be composed into a loop for long-running work.
For example, to handle incoming feedback, you can use:
`/schedule`
(research preview) to run a routine that checks for new reports
`/goal`
to define what done looks and
skills
to document how to verify it
Dynamic workflows
to orchestrate agents that triage each report, fix it, and review the fix
Auto mode
so the routine runs without stopping to ask for permission
Putting it together, a prompt could look like this:
/schedule every hour: check #project-feedback for bug reports. /goal: don't stop until every report found this run is triaged, actioned, and responded to. When fixing a bug, use a workflow to explore three solutions in parallel worktrees and have a judge adversarially review them.
Maintaining code quality
The quality of a loop’s output depends on the system around it. When designing the system:
Keep the codebase itself clean
: Claude follows patterns and conventions that already exist in your codebase.
Give Claude a way to verify its own work
: Encode what good looks like for you and your team with
skills
.
Make docs easy to reach:
Frameworks and libraries docs have up-to-date best practices.
Use a second agent for code reviews
: A reviewer with fresh context is less biased and not influenced by the main agent’s reasoning. You can use the built-in `/code-review` skill or
Code Review
for Github.
When an individual result doesn’t meet the standard, don’t stop at fixing the individual issue, try to encode it to improve the system for all future iterations.
Managing token usage
To manage token usage, loops should have clear boundaries:
Choose the right primitive and model for the job:
Smaller tasks don’t need multiple agents or loops. Some tasks can use cheaper and faster models.
Define clear success and stop criteria:
Be specific about what done looks like so Claude can arrive at the solution sooner (but not too soon).
Pilot before a large run:
Dynamic workflows can spawn hundreds of agents. Gauge usage on a smaller slice of the work first.
Use scripts for deterministic work
: Running a script is cheaper than reasoning through the steps. For example, a PDF skill can ship a form-filling script that Claude runs each time, instead of re-deriving the code.
Don’t run routines more often that you need to:
Match the interval to how often the thing you’re watching changes
Review usage:
The `/usage` command breaks down recent usage by skills, subagents, and MCPs, `/goal` with no arguments shows number of turns and token usage so far, `/workflows` shows each agent’s token usage and you can stop an agent at any time.
Getting started
To summarize:
Loop
You hand off
Use it when
Reach for
Turn-based
The check
You're exploring or deciding
Custom verification skills
Goal-based
The stop condition
You know what done looks like
/goal
Time-based
The trigger
The work happens outside your project on a schedule
/loop
,
/schedule
Proactive
The prompt
The work is recurring and well-defined
All of the above, and dynamic workflows
To get started with loops, look at the work you already do. Pick one task where you’re the bottleneck and ask which piece you could hand off: can you write the verification check? Is the goal clear enough? Does the work arrive on a schedule?
Once you have an idea, run the loop, observe the results like where it stalls or over-reaches, and don’t be afraid to iterate on it.
For more information, read the Claude Code docs on
running agents in parallel,
as well as the
loop
,
schedule
,
goal
, and
dynamic workflows
pages.
This article was written by Delba de Oliveira and Michael Segner
FAQ
No items found.
Related posts
Explore more product news and best practices for teams building with Claude.
Jun 17, 2026
Meet the winners of our Claude Opus 4.8 Build Day hackathon
Claude Code
Meet the winners of our Claude Opus 4.8 Build Day hackathon
Meet the winners of our Claude Opus 4.8 Build Day hackathon
Meet the winners of our Claude Opus 4.8 Build Day hackathon
Meet the winners of our Claude Opus 4.8 Build Day hackathon
Jun 24, 2026
Agent identity in Claude Tag: a new access model for autonomous, team-wide AI
Claude Code
Agent identity in Claude Tag: a new access model for autonomous, team-wide AI
Agent identity in Claude Tag: a new access model for autonomous, team-wide AI
Agent identity in Claude Tag: a new access model for autonomous, team-wide AI
Agent identity in Claude Tag: a new access model for autonomous, team-wide AI
Jun 3, 2026
Running an AI-native engineering org
Claude Code
Running an AI-native engineering org
Running an AI-native engineering org
Running an AI-native engineering org
Running an AI-native engineering org
May 12, 2026
How Anthropic's cybersecurity team built a threat detection platform with Claude Code
Claude Code
How Anthropic's cybersecurity team built a threat detection platform with Claude Code
How Anthropic's cybersecurity team built a threat detection platform with Claude Code
How Anthropic's cybersecurity team built a threat detection platform with Claude Code
How Anthropic's cybersecurity team built a threat detection platform with Claude Code
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
Startups
Startups
Startups
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
Claude Code
Coding
