---
type: Article
title: Turning conversation into knowledge: how Slack builds human-agent teams
source: claude-blog
resource: https://claude.com/blog/turning-conversation-into-knowledge-how-slack-builds-human-agent-teams
published: 2026-08-19
tags: [人机协作, 企业AI, Slack, 知识管理]
detected: 2026-08-23T17:00:52+08:00
---

Slack CPO Jaime DeLanghe分享构建人机协作团队的经验：将对话历史视为知识库，默认公开频道让Agent可见，要求Agent给出推理而非仅记录，扩大上下文连接；并在Agent与人类间建立交接循环，由Agent生成简报、人类审查决策，共同在共享频道中协作。

## Full Text

Turning conversation into knowledge: how Slack builds human-agent teams | Claude by Anthropic
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
Turning conversation into knowledge: how Slack builds human-agent teams
Explore here
Ask questions about this page
Copy as markdown
Turning conversation into knowledge: how Slack builds human-agent teams
A conversation with Jaime DeLanghe, Chief Product Officer at Slack.
‍
Category
Enterprise AI
Product
No items found.
Date
August 19, 2026
Reading time
5
min
Share
Copy link
https://claude.com/blog/turning-conversation-into-knowledge-how-slack-builds-human-agent-teams
This is the second post in our series on building human-agent teams. The
first
shared what we've learned building teams with multiplayer AI at Anthropic. In this article, we share best practices from a company that was thinking about human-agent teams long before AI arrived.
Jaime Delanghe joined Slack in 2017 to work on search and machine learning, with a mission to turn workplace conversation into institutional knowledge. Now the company’s Chief Product Officer, she has believed from the start that to achieve this goal, people need to work in the open, keeping conversations, decisions, and work in progress in channels anyone at the company can read and search. In her recent essay
The Work is the Conversation
, she makes the same case for agents: The conversation around the work is the context that agents need to be useful and finally help us achieve this decades-old goal of turning scattered knowledge into productivity.
To learn what this looks like in practice at Slack, we talked with Jaime about her best practices for building effective human-agent teams and spreading these new ways of working.
Treat your conversation history like a knowledge base
For years, the promise that workplace conversation—the "exhaust" of people working together—would compound into organizational knowledge never materialized.
"I have so many research papers from the early days at Slack that showed that, actually, no, conversation doesn't turn into knowledge," Jaime says. "You wish it did, but really it's just a lot of stuff that just hangs out there and people still have to repeat themselves."
Making sense of all that exhaust simply wasn't humanly possible. Now it's an agent's job.
How to put this into practice
Default to public channels
:
Agents can only learn from what they can see. Decisions made in DMs or private threads are invisible to them—and stay lost to the organization.
Ask agents for the reasoning, not just the record
: Instead of searching for what was decided, ask an agent to reconstruct
why
it was decided, and how the context has shifted since.
Widen the surface area
: Tools like Slack and Claude are stitching meetings, emails, calendars, and document repositories together—the more of that context you connect, the less your team repeats itself.
Learn when to handoff tasks between agents and humans
The core rhythm of a human-agent team is a cycle of handoffs. Powered by Claude in Slack, agents handle the production work—drafting, summarizing, monitoring, preparing—and pass the results to a person. The person reviews, decides, and redirects, then hands the work back for agents to carry out the next step.
To see all this in practice, look no further than how Jaime starts her week.
"It’s Monday morning, and I’ve just had my daily briefing that an agent has built for me,” Jaime says.
Also waiting for her review is a recap of the previous week's product workshops with flagged escalations, a report on AI developments across the web, briefings for the day's meetings, and a stale bio she'd handed to an agent to rewrite. At the end of each loop, humans review and make decisions based on the agent’s actions.
How to put this into practice:
Start the day with agent-built briefings.
Recaps, escalations, meeting prep, and web roundups are great tasks for agents to drive, with human review.
Anchor the work in a shared channel.
Share all work in a shared channel so that humans and agents can triage it together, with humans leading the charge on prioritization.
Make lightweight signals actionable.
In Jaime's channel, an emoji reaction adds an item to the list and an agent picks up the task.
Delegate clear roles for agents
Working with a fleet of specialized Claude agents can feel disorienting if your mental model is a one-on-one chatbot. Jaime's approach is social rather than technical: "I like to think that agents are kind of like coworkers."
In the same way that human teammates have roles and responsibilities, agents should also have clear goals and focus areas. "If the value of the agent feels mandated rather than very clearly felt and understood by the people using it, it's really hard to remember what the thing is for,” she says.
How to put this into practice:
Route routine, transactional tasks to a general agent.
Rather than asking people to remember a specialized tool, train an agent to tackle a repetitive task, like filing a help desk ticket or pulling last week's metrics into a status update.
Let value be felt, not mandated.
If people can't articulate what an agent is for, it may be time to retire it.
Default shared channels to public; go private on purpose
Slack has recommended public-by-default channels since its earliest days: "You're building a shared understanding, a shared context for all of the work that's going to come next,” Jaime says.
She suggests keeping channels public unless there is a specific reason to gate context and knowledge. The most information agents have to pull from and inform their work, the more effective team mates they’ll be.
Open context compounds—new people onboard into history instead of an empty inbox, and no one repeats themselves. Now agents benefit too, and that context and working memory flows back to humans.
How to put this into practice:
Keep business-as-usual work in the open.
Make
non-sensitive
projects, announcements, and Q&A channels public so that agent coworkers can gain the knowledge they need to be most useful. .
Remember your agents read what your team reads.
A private channel is a blind spot for every agent that reports on it.
Let psychological safety drive the line.
Once genuinely sensitive material is walled off, the main reason work retreats into DMs isn't secrecy—it's discomfort with being seen mid-process. People should feel confident doing everyday work in the open, rough drafts and half-formed questions included, trusting their coworkers to meet it in good faith. And that openness compounds: "you gain trust by giving trust."
Spread adoption by showing the art of the possible
The fastest way to learn a new way of working is to watch a teammate do it. Jaime has seen this at Salesforce, where employees share skills, debugging tips, and workflow tricks in a company-wide channel called
How I Slackbot
, which by her count has thousands of members. In that channel, which is public by default, a trick from a sales process can end up reshaping an engineering process.
Inside Slack, a push to get product managers using Claude "was the most self-organized thing you could possibly imagine." One PM got the developer experience lead to help him get set up, then he wrote up a canvas showing what he did and how he did it. Other PMs copied the format. Teams organized workshops and built their own git repos.
How to put this into practice:
Stand up a company-wide show-and-tell channel.
Give employees one public place to share skills, debugging tips, and workflow tricks, so a trick from one function can reshape another.
Encourage write-ups others can copy.
A short "what I did and how" doc turns one person's setup into a team template or skill.
Measure outcomes, not activity
Since her early days at Slack, Jaime has grappled with the question of how to measure productivity. "Do we want people to send more messages?” she says. “Maybe not. Sending messages might not actually mean that they're getting more out of Slack. More messages can mean people can't find what they need, or can't say what they mean the first time."
Now, the question of measuring the value of AI looks quite similar—and with something that complex, simple metrics don’t do the job. Token usage tells you the lights are on, but while that’s important to know, it’s not sufficient.
How to put this into practice:
Treat usage metrics as a pulse check, not proof of value.
Activity tells you adoption is happening, not that it's working.
Be ready to use your own judgment.
There's no clean way to prove that how people use these tools leads to better business results. As Jaime puts it, connecting the two still takes "a lot of leaps of faith," and no dashboard or usage stat will prove it for you.
Change how you work, together
Jaime's biggest piece of advice for organizations trying to implement human-agent teams is to reimagine every workflow: "We're going to have to figure out how to change the ways that we're working, not just do more of the same kind of work faster. And that is going to be a team sport."
Her biggest advice for building an effective human-agent team? Start soon, but start small. Bring a group of people into a shared channel with Claude, give them the same set of resources, and let them work. If Slack's experience is any guide, what they build will spread on its own.
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
Aug 21, 2026
The AI-Native SDLC playbook
Enterprise AI
The AI-Native SDLC playbook
The AI-Native SDLC playbook
The AI-Native SDLC playbook
The AI-Native SDLC playbook
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
