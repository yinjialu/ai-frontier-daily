---
type: Article
title: Characterizing interference weights in a tiny language model
source: transformer-circuits
resource: https://transformer-circuits.pub/2026/interference_effectiveness_helpfulness/index.html
published: 2026-08-21
tags: [可解释性, 干扰权重, 虚拟权重, Transformer]
detected: 2026-08-23T17:00:52+08:00
---

在小型单层Transformer中研究干扰权重：通过有效性和有益性打分，发现权重幅度与功能无关；大量无效虚拟权重可剪除，并识别出对训练损失有害的干扰权重实例，对机械可解释性有重要启示。

## Full Text

Characterizing interference weights in a tiny language model
Transformer Circuits Thread
Characterizing interference weights in a tiny language model
Authors
Nicholas L. Turner,
Jeffrey Wu,
Joshua Batson
†
Affiliations
Anthropic
Published
August 21, 2026
† Correspondence to
joshb@anthropic.com
Introduction
An ambitious hope for mechanistic interpretability is to read a neural network the way we read a computer program, providing a context-independent (or
global
) description of its computation
.  The most natural global components of a network are its weights; they describe the direct effect of each unit on another in every context in which they appear.
However, models leverage superposition in maximizing their capacity to represent different circuits
, and this presents two primary challenges to directly reading the weights.  First, the basis of neurons is polysemantic
: each neuron activation contributes to multiple features of the computation and they do so in a context-dependent fashion.  Dictionary learning techniques
and other methods
address polysemanticity by expanding the basis of neurons into more monosemantic components, and the model's weights can be re-expressed as global effects between these components called
virtual weights
.
But even if we found a perfect feature basis for the transformer, those features would still be written and read through low-dimensional projections, and the virtual weights between features would thus be forced into superposition
.  Such weight superposition has been postulated to result in interference weights: linear interactions of interpretable model components through the low-dimensional residual stream which are either irrelevant or harmful to the model's behavior.  Interference weights are thought to make it difficult to interpret a model's computations, even when the representations themselves are interpretable, because components that never interact on the data distribution can still be joined by large virtual weights that suggest a functional role.  If we could identify interference weights accurately, we could hope to remove them and recover a sparse model whose remaining weights reflect the circuits the model actually hoped to learn
.
We previously identified interference weights in a simple toy model based around a single low-dimensional projection
, and found that a weight's effect on the loss predicts whether it belongs to the circuit the model was trained to implement.
That note discusses multiple definitions of interference weights.  We use the definition above: linear interactions of interpretable model components through the low-dimensional residual stream which are either irrelevant or harmful to the model's behavior. This is equivalent to
"definition 2"
in A Toy Model of Interference Weights.  The choice implies that we classify individual weights as interference rather than looking for a latent difference between the model's weights and the "real" ones (
"definition 1"
).
In Claude 3.5 Haiku, we also observed that many virtual weights go unused across millions of tokens (i.e., their source and target feature never coactivate, see the relevant
Appendix section
of Circuit Tracing
), and that coactivation statistics can downweight connections between unrelated feature pairs; we suggested that these were interference weights without further evidence.  To date, we have lacked a
trained transformer
in which we could point at
specific interference weights
, characterize them, and connect them to performance.
Here, we train a one-layer transformer, decompose it into the virtual weights between its tokens, positions, features, and logits, and study how those weights combine to produce the model's behavior on the data distribution.  This provides a minimal naturalistic setting in which to analyze interference weights, which we approach by scoring weights along two axes.  A weight's
effectiveness
is the magnitude of its effect on the model's outputs.  A weight's
helpfulness
is the magnitude and sign of its effect on the loss.  This is the same measurement from the toy model work.  Helpfulness is accurate for finding interference weights, but expensive to compute.  A weight has to be effective to have helpfulness, but there's no inherent connection between a weight's effectiveness and the sign of its helpfulness.
Our 1L model can complete words like ACETYLCHOLINE
"uh-SEE-tul-KOH-leen", the neurotransmitter at every neuromuscular junction.  This example was derived from the transformer's training set, which includes some capitalized academic paper titles.
, predicting that the final "
E
" token follows "
IN
".  One term in that prediction is the path from "
IN
" to the logits via the residual stream, whose largest virtual weight votes to complete the word with "
utions
".  This token
never
follows "
IN
" in the training set, so every time this virtual weight affects the output, it only makes the model's loss worse.  This implies the role of weight superposition as there is no reason that this weight would be large if the model's virtual weights were trained directly.  While prior work has characterized the emergence and identifiability of interference weights in a toy setting, where a neural network is trained to emulate a larger, sparse, ground-truth model, this note is the first place, to our knowledge, that an interference weight like this one has been demonstrated inside a trained transformer by measuring their effect on the training loss
.
Expanding upon this result, we then present three major findings.  First, helpful and harmful weights are scattered across the entire range of virtual weight magnitudes.  Thus, naive attempts to read functional circuitry from raw weights can miss the ones that implement important circuits while highlighting confusing connections that never matter on real data.  Second, ineffective virtual weights are abundant and can be easily removed: pruning the least effective 70% only worsens the model's loss by 0.01 nats, and pruning 85% costs 0.1.  The most effective weights are overwhelmingly helpful, and they exceed the effectiveness of any harmful ones by an order of magnitude.  Third, the number of helpful virtual weights in this basis still appears large.   As a crude benchmark, our virtual weight model contains more helpful weights than parameters in the original transformer, even when constrained to the most effective and helpful.  The remaining weights may still be more interpretable than the original model, but we suspect that a similar model within a better basis may still provide further sparsity and interpretability.
A motivating example
We can decompose the prediction to complete ACETYLCHOLINE into the separate paths that feed the output and read off what each contributes.  When we do so, it's unclear which weights implement circuits for the model that are functional (improving the predictions in some contexts, if not this one), and which act as noise which is merely tolerated.
Our one-layer transformer
See the
Appendix
for training details.
has a simple decomposition we use to illustrate the basic problem.  The logit for any candidate token is a sum of contributions along three paths: the direct path from the current input (combining the input token and a position embedding), the attention path, and the MLP path.  We compute the contribution of each path separately: take its effect on the residual stream and multiply by the unembedding.
This is the logit lens
applied to each path.
We'll use more detailed decompositions later.
Which of these signals implement functional circuits?
No path individually ranks "
E
" as the top output.  Each places its largest contribution on a different, incorrect token: the direct path favors "
␣Mrs
", the attention path favors "
ely
", and the MLP path favors "
ATION
".  Instead, "
E
" is the one continuation every path scores somewhat highly.  We display where these votes sit among the other vocabulary effects and how they interact in the
Appendix
.
What interests us most about these combining paths is that several of these conflicting votes come from confusing-looking connections.  The MLP's strongest vote would complete the word as ACETYLCHOLINATION, which is not a real technical term.  The attention prediction ("
ely
") is lower-case, though every token so far has been upper-case.  And, as we've already highlighted, "
utions
" doesn't seem like it should follow "
IN
" in any context.  There might be reasonable explanations for these connections, but how can we tell?  Do we assume that the model knows something we don't?  Or are these interference weights contributing noise to the model's behavior, existing only because of compromises made in the compression of the residual stream?
In the following sections, we'll show how quantifying each weight's effectiveness and helpfulness helps answer these questions.  Ineffective or harmful weights are not valid lessons that the model has learned; they are interference weights that the model carries alongside its actual circuits.
The virtual weight model
The decomposition above was useful for demonstration, but the attention and MLP paths are too complex as units to permit an interpretable description because they are context-dependent transformations.  We might consider breaking them up into their components, but MLP neurons tend to be polysemantic
.
Some evidence suggests that token interactions through attention are interpretable
, though some evidence is based on models without an MLP.
We instead rewrite the model from its global interactions using more monosemantic components
, fitting a transcoder
to the MLP's inputs and outputs and retaining the native decomposition of the attention layer into heads.  After we expand the resulting decomposition of the model into virtual weights, we can compare our quantitative measurements with qualitative interpretability for each weight.
The basis we use consists of tokens, positions, transcoder features, and output logits.  Inputs enter the virtual weight model (the
VW model
) as a concatenated one-hot encoding of the vocabulary and a one-hot encoding of position into a single [vocabulary, position] axis of size
d_{v^′} =
5,120
Where the size of the vocabulary is 4096 and the context length is 1024
.  Our transcoder has 4,096 features (
d_f
) and the full VW model keeps the same 4,096 output logits (
d_v
) as the original transformer.  Every connection in the VW model sits within one of six families, each a product of matrices that contracts away the residual dimension (
d_m =
256), shown below.
Rewriting paths as virtual weights
These weight families describe the interactions of the basis units between the more complex nonlinearities — five of the families constitute linear maps into logits or features and the QK family is the one bilinear map, producing the attention pattern that conditions the two OV families.  Because our transformer has no normalization, each path is a fixed product of matrices
.  The VW model exactly reproduces the forward pass of the original transformer with an error term for the transcoder and appropriate composition of these matrices.
Materializing all six families inflates the parameter count from 2.9M to roughly 331M, about 100×, since each pair of endpoints now carries its own explicit weight rather than sharing the residual stream.  Implementing the equivalent forward pass also requires some additional details to manage the input encoding and separated OV paths, and we describe these details in the
Appendix
.
Effectiveness and helpfulness
Now that we have our set of virtual weights, two questions help us identify the interference weights among them: Does the weight have an appreciable effect within the model? And if it does, does it then lower the loss or raise it?  We make each question precise before using them to inspect virtual weights in the next section.
We define effectiveness as the magnitude of a weight's effect on the function the model computes.  We measure it as a second-order estimate of the KL divergence between the model's outputs with and without the weight (using the Fisher metric
).  Writing
a
for the vector of a weight's attributions to the logits and
p
for the output probabilities of each token, we can generally write this as
\textrm{fisher}(w) = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,\textrm{Var}_p(a)\,\right] = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,a^TFa\,\right],
where
F=\textrm{diag}(p) - pp^T
is the Fisher information matrix of the softmax with respect to the logits
.  Because this value is expressed in nats, it is comparable across all six families of weights, whether they target a logit directly or instead target model internals.  The
Appendix
gives the form the metric takes for each path.  We estimate this value for every virtual weight in the model over ~537M tokens of the training corpus.
Effectiveness measures which of a weight's effects survive interference from every other path.  A virtual weight can be large and still ineffective because its target is never plausible when its source is active and competing paths reliably outvote it.  For ACETYLCHOLINE, "
IN
"'s Tokens→Logits contribution to "
E
" survived the competing votes and contributed probability mass to a reasonably probable target.  Even though "
utions
" carried the larger raw virtual weight, that completion was sufficiently downvoted by other paths that the virtual weight did not contribute much to the output probability distribution.
Effectiveness says how much a weight moves the predictions, not whether it made those predictions more correct.  For that we measure helpfulness: the average change in loss when the weight is ablated from the forward pass.  If the loss rises when we remove a weight, the weight is helping the model toward the right answer; if the loss falls, it is harmful.
Recovering the sign of a weight's helpfulness with statistical significance takes a lot of data, because a single weight typically helps on some tokens and hurts on others (
Appendix
).  Helpfulness can be computed cheaply for weight families that target the logits (
Appendix
), but for the rest it is expensive.  We compute the average helpfulness for the subsets of weights in our worked examples over the entire training set and attach 95% (Gaussian) confidence intervals to each one.  We ran similar measurements for a random sample of the whole population over 1B tokens.
Several figures describe the distributions of effectiveness and helpfulness in the
Appendix
for reference.
The expected residual attribution (ERA) and target-weighted (TWERA) measurements in our previous work
can be considered proxies of effectiveness, under the assumption that large effects in the model internals propagate to the function outputs.  We don't encourage readers to read much into our change from ERA or TWERA to Fisher effectiveness.  The change is an improvement
It reduces false-negative effects by seeing which attributions reach the output distribution, and false positives by using a second-order estimate that helps account for saturated gradients
, and we also use a
counterfactual variant
for some weights that helps handle inhibition.
, but these metrics are quite similar (
Appendix
), we tried several related variants, and we do not think that further sharpening of this metric is high-leverage compared to, say, finding better bases.  Later, we'll suggest that the helpful weights are tens of percent of the VW model, and that pruning by Fisher effectiveness reaches a similar density before the loss suffers.  Since helpfulness is the most direct per-weight measure and Fisher already prunes to a similar density, a sharper metric has little room to improve.
Effectiveness surfaces helpful weights but does not isolate them
Having defined effectiveness and helpfulness, we can now use them to identify interference weights and interpret parts of the VW model.  We work through four examples.  The first returns to ACETYLCHOLINE to confirm that the confusing Tokens→Logit weight from "
IN
" was in fact interference and to show that effectiveness can filter interference weights from the most prominent effects.  The next three demonstrate lessons related to the effect: sometimes the largest magnitude virtual weights are indeed helpful; the most Fisher-effective weights tend to be helpful but are sometimes harmful; and weight families which do not target the logits have lower Fisher-effectiveness than those that do, but these families still show the same qualitative patterns relating weight magnitude, effectiveness, and helpfulness.  We walk through the last example in more detail, as effectiveness proved useful in interpreting the relevant circuitry.
As mentioned before, the largest Tokens→Logits virtual weight from "
IN
" points at "
utions
".  That weight's Fisher effectiveness, however, is around three orders of magnitude below that of the most effective weights from the same token.  It is also harmful; across the model's entire training set, "
utions
" never once follows "
IN
".  Every time this weight changes the output distribution, it pushes the predictions in the wrong direction.
Re-sorting "
IN
"'s weights by Fisher effectiveness not only drops "
utions
", it also lifts the "
E
" from ACETYLCHOLINE to second place.  The effectiveness sort is more interpretable across the top few weights, and, for these weights, it largely agrees with sorting by helpfulness directly.  The most effective weights from "
IN
" are all upper-case continuations consistent with the all-caps contexts where "
IN
" tends to appear, and they are phonetically plausible.
"
T
", ranked at the top, is indeed more likely to follow "
IN
" than "
E
".
In addition to sorting weights by effectiveness or helpfulness, we can use these measurements to inspect the largest virtual weights after filtering them by a threshold of either value.  The virtual weights describe the direct effect of each unit on another globally, so we think of filtering the weights by this kind of threshold as attempting to instantiate a version of the model without interference weights.  For this example, filtering by either helpfulness or effectiveness removes the expected interference weights and leaves us with upper-case continuations.  We'll study this filtering operation in more detail later when trying to study the VW model as a whole.
Instantiating the IN→Logit weights without interference
Zooming out from the top few weights to the full distribution shows what the effectiveness sort does in aggregate.  We co-vary virtual weight and Fisher effectiveness with helpfulness.  Any weights whose 95% confidence intervals include zero are colored gray as "not significant".
This means that some small helpfulness values will still be considered significant. See
the Appendix
for effect size analysis.
Effectiveness concentrates helpful and harmful weights (IN Tokens → Logits)
Virtual weight shows a weak relationship to helpfulness (panels 1 and 2); for this set, the virtual weight highlights few of the most important connections.  Fisher effectiveness has a much clearer relationship with helpfulness (panel 3).  Weights with increasing effectiveness bifurcate into helpful and harmful weights, with the most helpful extending to the largest effectiveness values.
However, note that the effectiveness histogram shows no obvious bimodality: there is no clean split into "effective" and "ineffective" weights, only a continuum of more and less effective ones. We also visualize this directly using an empirical CDF in the
Appendix
.
The two measurements have very different scales: virtual weights appear approximately normally distributed, while Fisher effectiveness is roughly
lognormally
distributed, varying by 10 orders of magnitude.  The median magnitude of virtual weight is approximately one third of the magnitude of the largest weight, while the median effectiveness of a virtual weight is 10,000× less than the maximum effectiveness.
This example might suggest that large virtual weights bury the most important weights, but that's not always true.
Indeed, many popular analysis methods like the logit lens
rely on interpretable virtual weights.
We can also readily find cases where naive virtual weight performs well at surfacing helpful connections.  Below, we show a Chinese feature whose largest virtual weights point at "
。
" (the equivalent of a period in East-Asian writing), a cluster of byte tokens such as "
\xe5\xae
", and "
\xe4\xbb
" (the leading bytes of the multi-byte CJK characters the feature predicts).  These high-magnitude weights are quite helpful.  The feature's strongest negative weights suppress Modern Latin-script tokens like "
␣European
" and "
␣fran
", which are intuitive for a Chinese-text feature.  Sorting or filtering barely changes the picture: the top weights are again CJK byte-prefixes ("
\xe5
", "
\xe6
", "
\xe7
").
This pattern matches features we previously described in
Towards Monosemanticity
; compared to the neuron basis, weights are generally easier to interpret within the feature basis.
Overall, we find that virtual weights are not inherently misleading, but they are not guaranteed to surface the most helpful connections.
See the virtual weight, effectiveness, and helpfulness plots in the
figure gallery
Fisher effectiveness reliably highlights the most helpful weights, but it does not fully remove interference weights.  Instead, the top of the ranking is enriched for the most helpful and harmful weights and the most effective weights are often helpful.  We can see this most clearly in a feature that primarily responds to the ends of words in European languages (especially French).  Its raw virtual weights again lead with ineffective and harmful connections targeting Arabic-script tokens instead of French.
Harmful weights overlap with helpful ones (Feature 3013 → Logits)
See more information on these distributions in the
figure gallery
Sorting or filtering by effectiveness moves these Arabic-script tokens down the ranking, but it does not entirely "clean" the weights.  The most harmful weights remain intermingled with the helpful ones across the high-effectiveness range, even though most of the weights on the large-effectiveness end are helpful.
Every example so far has analyzed weights between features and the logits.  Weights that target the model's internals (the QK, Tokens→Features, and Tokens→OV→Features weights) are generally less effective and less helpful, but the same patterns still appear.  We demonstrate how effectiveness can help to interpret feature activations and show an example of QK weights in the
figure gallery
.
Consider this feature that restricts its strong activations to newline tokens, and shows much weaker activations on some whitespace tokens.  Its top-50 activations all occur within repeated declaration blocks (common in Java, TypeScript and C# member lists), and its Features→Logits virtual weights predict newline and other whitespace tokens.
See the virtual weight, effectiveness, and helpfulness plots in the
figure gallery
The largest positive Tokens→Features virtual weights to this feature originate from positions.  Despite the feature firing on newline tokens and weakly on specific whitespace tokens, the newline token weight is buried deep in the distribution of weak positive weights and the whitespace tokens carry its strongest negative weights!  How does this feature know when to fire?
Seeing the virtual weights, we might try to understand the activation pattern using the position weights.  This turns out to be misleading.  Position input to this feature comes both from the Tokens→Features path and the OV path (Tokens→OV→Features), and it turns out that these two sum to a roughly constant bias.  We can see this clearly by covarying the two (plotted in the
Appendix
)
These values were collected across all context positions of 271 stratified contexts: the 31 contexts with largest feature activations, 120 others where the feature is active, and 120 sampled randomly.
— the input from the Tokens→Features and OV paths are strongly anti-correlated (OLS slope= -0.993,
r^2
=0.912), and the largest contribution from their sum only constitutes ~30% of the feature's effective threshold (including the JumpReLU threshold and the bias parameter).
We get better direction by inspecting which weights are most effective and helpful.  The most helpful or effective weights are negative weight whitespace tokens and the newline (see them by filtering to the top few above!).
We've already accounted for three inputs to this feature: vocabulary input from Tokens→Features, position input from Tokens→Features, and position input from Tokens→OV→Features.  The only other input comes through attention from vocabulary tokens.  The role of the Tokens→Features path must be to distinguish the current token in contexts containing relevant tokens from code.
The newline and whitespace tokens attend to similar keys within code like "
public
", "
);
", and others.
We show that below with strips for active and inactive token positions over newlines, whitespace, and other tokens.
The tokens → features weight raises the required attention input
While the whitespace and newline tokens recruit similar amounts of attention input (y-axis), the activation threshold for the whitespace tokens is much larger due to the negative direct path weights.  This means that the feature relies on the attention path to signal when it should activate and negates that signal for over tokens other than newline.  Effectiveness highlights where the role of inhibition is greater than that of excitation.
More generally, we've seen that effectiveness highlights the most helpful weights across each of the examples above.  Sorting by effectiveness is not always necessary to interpret parts of this model, but a large fraction of the most effective weights are helpful.
We can arrange our understanding of each transcoder feature above into a simple circuit diagram, giving an intuitive sense for the relative merits of sorting by virtual weights, effectiveness, and helpfulness.  We also collected the features we've described here and 18 others in
a separate page
to give a loose sense for how well filtering works.
The effectiveness tail is helpful
The examples above gave an impression of how effectiveness and helpfulness relate in a single node of the VW model at a time.  How does the model allocate effectiveness between helpful and harmful directions as a whole?
We first sample 1,111 weights from the six virtual weight families and estimate each one's mean helpfulness.
We compute this estimate over 1B tokens, along with a 95% confidence interval. The Appendix estimates
the fraction of weights that are non-null at several effect sizes
.
We sample log-uniformly across Fisher effectiveness rank to get increased resolution on the extreme values. Each dot below denotes a sample weight's mean helpfulness, and the red and blue lines depict the upper and lower confidence interval bounds, respectively.  Every point below has a confidence interval even if it's not visible.
The most effective weights are helpful
This display sorts the sample into three regimes for each weight family.  The ineffective weights unsurprisingly have near-zero helpfulness.  Where effectiveness is moderate, helpful and harmful weights are mixed, and effectiveness alone does not separate them.  Only helpful weights remain in the highest effectiveness regime.  The most effective helpful weight out-measures any harmful weight by an order of magnitude or more within each weight family.  This gap is much larger and more consistent than within the same plot for virtual weights (
Appendix
).
The data gives a clear understanding of the model's priorities.  Its most effective contributions to the output are overwhelmingly the helpful ones, and the weights that actively hurt the loss are confined to a lower range of effectiveness.  This is intuitive; a model trained to minimize loss has every reason to get its most consequential weights pointing in a good direction, and relatively little reason to police weights whose effects barely reach the output.
The model is still dense in this basis
Our deeper motivation to study interference weights is the hope that, once we identify them accurately, we can then remove them to extract a sparse model whose global circuitry we read directly
.  Here we find that, while we can cheaply remove a significant fraction of ineffective weights, many still remain.  We suggest that finding a new basis for the VW model's weights is the most promising route to further progress.
Fisher effectiveness can cheaply filter tens of percent
Fisher effectiveness can cheaply filter tens of percent
Δ
L
= 0.0702
density
0.15
fisher thresh
8.047e-10
Δ
L
= 0.0107
density
0.3
fisher thresh
1.283e-10
Δ
L
= 0.000146
density
0.55
fisher thresh
9.148e-12
0.0
0.2
0.4
0.6
0.8
1.0
Density
0
10
−3
10
−2
10
−1
10
0
Δ
L
Virtual weight magnitude
Fisher
First, we remove weights from the VW model in order from least to most effective (moving from right to left above) and measure the pruned model's loss on a held-out test set.  This costs approximately 0.01 nats at 70% sparsity (30% density) and under 0.1 nats at 85% sparsity (15% density).  This performs far better than raw virtual weight magnitude for every density and individual weight family (except for negative Features→Logits weights, see
Appendix
), similar to previous pruning literature
.  At 1%, where the parameter count roughly matches the original transformer, the pruned model's performance is significantly compromised.
It is natural to consider using helpfulness for this thresholding experiment instead as it directly measures whether removing a weight raises the loss.
Up to nonlinear effects in removing multiple weights at once.
Even within our single-layer transformer it is expensive to compute helpfulness for every weight, so instead we take a random sample of 7765 weights and attempt to estimate the fraction of helpful weights to act as an approximate floor on the density this basis can reach.
Weight filters in this basis won't yield much sparser models
Across the sample, roughly half (47.6%) of all weights have positive mean helpfulness (with 12.7% dead), and even counting only those whose confidence interval excludes zero leaves tens of percent (see more details in the
Appendix
).  Since our VW model increases the overall number of parameters by two orders of magnitude, we're still left with tens of millions of weights to interpret for a single-layer model.
Not allowing ourselves to remove any helpful weight is much stricter than many applications of circuit pruning today
.  If we instead try to preserve 90% of the sum of sampled positive helpfulness values (a kind of "helpfulness mass"), we estimate that we'd only need 2.43% density (
Appendix
), but this fraction quickly climbs to a similar regime (13.6%) when accounting for 99% of the helpfulness mass.  It is difficult to say which level of helpfulness mass is a better guide, particularly when we also expect nonlinear effects from removing multiple weights together.  We note that keeping 2% of the virtual weights would roughly double the number of parameters in the filtered, expanded VW model relative to the original transformer; if it were the case that all of the resulting weights were quite interpretable, we would be closer to an "upstairs" lift than previously observed.  Computing helpfulness for all weights is expensive, even in a tiny model like this, but the theoretical possibility remains intriguing.
Discussion
We identified interference weights via two properties: whether a virtual weight does anything to the model's outputs, and whether it lowers or raises the loss on the training data.  We used these measurements to make the theoretical implications of superposition concrete within a trained transformer model, demonstrated how identifying and filtering out interference weights helps to interpret model components, bounded the extent to which they affect the model's predictions, and measured our progress towards extracting a sparse interpretable model.
For practitioners reading circuits off virtual weights, we find that large virtual weights are not guaranteed to be helpful or even effective.  This does not make them inherently misleading — they reflect a real part of the model's forward pass — but it is cause for some caution in interpreting them directly.  Sometimes the largest weights are the functional ones, as for the Chinese feature whose top weights predicts intuitive byte-prefixes, and sometimes the largest weight is interference that never influences the output, as for the direct path Tokens→Logits weight from "
IN
"→"
utions
".  Sorting by effectiveness can help to highlight important weights and interpret the model's functional circuitry, even if it does not cleanly separate all helpful weights from the harmful ones.
We find that the model puts its most effective weights in helpful directions and confines its harmful ones to a lower-effectiveness range.  Helpfulness is close to a ground-truth measure of a weight's functional importance since it reads the change in loss directly, and we find that the cheaper effectiveness measurement largely tracks it at the largest values.  Between these helpful weights and ineffective ones, the model contains a middle regime of helpful and harmful weights with marginal effectiveness.  Harmful weights are a sign of the inherent tradeoff between implementing more, or more complex circuits, and the interference caused between them.
This work focuses on a small transformer to leverage the most accurate and expensive tools we have to identify interference weights.  Fisher effectiveness and helpfulness may be useful for interpreting
logit effects
in other settings, but they do not scale nicely to frontier models across other families, so further development of scalable proxies like ERA and TWERA
may be useful for interpreting model components. Another reason we chose a 1L model to study is that the tokens and logits both come with a trivially interpretable basis (the vocabulary), confining concerns about finding the right interpretable representation to just the MLP layer, where we used a transcoder. We hope that the fact that interference can clearly be seen even in the Tokens→Logits path — without the risk that the story is complicated by an imperfect extraction of features from superposition — is convincing to practitioners regardless of their views on the "right" decomposition of model components.
Decompositions of parameters, as in APD and VPD
, also allow for virtual weights given by multiplication through multiplication of consecutive terms through the residual stream, which will exhibit similar genres of interference.
We were unable to reach a highly sparse and interpretable model using Fisher effectiveness as the filtering criterion, and we suspect, based on our helpfulness computations, that no saliency scheme will perform much better.  We think this says less about the potential for a sparse interpretation of this model than about the basis in which we study it.  We expressed our virtual weight model using the coordinates of tokens and features of this transformer, and the same model can be dense in one basis but sparse in another
.  For example, the model may factor the tokens into languages or parts of speech such that the computation takes simple forms (e.g., tokens that end words lead to those that begin new ones).  We suspect that removing interference in this basis is not, on its own, a route to a sparse global model
The transcoder we trained also has room for improvement as it contains several polysemantic features, and the four attention heads in this model are also likely to be polysemantic
, but future work may uncover better bases for this task.
Avoiding interference weights was the original reason to study per-prompt attribution graphs rather than the global weights, and identifying them turns out to be necessary but not sufficient for reading global circuits.  We see the metrics here as instruments that might let such a basis be recognized once found: a better decomposition, if it exists, is one in which the vast majority of weights can be discarded as ineffective or harmful, and we are left with a sparse helpful set to interpret.
In this environment, we would still need to contend with competition effects through the softmax nonlinearities and understand how multiple paths interact.
Interference weights are one of the stranger implications of trained models approximating high-dimensional circuits through low-dimensional bottlenecks; despite significant optimization pressure, large, confident connections can actively harm the model's performance.  Concretely identifying these weights helps us see these circuits (and their required compromises) in action, showing that these superposed circuits play a significant role in model computation.
Related work
Superposition
has deep roots in the distributed-representations and compressed-sensing literatures (see the
related work
section of
Toy Models of Superposition
).  Toy Models of Superposition
provided the first concrete demonstration that this superposition occurs in trained networks.  The observation that the weights between features are themselves forced into superposition was named weight superposition in a Transformer Circuits update
.
A Toy Model of Interference Weights
demonstrated the basic phenomenon in the same toy model and developed initial strategies for detecting interference weights.
The difficulty interference poses for reading circuits off weights is the subject of the
global-weights analysis
in our circuit-tracing methods
.  There we reweighted virtual weights by coactivation statistics, through expected residual attribution (ERA): a weights-based attribution from the transcoder circuit analysis of Dunefsky et al.
that we adopt, and a target-weighted variant, TWERA, that we introduced.  Our Fisher effectiveness metric plays the same role but scores a weight by its estimated effect on the output distribution rather than by coactivation.
Removing weights by their lack of importance or salience has a long precedent in the pruning literature.  Magnitude pruning with retraining removes roughly ninety percent of the parameters of vision models without hurting accuracy
, and the lottery ticket hypothesis
showed that the surviving subnetworks can be trained in isolation from their original initializations, with follow-up work tying the phenomenon to stability under SGD noise
and dissecting the separate roles of signs and masks
; Blalock et al.
survey the field.  Closest to our approach are the classical second-order methods, Optimal Brain Damage
and Optimal Brain Surgeon
, which rank each weight by a saliency computed from the curvature of the loss; at a minimum of the loss this curvature coincides in expectation with the Fisher information
, so our Fisher effectiveness is a direct descendant of these criteria, applied to virtual weights and accumulated over the data distribution.  However, the weights this literature prunes are free parameters of the model, whereas our virtual weights are products of the transformer's matrices, so ablating one virtual weight has no counterpart as an edit to the original parameters.  Pruning establishes that trained networks are heavily over-provisioned with removable weight, which is consistent with the abundance of ineffective weights we observe.  Our focus concerns which weights of an interpretable expansion carry the computation, not how to compress the model in its original basis.
A complementary line of work incentivizes weight sparsity during training rather than scoring it afterward. Gao et al.
train transformers whose weights are constrained to be mostly zero and prune the result using a mask training procedure to isolate per-task circuits, finding that sparser weights trade capability for interpretability and that scale improves the frontier. On the transcoder side, sparsely connected cross-layer transcoders
mask the virtual weights between latents during training so that each latent depends on only a few upstream ones, targeting interference directly. Pushing weights toward sparsity is not the same as preserving what the model does. Drori
replicates the weight-sparse setup and finds that the resulting circuits, though small and interpretable, can be unfaithful to the model's computation, cautioning against optimizing the loss-versus-circuit-size frontier on its own. We instead take a fixed, fully trained model, and use hand-designed metrics to detect which virtual weights to prune.
The units of an interpretable weight description need not be the original matrices of a given model parametrization.  Attribution-based Parameter Decomposition
represents a trained network's parameters as a sum of components in parameter space, incentivized to be faithful (the components sum to the original parameters), minimal (few components are active on any given input), and simple (each spans as few matrices and ranks as possible).  Stochastic Parameter Decomposition
frames this program as linear parameter decomposition and learns rank-one subcomponents whose causal importance is estimated by stochastic ablation, making the approach more scalable and robust; follow-up work extends it to small transformers including GPT-2
, and Local Loss Landscape Decomposition
instead learns sparsely active parameter-space subnetworks that reconstruct per-sample loss gradients.  These methods search over learned decompositions of the parameters to discover functional components.  Both approaches share the premise that the architectural units are not the natural units of computation under superposition
, and both must separate weight that carries computation from weight that does not.  We take the decomposition as given by the architecture and ask which of those fixed weights are functional and which are interference.
A related line of work, developed under the headings of singular learning theory and developmental interpretability, likewise relates parameters to their effect on the loss, but through the geometry of the loss landscape rather than through individual virtual weights.  The local learning coefficient (LLC) of Lau et al.
measures the degeneracy of the population loss around a trained parameter and is explicitly motivated by the observation that neural-network loss landscapes are singular, so that Hessian- and Fisher-information-based measures degenerate and counting flat directions is provably insufficient.  Refined variants localize this quantity to model components such as attention heads or to data subdistributions
, and changes in the LLC over training have been used to detect stagewise development and phase transitions
, including in the toy model setting from which our analysis descends
.  Our Fisher-effectiveness metric shares the motivating question of which structures are functional, but is deliberately narrower: it is a per-virtual-weight, Fisher-information quantity evaluated at a single final checkpoint, and therefore sits inside the local-quadratic picture that the LLC is designed to correct.  We do not claim that effectiveness or helpfulness recover the singular geometry that singular learning theory targets.
Appendix
Acknowledgments
We thank all the members of the Anthropic interpretability team for providing feedback on the work. We are grateful to Thomas Conerly and Chris Olah for assistance reviewing the paper, as well as Kelley Rivoire and Chris Olah for their organizational leadership.
Citation Information
For attribution in academic contexts, please cite this work as
Turner, et al., "Characterizing interference weights in a tiny language model", Transformer Circuits, 2026.
BibTeX citation
@article{turner2026interference,
author={Turner, Nicholas L. and Wu, Jeffrey and Batson, Joshua},
title={Characterizing interference weights in a tiny language model},
journal={Transformer Circuits Thread},
year={2026},
url={https://transformer-circuits.pub/2026/workspace/index.html}
}
Training details
Transformer
The transformer we study is a one-layer, decoder-only transformer with residual width
d_m =
256, 4 attention heads of dimension
d_{\textrm{head}} =
64, a width-1024 MLP with ReLU activation, a 4,096-token vocabulary, and a 1,024-token context window, totaling ≈2.9M parameters (≈0.79M excluding the embedding and unembedding matrices). The model contains no normalization layers and no bias terms anywhere.
Attention is causal with standard softmax; scores are scaled by
\frac{1}{\sqrt{64}}
. Position information enters solely through a fixed (non-learned) additive sinusoidal position embedding
(an interleaved sin/cos table with maximum wavelength
2^{16}
) added to the residual stream immediately after the token embedding. Weights were initialized from a Gaussian with standard deviation
\frac{0.6}{\sqrt{d_m}}
≈ 0.0375 and then unit-normalized by the first application of the weight-norm projection.
The tokenizer is a 4,096-token BPE vocabulary obtained by truncating the tokenizer of the publicly released Pleias-1.2B model to its first 4,096 token ids
, keeping only the BPE merges whose inputs and output all survive the truncation.
Training text is drawn from the openly licensed Common Corpus (PleIAs)
, restricted to documents labeled as English or as code (the filter is a disjunction over the corpus's language/language_type metadata columns). The corpus copy is split into ten file shards; nine are used for training and the tenth is held out for evaluation. Each training sequence is 1,024 tokens: it begins with a sequence delimiter token, packs consecutive documents each prefixed by the sequence delimiter, and discards any remainder beyond 1,024 tokens (no carryover between sequences).
Training used Adam
with β = (0.9, 0.95) and no weight decay, under bfloat16 autocast, with gradients globally clipped to 1.5× an exponential moving average (decay 0.95) of recent gradient norms.
The model trained on ≈9.8×10⁷ unique tokens (95,464 unique sequences) over its 11,933 steps in a single pass with no data repetition. Training loss fell from 8.93 (≈ln 4096 at initialization) to ≈3.33 at the final step and was still decreasing when the step budget was exhausted.
Transcoder
A single-layer transcoder (SLT) was trained on the transformer's activations: it reads the pre-MLP residual-stream activation and is trained to predict the MLP output. It has 4,096 features over the 256-dimensional input, with a JumpReLU activation
(bandwidth 2, threshold initialized at 0.1); encoder biases were calibrated from
10^{4}
training activations so that each feature's pre-activation is positive on roughly half of the inputs at initialization.
The loss is a reconstruction term (squared error summed over output dimensions, averaged over the batch) plus a sparsity penalty (the L1 norm of feature activations weighted by the corresponding decoder-column norms)
. The sparsity coefficient ramped linearly from 0 to 2.0 over the course of training. Training used Adam with β = (0.9, 0.999) and no weight decay. The learning rate was 2×10⁻⁵ at the start of training and then linearly decayed to zero over the final 20%. The batch size was 16,384 activation vectors and training proceeded for 100,000 steps (≈1.64×10⁹ activation samples in total), collected by running the transformer over its training corpus (over more samples than its training data). Gradients were clipped to a global L2 norm of 1.0.
Activations were centered and normalized for training per input dimension using statistics estimated from
10^{8}
samples; after training these constants were folded into the transcoder weights, so the released transcoder consumes raw activations.
ACETYLCHOLINE example pairplot
In the
Motivating Example section
, we visualized the effects of three paths through the transformer when predicting ACETYLCHOLINE. Here we put those effects in context with all of the other logit effects, and compare them to one-another.
Details of the virtual weight model
The
Virtual Weight Model
section introduced the six virtual weight families as products of matrices that contract away the residual dimension. This section records the details needed to run the virtual weight model as an exact replacement for the transformer's forward pass.
The [token, position] encoding.
Inputs enter the VW model as a concatenated one-hot encoding of the vocabulary and a one-hot encoding of position, so each input to the VW model is a vector
x
of size
d_{v'} =
5,120, with exactly two active entries.
We materialize equivalent matrices to read this concatenated encoding by using the projection of each token embedding and position embedding onto the original transformer matrix. We can express this using a combined matrix that concatenates both embeddings from the original transformer
W_{[E, P]}
. This equivalence relies on the fact that our transformer model has no normalization.
Moved tokens.
The OV weight families (Tokens→OV→Logits and Tokens→OV→Features) act on the tokens that attention "moves" through the attention pattern. To express them as fixed weights we introduce a
moved-token
representation: applying the attention pattern to the stacked [token, position] one-hot vectors yields, at the query position:
m_q^{(h)} = \sum_{k \le q} A^{(h)}_{qk}\, t_k,
where
t_k
denotes a concatenated token vector.
The transcoder error term.
The single-layer transcoder predicts the MLP output but does not reconstruct it perfectly; there is a residual on each token
e = \textrm{MLP}_\textrm{out} - \textrm{SLT}_\textrm{pred}
. We apply
W_U e
(multiplying by the transformer's unembedding weights) as an additive per-token correction to the logits. This term is not attributable to any single virtual weight, so we hold it separate from the scoring: every effectiveness and helpfulness number we report is computed on the virtual weights, with the error term passed through unscored.
Full schematic diagram
Combining all of the details above, we give a schematic diagram of the VW model we analyze, along with its connections to the trained transformer.
Fisher effectiveness computation for all paths
The
Effectiveness and Helpfulness
section gave an expression for Fisher effectiveness:
\textrm{fisher}(w) = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,\textrm{Var}_p(a)\,\right] = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,a^TFa\,\right],
where
a
is a vector of attributions from a weight to each logit,
p
is the model's output probability distribution across tokens, and
F=\textrm{diag}(p) - pp^T
is the Fisher information matrix of the softmax with respect to the logits
. This section explains how we compute this quantity for each type of weight across the 6 virtual weight families.
Paths to logits
Three families target the logits directly: Tokens→Logits, Features→Logits, and Tokens→OV→Logits. For any weight in these families, you can represent its effect on the logits using an attribution vector
a
with only one nonzero entry at
j
(
a_j=s w
, where
s
is the source activation: the one-hot indicator of the [token, position] entry for the Tokens→Logits weights, the feature's activation for Features→Logits, or
A^{(h)}_{qk}
​ for the OV path — the head’s total attention to that token, summed over the positions it occupies).
Every other entry of the attribution vector is zero, so the general quadratic form simplifies to an expression of
a_j
and the target logit's output probability
p_j
:
\textrm{fisher}(w) = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,a^TFa\,\right] = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,p_j(1-p_j)\,a_j^2\,\right] = \tfrac{1}{2}\,w^2\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,s^2\,p_j(1-p_j)\,\right].
Paths to features
Let the attribution of a Tokens→Features or Tokens→OV→Features weight to a feature's activation be
\Delta{}f
. This implies an attribution
a
from this weight to the logits of
a = v\Delta{}f
, where
v
is that feature's logit effects. The quadratic form becomes
\Delta{}f^2 \textrm{Var}_p(v)
(again,
\textrm{Var}_p(v) = v^T F v
).
\textrm{fisher}(w) = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,a^TFa\,\right] = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,\Delta{}f^2 \textrm{Var}_p(v)\,\right].
An important choice is how
\Delta{}f
is computed. A linearized estimate, freezing the activation gate and taking
\Delta{}f = sw
when the feature is active, assigns zero attribution to any weight whose target feature is off under JumpReLU. This gives 0 attribution for inhibition effects that deactivate a feature, and may overestimate excitation effects near the activation threshold. We instead compute
\Delta{}f
counterfactually, passing the ablated pre-activation exactly through the nonlinearity:
\Delta{}f = f - \textrm{JumpReLU}(f_{\textrm{pre}} - sw)
. This captures both gate flips (a feature turning on or off because the weight was removed) and activation changes, though the computation no longer factors algebraically through the nonlinearity
. A diagonal approximation to the variance,
\textrm{Var}_p(v) \approx \sum_j p_j (1 - p_j) v_j^2
, correlates less well with helpfulness; we use the full variance.
QK weights
We derive a closed-form for the attribution to the attention pattern from modifying a single attention score. We then use that expression to find another for the imposed attribution vector
a
to the logits, which assumes that modifying the attention scores does not flip features on or off. We use
a
in the same fashion as for the other paths.
The same token can appear multiple times in a context and use the same QK weight to modify the attention scores. In the derivations below we take these uses as "independent" and our expressions are not exact when the same token appears multiple times.
Shifting attention patterns
Fix a query position,
q
. Ablating
sw
from a single attention score at position
k^*
scales the relevant term in the softmax computation by
e^{-sw}
.
Here,
s
refers to the indicator variable for the presence of a given token or position in the input representation. It technically scales it by
e^{-\Beta{}sw}
, where
\Beta{}
is the factor multiplying attention scores, but we omit that for brevity.
This shifts attention pattern values at all other positions
k \neq k^*
through the denominator or partition function
Z
.
A_{qk}' = A_{qk}\frac{Z}{Z'} = \frac{A_{qk}}{r},
defining
r
as the partition function ratio
\frac{Z'}{Z}
.
Note that we can rewrite this quotient as
r = \frac{Z'}{Z} = \frac{\sum_{k \neq k^*} e^{z_k} + e^{z_{k^*}}e^{-sw}}{\sum_{k}e^{z_k}} = \frac{\sum_{k} e^{z_k} + e^{z_{k^*}}e^{-sw} - e^{z_{k^*}}}{\sum_{k}e^{z_k}} = 1 - A_{q{k^*}}(1-e^{-sw}).
This implies that
A_{qk^*}e^{-sw} = A_{qk^*} + (r - 1)
. We'll use this expression below.
Shifting the attention score at a single position also shifts the pattern value at
k^*
by a factor to account for the change in the numerator:
A_{qk^*}' = A_{qk^*}e^{-sw}\frac{Z}{Z'} = \frac{A_{qk^*}e^{-sw}}{r}.
Consider the shift in each attention pattern value
\Delta{}A_{qk} = A_{qk} - A_{qk}'
. We can write this using the same expression with the use of an indicator variable for one term. For
k \neq k^*
\Delta{}A_{qk} = A_{qk} - \frac{A_{qk}}{r} = A_{qk}\frac{r - 1}{r}.
For
k^*
, we can use the expression inferred above to put this into a similar form:
\Delta{}A_{qk^*} = A_{qk^*} - \frac{A_{qk^*}e^{-sw}}{r} = \frac{A_{qk^*}r - (A_{qk^*} + (r - 1))}{r} = (A_{qk^*} - 1)\frac{(r-1)}{r}.
The expressions for
k \neq k^*
and
k = k^*
then condense to
\Delta{}A_{qk} = (A_{qk} - \mathbf{1}_{k = k^*})\frac{r-1}{r} = \alpha(A_{qk} - \mathbf{1}_{k = k^*}),
where we define
\alpha = \frac{r-1}{r}
.
Writing the attribution vector
For each context position
k
, we define
v_k
to be the vector of logit effects when attention to position
k
equals 1. This is the sum of Tokens→OV→Logits weights for the token and position indices at position k. We can define a similar vector
u_k
for the vector of feature pre-activation effects using the Tokens→OV→Features weights.
v_k = W_{\textrm{TOL}}[i_{\textrm{token}_k}, :] + W_{\textrm{TOL}}[i_{\textrm{pos}_k}, :]
u_k = W_{\textrm{TOF}}[i_{\textrm{token}_k}, :] + W_{\textrm{TOF}}[i_{\textrm{pos}_k}, :]
The direct attribution to the logits follows by summing the pattern shift against these per-position vectors. Ablating the weight shifts the head's output at query
q
by
\sum_k (A_{qk}' - A_{qk})v_k = -\sum_k \Delta{}A_{qk}v_k
. This simplifies to
\sum_k\alpha(\mathbf{1}_{k=k^*} - A_{qk})v_k = \alpha(v_{k^*} - \sum_kA_{qk}v_k) = \alpha(v_{k^*} - \bar{v}),
where we use
\bar{v}
to denote the original attribution to the logits. The same logic also follows for feature attributions, and we'll use a
\bar{u}
for the analogous term. We can also define
M_q
as the binary mask that indicates whether a feature has surpassed its activation threshold at position
q
.
All of this in place, we can write an expression for the attribution of one use of a QK weight to the logits as:
\alpha(v_{k^*} - \bar{v} + W_{\textrm{dec}}(M_q \odot (u_{k^*} - \bar{u}))),
where
W_{\textrm{dec}}
are the transcoder decoder weights and
\odot
denotes the elementwise product. The subtractions within the parentheses indicate that shifting attention between context positions with identical effects on downstream components has no overall effect.
Overall, this gives the following expression for our Fisher effectiveness equation over the QK weights:
\textrm{fisher}(w) = \tfrac{1}{2}\,\mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,\alpha^2 \textrm{Var}_p(v_k - \bar{v} + W_{\textrm{dec}}(M_q \odot (u_k - \bar{u})))\,\right].
For tractability the indirect route through the transcoder treats features as independent, using the full variance for each feature but dropping cross-feature covariances. The covariance between the direct and indirect routes is also dropped.
Computation
All expectations are estimated by averaging over
2^{29}
(approximately 537M) tokens of data from the training corpus; a weight's accumulated statistic is divided by the total token count, so scores are per-token averages. Sparsity-versus-loss evaluations of the resulting pruned models use a test set disjoint from the contexts used to estimate the scores.
The scores are designed to be computable from forward passes alone in a single streaming pass over the corpus for every weight simultaneously. Two structural facts make this cheap. First, the quadratic-form scores factor into a weight-dependent part and an activation statistic. For example, the Fisher effectiveness computation for weights to the logits
\textrm{fisher}(w) = 1/2\,w^2\,E[s^2\,p_j(1-p_j)]
, has an expectation that does not involve
w
. One pass therefore accumulates, for each (source, target) pair, a running sum of the relevant activation products and the multiplication by
w^2/2
happens once at the end. The same pass accumulates the sufficient statistics for all score variants at once. Second, the counterfactual scores, which do not factor through the nonlinearity, vanish wherever the source activation is zero (removing a weight from an inactive source changes nothing), so their cost scales with activation sparsity rather than with the full weight-matrix size; we evaluate them only at pairs whose source activation is nonzero, using a fused GPU kernel for the continuous-source case. Accumulation is embarrassingly parallel across tokens: independent shards process disjoint batches of the corpus, and their per-weight sums are added and normalized at the end.
Helpfulness computations for weight families targeting the logits
We defined
helpfulness
as the average change in loss when a weight is ablated from the forward pass, and noted that for weights targeting the logits the average can be read off cheaply. Here we derive the closed form to implement that computation. As in the effectiveness computation for these paths, a weight in the Tokens→Logits, Features→Logits, or Tokens→OV→Logits family contributes
sw
to a single logit
j
, where the source activation
s
does not depend on the weight.
For the OV path the source token can occupy several context positions. All of those uses feed the same logit, so here
s
is the head’s total attention to that token, summed over the positions it occupies, and the derivation below remains exact; there is no analogue of the independence approximation we used for the QK weights.
Fix a position and let
t
be the index of the target token there, so that the per-position loss is
\ell = -\log p_t = \log Z - z_t
, where
z
is the vector of logits and
Z = \sum_{k}e^{z_k}
is the partition function of the output softmax (the sum runs over the vocabulary). Ablating
sw
from logit
j
scales its term in the partition function by
e^{-sw}
, giving the ratio
r = \frac{Z’}{Z} = \frac{\sum_{k \neq j} e^{z_k} + e^{z_j}e^{-sw}}{\sum_{k}e^{z_k}} = 1 - \frac{e^{z_j}}{Z}(1 - e^{-sw}) = 1 - p_j(1 - e^{-sw}),
with primes marking post-ablation values.
Consider the change in loss under ablation,
\Delta{}\ell = \ell’ - \ell
. When
j \neq t
the target logit is untouched and the loss changes only through the partition function:
\Delta{}\ell = \log Z’ - \log Z = \log r.
When
j = t
the ablated logit is the target’s own,
z_t’ = z_t - sw
, and the loss also picks up the shift directly:
\Delta{}\ell = sw + \log r.
The two cases condense with an indicator:
\Delta{}\ell = \log\!\left(1 - p_j(1 - e^{-sw})\right) + sw\,\mathbf{1}_{j = t}.
The weight’s helpfulness is the expectation of this per-position change over the data distribution,
\textrm{helpfulness}(w) = \mathop{\mathbb{E}}_{x \sim \mathcal{D}}\!\left[\,\log\left(1 - p_j(1 - e^{-sw})\right) + sw\,\mathbf{1}_{j = t}\,\right].
Single weight helpfulness histograms
We noted in
Effectiveness and Helpfulness
that recovering the sign of a weight's helpfulness takes a large amount of data because a single weight typically helps on some tokens and hurts on others. We show more granular data for 10 sampled weights from each decile of the helpfulness distribution. We plot a histogram of the per-batch change in loss under ablation for each weight, rather than its overall average. Each batch consists of 16,384 tokens. You can show more or fewer weights or deciles using the sliders. The
linthresh
parameter was only chosen to separate zeros from nonzero data.
The distributions are typically broad and centered close to zero, with mass on both sides even for weights whose mean is confidently positive.
Mean helpfulness histograms
We described the helpfulness metric in
Effectiveness and Helpfulness
and showed a granular version of the data
above
. Here we plot the distribution of overall mean helpfulness across our sample of 7,765 weights computed over 1B tokens for reference, split by weight family. As above, the
linthresh
parameter was only chosen to separate zeros from nonzero data.
The distributions are centered near zero and are roughly symmetric, with the helpful side slightly heavier.
Sampled mean-helpfulness CDF
For reference, we plot the CDF of the distribution of overall mean helpfulness values. The shaded regions indicate where the mean helpfulness value typically cannot be distinguished from 0. We compute that region using a rolling median of the standard error estimate computed over the nearest 1% of the data at each point.
Helpfulness mass distribution
In the
pruning section
, we discussed a simple model of pruning performance that relaxes the constraint of keeping all (statistically significant) helpful weights and instead preserving the sum (or mass) of the helpful weights. This shows the distribution of helpfulness mass across the helpful, harmful, and nonzero weights within the random sample of 7765 weights (6750 of which have nonzero helpfulness). Each mass (y-axis value) is computed separately for each population (between positive, negative, and nonzero), but the percentage annotation refers to the fraction of the entire sample.
The sum of positive helpfulness values in this sample is 1.44×10-4. The sum of negative helpfulness magnitudes is 1.12×10-5.
Fisher effectiveness CDF
For reference, we plot the CDF of the distribution of Fisher effectiveness values. As
above
, the shaded regions indicate where the effectiveness value typically cannot be distinguished from 0. We compute this region using a rolling median of the standard error estimate computed over the nearest 1% of the data at each point.
Fisher mass distribution
For reference, we plot the mass distribution of Fisher effectiveness values. Unlike the
helpfulness plots above
, this includes every weight in the VW model. The mass is computed across each population (positive, negative, and nonzero), but the percentage annotation refers to the fraction of all weights.
331,350,016 weights, 315,487,613 with nonzero effectiveness
The sum of effectiveness across all positive weights is 3.62. The analogous sum across negative weights is 1.59.
Fisher effectiveness vs. expected attribution
Above
we asserted that Fisher effectiveness is quantitatively similar to previous metrics we've used as proxies for effectiveness. Here we compare a version of expected attribution to a matching version of Fisher effectiveness. The version of expected attribution includes some changes from the ERA equations from Ameisen et al
, using counterfactual attributions for weights targeting features and using linear gradient attributions instead of thresholding for QK weights or weights targeting the output probabilities. We show roughly 27,000 points below, sampling the top 300 of both axes and 4500 others for each panel.
Feature 1254 position input
In the
main text
, we described a feature that activates on newline tokens (primarily within declaration blocks). Here we plot its input from position embeddings, across the Token→Feature path and the Token→OV→Feature path. These two roughly cancel and add a small amount relative to the model's effective activation threshold.
Direct position input + attention position input ≈ constant
Virtual weight magnitude vs. helpfulness
In the main text, we showed that the tail of effective weights is also helpful. Here we plot the same relationship for virtual weights, finding that the gap between the weight of the most helpful weights and harmful ones is present for some paths, but not consistently so.
Threshold eval plots and CDFs for each weight
In the
pruning section
, we showed how the VW model performs after removing weights in increasing order of effectiveness. We perform the same experiment here for each weight family separately, and split it further into studying positive and negative weights.
ROPE plots
In the
main text
, we attached 95% (Gaussian) confidence intervals to the mean helpfulness of each of the 7,765 sampled weights, and in the aggregate and distribution figures, any weight whose interval includes zero lands in the gray “not significant” bin. That analysis ignores effect size, and with 1B tokens per estimate a weight can be deemed statistically significant while having a negligible effect on the loss.
Here we classify each sampled weight against a region of practical equivalence (ROPE)
: an interval
(-\varepsilon, \varepsilon)
of mean-helpfulness values we are prepared to treat as practically zero. Writing
(l_w, u_w)
for weight
w
's 95% confidence interval, at a given
\varepsilon
we call the weight positive if
l_w > \varepsilon
, negative if
u_w
<
-\varepsilon
, and practically zero if the whole interval lies inside
(-\varepsilon, \varepsilon)
; anything else is uncertain. As
\varepsilon \to 0
, the classification recovers the main text’s convention: non-null becomes “interval excludes zero,” and the practically-zero and uncertain buckets together become the gray bin.
Which effect sizes should we care about? A naive yardstick is the VW model’s loss budget: predicting uniformly over the 4,096-token vocabulary costs
\ln 4096 \approx 8.32
nats per token, and the trained model’s loss on the test set (the 10th shard of data) is
3.38
, so the weights collectively deliver about
4.94
nats per token. If that achievement were spread evenly over all
N_{\textrm{total}} \approx 331\textrm{M}
virtual weights in the six families, each would carry
\textrm{budget}/N_{\textrm{total}} \approx 1.5\times10^{-8}
nats per token; spreading each family’s share evenly within it gives the per-family yardstick
\textrm{budget}/N_{\textrm{family}}
, between
4.7\times10^{-8}
(QK) and
2.9\times10^{-7}
(Features→Logits). We also mark fixed fractions of the budget,
\textrm{budget}\times10^{-6}
through
10^{-4}
.
Full helpfulness table
Here we expand the
table from the main text
describing the proportion of weights that are deemed helpful and harmful by our simple significance testing.
