---
type: Article
title: Introducing GPT-Live
source: openai-news
resource: https://openai.com/index/introducing-gpt-live
published: 2026-07-08
tags: [全双工语音, GPT-Live, 连续交互, AI对话系统]
detected: 2026-07-09T04:39:38+08:00
---

OpenAI发布GPT-Live，采用全双工架构实现同时听说的连续交互，支持实时决策与打断，并可委托GPT-5.5处理复杂任务，显著提升语音对话自然度与智能化水平。

## Full Text

Introducing GPT-Live | OpenAI
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
Product
Release
Introducing GPT‑Live
A new generation of voice models for natural human-AI interaction, now powering ChatGPT Voice.
Loading…
Share
We’re launching GPT‑Live, a new generation of voice models that make talking with AI feel much more like having a real conversation.
GPT‑Live is built on a full-duplex architecture, meaning it can listen and speak at the same time. During conversations, GPT‑Live can show it’s paying attention with phrases like “mhmm” or “yeah”, engage in quick back-and-forth, or just stay quiet when you need a moment to think. The result is a voice experience that is refreshingly easy to talk to.
GPT‑Live is also our smartest voice model yet. For questions that require web search, deeper reasoning, or more complex work, it delegates to our latest frontier model behind the scenes and brings the result back into the conversation when it’s ready. While it works, GPT‑Live can keep talking with you and maintain the flow of conversation. At launch, GPT‑Live will use GPT‑5.5 in the background. As we release new frontier models, we’ll continuously update the model used by GPT‑Live.
These advances power a new ChatGPT Voice experience that is more intelligent and natural to use. Over time, we believe this research will also unlock the ability to use voice for increasingly complex, longer-running, and more agentic work.
We’re beginning to roll out two versions of GPT‑Live –
GPT‑Live‑1
and
GPT‑Live‑1 mini
– to ChatGPT users globally today. We also plan to bring them to the API soon, and developers and enterprises can sign up to be notified using this
form
⁠
.
Entering a new era of human-AI interaction
Our vision is to enable truly natural human–AI interaction: a world where collaborating with AI feels as fluid and responsive as working with another person, while reasoning and complex task execution happen seamlessly in the background.
Previous approaches
Older generations of voice AI systems brought us closer to that vision, but with important tradeoffs.
Cascaded voice systems
Cascaded voice systems rely on a series of models acting one after another to process each turn. The
original ChatGPT Voice
chained three models together: a speech-to-text model to transcribe your speech, a large language model to produce a response, and a text-to-speech model to convert it back into speech. This approach enabled us to talk to frontier AI models for the first time, but the complexity came at a cost: information could be lost across models, and responses were slow and stilted.
Cascaded voice system
Slow and stilted responses, long pauses
STT
GPT-5.5
TTS
STT
GPT-5.5
TTS
Transcript
Example conversation with Standard Voice Mode, using GPT-5.5 Instant
Turn-based voice models
Turn-based voice models like
ChatGPT Advanced Voice Mode
processed and generated audio within a single model, reducing latency and making conversations smoother — but they still operated through discrete turns. The model had to wait for the user to stop speaking before responding, resulting in rigid back-and-forth. In addition, because turn detection is based on silence, even a brief pause or background noise could be mistaken for the end of turn — causing the model to interrupt at unnatural times.
Turn-based voice model
Slightly faster and smoother responses, but back-and-forth with the model still feels rigid
Transcript
Example conversation with ChatGPT Advanced Voice Mode
Our new approach
GPT‑Live
addresses these limitations through two architectural changes.
Continuous interaction
First, we built GPT‑Live for continuous interaction using a full-duplex architecture
.
Instead of processing a sequence of separate messages, GPT‑Live continuously processes input while generating output. The model can therefore make interaction decisions many times per second: whether to speak, continue listening, pause, interrupt, or invoke a tool.
This allows the model to engage in more natural back-and-forth, maintain a better sense of time, and even perform live translation.
Continuous interaction
Fast, natural, expressive responses and more active listening
User
GPT-Live-1
Transcript
Example conversation with GPT-Live-1, using GPT-5.5 Instant
Delegation for deeper work
Second, we decoupled GPT‑Live — which handles continuous interaction — from deeper work. When a question requires search, reasoning, or more agentic capabilities, GPT‑Live can delegate the task to another model like GPT‑5.5. This allows it to keep the conversation going, even as it handles multiple tasks in the background.
This architectural change also allows GPT‑Live to continuously use the latest models and agents, combining frontier intelligence with natural interaction.
Delegation for deeper work
GPT-Live provides fast, natural responses, while GPT-5.5 handles search in the background
User
GPT-Live-1
GPT-5.5
Search + reason
Transcript
Example conversation with GPT-Live-1, using GPT-5.5 Instant
Evaluations
We built new human evaluations to measure pleasantness and the flow of conversation. In these head-to-head comparisons, GPT‑Live‑1 and GPT‑Live‑1 mini are strongly preferred over Advanced Voice Mode in matched 5–10 minute conversations that measure overall preference, turn-taking, interruptions, conversational flow, and how natural each interaction felt.
GPQA: GPT‑Live‑1 substantially outperforms Advanced Voice Mode on GPQA, which tests expert-level scientific reasoning across biology, chemistry, and physics.
BrowseComp: GPT‑Live‑1 shows strong gains over Advanced Voice Mode on BrowseComp, which tests agentic web search and the ability to find difficult-to-locate information.
τ³-Voice Telecom (internal variant)**: GPT‑Live‑1 outperforms Advanced Voice Mode on τ³-Voice Telecom, which tests voice agents on realistic, multi-turn telecom support tasks.
* GPT‑Live‑1 (instant) and GPT‑Live‑1 mini use the GPT‑5.5 Instant model in the background, while GPT‑Live‑1 Medium and GPT‑Live‑1 High use the GPT‑5.5 Thinking model with medium and high reasoning effort.
**
We used a customized user model, powered by our latest reasoning models, for this eval.
A new ChatGPT Voice experience
Each week, more than 150 million people talk to ChatGPT using features like Voice and Dictation. They use it to get hands-free everyday help, to practice languages, tell bedtime stories, or just chat during their commute.
Starting today, when you tap the Voice button to talk with ChatGPT, you’ll get an improved experience powered by GPT‑Live—with more natural conversations, smarter answers, better listening, and visual responses.
More natural conversations
Talking with ChatGPT should now feel much more like a real conversation. You can interrupt with a question, pause to gather your thoughts, or ask ChatGPT to slow down. It naturally acknowledges what you’re saying with phrases like “mhmm” or “got it,” so you know it’s following along. We’ve also remastered the nine distinct voices in ChatGPT for GPT‑Live.
Smarter answers
ChatGPT Voice can now draw on our latest frontier models, giving you smarter answers when you need them. You can also choose the level of reasoning that fits your needs: Instant for fast responses, or Medium and High when you want ChatGPT to spend more time thinking.
Better listening
If you take a moment to think, ChatGPT Voice now waits instead of jumping in and interrupting. If you ask it to stay quiet and listen, it will. And when there’s background noise, like passing traffic or nearby conversations, ChatGPT is better at focusing on your voice instead of getting distracted.
Visual answers at a glance
Some answers are more useful when you can see them. While you’re talking, ChatGPT can now show rich visual cards for topics like weather, stocks, sports, and more. Voice also continues to support search, memory, images, and file uploads.
The result is a ChatGPT Voice experience that feels more natural, more capable, and more useful in everyday life.
Safety designed for voice
GPT‑Live was designed to be safe by default. It builds on the safety advances from our latest models while adding dedicated safety training across key risk areas and new safeguards designed specifically for voice.
Expanded safety testing
To better reflect how people use voice in real-life settings, we began by expanding our safety testing to include new audio-native evaluations. We also created synthetic evaluations that use generated audio to focus more intensively on key safety areas, drawing on what we learned from Advanced Voice Mode. Those areas include self-harm, psychosis and mania,
emotional reliance on AI
, violence, and sexual content. Internal experts also red-teamed the model for risks unique to voice.
In our testing, GPT‑Live performed comparably to or better than Advanced Voice Mode across nearly all of the areas we evaluated. You can read more about our testing and safeguards in the GPT‑Live
system card
⁠
(opens in a new window)
.
Built-in safeguards
Because voice conversations unfold in real time, we also built safeguards that can act while the model is speaking. When the system detects potentially unsafe output, it can steer the model toward a safer response, surface additional safety messaging or resources, or end the voice conversation in higher-risk cases. For conversations involving self-harm, we adapted ChatGPT’s support flows for voice, including offering expert-vetted crisis helpline support.
We designed additional protections to support teen users, and trained age-appropriate behavior directly into the model to reduce the risk of inappropriate responses. Parents can choose whether their teen can use ChatGPT Voice through Parental Controls, and linked parents may be notified in higher-risk situations involving signs of potential self-harm or suicidal intent.
Learning from real-world use
We’re also rolling out longer-term measurement and post-launch monitoring focused on emotional reliance to continue improving our understanding and refining safeguards. Building on our previous research into
affective use and emotional well-being
, this will help us identify emerging patterns and improve how the system responds in emotionally sensitive interactions.
Finally, GPT‑Live is designed for conversation, not voice impersonation. It uses a set of predefined voices in ChatGPT, with safeguards to prevent it from imitating a real person’s voice.
We’re committed to supporting safety and well-being and will keep strengthening these protections as we learn from real-world use.
Availability & limitations
GPT‑Live is rolling out now to ChatGPT users globally across iOS, Android, and
ChatGPT.com
⁠
(opens in a new window)
. GPT‑Live‑1 will become the default model powering ChatGPT Voice for Go, Plus, and Pro users, and GPT‑Live‑1 mini will become the default for Free users. More availability details can be found in our
Help Center
⁠
(opens in a new window)
.
We’ve optimized GPT‑Live for some of the most popular languages in ChatGPT. For certain languages, the model may have a non-native accent or gaps in fluency. We’re actively working to improve the experience across languages.
At launch, GPT‑Live will not support voice with video or screen sharing in ChatGPT, but we’re working to introduce these capabilities soon. You can still access legacy versions of ChatGPT Voice, including Standard and Advanced Voice Mode, where these features are available.
2026
ChatGPT
Author
OpenAI
Keep reading
View all
Previewing GPT-5.6 Sol: a next-generation model
Product
Jun 26, 2026
New usage analytics and updated spend controls for enterprises
Product
Jun 18, 2026
Improving health intelligence in ChatGPT
Product
Jun 18, 2026
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
