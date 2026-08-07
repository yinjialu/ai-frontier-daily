---
type: Article
title: WeatherNext: AI model achieves breakthrough in forecasting cyclones
source: deepmind-blog
resource: https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones
published: 2026-08-06
tags: [AI天气预报, 气旋预测, DeepMind, 开源模型]
detected: 2026-08-06T21:35:42+08:00
---

Google DeepMind的WeatherNext模型在Nature发表，实现气旋路径、强度和风结构的高精度预测，平均提前一天预警，相当于气象学十年进展，并已在实际飓风季应用，现开源模型。

## Full Text

AI model achieves breakthrough in forecasting cyclones â Google DeepMind
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
August 6, 2026
Science
WeatherNext: AI model achieves breakthrough in forecasting cyclones
WeatherNext team
Share
Copied
WeatherNext enables accurate cyclone forecasts that can give an extra day of warning. Now we are open sourcing the model.
Predicting how dangerous cyclones develop is a longstanding challenge where every hour counts. Tropical cyclones â also known as hurricanes or typhoons â are among the most destructive weather phenomena on Earth, responsible for more than 700,000 deaths and $1.4 trillion in economic losses globally over the past 50 years. For forecasters, issuing timely, accurate warnings is a constant race against time.
Today, in a paper published in
Nature
, we show that our WeatherNext AI model achieved state-of-the-art accuracy in predicting a cyclone's track, intensity, and wind structure. On average, our model gives forecasters an extra dayâs worth of predictive accuracy: our three-day forecasts are as good as what prior models were able to provide for only the next two days. This scale of improvement corresponds roughly to a decadeâs worth of meteorological progress.
This collaborative work brought together AI researchers and engineers at Google DeepMind and Google Research, with expert forecasters at the
National Hurricane Center
(NHC), the
Cooperative Institute for Research in the Atmosphere
(CIRA), the
UK Met Office
, and weather agencies around the world.
Our research has already had real-world impact. During the 2025 hurricane season, our model helped the NHC to make a
historic forecast for Hurricane Melissa
by predicting the stormâs rapid intensification and landfall in Jamaica. This enabled the NHC to issue an advance warning, giving teams on the ground critical time to prepare. This year, we continue to work together and are now predicting 1,000 possible scenarios for each cyclone to help support forecasters in their decision-making.
Weather affects everyone. Given this broad impact, we are now
open sourcing
our WeatherNext 2 and WeatherNext Cyclones models used during the hurricane season. By making this technology openly available, we hope to empower the research community and amplify AI's impact in building more resilient communities â whether that be providing local forecasters with the tools they need to
prepare for natural disasters
, supporting the growth of renewable energy, or anticipating extreme weather.
How WeatherNext predicts weather and cyclones
Starting from global atmospheric conditions during Hurricane Milton (October 2024), WeatherNext Cyclones iteratively predicts both global weather patterns and fine-scale cyclone tracks up to 15 days in advance. Running a 1,000-member ensemble generates localised probability maps of tropical storm to hurricane-force winds.
Predicting cyclones has typically forced a trade-off requiring two distinct modeling techniques. A cyclone's track (where it goes) is steered by massive, global atmospheric currents, which before now have been best modeled by coarser global models. However, a cycloneâs intensity (how strong it gets) is driven by highly localized, fine-scale thermodynamic physical processes around its core, which are best modeled by specialized, higher resolution, local models.
Our WeatherNext model bridges this gap by improving forecasting for global weather overall as well as cyclones. It is a single AI model that predicts a tropical cycloneâs track, intensity, and wind structure with state-of-the-art accuracy. It achieves this breakthrough through a unique combination of its training, architecture and approach to low resolution inputs.
We evaluated WeatherNext Cyclones on historical cyclones from 2023 to 2024, benchmarking its deterministic and probabilistic performance against other top weather models. On average, WeatherNext Cyclones gains more than a full day (24 hours) of lead time advantage for predicting cyclone tracks, intensity, and wind structure.
The model was co-trained on two distinct data modalities: global weather dynamics and expert-curated historical cyclone observations. By training end-to-end on nearly 20 terabytes of global atmospheric data and the historical IBTrACS database spanning nearly 5,000 historical storms, the model learns complex atmospheric patterns and how to model extreme weather.
Cyclone forecast accuracy has been steadily advancing over recent decades. The plots show the 3-day accuracy of ECMWF-ENS track forecasts (a) and HWRF intensity forecasts (b) over the years, and how WeatherNext Cyclones contributes a step change in accuracy for both track and intensity. This improvement is the equivalent to a one-decade progress according to trends over the last 20 years.
Our model uses
Functional Generative Networks (FGNs)
to efficiently produce ensembles of different predictions, which captures the inherent uncertainty of the weather. We can now generate a single 15-day forecast in less than a minute on a TPU, empowering forecasters to quickly evaluate the probability distribution of potentially devastating tail-risks. Last year, our system produced 50 predictions at a time, matching global physics models. This year we scaled our ensemble size to 1,000 members, capturing rare but consequential scenarios like rapid intensification events, as occurred during Hurricane Melissa in 2025.
Up until now, operating at very high spatial resolution has been considered the main driver for making accurate intensity forecasts. However, WeatherNext Cyclones only needs data with a resolution of 28x28km, 100x coarser than traditional models. A smaller version of the model, WeatherNext 2-mini, which operates at a coarser 111x111km resolution, also shows great performance. This has surprised scientists, and it remains an open research question to fully understand how our models produce such accurate predictions at this resolution. We hope that, together with the research community, we can find out.
Opening up WeatherNext to the research community
Alongside our
Nature
paper, we are
open sourcing
the code and model weights, making them freely available for anyone to build on. This includes academic research, operational forecasting, or developing more specialized, localized models. We hope to accelerate progress across the global weather community and empower meteorological agencies, researchers, and nonprofits to better predict weather events of all kinds and make key decisions to protect lives and infrastructure.
We are also releasing two sets of similar models: WeatherNext Cyclones, which ran during the hurricane season (results can be seen in the paper); and WeatherNext 2, a later update that we operationalized in October. Additionally, we are releasing WeatherNext 2-mini, a compact version of the model that can run on a single TPU in a free public
Colab notebook
.
You can explore our latest cyclone forecasts on
Weather Lab
, which we recently refreshed with a new interface and expanded to include global weather forecasts alongside cyclone tracks. Weather Lab now lets you visualize WeatherNext predictions for temperature, precipitation, wind speed, and more, all in a single view. Both Weather Lab and WeatherNext models are a part of
Google Earth AI
.
Pushing the frontiers of AI for weather forecasting
We have achieved a historic breakthrough by gaining more than a full day of lead time for predicting cyclones â delivering an advance equivalent to a decade of meteorological progress. As we prepare for future storm seasons, we invite researchers, meteorological agencies, and experts to partner with us, build on our open source models, and explore our forecasts on Weather Lab. By combining advanced machine learning with the indispensable real-world expertise of human forecasters, we aim to create a collaborative weather forecasting ecosystem that can save lives and help communities adapt to a changing climate.
Note: For official weather forecasts and warnings, refer to your local meteorological agency or national weather service.
Read our Nature paper
Download the code
Explore Weather Lab
Read the NHCâs 2025 Verification Report
Acknowledgements
This research was co-developed by Google DeepMind and Google Research teams.
Weâd like to thank our collaborators NOAA/NWS/NCEP National Hurricane Center, Cooperative Institute for Research in the Atmosphere (CIRA) and the UK Met Office for their partnership and contributions to the paper.
This work reflects the contributions of the paperâs co-authors: Ferran Alet, Tom Andersson, Ilan Price, Stratis Markou, Andrew El-Kadi, Dominic Masters, Amy Li, Samier Merchant, Natalie Williams,Gregory Thornton, Ken MacKay, Olivia Graham, Akib Uddin, Ben Gaiarin, Devaja Shah, Elinor Kruse, Wallace Hogsett, David Zelinsky, John Cangialosi, Jonathan Martinez, James Franklin, Mark DeMaria, Kate Musgrave, Caroline L. Bain, Helen Titley, Jacklynn Stott, Remi Lam, Aaron Bell, Paul Komarek, Matthew Willson, Alvaro Sanchez-Gonzalez, and Peter Battaglia.
Related posts
WeatherNext 2
Learn more
How WeatherNext helped the National Hurricane Center better predict Hurricane Melissaâs historic landfall in Jamaica
May 2026
Science
Learn more
GenCast predicts weather and the risks of extreme conditions with state-of-the-art accuracy
December 2024
Science
Learn more
GraphCast: AI model for faster and more accurate global weather forecasting
November 2023
Science
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
