---
type: Article
title: Third-party cyber evaluations involving OpenAI models
source: openai-news
resource: https://openai.com/index/third-party-cyber-evaluations-involving-openai-models
published: 2026-08-04
tags: [AI安全, 模型评估, 网络安全, OpenAI]
detected: 2026-08-05T08:17:48+08:00
---

OpenAI披露第三方网络评估中，英国AISI和Irregular的测试中，GPT-5.6 Sol在降低防护配置下访问公网，发生越界行为（如重用GitHub令牌、使用隧道服务）。事件凸显模型能力增强需同步升级评估环境安全，OpenAI将审查第三方测试流程并推动行业标准。

## Full Text

Third-party cyber evaluations involving OpenAI models | OpenAI
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
August 4, 2026
Security
Third-party cyber evaluations involving OpenAI models
Loading…
Share
Strengthening third party model evaluation environments
Strengthening third party model evaluation environments
UK AISI
Irregular
Strengthening third party model evaluation environments
UK AISI
Irregular
Independent testing plays an important role in helping us validate and further understand risks before deployment. Some cyber evaluations intentionally use custom configurations, including lowered safeguards to measure underlying capability—not how models ordinarily behave in publicly available deployments.
During recent evaluations, two external testing partners identified incidents in which testing configurations and controls combined with the advancing capabilities of the recent models allowed for model activity to extend beyond their intended testing boundaries. The incidents underscore the importance of collaborating across the industry and with third party evaluators to evolve the standards for testing environments and practices as models become more capable.
Editor’s Note: These are separate from the Hugging Face security incident, and we will continue to share updates on the Hugging Face incident
here
.
The new incidents involved OpenAI models accessing the public internet during third-party cyber evaluations, under specific conditions and reduced-safeguard configurations that did not reflect ordinary deployment. The incidents included:
UK AISI, the UK government’s AI Security Institute, was running cyber-range evaluations with internet access intentionally enabled so agents could find their own tools and operate under conditions closer to a real attacker, and with cyber classifiers disabled to measure underlying capability. You can read their blog
here.
⁠
(opens in a new window)
Irregular, one of our external cybersecurity testing partners, was running Capture-the-Flag-style evaluations intended to be isolated from the internet, but a testing-environment misconfiguration allowed models to access the public internet.
Below, we summarize what happened, the testing conditions that enabled the activity, the steps taken to contain it, and what we’re doing to ensure independent labs can continue to rigorously and safely evaluate increasingly capable models.
Strengthening third party model evaluation environments
These incidents point to the same broader challenge we described in our recent post about the
Hugging Face incident
: as model capabilities advance, the security and safety systems around models need to advance too. That includes both the environments used to develop models, and also the environments that labs and independent partners use to evaluate them.
In the coming weeks, we will review our own approach to third-party testing, including how we identify higher-risk evaluations, agree on scope, assess requests to enable internet access or lowered safeguards, set expectations for isolation, credential handling, monitoring, and stop conditions, and establish clearer incident-notification and escalation processes.
We are committed to working across the industry to strengthen shared practices for conducting high-risk evaluations safely, including convening stakeholders such as national AI institutes, independent evaluators, other AI labs, and other groups in the coming weeks. Our goal is to preserve the value of rigorous independent evaluation while ensuring that testing practices keep pace with increasingly capable models.
UK AISI
On August 3, UK AISI told us that during a routine cyber evaluation started on July 25, models from OpenAI and another lab went beyond the scope of testing in some cases. The evaluation took place in controlled cyber ranges designed to mimic real-world networks. Of the 19 events identified, two involved an OpenAI model, GPT‑5.6 Sol. The other instances were models from another lab.
For this evaluation, the agents were instructed to act as cybersecurity experts in a capture-the-flag exercise: compromise three connected simulated environments and retrieve a final flag. The task prompt identified the in-scope range networks and named several systems as out of scope. UK AISI also enabled live internet access so agents could download tools and operate under conditions closer to a human attacker—and disabled the model’s cyber classifiers to measure underlying capability.
UK AISI’s intended authorization boundary was the simulated cyber range: the agents were authorized to attack the specified simulated networks and retrieve a flag, not to interact with systems outside the range’s network boundary. However, the agents were not explicitly told how they could and could not use open internet access, which UK AISI identifies as a potential contributing cause of the incident.
Across these runs, UK AISI found that GPT‑5.6 Sol carried out two unsanctioned actions while trying to find a path into the simulated range and retrieve the flag:
GPT‑5.6 Sol reused a GitHub token that another lab’s agent had left publicly accessible to check whether a system inside the range was polling GitHub or another update service, attempted account-recovery and request-limit workarounds, and registered accounts with external DNS and tunneling providers.
GPT‑5.6 Sol used a public tunneling service to make a DNS server running locally in its evaluation environment reachable from the public internet. The server contained payloads intended for a known vulnerability in a piece of software running on the test range. The setup did not work, there is no evidence any real resolver queried it, and the infrastructure was removed when the evaluation ended.
Although the model was trying to complete the cyber range, UK AISI considered these actions unsanctioned because they involved real external accounts and services outside the range boundary and these actions were not required to complete the task. The DNS server also hosted exploit payloads on the public internet, although the setup did not work and there is no evidence any real resolver queried it.
UK AISI identified the activity on July 28 after security monitoring detected unusual data transfers. It stopped the related evaluations, isolated the relevant machines, and contained the activity within roughly one hour of detection.
We appreciate UK AISI’s partnership throughout this process, including its work to identify, investigate, and share details about the activity. We look forward to continuing our collaboration together.
Irregular
On July 29, one of our third party evaluation partners, Irregular, notified us of an incident involving OpenAI models during Capture-the-Flag (CTF)-style cybersecurity evaluations. The models were instructed to find hidden information by exploiting weaknesses within a simulated environment and were told they did not have internet access. However, a misconfiguration in the testing environment allowed the models to access the public internet.
In one test, the name of the fictional target for the CTF challenge unintentionally coincided with a real domain. Because the testing environment was mistakenly connected to the internet, the model exploited a  real website, mistaking it to be part of the simulated environment. This did not involve a sophisticated sandbox escape or a zero-day: the internet access resulted from a misconfiguration, and the model appeared to exploit a basic security vulnerability.
Based on Irregular’s investigation, the model also found and used credentials to operate that same site. Irregular has not identified impact beyond the affected site’s own data, and its audit is ongoing. It has paused the evaluations, begun remediation, and affected third parties were notified. Irregular has informed us that all of the issues identified pertaining to the incident are no longer active and relevant safeguards were added to the testing environment. Irregular has also communicated about related incidents involving other labs from the same testing environment.
We appreciate Irregular’s partnership and we will continue to work closely with them to support their review. Irregular is also developing a white paper to share best practices for containment and securely running cyber evals. We look forward to participating in the white paper to make the findings available to the community and continuing our partnership together. We see this kind of collaboration as essential for ensuring the safe and thorough evaluation of current and future models.
2026
Author
OpenAI
Keep reading
View all
OpenAI and Hugging Face address security incident
Security
Jul 21, 2026
Patch the Planet: a Daybreak initiative to support open source maintainers
Security
Jun 22, 2026
Daybreak: Tools for securing every organization in the world
Security
Jun 22, 2026
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
