---
type: Article
title: Gemini Robotics 2 brings whole body intelligence to robots
source: deepmind-blog
resource: https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots
published: 2026-07-28
tags: [Gemini Robotics 2, VLA, 具身智能, 机器人控制]
detected: 2026-08-02T17:00:22+08:00
---

Google DeepMind发布Gemini Robotics 2，作为机器人智能层，赋予机器人全身控制、精细操作与多机器人协作能力。该VLA模型可将视觉与语言输入转化为电机控制，支持人形机器人及双臂机器人，并能快速适配新机器人本体，实现本地化运行。

## Full Text

Gemini Robotics 2 brings whole body intelligence to robots â Google DeepMind
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
July 30, 2026
Models
Gemini Robotics 2 brings whole body intelligence to robots
Carolina Parada
Share
Copied
Your browser does not support the video tag.
From feet to fingertips â we are teaching robots intelligent whole-body control, fine dexterity, and teamwork to complete a broad range of complex tasks
For decades, weâve dreamed of robots that can seamlessly step into our world and lend a hand. Now, that vision takes a significant stride forward.
Most robots are pre-programmed or teleoperated for narrow, repetitive task sequences. They lack the ability to truly learn for themselves or adapt to unpredictable environments. Moreover, transferring learned skills from one robot body to another remains incredibly difficult. To take on the hardest problems at scale, robots of every shape and size need AI models giving them the ability to think, act, and interact intelligently to safely complete tasks.
We demonstrated how Gemini's multimodal understanding could drive real-world action with
Gemini Robotics
. Today, we are introducing Gemini Robotics 2 - the intelligence layer powering the next generation of truly adaptable robots. As it takes its first literal steps, this major advance unlocks intelligent whole-body control, advanced dexterity, and multi-robot collaboration.
Gemini Robotics 2 enables robots to reason through every movement, unlocking a broad range of tasks. For example, it can enable a humanoid to walk, crouch, stretch, and manipulate objects to clean up a cluttered room. It can even team up with other robots to finish the job faster. And this profound intelligence can also run locally on-device while seamlessly adapting to entirely new robotic bodies in just a few hours.
We are making this possible through three highly capable models:
Gemini Robotics 2
: Our most advanced vision-language-action model (VLA) that converts vision and language input into motor control, enabling a robot to take action. This model is capable of controlling full humanoids, from feet to fingertips, and other bi-arm robots. It also brings a new level of dexterous manipulation on both hands and grippers.
Gemini Robotics ER 2
: Our most capable embodied reasoning (ER) model. It is a vision language model (VLM) that acts as our agent, enabling robots to communicate with humans, understand the physical world and plan multi-step tasks lasting several minutes. We are also introducing the ability for robots to work together as a team.
Gemini Robotics On-Device 2
: Our most efficient vision-language-action model (VLA) optimized to run locally on robotic devices. This model can now achieve fast adaptation to completely new robot embodiments with a few hours of data.
Slide 1 of 3
Gemini Robotics 2 controlling three different embodiments, using the same model checkpoint â the Apptronik Apollo 2 robot with SharpaWave hands, the Apollo 2 robot with Inspire hands, and the Franka Duo with the Robotiq gripper â on a wide variety of whole-body and dexterous manipulation tasks. Each bar represents the average success rate over multiple tasks within the same skill category. For multifinger tasks we show individual task performance. While Gemini Robotics 2 achieves a medium to high success rate for whole-body and gripper-based dexterous tasks, the multi-finger dexterous manipulation remains challenging.
Gemini Robotics ER 2, our reasoning model, is now available on
Google AI Studio
and in private preview on
Gemini Enterprise Agent Platform
. Our VLA and On-Device models are available to
early-access partners
. Read how to bring these models to your hardware on our
Developer blog
.
Humanoids in motion: Managing whole-body tasks
The world is built for human movements; it requires us to reach, bend, and balance in tight, cluttered spaces. While our previous models controlled the humanoidâs upper-body to achieve table-top tasks, Gemini Robotics 2 expands physical AI into whole-body motions.
For the first time, our model can now control entire humanoid robots, translating intent into intelligent whole-body control. For example, when controlling
Apptronikâs Apollo 2
humanoid robot, we can ask it to
âput the watering can into the green bin in the bottom shelf.
â Apollo processes the instruction, walks to the table, and picks up the watering can, takes a few steps to the shelves, and places it precisely in its destination. While our robots have more to advance in movement speed, this is an important step towards the skills needed to complete more complex, real-world tasks that require whole-body coordination.
Your browser does not support the video tag.
Bringing advanced dexterity to hands and grippers
To be genuinely useful in our homes and workplaces, robots need finesse. Gemini Robotics 2 unlocks a new level of physical dexterity across different end effectors, whether a robot is using hands or grippers, enabling robots to be more useful than ever before.
The model can now control the five-fingered, 22 degree-of-freedom SharpaWave hand on the Apollo 2 robot to complete delicate actions like tying knots or sealing a ziplock bag. It can also operate standard two-fingered parallel grippers on a
Franka Duo platform
to perform complex dexterous tasks (e.g. tight packing). We are continuing to advance the level of precision and speed to achieve human-level dexterity.
Your browser does not support the video tag.
Unlocking advanced tasks with agentic reasoning and multi-robot collaboration
Most real-world tasks require multiple steps over an extended period of time. To manage this complexity, our embodied reasoning (ER) model, Gemini Robotics ER 2, serves as the robotâs high-level brain, processing user instructions and communicating with humans. It observes the room, reasons about the steps needed to complete the task, coordinates with the VLA to carry out the actions, and tracks progress until the task is done. This setup allows robots to execute complex multi-step tasks, self-correct if a step fails, and generalize to novel situations and goals.
In this update, we are enabling robots to more reliably execute longer task sequences, lasting several minutes and involving hundreds of decisions. Gemini Robotics ER 2 now understands when tasks begin and end, and can pinpoint the moment key events occur, marking a step change in progress understanding.
Furthermore, we are introducing multi-robot collaboration. This enables different types of robots to communicate and work together to solve complex workflows a single robot could not do alone.
Your browser does not support the video tag.
Adapting fast on-device models for any robot
Many robotic applications need to operate without network latency or internet connectivity. Gemini Robotics On-Device 2 is built specifically to handle these constraints â it is our most-efficient vision-language-action model (VLA) optimized to run locally on robotic devices.
This model is natively multi-embodiment and inherits our advanced âmotion transferâ techniques from
Gemini Robotics 1.5
. We can now adapt to new bi-arm robot embodiments with just a few hours of adaptation time, typically with less than 200 examples. This works even with new embodiments with drastically different shapes, sensors and degrees of freedom, as shown below with a diverse set of tasks being performed by the Dexmate, SO101, and Trossen platforms.
Your browser does not support the video tag.
Advancing our commitment to safe and responsible robotics
Safety is foundational to our robotics research. As robots gain more physical capabilities, we are committed to ensuring end-to-end safety and alignment. With each release, weâve taken a multi-layered approach that combines traditional physical safety measures with robust AI safety frameworks.
Gemini Robotics 2 specifically advances robotics safety for navigating the uncertainty of the real world and collaborating alongside humans.
Weâre introducing
ASIMOV-Agentic
, a new benchmark for agentic safety orchestration and uncertainty resolution. For example, it measures the embodied reasoning agentâs ability to refuse unsafe tool calls from a VLA.It also measures the agentâs ability to predict whether a task is possible and to proactively request human intervention when uncertain.
Additionally, with enhanced embodied reasoning, Gemini Robotics ER 2 is our safest robotics model to date in safety constraint following and human proximity benchmarks. It can better detect when humans are nearby, trigger safety tool calls and bring the robot to a safe stop if someone approaches too closely. This is a key requirement in collaborative safety standards. Read our
Gemini Robotics 2: Safety Technical Report
for more details.
Building towards general-purpose physical AI
Gemini Robotics 2 marks an important milestone on the path toward solving AGI in the physical world. Unlocking the true potential of robotics requires moving past single-task automation toward general-purpose intelligence. By building this core intelligence, our goal is to enable AI in the physical world that can work alongside humans to solve complex challenges.
Explore Gemini Robotics 2
Try in Google AI Studio
View Gemini Robotics ER 2 Model Card
View Gemini Robotics On-Device 2 Model Card
Learn more on the Developer blog
Sign up for our Trusted Tester Program
Try in Gemini Enterprise Agent Platform (Private Preview)
Acknowledgements
This work was developed by the Gemini Robotics team: Abhijit Ogale, Abhishek Jindal, Adil Dostmohamed, Adrian Collister, Alan Thompson, Alessio Quaglino, Alex Bewley, Alex Hofer, Alex Taeho Kim, Alex X. Lee, Alex Zihao Zhu, Allen Chai, Amaris Paryag, Amit Hampaul, Amy Nommeots-Nomm, Amy Shen, Andre Araujo, Anirudha Majumdar, Anna Volosina, Annie S. Chen, Annie Xie, Anthony Brohan, Antoine Laurens, Arunkumar Byravan, Asaf Revach, Assaf Hurwitz Michaely, Baruch Tabanpour, Ben Moran, Benoit Landry, Bingyi Cao, Bogdan Mazoure, Brandon Hernaez, Brijen Thananjeyan, Bryan Anenberg, Caden Lu, Carl Doersch, Carolina Parada, Charles Shu, Chengda Wu, Christine Chan, Christy Koh, Chuyuan Fu, Claire Cui, Clare Lee, Claudio Fantacci, Connor Schenck, David Rendleman, Deepali Jain, Demetra Brady, Dennis Li, Dhruv Shah, Dimple Vijaykumar, Dirk Ehrlich, Divya Garikapati, Dmitry Kalashnikov, Dre Mahaarachchi, Dushyant Rao, Erik Frey, Fangchen Liu, Francesco Romano, Frankie Garcia, Gabor Simko, Gautam Salhotra, Giulia Vezzani, Grace Popple, Grace Vesom, Graziano Misuraca, Guangyao Zhou, Hagen Soltau, Hanzi Mao, Hao-Tien Lewis Chiang, Harris Chan, Hila Noga, Howard Zhou, Ian Storz, Idan Lev-Yehudi, Ignacio Rocco, Inessa Konstanz, Isaac Reid, Ishita Prasad, Ivan Kapelyukh, J. Chase Kew, Jacky Liang, Jake Varley, James Susilo, Jasmine Hsu, Jerad Kirkland, Jeremy Plassmann, Jessica Lo, Jie Tan, Jimmy Yan, Jingwei Zhang, Jinyu Xie, Jose Enrique Chen, Joshua Ainslie, Joss Moore, Juanita Bawagan, Junkyung Kim, Justin Lidard, Kanishka Rao, Kathryn Quinn Shea, Kaustubh Sridhar, Keerthana Gopalakrishnan, Ken Caluwaerts, Kenneth Oslund, Khimya Khetarpal, Konstantinos Bousmalis, Krista Reymann, Krzysztof Choromanski, Ksenia Konyushkova, Kun Zhang, Kunal Aneja, Laura Graesser, Leen Verburgh, Leonard Hasenclever, Li-Heng Lin, London Chappellet-Volpini, Lucie Kerley, Maria Attarian, Maria Bauza Villalonga, Marissa Giustina, Max McCabe, Meet Kirankumar Dave, Mehdi S. M. Sajjadi, Metin Toksoz-Exley, Michael Neunert, Michael Noseworthy, Michiel Blokzijl, Miguel Rivas, Mithun George Jacob, Mitsuhiko Nakamoto, Mo Dawoud, Mohan Kumar Srirama, Mohit Sharma, Mohit Shridhar, Muinat Abdul, Murilo F. Martins, Nathan Batchelor, Nicolas Heess, Niko Milonopoulos, Norman Di Palo, Oliver Groth, Ouais Alsharif, Padmini Copparapu, Parth Parekh, Paul Ruiz, Paul Wohlhart, Peide Huang, Peng Xu, Peter Pastor, Petko Yotov, Phil Duffy, Philemon Brakel, Rachel Sterneck, Rajkumar Vasudeva Raju, Ravin Kumar, Razvan Surdulescu, RenÃ© Wagner, Reza Sanatinia, Robert Baruch, Robert Moreno, Rohan Thakker, Roland Hafner, Sajjad Zafar, Sally Jesmonth, Sam Haves, Saminda Abeyruwan, Sandy Han Huang, Scott Crowell, Seliem El-Sayed, Sergey Yaroshenko, Sergio Martinez Abad, Serkan Cabi, Sharath Maddineni, Shuang Li, Sichun Xu, Silvia Cruciani, Skanda Koppula, Skye Yang, Soo Sung, Stefan Welker, Stefani Karp, Stefano Saliceti, Steven Hansen, Stuart Bowers, Sumeet Singh, Svetlana Grant, Takahiro Miki, Takuma Yoneda, Thomas Buschmann, Thomas Lampe, Thomas Power, Thor Schaeff, Tim Hertweck, Tingnan Zhang, Todd McInally, Todor Davchev, Tong Zhao, Travers Rhodes, Tsang-Wei Edward Lee, Vika Koriakin, Vikas Sindhwani, Wenhao Yu, Wentao Yuan, Xiaolin Fang, Yahav Nussbaum, Ying Sheng, Ying Xu, Yuheng Kuang, Yuxiang Yang, Yuxiang Zhou
For their leadership and support of this effort, weâd like to thank: Jean-Baptiste Alayrac, Zoubin Ghahramani, Koray Kavukcuoglu and Demis Hassabis. Weâd like to recognize the many teams across Google and Google DeepMind that have contributed to this effort including Legal, Marketing, Communications, Responsibility and Safety Council, Responsible Development and Innovation, Policy, Strategy and Operations, and our Business and Corporate Development teams. Weâd like to thank everyone on the Robotics team not explicitly mentioned above for their continued support and guidance. Finally, weâd like to thank our partners: Apptronik, Boston Dynamics, and Agile Robots teams for their support.
Related posts
Gemini Robotics
Learn more
Gemini Robotics ER 2: powering robotics with video understanding, task orchestration, and multi-robot collaboration
July 2026
Models
Learn more
Gemini Robotics-ER 1.6: Powering real-world robotics tasks through enhanced embodied reasoning
April 2026
Models
Learn more
Gemini Robotics 1.5 brings AI agents into the physical world
September 2025
Models
Learn more
Gemini Robotics brings AI into the physical world
March 2025
Models
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
