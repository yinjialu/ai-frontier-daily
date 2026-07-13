---
type: Article
title: Separating signal from noise in coding evaluations
source: openai-news
resource: https://openai.com/index/separating-signal-from-noise-coding-evaluations
published: 2026-07-08
tags: [编程基准测试, 模型评估, 数据质量, SWE-Bench]
detected: 2026-07-09T04:39:38+08:00
---

OpenAI审计SWE-Bench Pro发现约30%任务存在缺陷，包括测试严格、提示不明确、覆盖率低等，提醒开发者需仔细审查基准测试结果以避免误导模型能力评估。

## Full Text

Separating signal from noise in coding evaluations | OpenAI
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
July 8, 2026
Research
Publication
Separating signal from noise in coding evaluations
Through a detailed audit, we find widespread task issues in SWE-Bench Pro and estimate that ~30% of the tasks are broken.
Loading…
Share
Methodology
Methodology
Human-supervised agent review
Human annotation campaign
Discussion
Table of contents
Methodology
Human-supervised agent review
Human annotation campaign
Discussion
Accurately measuring our models’ capabilities is important for sound deployment and safety decisions, including decisions under OpenAI’s
Preparedness Framework
⁠
(opens in a new window)
. With each model release, we report results for a variety of external and internal benchmarks to track model progress. When evaluations have flaws that affect results, they can give a false understanding of capabilities, misrepresenting safety cases and affecting research priorities.
We
recently investigated
how one of the most widely used coding benchmarks, SWE-bench Verified, had fundamental design and contamination issues, and found that the eval no longer provided meaningful signal on software development capabilities. At the time, we encouraged the wider community to switch to SWE-Bench Pro.
SWE-Bench Pro
⁠
(opens in a new window)
was designed to improve on SWE-bench Verified by testing models on longer horizons and more realistic coding tasks to better track agentic coding capabilities. As in SWE-bench Verified, tasks are sourced programmatically from the history of feature changes in a set of public and private repositories. Models are required to implement a solution that passes new tests for a feature, without breaking existing functionality. On the 731-task public split, frontier models improved from a pass rate of 23.3% to 80.3% in eight months.
We’ve since performed a similar audit on SWE-Bench Pro, reviewing the dataset using a datapoint analysis pipeline. The pipeline reviewed model attempts at the task, task metadata, and failure traces to flag likely evaluation flaws. Each flagged task was then assessed through multiple investigator-agent passes and independently reviewed by five experienced software engineers, with disagreements escalated for further investigation.
We find evidence of breaking issues in a significant portion of the dataset. Our datapoint analysis pipeline flagged 200 (27.4%) broken tasks, while the human annotation campaign identified 249 (34.1%).
The issues primarily fell into four categories:
Overly strict tests
1
enforce specific implementation details not specified in the prompt, invalidating many functionally correct submissions.
Underspecified prompts
2
omit requirements that hidden tests enforce and that are not reasonably inferable.
Low-coverage tests
under check the requested feature, so incomplete fixes can pass.
A
misleading prompt
points models toward the wrong behavior or contradicts what tests require.
Our findings point to the difficulty of curating hard but fair benchmarks and the growing utility of agents for scalable data quality checks. In light of these results, we estimate that ~30% of SWE-bench Pro tasks are broken, and advise that model developers carefully examine results.
Methodology
Our aim is to ensure that task failures reflect genuine model limitations, and task successes reflect complete and valid solutions to the prompt requirements. To check the quality of the data used in the evaluation, we created a quality assurance pipeline to assess whether each datapoint accurately reflects model capabilities.
An initial data quality pipeline flags problems for review. We validate with a deeper agent-assisted audit of flagged tasks and a human annotation campaign working with experienced engineers.
An initial automated filter reviews the instructions given to the model, attempts by the model to solve the task, and the tests used to grade these attempts to flag likely broken or problematic examples. This filter flagged 286 potentially broken tasks. We then conducted a deeper review of that subset in two ways: a human-supervised agent review, which conducts extensive checks with investigator agents and a final human judgment; and a human annotation campaign working with experienced software developers.
Human-supervised agent review
Each flagged problem is audited with Codex-based investigator agents that were given access to the task repository and environment. This helps them distinguish reasonable task ambiguity, which can often be resolved by studying nearby code and repository conventions, from true underspecification. The agent can run tests, inspect files in the repo, and investigate model attempts and their common failure modes on the task. After several independent repeats of these deeper audits, a researcher reviewed the summaries, made a final judgment, and labeled the likely issues.
Human annotation campaign
In parallel, we ran a human annotation campaign over the flagged subset. We worked with experienced software engineers who were trained on the benchmark goals, issue taxonomy, and edge cases before reviewing tasks. Each task was reviewed by five engineers.
Reviewers formed an independent judgment from the visible problem statement, test cases, and the ground-truth reference solution (known as the gold patch) before using the pipeline analysis or transcript as supporting context. The reviewers then assigned a label and severity rating based on concrete evidence, and escalated disagreements or low-confidence cases for further review.
Human reviewers were more likely than the investigator agents to mark tasks as broken. There was also some disagreement on categories between the two review paths, but in no flagged task was “not broken” the most common human label. Of the categories the agent pipeline flagged, reviewers’ judgments overlapped in 74% of cases.
Compared with the agent pipeline, the human reviewers were also more likely to select multiple labels for a task, indicating that they found tasks to be broken in multiple ways or did not fit cleanly into a single category. This suggests the agent-plus-reviewer pipeline resulted in conservative labeling: it captured the same broad failure modes humans identified, while undercounting cases where reviewers saw additional or overlapping issues. The largest difference was in low-coverage tests, which humans selected as the most common issue for 9.4% of the benchmark compared with 4.1% from the agent pipeline.
Failure modes
Misleading prompt
Overly strict tests
Underspecified prompt
Low-coverage tests
In several cases the task prompt prescribed a specific implementation, but the hidden test cases expected different behavior.
OpenLibrary-77c16d5
This task involves normalizing table-of-contents entries and rendering them back to Markdown via
TocEntry.to_markdown()
. The task prompt specifies serialization down to character-level spacing, describing how exact spacing and pipes are enforced, and gives examples such as
" | Chapter 1 | 1"
and
"** | Chapter 1 | 1"
:
None
1
"[space]| Chapter 1 | 1"
2
"**[space]| Chapter 1 | 1"
3
"[space]| Just title | "
The hidden
test_to_markdown
assertions instead require
"  | Chapter 1 | 1"
and
"**  | Chapter 1 | 1"
:
None
1
"[space][space]| Chapter 1 | 1"
2
"**[space][space]| Chapter 1 | 1"
3
"[space][space]| Just title | "
There are two leading spaces in the hidden tests, but the example given to the model only contains one leading space. If a model rightly follows the given prompt, that one-character difference would fail the hidden test cases and the task would be marked incorrect.
Discussion
The issues we have identified, coupled with similar cases in
SWE-bench Verified
, highlight the importance of rigorously checking benchmarks. Issues and pull requests from open-source repositories were originally created for human collaboration, often through long back-and-forths between maintainers and contributors. As a result, problem descriptions, merged code, and unit tests do not always line up to form clean, isolated tasks for evaluating models reliably. In particular, tests included in pull requests can be overly strict because they are written to validate a specific change, rather than to define an implementation-agnostic standard for solving the task.
At the same time, evaluation flaws are easier to detect now than they would have been even a short time ago. As model capabilities improve, we can use those models to inspect prompts, tests, patches, traces, and edge cases with much greater depth and consistency, helping surface benchmark issues that were previously costly or impractical to find at scale.
We hope the wider evaluation community will develop new benchmarks built by experienced software developers specifically to test model capabilities. That approach can preserve the high bar and realism we want to measure model capabilities, and allows for better human oversight throughout the process. Given the issues uncovered in this analysis, we retract our earlier recommendation to adopt SWE-Bench Pro.
Ultimately, an eval should provide meaningful signal through benchmarks that are hard to game, easy to trust, and genuinely reflective of model capability or alignment. Because these results inform OpenAI’s deployment and safety decisions, the evals we track need to be valid and informative.
2026
Software & Engineering
Author
OpenAI
Footnotes
1
We
previously
⁠
referred to this category as narrow tests.
2
We previously referred to this category as wide tests.
Keep reading
View all
Introducing GeneBench-Pro
Research
Jun 30, 2026
A near-autonomous AI chemist improves a challenging reaction in medicinal chemistry
Research
Jun 17, 2026
Introducing LifeSciBench
Research
Jun 17, 2026
Research
Research Index
Research Overview
Economic Research
Latest Advancements
GPT-5.5
GPT-5.4
GPT-5.3 Instant
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
Manage Cookies
English
United States
