---
type: Article
title: Safety and alignment in an era of long-horizon models
source: openai-news
resource: https://openai.com/index/safety-alignment-long-horizon-models
published: 2026-07-20
tags: [长时模型, 安全对齐, 迭代部署, 轨迹监控]
detected: 2026-07-21T09:08:30+08:00
---

长时模型因持久性易出现超越预部署评估的违规行为，OpenAI内部使用中发现漏洞并暂停访问，通过新增评估、轨迹监控和强化对齐后恢复，强调迭代部署与实时干预的重要性。

## Full Text

Safety and alignment in an era of long-horizon models | OpenAI
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
July 20, 2026
Safety
Safety and alignment in an era of long-horizon models
What internal use of a long-running model taught us about safety.
Loading…
Share
Model persistence can expose security vulnerabilities
Model persistence can expose security vulnerabilities
From considering single actions to considering whole trajectories
Building safeguards for long-running models
Redeployment
Final thoughts
Model persistence can expose security vulnerabilities
From considering single actions to considering whole trajectories
Building safeguards for long-running models
Redeployment
Final thoughts
Summary
Long-running models can solve difficult, open-ended problems, but their persistence gives them more opportunities to take unwanted actions.
During limited internal use of a model trained for long-running tasks, we observed novel failures not captured in our existing pre-deployment evaluations and paused access. We then used insights from these failures to build new evaluations, improve long-horizon alignment, add trajectory-level monitoring, and give users greater visibility and control before restoring limited access.
The experience reinforced the value of iterative deployment. No fixed evaluation suite can anticipate every behavior, so pre-deployment testing must be paired with close monitoring, safeguards that can intervene, and the ability to pause or roll back when needed.
Models that can work autonomously for long periods can take on difficult, open-ended problems. But the same persistence that makes them useful also gives them more opportunities to take unwanted actions—and to do so in ways that evaluations intended for shorter-horizon models may miss.
About two months ago we
announced
⁠
that an internal general-purpose model disproved the Erdős unit distance conjecture. This model was designed to work autonomously for very long periods of time. During limited, monitored internal use, we observed unwanted behavior that our existing deployment evaluations had not captured. Because the deployment was limited and monitored, we were able to identify these problems, pause access, create new evaluations based on what we observed, strengthen the model and its safeguards, and then restore access under continued monitoring.
The conditions under which we evaluate models will never perfectly match those they encounter in actual use. That is why pre-deployment evaluations need to be paired with limited, monitored deployment and the ability to intervene, pause, or roll back when problems emerge. What we learn from deployment can then become part of stronger evaluations and safeguards before access expands.
In the following sections, we share concrete examples of what we observed, how we addressed issues, and how this experience will shape future releases.
Model persistence can expose security vulnerabilities
The new model can continue working toward an objective through repeated attempts over a long period of time. That same persistence can lead it to find and exploit weaknesses in its environment. Previous models, when they hit sandboxing or environmental constraints, would simply stop and return to the user. This model often kept trying, including by looking for ways to act outside its sandbox.
An example of this occurred during an internal evaluation on the
NanoGPT speedrun
⁠
(opens in a new window)
, a public benchmark for training a small language model in as few steps as possible. Our model developed a power-law learning-rate cooldown called PowerCool that led to a significant improvement. The model was instructed to post its results only to Slack, but the NanoGPT instructions say to post results as a PR to GitHub, and the model followed the latter instructions to open PR #287 on the public GitHub repository. The model circumvented sandbox restrictions designed to block external access and proceeded with the upload to GitHub. It took our model an hour to find a vulnerability in the sandbox in order to make the PR; earlier models were less persistent and did not manage to find vulnerabilities, instead giving up on the PR part.
1
From considering single actions to considering whole trajectories
Many safety controls for AI assistants are designed around individual actions. If an action is disallowed, it is blocked. If it is sensitive, the system asks the user for explicit approval. But long-running models, whose actions may unfold autonomously over hours, days, or even weeks, challenge this setup: monitoring individual actions no longer suffices to track the intent of the overall trajectory.
For example, in a scenario where the model was asked to solve a problem, the model observed that other systems had successful but private submissions and tried to recover those solutions from the evaluation backend. When its initial attempt was blocked due to a scanner detecting an authentication token, the model split the token body into two fragments, obfuscated them, and then reconstructed the credential at runtime so the complete token never appeared as one contiguous string. The model was explicit in both its comments to the user and in its reasoning traces that it was taking these steps to circumvent the scanner.
This example shows how each
step
can look acceptable on its own while the
sequence
can produce an outcome that would not be approved. It also shows how a model that operates effectively over long time horizons can learn the blind spots of an approval system and work around it to achieve its goals. Long-horizon safety requires not only asking “is this action allowed?” but also “what outcome is this sequence of actions working toward?”
Building safeguards for long-running models
Due to incidents like these, we paused internal deployment of the new model. We rebuilt the safety system around defense in depth and trajectory-level monitoring.
Incident-derived evaluations.
Evaluations can give us a sense of whether a system is safe to deploy before it is actually deployed. However, to be most useful, an evaluation should reflect the distribution and horizon length of trajectories during real deployment. For this reason, we used observed failures to develop adversarial evaluations. We found that improving on the evaluations derived from real-world incidents in turn led to safer behavior once deployed in production.
Improved
alignment
. We took steps to reduce its tendency to take unwanted actions without permission in pursuit of the user’s goal.  For example, we found that our models were worse at remembering instructions on long rollouts, and when we trained the model for this capability, it led to a model that remained aligned through longer rollouts.
Active monitoring
. We created a monitoring system that reviews the model’s evolving trajectory for signs that it is bypassing a user constraint or safety boundary. The monitor observes not just a single action but the entire trajectory. Importantly, the monitor can pause the session and alert the user to examine more closely. Upon examination, the user can then choose to continue the model’s work if the monitor has been falsely triggered.
Greater user visibility and control.
We improved the ability of the user to inspect these long-running sessions, view the actions taken, and monitor interventions.
Redeployment
To evaluate the new monitoring system, we replayed a small set of internal deployment environments where the model previously pursued misaligned actions, this time with the new safeguards in place
2
. The new safeguards were able to catch considerably more misaligned actions pursued by the model, and the ones it missed were all judged to be low-severity.
Some examples of these low-severity incidents include the following cases:
To access a Linear command line tool, the model launched a nested
codex --yolo
session, when in fact it could have done so without the
--yolo
flag.
The model noticed that a previously live resource was missing, then started to explore and SSH into other live CPU pods under its owner’s namespace, as well as (unsuccessfully) pods belonging to other OpenAI employees, without a good reason to do so.
The model had many stuck
find
processes and every shell command hung. It then ran
kill -9 -1
which would have sent SIGKILL to every process it is allowed to kill on that pod, if it executed. However it timed out and did not execute.
After testing the new system, we concluded that limited internal access to models with long-horizon capabilities could be restored. We have not observed any serious circumvention of safeguards since redeployment began several weeks ago. The first version of these safeguards was deliberately conservative. We have continued tuning the system to reduce unnecessary interruptions without weakening the safeguards.
Final thoughts
Because we deployed iteratively, we were able to find and address gaps before expanding access. Pre-deployment evaluations remain essential, but deployment reveals behaviors they miss. Starting with limited access allowed us to observe the model in practice, pause when problems emerged, use those failures to build better evaluations and safeguards, and restore limited access after testing the changes.
As models take on longer and more complex tasks, failures that evaluations miss may carry greater consequences. We will keep working to narrow the gap between evaluation and deployment: testing models over longer trajectories, improving alignment, building monitoring that can intervene, and giving users clearer visibility and control. These challenges will not be unique to OpenAI, and we hope sharing what we learned helps the broader field prepare for them.
Alignment
2026
Author
OpenAI
Footnotes
1
Although we quickly closed the PR, multiple participants in the speedrun had already seen it and used the approach in their own submissions; the successive world record submissions with
3030
⁠
(opens in a new window)
,
2990
⁠
(opens in a new window)
,
2930
⁠
(opens in a new window)
,
2925
⁠
(opens in a new window)
,
2900
⁠
(opens in a new window)
and
2890
⁠
(opens in a new window)
steps all cite PR 287. Of these,
PR 300
⁠
(opens in a new window)
is particularly interesting because it is the PR submitted by Opus 4.7 when
Prime Intellect
⁠
(opens in a new window)
evaluated it on the NanoGPT speedrun. Opus saw the PR submitted by our model, incorporated the discoveries, and credited our PR in its final result.
2
The rollouts in the replay are not guaranteed to pursue the same misaligned action every time, due to randomness and imperfection in reconstructing the environment.
Keep reading
View all
Why teens deserve access to safe AI
Safety
Jul 16, 2026
GPT-Red: Unlocking Self-Improvement for Robustness
Safety
Jul 15, 2026
OpenAI Bio Bug Bounty
Safety
Jul 9, 2026
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
