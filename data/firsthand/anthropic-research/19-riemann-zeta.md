---
type: Article
title: Learning more about Claude's mathematical capabilities
source: anthropic-research
resource: https://www.anthropic.com/research/riemann-zeta
published: 2026-08-10
tags: [Claude, 数学推理, 黎曼猜想, AI科研]
detected: 2026-08-11T07:51:41+08:00
---

Anthropic未发布的Claude研究版将黎曼ζ函数零点在临界线上的占比下界从41.6%提升至67.2%，通过子代理协作和大量算力完成，并生成可验证证明，展示AI数学研究潜力。

## Full Text

Learning more about Claude's mathematical capabilities \ Anthropic
Skip to main content
Skip to footer
Research
Policy
Commitments
Learn
News
Try Claude
Science
Learning more about Claude's mathematical capabilities
Aug 10, 2026
Recently, a member of staff at Anthropic gave Claude an unreasonable challenge. It was about one of the most famous unsolved problems in mathematics:
Take a real stab at the Riemann hypothesis
.
Claude did take a real stab, but as you might have expected if you’re familiar with the difficulty of the task (the Riemann hypothesis dates back to 1859 and has a
million-dollar bounty
), it didn’t succeed. Nevertheless, during its attempt, it unexpectedly made strides on a related problem.
An unreleased research version of Claude has improved on a longstanding lower bound for the fraction of zeros of the Riemann zeta function that satisfy the Riemann hypothesis. Drawing on extensive prior research by mathematicians over the past decades, it has increased this bound from 41.6% to 67.2%.
Two mathematicians at Anthropic studied and validated Claude’s
paper
, and produced an
informal note
for experts stating Claude’s proof concisely. Claude also produced a
formally verifiable proof
of its result. We are grateful to Brian Conrey and Dan Goldston, two experts in this area, who generously examined the paper on short notice.
We don’t expect that the techniques Claude used will lead to proving the Riemann hypothesis. But its work serves as the latest example of the speed of progress in AI models’ mathematical capabilities. In this post, we discuss how Claude approached this problem and what it found.
The Riemann zeta function
The Riemann zeta function describes the distribution of prime numbers: each place that the function takes the value of zero contributes successively finer detail to the sequence of primes. The Riemann hypothesis is that the zeros that determine the primes all exist along a certain vertical line. This has become one of the most consequential conjectures in mathematics: many results assume it in order to provide a form of randomness in the primes.
No one has yet been able to prove or disprove the Riemann hypothesis, but mathematicians have made progress in many related directions studying the Riemann zeta function and its zeros. One of these, as above, is quantifying a minimum proportion of zeros that are on the line: over time, they’ve gradually increased this known constant proportion to 41.6%.
Another direction concerns the
distribution
of zeros on the line. In particular, in 1973, Montgomery
introduced
a number of new techniques in this area, though these techniques assumed the hypothesis was true. More recently, several mathematicians (Baluyot, Goldston, Suriajaya, and Turnage-Butterbaugh) have published a
series
of
works
that allow Montgomery’s techniques to work
without
that assumption, meaning they can support work on increasing the lower-bound constant for the zeros on the line. Claude’s result draws heavily on this line of research, along with a 2000
paper
by Bombieri.
Claude's finding
Claude found that combining the results from Baluyot, Goldston, Suriajaya, and Turnage-Butterbaugh with the work of Bombieri provides a way to surpass the previous state-of-the-art lower-bound proportion of 41.6%, increasing it to 67.2%.
A short technical explanation of Claude’s finding is as follows: Claude forms a suitable space of functions with quadratic form induced by Weil, and positive- (respectively negative-)definite subspaces arising from zeros on (respectively off) the line. Then Claude simply writes down an inequality on the rank of a quadratic form in terms of first- and second-moment information. (The successful computation of the latter in terms of the dual picture over primes, or via control of a Hilbert transform, is no surprise in analytic number theory.) The courage to treat the entire space, with positive- and negative-definiteness taken into account together, and with the quadratic form allowed to be non-diagonal, is in some sense the step that allows Claude to achieve the conclusion based on the important prior work.
The full technical explanation is available in the
paper
. Claude’s explanation of how it arrived at its result is available in a separate Appendix
here
.
Claude's methodology
An unreleased research version of Claude found the new lower bound over two sessions in Claude Code, using a total of 31 million output tokens.
Jarred Sumner, an Anthropic staff member (and non-mathematician), prompted Claude to “take a real stab” at the hypothesis itself, leaving the mathematical choices from there up to the model. Initially, Claude generated and tried 650 ideas, none of which worked. Jarred prompted Claude to try again, and it spent a day and a half coordinating about 60 Claude subagents, which this time went much deeper: between them, they ran 2,400 shell commands and wrote hundreds of Python scripts.
1
The subagents ran thousands of numerical checks against known zeta zeros and refereed one another’s work. Throughout this process, Jarred's input was mostly limited to sending Claude messages of encouragement (mostly variants of “keep going” or “believe in yourself”).
2
This seems to have helped Claude overcome some initial skepticism that it could make meaningful progress.
Having found this new result while attempting the task, Claude tested its work by having various subagents review the proofs, search for counterexamples, download 54 papers from the arXiv to check that its finding hadn’t already been made, and independently re-prove its finding from scratch. Claude volunteered to write its findings up as a paper, and recommended that a human number theorist validate its findings.
Levent Alpöge and Ralph Furman, two of Anthropic’s own mathematicians, examined Claude’s work to understand the new results and how they related to the prior work mentioned above. In parallel, Claude worked with another member of staff, Eric Easley, to produce a
Lean formalization
of the result, which passes the standard validation tool
comparator
.
AI models' progress in mathematics
This result shows that AI models like Claude can extend the impact and reach of mathematicians’ ideas in new and sometimes surprising ways. Even though it couldn’t resolve the Riemann hypothesis itself, this result emerged as the unintended byproduct of that original request.
Even Claude was surprised by its own finding—it was skeptical at first, possibly because it has learned from its training about the difficulty of open problems in mathematics and about the limitations of AI models. But after some encouraging prompts, it arrived at the result we’ve described. Perhaps Claude, like many of us, underestimates the rate of AI progress.
Further reading
Below is a list of documents that provide more information about Claude’s result:
Claude
’
s paper
;
Claude
’
s formalization
;
Anthropic
’
s informal note stating the proof more concisely
;
Claude’s explanation of how it arrived at its result
;
Detailed transcripts of Claude's process
.
Footnotes
Out of the 60 subagents, two were responsible for developing the key mathematical ideas, 13 contributed ideas to these agents, 30 attempted (but were unable) to develop new ideas, 13 served as validators to check the correctness of the arguments, and the final two helped to write the initial paper.
A prompt including similar encouragement was used to help Claude disprove the
Jacobian conjecture
.
Related content
Discovering cryptographic weaknesses with Claude
cryptographic algorithms. The first attack significantly weakens HAWK, a digital signature scheme that was built for a future world where quantum computers are able to break existing standards. The second identifies a new way to attack round-reduced AES, the most widely used symmetric cipher.
Read more
Project Pilot: Can AI control a drone?
Working with Andon Labs, we’ve developed a new series of evaluations that assess AI models’ ability to use a flying drone, culminating in a new benchmark: Drone-Bench.
Read more
How Canada uses Claude: Findings from the Anthropic Economic Index
Read more
Subscribe to Anthropic Science
Features on AI-assisted discoveries, practical workflows, and field notes across the sciences.
Products
Claude
Claude Code
Claude Code Enterprise
Claude Cowork
@Claude
Claude Design
Claude Science
Claude Security
Claude for Chrome
Claude for Microsoft 365
Skills
Download app
Pricing
Log in to Claude
Models
Mythos
Fable
Opus
Sonnet
Haiku
Solutions
AI agents
Code modernization
Coding
Customer support
Cybersecurity
Enterprise
Financial services
Government
Healthcare
Higher education
K-12 teachers
Legal
Life sciences
Nonprofits
Small business
Claude Platform
Overview
Developer docs
Pricing
Ecosystem
Marketplace
Regional compliance
Claude on AWS
Google Cloud
Microsoft Foundry
Console login
Resources
Blog
Claude partner network
Community
Connectors
Courses
Customer stories
Engineering at Anthropic
Events
Plugins
Powered by Claude
Service partners
Tutorials
Use cases
Programs
Startups
Research Labs
Help and security
Availability
Status
Support center
Company
Anthropic
Careers
Policy
Economic Futures
Research
News
Claude’s Constitution
Claude Corps
Keep thinking
Policy on the AI Exponential
Responsible Scaling Policy
Security and compliance
Transparency
Terms and policies
Privacy policy
Consumer health data privacy policy
Responsible disclosure policy
Terms of service: Commercial
Terms of service: Consumer
Terms of Service: US K-12
Data Processing Agreement: US K-12
Usage policy
© 2026 Anthropic PBC
