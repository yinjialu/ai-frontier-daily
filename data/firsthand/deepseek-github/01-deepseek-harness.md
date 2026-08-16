---
type: Article
title: deepseek-ai/deepseek-harness
source: deepseek-github
resource: https://github.com/deepseek-ai/deepseek-harness
published: 2026-08-13
tags: [DeepSeek, AI Agent, 插件化, 开源框架]
detected: 2026-08-17T07:39:55+08:00
---

DeepSeek Harness是DeepSeek AI开源的智能体框架，采用'一切皆插件'架构，基于Cordis构建，支持npx快速启动Web UI，当前为开发者预览版，接口可能变动。

## Full Text

GitHub - deepseek-ai/deepseek-harness: DeepSeek Harness: Everything is a Plugin. · GitHub
Skip to content
Navigation Menu
Sign in
Appearance settings
Platform
AI CODE CREATION
GitHub Copilot
Write better code with AI
GitHub Copilot app
Direct agents from issue to merge
MCP Registry
Integrate external tools
DEVELOPER WORKFLOWS
Actions
Automate any workflow
Codespaces
Instant dev environments
Issues
Plan and track work
Code Review
Manage code changes
Code Quality
Enforce quality at merge
APPLICATION SECURITY
GitHub Advanced Security
Find and fix vulnerabilities
Code security
Secure your code as you build
Secret protection
Stop leaks before they start
EXPLORE
Why GitHub
Documentation
Blog
Changelog
Marketplace
View all features
Solutions
BY COMPANY SIZE
Enterprises
Small and medium teams
Startups
Nonprofits
BY USE CASE
App Modernization
DevSecOps
DevOps
CI/CD
View all use cases
BY INDUSTRY
Healthcare
Financial services
Manufacturing
Government
View all industries
View all solutions
Resources
EXPLORE BY TOPIC
AI
Software Development
DevOps
Security
View all topics
EXPLORE BY TYPE
Customer stories
Events & webinars
Ebooks & reports
Business insights
GitHub Skills
SUPPORT & SERVICES
Documentation
Customer support
Community forum
Trust center
Partners
View all resources
Open Source
COMMUNITY
GitHub Sponsors
Fund open source developers
PROGRAMS
Security Lab
Maintainer Community
Accelerator
GitHub Stars
Archive Program
REPOSITORIES
Topics
Trending
Collections
Enterprise
ENTERPRISE SOLUTIONS
Enterprise platform
AI-powered developer platform
AVAILABLE ADD-ONS
GitHub Advanced Security
Enterprise-grade security features
Copilot for Business
Enterprise-grade AI features
Premium Support
Enterprise-grade 24/7 support
Pricing
Search
/
Sign in
Sign up
Appearance settings
You signed in with another tab or window.
Reload
to refresh your session.
You signed out in another tab or window.
Reload
to refresh your session.
You switched accounts on another tab or window.
Reload
to refresh your session.
Dismiss alert
{{ message }}
Uh oh!
There was an error while loading.
Please reload this page
.
deepseek-ai
/
deepseek-harness
Public
Notifications
You must be signed in to change notification settings
Fork
13.1k
Star
131k
Code
Discussions
Security and quality
0
Insights
Additional navigation options
Code
Discussions
Security and quality
Insights
master
Branches
Tags
Go to file
Code
Open more actions menu
Folders and files
Name
Name
Last commit message
Last commit date
Latest commit
History
12,293 Commits
12,293 Commits
.agents
.agents
.claude
.claude
.github
.github
apps
apps
assets
assets
docs
docs
examples
examples
native
native
packages
packages
patches
patches
python
python
scripts
scripts
vendor
vendor
website
website
.editorconfig
.editorconfig
.gitattributes
.gitattributes
.gitignore
.gitignore
.gitlab-ci.yml
.gitlab-ci.yml
.jscpd.json
.jscpd.json
.oxlintrc.json
.oxlintrc.json
.oxlintrc.staged.json
.oxlintrc.staged.json
.rgignore
.rgignore
AGENTS.md
AGENTS.md
BENCHMARK.md
BENCHMARK.md
CLAUDE.md
CLAUDE.md
CONTRIBUTING.i18n.yaml
CONTRIBUTING.i18n.yaml
CONTRIBUTING.md
CONTRIBUTING.md
CONTRIBUTING.zh.md
CONTRIBUTING.zh.md
LICENSE
LICENSE
README.i18n.yaml
README.i18n.yaml
README.md
README.md
README.zh.md
README.zh.md
THIRD_PARTY_NOTICES.md
THIRD_PARTY_NOTICES.md
knip.json
knip.json
lefthook.yml
lefthook.yml
package.json
package.json
pnpm-lock.yaml
pnpm-lock.yaml
pnpm-workspace.yaml
pnpm-workspace.yaml
pytest.ini
pytest.ini
tsconfig.base.client.json
tsconfig.base.client.json
tsconfig.base.json
tsconfig.base.json
tsconfig.client.json
tsconfig.client.json
tsconfig.host.json
tsconfig.host.json
tsconfig.json
tsconfig.json
tsdown.config.ts
tsdown.config.ts
vitest.config.ts
vitest.config.ts
vitest.e2e.config.ts
vitest.e2e.config.ts
vitest.shared.ts
vitest.shared.ts
vitest.snapshot.config.ts
vitest.snapshot.config.ts
vitest.web-stress.config.ts
vitest.web-stress.config.ts
vitest.web.config.ts
vitest.web.config.ts
vitest.web.perf.config.ts
vitest.web.perf.config.ts
View all files
Repository files navigation
README
Contributing
MIT license
More
items
DeepSeek Harness
English |
中文
DeepSeek Harness (
dsh
) is an open-source agent harness developed by
DeepSeek AI
.
It uses an architecture where
everything is a plugin
, and is powered by
Cordis
, whose design is described in
A Programming Paradigm for Spatiotemporal Composability
.
Developer preview
DeepSeek Harness is currently in
developer preview
and is iterating rapidly.
THERE WILL BE COMPATIBILITY-BREAKING CHANGES.
Run
Run from
npm
Install
Node.js
, then run:
npx @deepseek-ai/dsh web
The command starts the Web UI, served at
http://127.0.0.1:3080
by default. See
Web UI guide
.
Run from source
To run from a repository checkout:
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd
deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
Community and support
Feel free to submit feedback or bug reports through
GitHub Discussions
.
Add the
dsh-plugin
topic to your plugin repository for discoverability.
Join
DeepSeek Harness Discord community
.
Contributing
See
CONTRIBUTING.md
.
Development
Start with the
development guide
and
architecture documentation
.
For agents, follow
AGENTS.md
.
License
MIT
Third-party dependencies and their licenses are disclosed in
THIRD_PARTY_NOTICES.md
.
About
DeepSeek Harness: Everything is a Plugin.
deepseek.com/harness
Topics
ai-agents
cordis
dsh
dsh-plugin
Resources
Readme
MIT license
Contributing
Contributing
Activity
Custom properties
Stars
131.1k
stars
Watchers
540
watching
Forks
13.1k
forks
Report repository
Contributors
Languages
Footer
© 2026 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Community
Docs
Contact
Manage cookies
Do not share my personal information
You can’t perform that action at this time.
