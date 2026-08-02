---
type: Article
title: Operation “Stop News”: Recidivist influence activity
source: openai-news
resource: https://openai.com/index/disrupting-malicious-uses-of-ai-stop-news-2025
published: 2025-10-01
tags: [AI安全, 虚假信息, 影响力行动, OpenAI]
detected: 2026-08-02T17:00:22+08:00
---

OpenAI封禁俄罗斯背景的“Stop News”再犯影响力行动，该行动利用ChatGPT生成文本、视频脚本及SEO描述，针对非洲和英国传播亲俄内容，但影响力有限。

## Full Text

Operation “Stop News”: Recidivist influence activity | OpenAI
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
October 1, 2025
Operation “Stop News”: Recidivist influence activity
OpenAI banned accounts linked to a Russia-origin operation we dubbed “Stop News”, using AI to generate recidivist influence content targeting Africa and the UK.
Loading…
Share
This case study was originally published in OpenAI’s
October 2025
⁠
(opens in a new window)
report.
Actor
We banned a set of accounts that were attempting to use our models to generate content for the covert influence operation we wrote about in October 2024 as “Stop News”. This activity originated in Russia and appeared consistent with an operation run by a marketing company. Our investigation identified efforts by this actor to use other companies’ AI tools to generate videos that were then posted on YouTube and TikTok. We are not able to independently confirm which models they eventually used.
Behavior
Similar to the activity we disrupted in October 2024, this operation mainly used our models to generate content which was then posted on social media and a set of websites that posed as the same news outlets in Africa and the UK that we wrote about last year.
While this activity appeared to be an attempt to continue the earlier operation following our and industry peers’ disruptions, we identified some notable differences. First, the proportion of image generation was significantly lower. Where the original Stop News activity was, as we noted at the time, unusually prolific in its use of imagery, the latest activity focused more on text generation, with image generation being relatively rare. This is consistent with the assessment by the French digital agency, VIGINUM, that “since the publication of the Meta and OpenAI reports, the use of AI-generated images has fallen drastically”.
Second, the operation also used ChatGPT to generate scripts and descriptions for news-style short videos. Typically, the operators would input a lengthy Russian-language text and ask to generate a video script from it. They would then ask the model to translate the text into French. Third, they would ask the model to generate an SEO-optimized description and hashtags.
Some of these scripts featured in videos on a YouTube channel linked to the Stop News operation’s Africa-focused website, newstop[.]africa. Others featured on a YouTube channel and TikTok channel that did not bear the “Stop News” brand. These channels featured an AI-generated person reading the news. In most cases, brief clips of the newsreader were interspersed with video footage of events in, or relating to, Africa. The clips of the newsreader do not appear to have been generated using our models; we are not able to independently confirm which service was used. The newsreader’s appearance evolved through 2025, as the below screenshots of TikTok videos illustrate.
Left to right, the AI-generated newsreader praising Russia in January 2025, early June 2025, and late June 2025, from the operation’s TikTok account.
In the most elaborate cases, the operators used our models to generate video prompts apparently for use with other AI models. In this scenario, they first generated a Russian-language video script, then broke it down into two-sentence snippets, and asked ChatGPT to generate a video prompt for each snippet. Once the video prompts had been created, the operators then asked the model to translate the entire script into French.
Left to right: three screenshots from a TikTok video praising Russia’s “Africa Corps”. The operators used ChatGPT to generate the audio script in Russian, broke it into two-sentence snippets, and then generated a video prompt for another model for each snippet. The images above correspond with the video prompts. We are not able to independently confirm which service was used to create the videos. Of note, the caption in the right-hand image contains a grammatical error (“ces” instead of “ses”) which was not present in the French-language translation provided by ChatGPT. This suggests that the caption was transcribed from audio, and not proofread by someone with French skills.
Completions
This operation’s activity fell into three main categories. First, it generated French-language content that criticized the role of France and the United States in Africa and praised the role of Russia there. Second, it generated English-language content that criticized Ukraine and its international supporters. On some occasions, the operators also generated images to accompany their text content. On rare occasions, they asked ChatGPT to generate promotional articles and Google ad texts for their main news brand, “Newstop Africa”. Rather than focusing on Newstop Africa alone, some of these promotional articles bracketed the Newstop brand with legitimate news outlets, likely to make it appear more credible by association.
Tweet by operation’s main Africa-focused X account. The image was generated using our model.
The third set of activity consisted of generating promotional materials for what looked like a range of commercial companies in Russia. This included generating ads for unlicensed online gambling. Such a combination of different content generation types is consistent with a commercial company running covert influence operations for hire alongside more traditional advertising, and is consistent with the activity that we reported last year.
Impact
Despite this operation’s increased focus on short video content and its more complex use of multiple AI tools, the content it posted appears to have only gained limited views or audiences. The core “Newstop Africa” X account only had 172 followers as of August 2025, and according to X’s “Top tweets” function, the highest number of retweets on any of its posts was four.
The YouTube and TikTok channels featuring an AI newsreader had approximately 1,900 followers each; the TikTok channel recorded 5,855 likes, or an average of 105 likes for each of the 56 videos it posted. The most viewed video recorded 63,300 views, the least viewed just 87. The YouTube channel listed some 255,000 views across 50 videos, or an average of 5,100 views per video, but we see no evidence of these videos having been re-shared, cited in the media, or otherwise achieved wider resonance.
Our original assessment of this operation in our October 2024 report was that it reached Category 3 on the Breakout Scale, based largely on a number of apparent “information partnerships” that appeared to have been set up with UK-based websites. However, subsequent research by VIGINUM and open-source researchers demonstrated that these “partnerships” were likely fictional, and “exploited technical flaws on these external sites” to add content without the administrators’ knowledge. On this basis, we would currently assess that this operation’s activity is more appropriately in Category 2, activity on multiple internet platforms, but without significant breakout to authentic communities.
Author
OpenAI
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
