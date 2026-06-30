---
type: Article
title: Inside Genebench-Pro
source: openai-news
resource: https://openai.com/index/genebench-pro/case-studies
published: 2026-06-30
tags: []
detected: 2026-07-01T01:06:02+08:00
---

(摘要生成失败)

> 失败原因：RuntimeError: claude 退出码 1: Not logged in · Please run /login

## Full Text

Inside Genebench-Pro | OpenAI
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
June 30, 2026
Inside Genebench-Pro
A closer look at the benchmark, its questions, and supporting materials.
Share
Case studies
Case studies
Somatic oncology: Structural variant-guided tumor therapy benefit-risk decision
Functional genomics: CRISPR target validation: lncRNA transcript or genomic locus?
Statistical genetics: Prioritizing protein drug targets in a linked genetic locus
Clinical genomics / carrier screening: DRX1 carrier-screening residual risk under CNV and pseudogene calibration
Single-cell genomics: Activated-monocyte eQTL after ambient RNA correction
Structural genetics: Nested structural variant: expression support and clinical association
Regulatory genomics: Measuring chromatin loop strength after structural-variant and mapping artifact masking
Statistical genetics: Multi-parent QTL mapping with founder reconstruction
Population genetics: Parent-specific ancestry and recent admixture timing
Population genetics: Estimating selection from noisy ancient-DNA time series
Table of contents
Case studies
Somatic oncology: Structural variant-guided tumor therapy benefit-risk decision
Functional genomics: CRISPR target validation: lncRNA transcript or genomic locus?
Statistical genetics: Prioritizing protein drug targets in a linked genetic locus
Clinical genomics / carrier screening: DRX1 carrier-screening residual risk under CNV and pseudogene calibration
Single-cell genomics: Activated-monocyte eQTL after ambient RNA correction
Structural genetics: Nested structural variant: expression support and clinical association
Regulatory genomics: Measuring chromatin loop strength after structural-variant and mapping artifact masking
Statistical genetics: Multi-parent QTL mapping with founder reconstruction
Population genetics: Parent-specific ancestry and recent admixture timing
Population genetics: Estimating selection from noisy ancient-DNA time series
Case studies
These 10 case studies showcase representative questions from GeneBench-Pro. Each case study includes the original prompt, datasets, and supporting materials. For an overview of the benchmark and key findings, see the
announcement blog
.
Note: File previews show excerpts from the full datasets.
Case study 1
Somatic oncology: Structural variant-guided tumor therapy benefit-risk decision
Read the full study
(opens in a new window)
Estimate whether a synthetic TXR1-directed inhibitor has positive clinical utility in tumors whose target activation is driven by a structural variant. TXR1, TXR1i, DLR1, and star-allele labels are synthetic benchmark labels.
The target subgroup has to be recovered from long-read, expression, tumor-quality, and pharmacogenomic evidence before benefit and toxicity can be interpreted as a treatment decision.
Released prompt shown to the model
A molecular tumor board registry contains trial-eligible advanced solid-tumor cases considered for a TXR1-directed inhibitor. Estimate, for tumors with SV-driven TXR1 target-mediated activation at time zero, the marginal effect of TXR1i versus non-TXR1 systemic therapy on week-16 clinical benefit as if all patients had an assessable week-16 visit. Also estimate the 8-week treatment-limiting toxicity/discontinuation risk under TXR1i in the same target population. Report net clinical utility = benefit risk difference (percentage points) - 0.35 * toxicity risk (percentage points), and choose therapy_class_code 1 if TXR1i has positive net utility and 0 otherwise.
Use percentage-point units for all non-code quantities. Positive benefit means TXR1i improves week-16 clinical benefit relative to non-TXR1 systemic therapy.
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"therapy_class_code"
:
<int>
,
4
"benefit_rd_pp"
:
<float>
,
5
"toxicity_dropout_risk_pp"
:
<float>
,
6
"net_clinical_utility_pp"
:
<float>
7
}
,
8
"reasoning"
:
"<description of method and QC>"
9
}
Files provided to the model
clinical_registry.tsv.gz
expression_summary.tsv.gz
germline_pgx.tsv.gz
longread_txr1_region.tsv.gz
tumor_assay_metrics.tsv.gz
dlr1_allele_table.tsv.gz
data_dictionary.tsv.gz
patient_id
analysis_set
age
sex
site
calendar_period
ecog
tumor_burden
prior_lines
prior_resistance
lineage_class
therapy_class
assessed16
benefit16
tox_stop_8wk
time_zero_day
MTB0001
1
73.8
M
S1
P2
2
0.787
3
1
A
TXR1i
0
1
0
MTB0002
1
55.2
M
S3
P1
1
2.637
0
1
A
TXR1i
1
0
0
0
MTB0003
1
68.8
F
S4
P2
0
0.891
2
1
A
TXR1i
1
1
1
0
MTB0004
1
82.8
F
S2
P2
2
4.101
0
0
B
TXR1i
1
0
0
0
MTB0005
1
65.5
F
S1
P3
1
7.0
1
1
A
TXR1i
1
0
0
0
Registry covariates, therapy, week-16 assessment, benefit, and early toxicity.
Case study 2
Functional genomics: CRISPR target validation: lncRNA transcript or genomic locus?
Read the full study
(opens in a new window)
Decide whether an apparent lncRNA dependency is transcript-specific or driven by nearby-locus and neighbor-gene effects.
Transcript-directed evidence has to survive controls for local DNA-locus perturbation, neighbor-gene repression, guide swaps, GC toxicity, and plate effects.
Released prompt shown to the model
You are given pooled CRISPRi screening data, guide-level local expression measurements, transcript-targeting CasRx follow-up data, and single-guide follow-up growth measurements for a nominated lncRNA program (LINC473) and a nearby coding gene (KIN1). The identifiers LINC473, KIN1, and ANKRD42 are synthetic benchmark labels; any resemblance to real human genes is coincidental.
Estimate the requested quantities.
Definitions:
lncrna_specific_lfc: the pooled-screen matched-control day-10 log2 growth effect expected at 100% effective knockdown of the dominant LINC473 transcript, not local DNA-locus effects.
neighbor_mediated_lfc: the pooled-screen matched-control day-10 log2 growth effect expected at 100% KIN1 repression in the local LINC473-locus model after accounting for concomitant LINC473 transcript knockdown.
advance_target: 1 if the evidence supports advancing LINC473 as a transcript-directed target, else 0.
Conventions:
all growth effects are log2(day10/day0) competitive-growth effects relative to matched controls;
more negative numbers indicate stronger loss of fitness;
set advance_target to 1 only if lncrna_specific_lfc <= -0.08 and neighbor_mediated_lfc > -0.25; otherwise 0.
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"advance_target"
:
<int>
,
4
"lncrna_specific_lfc"
:
<float>
,
5
"neighbor_mediated_lfc"
:
<float>
6
}
,
7
"reasoning"
:
"<description of method and QC>"
8
}
Files provided to the model
guide_map.tsv.gz
local_expression.tsv.gz
guide_followup.tsv.gz
crispri_counts.tsv.gz
casrx_followup.tsv.gz
guide_id
nominal_target
chr
coord
strand
dist_lnc_tss_bp
dist_neighbor_tss_bp
guide_gc_frac
g001
LINC473
chr7
100014
+
14
30
0.624
g002
LINC473
chr7
100035
-
43
67
0.584
g003
LINC473
chr7
100051
+
116
56
0.622
g004
LINC473
chr7
100066
-
59
66
0.617
g005
LINC473
chr7
100088
+
74
77
0.715
Guide coordinates, targets, distances, and GC features.
Case study 3
Statistical genetics: Prioritizing protein drug targets in a linked genetic locus
Read the full study
(opens in a new window)
Estimate direct disease effects for two nearby proteins using cis multivariable Mendelian randomization (cis-MVMR) while handling assay scale, allele orientation, winner's curse, LD, and residual local pleiotropy.
The two proteins share a correlated locus. The analysis has to move from marginal associations to conditional, LD-aware disease effects on a common protein scale.
Released prompt shown to the model
You are given association summary statistics and metadata for two nearby proteins (PROTA and PROTB), a binary disease outcome, a locus correlation reference, and protein measurement records.
Goal: estimate the direct log-odds effect of each protein on the disease outcome per +1 SD increase in log10 concentration, conditional on the other protein.
Interpretation: theta_PROTA and theta_PROTB use the same log-odds per-SD scale defined in the goal.
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"theta_PROTA"
:
<float>
,
4
"theta_PROTB"
:
<float>
5
}
,
6
"reasoning"
:
"<description of method and QC>"
7
}
Files provided to the model
protein_PROTA_phase1.tsv.gz
protein_PROTB_phase1.tsv.gz
disease_association.tsv.gz
variant_metadata.tsv.gz
locus_correlation_EUR.npz
protein_PROTA_phase2.tsv.gz
protein_PROTB_phase2.tsv.gz
dataset_metadata.tsv.gz
protein_measurements.tsv.gz
snp
pos_bp
effect_allele
other_allele
maf
beta
se
pval
rs200000
50000000
A
C
0.42215
0.006438668310706808
0.003267330091203412
0.04876727714241972
rs200001
50010126
A
C
0.05709
0.011008993337581301
0.006955239208750407
0.11345916603941006
rs200002
50020253
G
T
0.09021
0.009922014757116319
0.005633023027015518
0.07817048492026045
rs200003
50030379
G
T
0.48399
0.010569215614164573
0.0032291419740237445
0.0010638520681901973
rs200004
50040506
A
G
0.37703
0.007036551378238654
0.0033297592321269802
0.034580976884336506
Screening-stage protein association summaries for PROTA.
Case study 4
Clinical genomics / carrier screening: DRX1 carrier-screening residual risk under CNV and pseudogene calibration
Read the full study
(opens in a new window)
Estimate ancestry-specific carrier frequencies, residual risk after a negative screen, partner carrier frequency, and affected-conceptus risk from carrier-screening assay data.
The residual-risk estimate depends on pseudogene-aware carrier calls, founder-haplotype collapse, ancestry-specific assay calibration, and standardization from tested partners back to the full partner roster.
Released prompt shown to the model
Using cohort_roster.tsv.gz, partner_roster.tsv.gz, calibration_controls.tsv.gz, target_metadata.tsv.gz, and assay_observations.tsv.gz, estimate residual reproductive risk for an autosomal recessive DRX1 condition. Report all quantities on the probability scale, not as percentages: carrier_frequency_afr and carrier_frequency_eur among screening-roster adults; residual_carrier_risk_afr_negative for an AFR screening-roster adult with a negative DRX1 screen; partner_carrier_frequency_full_roster for a uniformly sampled partner_roster.tsv.gz row; and couple_reproductive_risk for an affected conceptus when the index person is AFR and screen-negative and the partner is drawn from partner_roster.tsv.gz. Assume autosomal recessive inheritance with a 1/4 affected-conceptus risk conditional on both biological parents being carriers.
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"carrier_frequency_afr"
:
<float>
,
4
"carrier_frequency_eur"
:
<float>
,
5
"residual_carrier_risk_afr_negative"
:
<float>
,
6
"partner_carrier_frequency_full_roster"
:
<float>
,
7
"couple_reproductive_risk"
:
<float>
8
}
,
9
"reasoning"
:
"<description of method and QC>"
10
}
Files provided to the model
cohort_roster.tsv.gz
calibration_controls.tsv.gz
assay_observations.tsv.gz
partner_roster.tsv.gz
target_metadata.tsv.gz
sample_id
collection
ancestry
family_history_tier
S_EUR_0001
screening
EUR
0
S_EUR_0002
screening
EUR
0
S_EUR_0003
screening
EUR
0
S_EUR_0004
screening
EUR
0
S_EUR_0005
screening
EUR
1
Screening-roster adults with ancestry and screening context.
Case study 5
Single-cell genomics: Activated-monocyte eQTL after ambient RNA correction
Read the full study
(opens in a new window)
Estimate a genotype effect on activated-monocyte expression after removing ambient RNA and technical contamination from single-cell RNA-seq data.
Ambient RNA affects both target expression and the marker panel used to call activation state, so correction has to occur before the eQTL model.
Released prompt shown to the model
Estimate the per-allele log rate ratio for CXCL10 expression in the activated monocyte subpopulation from the provided single-cell RNA-seq data.
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"beta_activated"
:
<float>
4
}
,
5
"reasoning"
:
"<description of method and QC>"
6
}
Files provided to the model
cells.csv.gz
empty_drops.csv.gz
donors.csv.gz
cell_id
donor
total_umi
HBB
IFI6
ISG15
LST1
CXCL10
D01_C001
D01
1113
7
3
4
83
5
D01_C002
D01
1103
6
3
3
112
10
D01_C003
D01
1141
9
8
12
63
9
D01_C004
D01
1250
7
60
43
2
17
D01_C005
D01
1045
9
1
2
51
15
Per-cell UMI counts for marker genes, contamination markers, and the target gene.
Case study 6
Structural genetics: Nested structural variant: expression support and clinical association
Read the full study
(opens in a new window)
Estimate whether a nested structural subhaplotype inside an anonymous inversion-like locus has a calibrated clinical association and credible expression support.
A nested copy-dosage signal can be confounded by the broader inversion orientation, so dosage calibration, expression support, and clinical modeling have to remain distinct.
Released prompt shown to the model
Analyze the released files for anonymous Locus Q. Estimate the full-cohort source-population clinical association and molecular expression support for the calibrated nested segment-B structural copy dosage, separating the nested segment-B dosage from the broader outer-orientation dosage. Report subhap_log_or as the natural-log source-population total-effect odds ratio for case status per additional calibrated segment-B copy. Report expression_log_fc as the natural-log expression fold-change per calibrated segment-B copy for the expression-supported gene. Report target_support_code as 1 if the supported gene has a positive expression_log_fc and the clinical association is protective (subhap_log_or < 0), otherwise 0. Report n_calibrated_carriers as the number of reliable breakpoint-panel samples carrying at least one segment-B copy.
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"n_calibrated_carriers"
:
<int>
,
4
"target_support_code"
:
<int>
,
5
"expression_log_fc"
:
<float>
,
6
"subhap_log_or"
:
<float>
7
}
,
8
"reasoning"
:
"<description of method and QC>"
9
}
Files provided to the model
cohort.tsv.gz
marker_info.tsv.gz
expression_panel.tsv.gz
file_notes.tsv.gz
tag_markers.tsv.gz
breakpoint_panel.tsv.gz
sampling_design.tsv.gz
sample_id
case
age
age_band
sex
pc1
pc2
pc3
ancestry_group
clinic_stratum
recruitment_stream
Q00012
1
50.45
50_64
0
-1.01514
-0.21032
-0.08849
EUR
tertiary
clinic
Q00028
0
57.39
50_64
0
-1.25987
-0.12498
0.2344
EUR
regional
registry
Q00029
1
68.4
65_plus
0
0.91598
0.62177
0.01891
AFR
tertiary
clinic
Q00030
1
74.07
65_plus
1
0.21125
-0.59634
-0.08197
EAS
community
registry
Q00032
1
82.82
65_plus
0
-1.12034
-0.24372
0.14665
EUR
community
clinic
Clinical and covariate data for the full cohort.
Case study 7
Regulatory genomics: Measuring chromatin loop strength after structural-variant and mapping artifact masking
Read the full study
(opens in a new window)
Quantify a focal case-control Hi-C loop-strength difference after removing low-mappability and structural-variant artifacts from the expected-contact background.
The target loop is defined at 20 kb resolution, but the expected-contact model is distorted unless low-mappability contacts and a case-only SV stripe are masked first.
Released prompt shown to the model
You are given Hi-C contact matrices at 20 kb and 40 kb resolution plus bin annotations. Estimate the loop enrichment at the 20 kb interaction between `bin_id = 8` and `bin_id = 17` in `bins_20kb.tsv.gz`. Report three quantities: `case_loop_strength` (mean log2(observed/expected) across case replicates), `control_loop_strength` (mean log2(observed/expected) across control replicates), and `delta_loop_strength` (case minus control).
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"case_loop_strength"
:
<float>
,
4
"control_loop_strength"
:
<float>
,
5
"delta_loop_strength"
:
<float>
6
}
,
7
"reasoning"
:
"<description of method and QC>"
8
}
Files provided to the model
bins_20kb.tsv.gz
bins_40kb.tsv.gz
contacts_20kb.tsv.gz
contacts_40kb.tsv.gz
bin_id
chrom
start
end
gc_content
mappability
re_sites
0
chr8
400000
420000
0.46199033821572594
0.9787574214704273
5
1
chr8
420000
440000
0.5044124208534677
0.8901084943498397
5
2
chr8
440000
460000
0.43218451584938194
0.9056879289326712
3
3
chr8
460000
480000
0.4733197282681218
0.9376529840664789
3
4
chr8
480000
500000
0.4444956062150748
0.8682565517981877
4
Target-resolution bin annotations.
Case study 8
Statistical genetics: Multi-parent QTL mapping with founder reconstruction
Read the full study
(opens in a new window)
Map a chromosome-1 quantitative-trait locus in an eight-founder recombinant population by reconstructing founder ancestry before testing the phenotype association.
The visible marker data are biallelic, but the biological signal is founder ancestry. A defensible analysis therefore has to reconstruct founder state, check marker orientation, and separate the QTL from a batch-aligned nuisance peak.
Released prompt shown to the model
Map the chromosome 1 QTL in an 8-founder multi-parent population. Report the position (cM) and which founder carries the high-effect allele.
Report high_founder as "F1".."F8".
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"high_founder"
:
"<string>"
,
4
"qtl_pos_cM"
:
<float>
5
}
,
6
"reasoning"
:
"<description of method and QC>"
7
}
Data files:
markers.tsv.gz: marker metadata
founders.tsv.gz: founder alleles at each marker
ril_genotypes.npz: observed RIL genotypes (biallelic)
phenotypes.tsv.gz: phenotype and covariates
Files provided to the model
markers.tsv.gz
ril_genotypes.npz
founders.tsv.gz
phenotypes.tsv.gz
marker_id
chr
pos_cM
m2_065
2
59.762431265596575
m2_103
2
94.52656615104739
m2_107
2
98.18761427503033
m2_079
2
72.20130244108847
m1_054
1
49.907510212292195
Marker identifiers, chromosomes, and genetic-map positions.
Case study 9
Population genetics: Parent-specific ancestry and recent admixture timing
Read the full study
(opens in a new window)
Infer parent-specific ancestry proportions and recent admixture timing from phased local-ancestry tracts after repairing reciprocal artifacts and a chromosome-specific label inversion.
Ancestry fractions and pulse times both change if reciprocal tract artifacts, chromosome-local label inversion, or map denominators are handled incorrectly.
Released prompt shown to the model
You are given phased local-ancestry tracts for one admixed individual. Estimate, for each transmitted parental haplotype, the fraction of ancestry A across the called tract span and the number of generations since a single recent admixture pulse. Label parent1 as the haplotype with the smaller ancestry-A fraction and parent2 as the haplotype with the larger ancestry-A fraction.
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"parent1_A_fraction"
:
<float>
,
4
"parent1_t"
:
<float>
,
5
"parent2_A_fraction"
:
<float>
,
6
"parent2_t"
:
<float>
7
}
,
8
"reasoning"
:
"<description of method and QC>"
9
}
Files provided to the model
segments.tsv.gz
map_info.tsv.gz
chrom
hap
start_morgan
end_morgan
anc
posterior
low_complexity_frac
chr1
h1
0.03
0.505
A
0.985
0.08
chr1
h1
0.505
0.535
B
0.62
0.92
chr1
h1
0.535
1.478849
A
0.985
0.08
chr1
h1
1.503727
1.852681
B
0.985
0.08
chr1
h1
1.852681
2.422373
A
0.985
0.08
Phased local-ancestry tracts with coordinates, ancestry labels, posterior values, and QC annotations.
Case study 10
Population genetics: Estimating selection from noisy ancient-DNA time series
Read the full study
(opens in a new window)
Infer which of two haploid loci is under stronger positive selection from ancient allele-frequency time series while accounting for allele orientation, directional error, drift, and changing population size.
Noisy ancient trajectories are not directly comparable until both loci are placed on the same derived-allele scale and the provided sample-level sequencing-error values are modeled directly.
You are given allele-frequency time series data from two haploid loci sampled over multiple generations.
One locus is under stronger positive selection than the other. Estimate the selection coefficient s for the more strongly selected locus, where s > 0 means the derived allele is favored.
Assume instrument-driven sequencing error is ~1%. The seq_error column is the average of the two directional allele-miscall rates for that locus and sample.
The selected_locus value must be "A" or "B".
These data came from a real experiment; you will be graded not just on numerical correctness but the quality of analytical reasoning you exhibit; do not attempt to take any shortcuts.
Return your final answer as exactly one JSON object.
Do not wrap the JSON in markdown.
Do not add prose before or after the JSON.
Do not omit any keys shown in the example.
Return the JSON object in your final answer:
JSON
1
{
2
"answer"
:
{
3
"selected_locus"
:
"<string>"
,
4
"s"
:
<float>
5
}
,
6
"reasoning"
:
"<description of method and QC>"
7
}
Files provided to the model
locus_A_timeseries.tsv.gz
variant_info.tsv.gz
locus_B_timeseries.tsv.gz
Ne_schedule.tsv.gz
generation
alt_reads
total_reads
seq_error
sample_year
6
36
40
0.16
-4500
12
34
45
0.16
-4278
18
41
55
0.16
-4056
24
38
70
0.16
-3833
30
36
90
0.16
-3611
Read-count time series for locus A.
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
Your privacy choices
English
United States
