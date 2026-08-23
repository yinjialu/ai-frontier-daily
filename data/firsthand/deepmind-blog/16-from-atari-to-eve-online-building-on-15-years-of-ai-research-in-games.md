---
type: Article
title: From Atari to EVE Online: Building on 15 Years of AI Research in Games
source: deepmind-blog
resource: https://deepmind.google/blog/from-atari-to-eve-online-building-on-15-years-of-ai-research-in-games
published: 2026-08-21
tags: [游戏AI, 深度强化学习, AlphaGo, AI研究]
detected: 2026-08-23T17:00:52+08:00
---

Google DeepMind回顾15年游戏AI研究历程：从Atari DQN、AlphaGo到与EVE Online等游戏开发商合作，探索AI与游戏融合的新前沿，强调游戏作为AI研究引擎的重要性。

## Full Text

Exploring new frontiers of AI and games research â Google DeepMind
Skip to main content
Explore our next generation AI systems
Explore models
Gemini
Gemini
Build intelligent agents
Gemini Omni
Create anything from anything
Nano Banana
Create and edit detailed images
Gemini Audio
Talk, create and control audio
Specialized models
Veo
Generate cinematic video with audio
Imagen
Generate high-quality images from text
Lyria
Generate high fidelity music and audio
World models & physical AI
Genie 3
Generate and explore interactive worlds
Gemini Robotics
Perceive, reason, use tools and interact
Open models
Gemma
Build responsible AI applications at scale
Our latest AI breakthroughs and updates from the lab
Explore research
Breakthroughs
SIMA 2
An agent that plays, reasons, and learns with you
Genie 3
Generate and explore interactive worlds
AlphaGo
Mastering the game of Go
Gemini Robotics
Perceive, reason, use tools and interact
Learn more
Evals
Publications
Responsibility
Frontier safety
Unlocking a new era of discovery with AI
Explore science
Breakthroughs
AlphaFold
Predict protein structures with high accuracy
WeatherNext
Fast and accurate AI weather forecasting
AlphaEarth
Map our planet in unprecedented detail
AlphaEvolve
Design advanced algorithms for math and applications in computing
Learn more
Gemini for Science
Experimental Tools
Science Skills
Our mission is to build AI responsibly to benefit humanity
About Google DeepMind
Responsibility
Ensuring AI safety through proactive security, even against evolving threats
News
Discover our latest AI breakthroughs, projects, and updates
Careers
Weâre looking for people who want to make a real, positive impact on the world
Learn more
Education
Our National Partnerships for AI
Accelerator programs
The Podcast
Models
Explore our next generation AI systems
Explore models
Gemini
Gemini
Build intelligent agents
Gemini Omni
Create anything from anything
Nano Banana
Create and edit detailed images
Gemini Audio
Talk, create and control audio
Specialized models
Veo
Generate cinematic video with audio
Imagen
Generate high-quality images from text
Lyria
Generate high fidelity music and audio
World models & physical AI
Genie 3
Generate and explore interactive worlds
Gemini Robotics
Perceive, reason, use tools and interact
Open models
Gemma
Build responsible AI applications at scale
Research
Our latest AI breakthroughs and updates from the lab
Explore research
Breakthroughs
SIMA 2
An agent that plays, reasons, and learns with you
Genie 3
Generate and explore interactive worlds
AlphaGo
Mastering the game of Go
Gemini Robotics
Perceive, reason, use tools and interact
Learn more
Evals
Publications
Responsibility
Frontier safety
Science
Unlocking a new era of discovery with AI
Explore science
Breakthroughs
AlphaFold
Predict protein structures with high accuracy
WeatherNext
Fast and accurate AI weather forecasting
AlphaEarth
Map our planet in unprecedented detail
AlphaEvolve
Design advanced algorithms for math and applications in computing
Learn more
Gemini for Science
Experimental Tools
Science Skills
About
Our mission is to build AI responsibly to benefit humanity
About Google DeepMind
Learn more
Education
Our National Partnerships for AI
Accelerator programs
The Podcast
Responsibility
Ensuring AI safety through proactive security, even against evolving threats
News
Discover our latest AI breakthroughs, projects, and updates
Careers
Weâre looking for people who want to make a real, positive impact on the world
Build with Gemini
Try Gemini
Google DeepMind
Google AI
Learn about all our AI
Google DeepMind
Explore the frontier of AI
Google Labs
Try our AI experiments
Google Research
Explore our research
Products and apps
Gemini app
Chat with Gemini
Google AI Studio
Build with our next-gen AI models
Google Antigravity
Our agentic development platform
Models
Research
Science
About
Build with Gemini
Try Gemini
August 21, 2026
Research
From Atari to EVE Online: Building on 15 Years of AI Research in Games
Alexandre Moufarek and Adrian Bolton
Share
Copied
From Atari to Go to StarCraft, games have driven some of the biggest breakthroughs in AI. Now, weâre partnering with game developers to prototype new gameplay experiences that push the frontiers of both gaming and AI.
Since DeepMindâs foundation in 2010, the constrained yet rich worlds of games have played a critical role in understanding intelligence. They have driven some of our biggest AI breakthroughs, from mastering Atari to helping solve protein structure prediction - and they are still at the heart of what we do.
Gaming is in GDMâs DNA. Demis Hassabis, one of Google DeepMind's founders, is himself a former game developer, as are many of us in the GDM team. Together, we have decades of hands-on experience in game development and a deep respect for the craft of making games.
Weâve always been clear that doing AI research with games requires deep partnership with game developers - like our major new
research partnership with Fenris Creations
and the EVE Universe that we unveiled earlier this year, and the work weâve done together with acclaimed studios like
Hello Games
,
Coffee Stain Studios
,
Foulball Hangover
and others.
Games as the engine of AI research
Our journey began when a small team trained a deep neural network to play Atari 2600 games directly from raw pixels. The Deep Q-Network (DQN) learned to play 49 different games â from
Pong
to
Breakout
to
Space Invaders
â without any game-specific engineering. The
2015 Nature paper
on DQN helped catalyze the modern era of deep reinforcement learning.
From there, we attempted to master more complex games, with each milestone producing more capable and general systems.
AlphaGo
defeated world champion Go player Lee Sae Dol in 2016 â a feat many experts thought was still a decade away.
AlphaGo Zero
surpassed every previous version by learning entirely from self-play, with no human data at all.
AlphaZero
generalized this approach to master chess, shogi, and Go with one algorithm, while
MuZero
learned to play without even knowing the rules. In 2019,
AlphaStar
reached Grandmaster level in
StarCraft II
, navigating real-time complexity and imperfect information.
For each game, AI enriched the playing experience. AlphaGo's famous
Move 37
was a play so unexpected that professional commentators initially thought it was a mistake, overturning centuries of received wisdom in Go and inspiring experts to explore new strategies. AlphaZero similarly inspired entirely new lines of play in chess. Crucially, the spirit of exploration that succeeded in games had profound impacts for other AI systems:
AlphaFold
applied these foundations to help solve the 50-year grand challenge of protein structure prediction, a breakthrough which was recognized with the 2024 Nobel Prize in Chemistry.
From mastering games to understanding them
Our earlier work demonstrated that AI could master any game given a clear objective and enough training. But the real world doesn't come with scores and rule books â which led us to ask a fundamentally different question: can AI understand and interact with any game world the way a person would?
This is the challenge behind
SIMA
, our Scalable Instructable Multiworld Agent. Rather than optimizing for a high score, SIMA is a generalist agent that âseesâ what a player would see on screen, understands natural language instructions, and acts through ordinary keyboard and mouse controls â requiring no APIs or source code access.
Powered by Gemini, our frontier AI models,
SIMA 2
acts as an interactive companion capable of real-time reasoning and conversation. It achieves human-like play across complex 3D research environments and video games including
No Man's Sky
,
Valheim
,
Hydroneer
, and more.
For game developers, a truly general gaming agent would unlock AI capabilities that work with existing games â no modifications to the game code required. This could power entirely new gameplay, from AI companions that genuinely understand the game world to Non-Player Characters (NPCs) that adapt and respond in ways that scripted systems never could.
A general gaming agent could also transform how games are made. During development, when the game changes with every commit, such agents could enable truly robust QA testing. Post-launch, when new content is introduced or players behave unpredictably, they could adapt in real time â generalising to new situations without needing to be re-scripted.
To develop SIMA agents safely and responsibly, we've partnered with acclaimed game studios and we are building a growing portfolio of games for AI research. This allows us to challenge our agents with ever more complex tasks that may one day transfer to solving problems in the real world.
Exploring new frontiers of AI and games research, in partnership with game developers
Game studios bring expert craft, extraordinary game worlds, and deep knowledge of their players. We bring frontier AI â from Gemini to research in generative interactive environments and embodied agents â research expertise, and our teamâs unique game development background and years of experience building AI for interactive environments. Together, we focus on discovering breakthrough experiences â never-before-seen gameplay that wouldn't be possible without AI.
It's not about the tech, it's about fun experiences. So we take a âshow, don't tellâ approach with our partners. Our team works hand in hand with game developers, exploring new ideas and building playable prototypes to find the fun.
Our latest research partnership with
Fenris Creations
, the independent studio behind the EVE Universe, represents a new chapter in our history of AI research in games.
Fenris Creations has spent more than two decades building one of the most extraordinary persistent worlds in gaming.
EVE Online
, launched in 2003, is a massively multiplayer space simulation where thousands of players share a single universe that has evolved continuously for more than 20 years. Its player-driven economy features real supply-and-demand dynamics and trade networks spanning thousands of star systems. Its landscape â shaped by alliances, conflicts and diplomacy â is driven by human interaction.
For AI research, this is a golden opportunity. It's a living, evolving world that demands precisely the capabilities we believe are essential for frontier AI:
Continual learning
: Acquiring new skills without forgetting what came before, in a constantly changing world.
Memory:
Accumulating and retrieving knowledge across timescales that extend far beyond today's model context windows.
Long-horizon planning
: Reasoning over weeks, months, or even years.
Complex multi-agent dynamics:
Navigating cooperation, competition, negotiation, economics, and emergent social behavior at scale.
These challenges sit at the core of our broader research initiative to create systems that learn continuously from experience, with the rate of learning accelerating over time. We believe these frontier capabilities could unlock new gameplay experiences in the future.
EVE Online was envisioned from day one as a sandbox of lasting consequences, shaped by its players. This has driven countless stories of human growth for players and employees across the decades. Together with Google DeepMind, weâre pushing into uncharted territory where AI must learn, adapt and remember on timescales that no other game environment demands, while helping us understand how humans and AI can coexist in a virtual environment before we have to contend with the same questions in real life.
Hilmar PÃ©tursson
CEO of Fenris Creations
Our research partnership extends across Fenris Creations' expanding universe, offering distinct environments for AI development. While
EVE Online
offers a large-scale single-shard persistent universe,
EVE Vanguard
is played from a first-person perspective, bringing ground-level, fast-paced tactical decision-making to the broader persistent world. This creates opportunities to study agents operating across multiple levels of abstraction, from twitch-level tactics to galaxy-spanning strategy.
Furthermore,
EVE Frontier
â with its programmable "Smart Assembliesâ and its open, extensible architecture â offers an open-ended environment where the very rules of the world can change, demanding agents that adapt to entirely new game mechanics.
A âshow, donât tellâ session during a workshop with Google DeepMind and Fenris Creations where our teams share playable prototypes, feedback and discuss ideas for new gameplay experiences
Our collaboration has already delivered real player value: the
Aura Guidance
system uses Gemini to deliver player-generated knowledge, based on real Rookie Help questions and answers, to help new pilots.
Our longer-term research program begins with an offline instance of EVE Online, which is a safe sandbox, separate from live players. It then progresses through EVE Frontier as a space to study how humans and agents can coexist in a persistent and open-ended world. Only when capabilities are mature would we consider bringing them to EVE Online and EVE Vanguard with the aim of enriching human play.
The road ahead
Games have always been a mirror for intelligence. As they become more complex, more persistent, and more open-ended, so do the AI systems we build to navigate them.
We are aiming for the same ultimate goal we always have: AI as a catalyst, not a replacement. Our long-term ambition is to unlock breakthrough gameplay experiences, make games more accessible and more personalized, and â as we've seen from AlphaGo to AlphaFold â apply what we learn in games to problems in the real-world and to advance scientific discovery.
We're grateful to all of our game partners on this journey, and to Fenris Creations for joining us on this next chapter. We can't wait to share what we discover.
Learn more about SIMA 2
Learn more about our partnership with Fenris Creations
Acknowledgements
Weâd like to recognize the many teams across Google DeepMind for their contributions over the years to advancing AI research safely and responsibly in games.
Special thanks to all of the game developers who partnered with us: Coffee Stain (
Valheim, Satisfactory, Goat Simulator 3),
Fenris Creations (EVE Online, EVE Vanguard, EVE Frontier), Foulball Hangover (
Hydroneer),
Hello Games (
No Man's Sky),
Keen Software House (
Space Engineers),
RubberbandGames (
Wobbly Life),
Strange Loop Games (
Eco),
Thunderful Games (
ASKA, The Gunk, Steamworld Build
), Digixart (
Road 96
), and Tuxedo Labs & Saber Interactive (
Teardown).
Related posts
SIMA 2: An Agent that Plays, Reasons, and Learns With You in Virtual 3D Worlds
November 2025
Research
Learn more
Follow us
Sign up for updates on our latest innovations
I accept Google's Terms and Conditions and acknowledge that my information will be used in accordance with
Google's Privacy Policy
.
Sign up
Build AI responsibly to benefit humanity
Models
Gemini
Gemini Omni
Nano Banana
Gemini Audio
Gemma
Genie
Lyria
Veo
Research
Gemini Robotics
Breakthroughs
Evals
Publications
Frontier safety
Responsibility
Science
AlphaFold
AlphaGenome
WeatherNext
AlphaEarth
AlphaEvolve
Products
Gemini app
Google AI Studio
Google Antigravity
Learn more
About
News
Careers
National Partnerships for AI
Accelerator programs
The Podcast
About Google
Google products
Privacy
Terms
Cookies management controls
