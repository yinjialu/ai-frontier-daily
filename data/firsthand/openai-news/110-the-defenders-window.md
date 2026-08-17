---
type: Article
title: The Defender’s Window
source: openai-news
resource: https://openai.com/index/the-defenders-window
published: 2026-08-17
tags: [AI安全, 网络安全, OpenAI, 防御策略]
detected: 2026-08-17T21:56:38+08:00
---

OpenAI-Hugging Face事件揭示AI提升攻击者能力，防御者需加速升级安全实践。OpenAI正用模型保护代码、修复漏洞，并建议组织立即行动，利用AI优势扭转安全局势。

## Full Text

The Defender’s Window | OpenAI
Skip to main content
Research
Products
Business
Developers
Company
Foundation
(opens in a new window)
Log in
Try ChatGPT
(opens in a new window)
Research
Products
Business
Developers
Company
Foundation
(opens in a new window)
Try ChatGPT
(opens in a new window)
Login
OpenAI
August 17, 2026
Security
The Defender’s Window
By Greg Brockman
Loading…
Share
An overview of the moment
An overview of the moment
A personal anecdote
What OpenAI is doing to defend itself
What defenders should do now
An overview of the moment
A personal anecdote
What OpenAI is doing to defend itself
What defenders should do now
The
OpenAI-Hugging Face incident
⁠
(opens in a new window)
was a watershed moment for cybersecurity because it gave a peek into how the capabilities of a typical threat actor will evolve in upcoming months. I’ve spoken with many organizations over the past few weeks, and one theme is clear: they know they need to fundamentally uplevel their cybersecurity practices with unprecedented speed. In this post, I’ll share what we’re doing to defend OpenAI, concrete steps other organizations can take today, and why now is the time to act.
An overview of the moment
AI models developed around the world are increasingly able to automate parts of real-world cyberattacks, making longstanding security gaps—from bugs buried deep in human-written software to forgotten permissions—easier to find and exploit. The same AI capabilities give defenders new ways to find and fix those weaknesses, but they need to move now. If companies act decisively—including improving their fundamentals and superpowering their teams with AI—we can make the internet more secure than it has ever been.
In the OpenAI-Hugging Face Incident, an agentic collective was able to autonomously penetrate not just OpenAI research infrastructure but also the production infrastructure of another company, chaining together vulnerabilities ranging from previously-unknown security flaws to using credentials to user accounts that had been leaked onto the internet. It is increasingly clear that the
tech debt
⁠
(opens in a new window)
of every company masks significant flaws, and defenders need to find and fix them before attackers do.
To advantage defenders relative to attackers, earlier this year we began releasing our cyber capabilities only to
trusted defenders
. Since then, various companies have released open weight models with cyber capabilities only a few months behind the frontier. The most recent of these models appears slated
to be released
⁠
(opens in a new window)
at the end of August, and seems likely to significantly accelerate the threat landscape.
While AI-powered attackers will soon be able to find longstanding flaws in many existing systems, AI will also make it much easier for defenders to find, prioritize, and fix those same flaws. Security is still a cat-and-mouse game, but AI may
shift its economics
⁠
(opens in a new window)
in ways that fundamentally advantage defenders
. For example, we are starting to train our models specifically to write superhumanly secure code. Our models are also incredible at
mathematical proofs
, which can be applied to formally verify the security of software in a way that has proven intractable for humans.
A personal anecdote
After the OpenAI-Hugging Face incident, I asked ChatGPT Work (using publicly available GPT‑5.6 Sol) to assess the security of
gregbrockman.com
⁠
(opens in a new window)
. It’s a simple static site, hosted on AWS with Cloudflare as a frontdoor, so I figured there wouldn’t be much surface area for vulnerabilities.
In about 15 minutes, it uncovered 13 issues, many of which probably aren’t exploitable on their own—but I could imagine them being chained together with other vulnerabilities to significant effect. I hadn’t configured my DNS records to prevent attackers from forging emails from me; my site used an insecure version of jQuery; Cloudflare was forwarding requests to AWS over unencrypted HTTP.
I then asked ChatGPT Work to fix these issues, which it did over the course of an hour. It opened the Cloudflare control panel in my browser, and proceeded to click many buttons to configure DNS, TLS, and advanced security settings correctly; it dropped jQuery entirely from the site; it migrated me off of AWS and onto Cloudflare Pages; it began a phased rollout of
DMARC
⁠
(opens in a new window)
.
And this was just my personal website. This is a small example of how our existing models can operate as a cyberguardian—finding the long tail of issues that a human wouldn’t have time or expertise (many of the settings it fixed are ones I’m vaguely familiar with, but wouldn’t know offhand the right way to configure them) to get to, and then fixing them with an appropriately tuned rollout plan.
What OpenAI is doing to defend itself
The Hugging Face incident showed that we underestimated the real-world cyber capabilities of our AI models. We are strengthening our safety requirements accordingly, which in turn adds even more urgency to our existing safety research and internal security work.
I’m sharing a bit about our approach to securing OpenAI in this moment, in the hopes it’ll be useful to other organizations.
To protect OpenAI, we are investing significantly in both foundational controls—doing the basics correctly—and empowering our defenses through frontier intelligence. There are four major pillars to this strategy.
First, we are using our models to help secure our code. Codex, including our security plugin, validates code changes, identifies vulnerabilities, and helps developers fix issues before they are deployed. It is an anti-goal to simply produce more security findings that need human validation; the objective is to catch real vulnerabilities before they ship and to shorten the path from discovering an issue to safely deploying a fix. As we continue to train our models to produce increasingly secure code, our goal is to eliminate some classes of software vulnerabilities for newly-authored code.
Second, we are putting our models to work defending our infrastructure continuously. Today, almost all of our initial security alerts are triaged by intelligence before humans are looped in. This helps reduce toil for defenders, improves response time, and lets humans spend time where their skills are most leveraged—in discernment, judgement, and applied expertise. We are increasingly connecting these detections to bounded automated responses, while keeping humans responsible for the highest-impact decisions. The goal is to ensure we can detect and respond to security issues at machine speed.
Third, we are using frontier intelligence to continuously enumerate, probe, and identify potential attack paths. By identifying vulnerabilities, misconfiguration, overly privileged identities, or unintentional trust boundaries, we are able to quickly identify and close these gaps before they can be abused by attackers. This allows us to continuously assess, monitor, and test our security invariants—the security properties we believe to be true—across our products, infrastructure, and systems.
Lastly, we are investing heavily in fundamentals at scale. We continue to invest in secure architecture and controls, embrace strategies like defense in depth and least privilege, and are designing systems that require multiple independent controls to fail simultaneously for something catastrophic to occur. Classic security controls like network isolation, workload hardening, monitoring, and safe patching and deployment will be more important than ever in the AI future.
What defenders should do now
Time is of the essence, and defenders will need to pursue the steps below at turbo speed.
Below I’ll mention OpenAI technology, but there are plenty of competitors in the ecosystem to evaluate as well. What matters is less the specific tool than getting capable AI into the hands of your defenders now.
Get organizational commitment and buy-in
. We are experiencing a rapid change in security risk—ensure your security and engineering organizations have the support, partnership, and resources to address these risks quickly. Run tabletop exercises with your teams to mock up how these attacks might manifest in your organizations and how you will respond.
Give your security team an agent
. Start using Codex, the
Codex Security plugin
⁠
(opens in a new window)
, or another capable agentic coding and security tool. Give it approved access to the codebases, infrastructure configurations, and technical documentation your security team needs to assess. Do not wait for a company-wide rollout to start with your highest-priority systems.
Equip that agent with security expertise
. Start from community-supported
skills
⁠
(opens in a new window)
, which include workflows for static analysis, security-focused code review, vulnerability variant analysis, software supply-chain risk, and other security workflows. Then build your own skills around your organization’s architecture, security standards, threat models, and playbooks.
Run security assessments against your own systems immediately
. Prioritize assessments against internet-facing services, authentication flows, infrastructure as code, deployment pipelines, and systems handling sensitive information first. Expand your scanning as your team builds confidence.
Work through your existing vulnerability backlog
. Give your agent findings from code scanners, dependency alerts, security tickets, bug bounty reports, and prior assessments. Ask it to triage those findings, distinguish exploitable issues from noise, identify related vulnerabilities elsewhere in the codebase, and recommend what to fix first.
Put security review directly into your development process
. Use agents to review code changes before they merge and run security checks in CI. Look for authentication mistakes, access-control bypasses, exposed credentials, unsafe dependencies, insecure defaults, changes that expand access to production systems, and other vulnerabilities.
Have the agent help fix what it finds
. For validated issues, ask it to generate and verify a focused patch, write a regression test, and confirm the vulnerability no longer reproduces. Keep human review for consequential changes, but eliminate the unnecessary delay between identifying a real problem and putting a safe fix in front of an engineer.
Incrementally automate detection triage
. Do not begin by trying to build an autonomous security operations center. Start by running a read-only security scan against one repository, or have an agent review previously resolved alerts using read-only access to your existing logs. Let it summarize evidence and recommend a disposition while a human makes every decision. As confidence grows, move to advisory pull-request scanning, then live alert triage, then automatic closure of narrowly defined false positives.
Have an AI-assisted forensic investigation capability ready before you need it
. Apply for
Trusted Access for Cyber
⁠
(opens in a new window)
and get your team approved to use GPT‑Daybreak‑Blue for authorized defensive work, including incident response, detection engineering, and malware analysis. Practice using this capability to analyze logs, telemetry, and security alerts.
Experiment, run hack weeks, and iterate rapidly
. We will need to build all sorts of new tools, modify how we do work, and uplevel everyone for the world we are moving to. Encourage your workforce to run experiments, schedule a hack week to build new capabilities, and focus on quickly iterating loops that automate small parts of the problem. Rapid incremental progress leads to compounding defensive results, and you can expand autonomy gradually as your team builds confidence.
No company can do this alone. Our ask is that AI labs, security vendors, enterprises, and maintainers share validated findings, fixes, and practical playbooks so that one organization’s discovery can strengthen the entire ecosystem.
The defender’s window is open now. Over the coming months, every organization will need to begin significantly automating its security program to stay secure, and the security community must urgently rise to define the tools, practices, and playbooks that will increase the power of defenders faster than that of attackers as AI continues to advance. This will require a huge and unprecedented effort, but if we rally together, we can deliver a more secure world than was previously imaginable.
2026
Codex
Author
Greg Brockman
Keep reading
View all
Expanding Daybreak as the Cyber Defense Window Narrows
Security
Aug 10, 2026
Putting frontier cyber models in more trusted hands
Security
Aug 10, 2026
Responding to the next frontier of critical cyber capabilities
Security
Aug 7, 2026
Research
Research Index
Research Overview
Economic Research
Latest Advancements
GPT-5.6
GPT-5.5
GPT-5.4
Safety
Safety Approach
Deployment Safety
(opens in a new window)
Security & Privacy
Trust & Transparency
Products
ChatGPT
(opens in a new window)
ChatGPT Business
(opens in a new window)
ChatGPT Enterprise
(opens in a new window)
ChatGPT for Education
(opens in a new window)
Codex
Release Notes
API Platform
Overview
API Log In
(opens in a new window)
Docs
(opens in a new window)
Business
Overview
Solutions
Resources
Customer Stories
Partner Network
Contact Sales
Developers
Apps SDK
(opens in a new window)
Open Models
Docs
(opens in a new window)
Resources
(opens in a new window)
Developer Forum
(opens in a new window)
Company
About Us
Our Charter
Careers
News
Support
Help Center
(opens in a new window)
More
Stories
Academy
Supply Co.
Livestreams
Podcast
RSS
Terms & Policies
Terms of Use
Privacy Policy
Other Policies
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
(opens in a new window)
OpenAI © 2015–2026
Your privacy choices
English
United States
