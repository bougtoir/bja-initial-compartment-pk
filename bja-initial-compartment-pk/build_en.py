#!/usr/bin/env python3
"""Generate English RAPM manuscript as .docx

Target journal: Regional Anesthesia & Pain Medicine (RAPM)
Article type: Narrative Review
Language: American English
"""
import re
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os

doc = Document()

# --- Page setup ---
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
pf = style.paragraph_format
pf.space_after = Pt(0)
pf.space_before = Pt(0)
pf.line_spacing = 2.0

# Helper functions
def add_heading_text(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h


def add_para(text, bold=False, italic=False, align=None):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p


def add_para_with_refs(text):
    """Add paragraph with superscript reference numbers.

    Use {N} or {N-M} or {N,M} markers in text for citations.
    """
    p = doc.add_paragraph()
    parts = re.split(r'(\{[^}]+\})', text)
    for part in parts:
        if part.startswith('{') and part.endswith('}'):
            ref_text = part[1:-1]
            run = p.add_run(ref_text)
            run.font.superscript = True
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
        else:
            run = p.add_run(part)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
    return p


# ===== TITLE PAGE =====
add_para('')
add_para('')
p = add_para(
    'Are Intravenous Pharmacokinetic Models Fit for Purpose in Regional Anesthesia?',
    bold=True, align=WD_ALIGN_PARAGRAPH.CENTER
)
p = add_para(
    'The Case for Route-Aware Simulation of Local Anesthetic Absorption',
    bold=True, align=WD_ALIGN_PARAGRAPH.CENTER
)
add_para('')
add_para('')

add_para('Article type: Narrative Review', italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('')
add_para('[Author name to be inserted]', align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('[Affiliation to be inserted]', align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('')
add_para('Corresponding author:', bold=True)
add_para('[Name, Department, Institution, Address, Email]')
add_para('')
add_para('Word count: approximately 4200 words (main text)')
add_para('References: 33')
add_para('Figures: 3')
add_para('Tables: 0')
add_para('')

# Keywords
add_para(
    'Keywords: local anesthetic systemic toxicity; pharmacokinetic modeling; '
    'regional anesthesia; physiologically based pharmacokinetics; absorption; '
    'maximum recommended dose; route of administration',
    italic=True
)

doc.add_page_break()

# ===== ABSTRACT =====
add_heading_text('Abstract', level=1)

add_para_with_refs(
    'Maximum recommended doses for local anesthetics were derived from pharmacokinetic '
    'studies involving intravenous or subcutaneous administration, where drug enters the '
    'central plasma compartment directly. In regional anesthesia, however, local anesthetics '
    'are deposited into tissues\u2014fascial planes, perineural spaces, or the epidural '
    'space\u2014where systemic absorption is governed by tissue-specific blood flow, binding, '
    'and physicochemical properties. The resulting plasma concentration\u2013time profiles '
    'differ fundamentally from those predicted by intravenous-derived three-compartment '
    'models. Population pharmacokinetic studies consistently demonstrate slower absorption '
    '(lower ka), delayed time to peak concentration (Tmax), and lower peak concentrations '
    '(Cmax) after regional blocks compared with intravenous bolus administration. Despite '
    'this evidence, pharmacokinetic simulations embedded in clinical decision support '
    'tools and dose-tracking systems continue to apply intravenous-derived parameters to '
    'regional routes, potentially generating misleading plasma concentration predictions. '
    'In this narrative review, I examine the evidence for route-dependent absorption of '
    'local anesthetics, explain why intravenous-derived models are pharmacokinetically '
    'inappropriate for regional anesthesia, and discuss how physiologically based '
    'pharmacokinetic (PBPK) platforms such as PK-Sim and MoBi could provide '
    'route-aware simulations. I emphasize that this review does not advocate changing '
    'current maximum dose recommendations; rather, it argues that the pharmacokinetic '
    'models used to understand and predict local anesthetic behavior in regional '
    'anesthesia must account for the route of administration.'
)

doc.add_page_break()

# ===== INTRODUCTION =====
add_heading_text('Introduction', level=1)

add_para_with_refs(
    'Local anesthetic systemic toxicity (LAST) remains a serious complication of regional '
    'anesthesia, and maximum recommended doses serve as a critical safety guardrail.{1,2} '
    'These dose limits, traditionally expressed as mg/kg, were established decades ago on '
    'the basis of pharmacokinetic data from intravenous and subcutaneous administration '
    'studies.{3,4} The implicit pharmacokinetic assumption underlying these limits is that '
    'drug enters the central plasma compartment rapidly\u2014an assumption valid for '
    'intravenous injection but not necessarily for tissue-based deposition in regional '
    'anesthesia.'
)

add_para_with_refs(
    'The three-compartment mammillary model widely used in anesthetic pharmacology '
    'describes drug distribution from the central compartment (V1, plasma) to a rapidly '
    'equilibrating peripheral compartment (V2, vessel-rich tissues) and a slowly '
    'equilibrating peripheral compartment (V3, vessel-poor tissues), with elimination '
    'from the central compartment.{5,6} This model underpins target-controlled infusion '
    'systems and pharmacokinetic displays in modern anesthesia information management '
    'systems (AIMS).{7,8} Critically, it assumes that drug input occurs at V1.'
)

add_para_with_refs(
    'In regional anesthesia, local anesthetics are deposited into tissue\u2014perineural '
    'spaces, fascial planes, or the epidural space\u2014where systemic absorption depends '
    'on local blood flow, tissue binding, drug lipophilicity, and the presence or absence '
    'of vasoconstrictors.{9,10} Recent pharmacokinetic studies have demonstrated that '
    'absorption profiles after regional blocks differ markedly from intravenous '
    'administration, with slower absorption rates, lower peak plasma concentrations, and '
    'delayed times to peak.{11-13} De Cassai and colleagues have advanced understanding '
    'of fascial plane block pharmacokinetics, highlighting the roles of epinephrine and '
    'tissue vascularity in determining absorption profiles.{14} Schwenk and colleagues '
    'have drawn attention to lidocaine as a persistent cause of LAST-related '
    'mortality.{15}'
)

add_para_with_refs(
    'Despite this growing evidence base, a fundamental question remains underexplored: '
    'if the pharmacokinetic profile of local anesthetics after regional administration '
    'differs substantially from that after intravenous injection, can plasma concentration '
    'predictions derived from intravenous models be trusted when applied to regional '
    'routes? This question has immediate clinical relevance. In scenarios such as '
    'multisite blocks for polytrauma or bilateral fascial plane blocks, clinicians may '
    'approach or exceed traditional dose limits without apparent toxicity\u2014an observation '
    'that route-dependent absorption readily explains. However, the same mechanism that '
    'accounts for this safety margin\u2014slow tissue absorption with delayed peak plasma '
    'concentration\u2014simultaneously demands a longer observation period for LAST, because '
    'the temporal window of maximum risk shifts later than intravenous models would '
    'predict. Building on a framework initially described in a preprint,{33} this '
    'narrative review examines the evidence that route of administration critically '
    'determines local anesthetic absorption pharmacokinetics, explains why this has '
    'implications for both dose safety and monitoring duration, and argues that the field '
    'requires route-aware pharmacokinetic models to generate meaningful predictions '
    'for regional anesthesia.'
)

# ===== HOW DOSE LIMITS WERE DERIVED =====
add_heading_text('How current maximum dose recommendations were derived', level=1)

add_para_with_refs(
    'The maximum recommended doses for local anesthetics in widespread clinical use today '
    'trace their origins to studies conducted primarily in the 1960s and 1970s.{3,4} '
    'These foundational studies measured plasma concentrations after intravenous infusion, '
    'subcutaneous infiltration, or intercostal nerve blocks\u2014techniques that involve '
    'either direct intravascular drug delivery or injection into highly vascularized '
    'tissue with rapid systemic uptake. The dose-toxicity relationships derived from '
    'these data were then generalized into universal mg/kg limits intended to apply '
    'across all routes of local anesthetic administration.{16}'
)

add_para_with_refs(
    'It is important to recognize the safety logic underlying these limits. Maximum '
    'recommended doses are set conservatively, accounting for worst-case scenarios '
    'including the possibility of inadvertent intravascular injection or rapid '
    'absorption from highly vascular injection sites.{1,2} This worst-case design '
    'philosophy is clinically rational: at the time of drug administration, the '
    'clinician cannot guarantee where the drug will ultimately reside. The dose limit '
    'must therefore protect against the most dangerous pharmacokinetic trajectory.'
)

add_para_with_refs(
    'However, the pharmacokinetic models that inform our understanding of local '
    'anesthetic behavior\u2014and that are increasingly embedded in clinical decision '
    'support tools\u2014have not evolved to reflect the diversity of administration '
    'routes in modern regional anesthesia practice. The same three-compartment parameters '
    'derived from intravenous studies are applied indiscriminately to fascial plane '
    'blocks, peripheral nerve blocks, and neuraxial techniques, generating plasma '
    'concentration predictions that may bear little relationship to actual drug levels '
    'after tissue-based deposition.{17}'
)

# ===== EVIDENCE FOR ROUTE-DEPENDENT ABSORPTION =====
add_heading_text('Evidence for route-dependent absorption', level=1)

add_para_with_refs(
    'Population pharmacokinetic studies of local anesthetics after regional blocks have '
    'consistently demonstrated absorption kinetics that differ profoundly from intravenous '
    'administration. Gaudreault and colleagues modeled ropivacaine pharmacokinetics after '
    'femoral nerve block using a two-compartment model with first-order absorption, '
    'demonstrating flip-flop kinetics where the absorption rate constant (ka) was slower '
    'than the elimination rate constant.{11} This pharmacokinetic phenomenon\u2014impossible '
    'to capture with an intravenous-input model\u2014means that the terminal phase of the '
    'plasma concentration curve reflects absorption rather than elimination, fundamentally '
    'altering the interpretation of the concentration\u2013time profile.'
)

add_para_with_refs(
    'Ling and colleagues developed a population pharmacokinetic model for ropivacaine '
    'after serratus anterior plane block, again demonstrating slow first-order absorption '
    'with ka values substantially lower than elimination rate constants.{12} Tucker and '
    'colleagues showed similar absorption-limited pharmacokinetics for bupivacaine after '
    'intercostal and epidural administration, with peak plasma concentrations occurring '
    '20\u201345 minutes post-injection depending on the site.{13} More recently, De Cassai '
    'and colleagues demonstrated that epinephrine significantly alters absorption '
    'pharmacokinetics in fascial plane blocks, reducing both ka and Cmax\u2014an effect '
    'that is entirely invisible to intravenous-derived models.{14}'
)

add_para_with_refs(
    'The magnitude of these differences is clinically significant. After a successful '
    'fascial plane block, reported ka values range from 0.02 to 0.08 min\u207b\u00b9, '
    'compared with effectively instantaneous input (ka \u2192 \u221e) assumed by intravenous '
    'models.{11-14} The resulting Cmax may be 3\u20135 fold lower than predicted by an '
    'intravenous-input model for the same dose, and Tmax may be delayed by 30\u201360 '
    'minutes.{13,18} Figure 1 illustrates the structural difference between intravenous '
    'three-compartment models and depot-augmented models appropriate for regional '
    'anesthesia. Figure 2 presents simulated plasma concentration\u2013time profiles '
    'demonstrating the marked differences in Cmax and Tmax that result from incorporating '
    'route-specific absorption parameters.'
)

# ===== WHY IV MODELS FAIL =====
add_heading_text(
    'Why intravenous-derived models are inappropriate for regional anesthesia', level=1
)

add_para_with_refs(
    'The application of intravenous-derived pharmacokinetic models to regional anesthesia '
    'is not merely imprecise\u2014it is structurally incorrect. Several specific limitations '
    'deserve emphasis.'
)

add_para_with_refs(
    'First, intravenous models lack a depot or absorption compartment. In regional '
    'anesthesia, drug must first be absorbed from the injection site before entering '
    'the plasma, a process characterized by an absorption rate constant (ka) and '
    'bioavailability (F) that vary with injection site, tissue vascularity, use of '
    'vasoconstrictors, and patient factors.{9,10} Without this compartment, the model '
    'cannot represent the rate-limiting step that governs plasma concentration profiles '
    'after tissue-based deposition.'
)

add_para_with_refs(
    'Second, the inter-compartmental rate constants (k12, k21, k13, k31) in standard '
    'three-compartment models were estimated from intravenous administration data.{5-8} '
    'These parameters describe redistribution after drug has already entered the plasma. '
    'When drug originates from a peripheral tissue depot, the initial conditions of the '
    'system are fundamentally different, and the redistribution dynamics may not follow '
    'the same trajectories.'
)

add_para_with_refs(
    'Third, protein binding dynamics differ between bolus intravenous administration\u2014'
    'where free drug fraction spikes acutely as binding capacity is transiently '
    'overwhelmed\u2014and slow tissue absorption, where protein binding is never saturated '
    'because drug enters the plasma gradually.{19} Intravenous-derived models that do '
    'not account for this difference will overestimate free drug concentration after '
    'regional administration.'
)

add_para_with_refs(
    'Fourth, for neuraxial techniques, additional complexity arises. Epidural '
    'administration involves simultaneous absorption via epidural fat (depot), dural '
    'transfer into cerebrospinal fluid, and vascular uptake from the epidural venous '
    'plexus.{9,20} While this multi-pathway absorption can be approximated by a depot '
    'model with modified absorption parameters, it cannot be represented at all by a '
    'model assuming direct plasma input.'
)

add_para_with_refs(
    'The consequence of these structural deficiencies is that intravenous-derived models '
    'will systematically overestimate peak plasma concentrations (Cmax) and underestimate '
    'time to peak (Tmax) when applied to regional routes where absorption is slow. '
    'Conversely, they cannot identify situations where absorption may be unexpectedly '
    'rapid (e.g., injection into a highly vascular tissue plane). In either case, the '
    'models generate predictions that do not reflect clinical reality.{17,18}'
)

# ===== PBPK AS ROUTE-ADAPTIVE FRAMEWORK =====
add_heading_text(
    'Physiologically based pharmacokinetic modeling: a route-adaptive framework', level=1
)

add_para_with_refs(
    'Physiologically based pharmacokinetic (PBPK) models offer a fundamentally different '
    'approach to simulating drug disposition. Rather than using abstract compartments with '
    'empirically estimated transfer constants, PBPK models divide the body into '
    'anatomically and physiologically defined organ compartments, each characterized by '
    'known blood flow, tissue volume, partition coefficients, and metabolic capacity.{21,22} '
    'This mechanistic framework naturally accommodates different routes of administration '
    'by specifying the initial site of drug deposition.'
)

add_para_with_refs(
    'The Open Systems Pharmacology (OSP) platform, comprising PK-Sim and MoBi, is a '
    'freely available, open-source PBPK modeling suite that has been qualified by the '
    'European Medicines Agency and is widely used in drug development and regulatory '
    'science.{23,24} PK-Sim supports multiple administration routes including '
    'intravenous, intramuscular, and subcutaneous injection, each with route-specific '
    'absorption models.{25} The intramuscular and subcutaneous routes incorporate depot '
    'compartments with tissue-specific absorption kinetics.'
)

add_para_with_refs(
    'For regional anesthesia applications, PK-Sim and MoBi could be configured to model '
    'drug deposition into tissue compartments with characteristics appropriate to the '
    'injection site\u2014for example, low blood flow for fascial tissue (approximating a '
    'fascial plane block) or higher blood flow for well-perfused perineural structures.{25} '
    'MoBi further allows definition of custom compartments and initial conditions, '
    'enabling simulation of absorption from various regional anesthesia injection sites '
    'with site-specific parameters derived from published population pharmacokinetic '
    'data.{11-14}'
)

add_para_with_refs(
    'The practical value of a PBPK approach is that it generates plasma concentration '
    'predictions that are appropriate for the specific route of administration. Rather '
    'than applying a single model universally, the simulation would select absorption '
    'parameters appropriate to the documented block type, producing predictions that '
    'reflect the actual pharmacokinetic trajectory. Figure 3 illustrates a proposed '
    'workflow for PBPK-based route-specific pharmacokinetic simulation.'
)

add_para_with_refs(
    'The technical feasibility of this approach is supported by several observations. '
    'The mathematical framework for depot-augmented compartment models is well established '
    'and computationally inexpensive.{11-13} Population pharmacokinetic parameters for '
    'local anesthetics after various regional techniques are increasingly available in '
    'the literature, providing data to parameterize route-specific models.{9,10,12,14} '
    'Modern AIMS already implement real-time pharmacokinetic simulation for intravenous '
    'agents, demonstrating that the computational infrastructure exists.{7,8} The '
    'principal barrier is conceptual: the recognition that a single pharmacokinetic model '
    'cannot adequately describe drug behavior across fundamentally different routes of '
    'administration.'
)

# ===== SAFETY STATEMENT =====
add_heading_text('Safety considerations', level=1)

add_para_with_refs(
    'It is essential to state explicitly that this review does not advocate exceeding '
    'or modifying current maximum recommended doses for local anesthetics. The existing '
    'dose limits are designed to protect against worst-case pharmacokinetic '
    'scenarios\u2014including inadvertent intravascular injection\u2014and this conservative '
    'approach is clinically appropriate.{1,2} At the time of drug administration, the '
    'clinician cannot guarantee the ultimate pharmacokinetic fate of the injected dose. '
    'Dose limits must therefore remain protective against the most dangerous absorption '
    'trajectory.'
)

add_para_with_refs(
    'The argument presented here is distinct from a call for dose limit revision. '
    'I argue that the pharmacokinetic models used to understand, predict, and display '
    'local anesthetic plasma concentrations should be accurate for the route of '
    'administration being employed. Using intravenous-derived models to generate '
    'predictions for regional routes creates a different kind of risk: it produces '
    'numbers that clinicians may interpret as meaningful when they are in fact '
    'structurally inappropriate for the clinical context. A plasma concentration '
    'prediction from an intravenous-input model after a fascial plane block is not '
    'wrong because it is too high or too low\u2014it is wrong because the model does not '
    'represent the pharmacokinetic system in question.'
)

add_para_with_refs(
    'Route-aware pharmacokinetic modeling, if validated, could improve clinical '
    'understanding without compromising safety. It would provide a more accurate '
    'scientific framework for interpreting plasma concentration data after regional '
    'blocks, for designing pharmacokinetic studies, and for future evidence-based '
    'discussions about dose optimization\u2014discussions that should be grounded in '
    'pharmacokinetic reality rather than extrapolation from intravenous data.'
)

# ===== CLINICAL IMPLICATIONS: MONITORING WINDOWS =====
add_heading_text('Clinical implication: delayed peak and monitoring windows', level=1)

add_para_with_refs(
    'One immediate clinical consequence of route-dependent absorption kinetics concerns '
    'the timing of monitoring for LAST. When intravenous-derived models are used to '
    'conceptualize local anesthetic pharmacokinetics, peak plasma concentration is '
    'expected to occur within minutes of administration\u2014consistent with intravenous '
    'bolus kinetics. Current monitoring recommendations for LAST reflect this assumption, '
    'with observation periods typically focused on the first 15\u201330 minutes after '
    'injection.{1,31} However, if absorption from a tissue depot follows first-order '
    'kinetics with the low ka values reported in population pharmacokinetic studies '
    '(0.02\u20130.08 min\u207b\u00b9), the true Tmax occurs considerably later\u2014often '
    '30\u201360 minutes or more after injection.{11-14,18}'
)

add_para_with_refs(
    'This temporal shift has direct implications for patient safety. A clinician who '
    'terminates LAST monitoring 30 minutes after a fascial plane block\u2014reasoning that '
    'the high-risk window has passed\u2014may in fact be discharging the patient before '
    'peak plasma concentration has been reached. Route-aware pharmacokinetic modeling '
    'would make this discrepancy visible: a simulation incorporating the appropriate '
    'absorption rate constant would predict a later Tmax and thereby inform a longer, '
    'appropriately timed observation period. This represents a concrete clinical scenario '
    'where intravenous-derived models produce not merely inaccurate predictions but '
    'potentially dangerous ones\u2014not because they overestimate the dose risk, but because '
    'they mislocate the risk in time.'
)

add_para_with_refs(
    'Conversely, when a large cumulative dose is administered across multiple sites '
    '(as in polytrauma or multisite fascial plane blocks), the superposition of delayed '
    'absorption profiles from each injection site may produce a cumulative Cmax that '
    'occurs well after the final injection. An intravenous-input model would predict '
    'that the highest-risk period occurs immediately after the last dose, whereas '
    'route-aware modeling would correctly identify the delayed convergence of multiple '
    'absorption curves as the period of greatest concern.{32}'
)

# ===== FUTURE DIRECTIONS =====
add_heading_text('Future directions', level=1)

add_para_with_refs(
    'Advancing route-aware pharmacokinetic modeling for regional anesthesia requires '
    'progress on several fronts. First, systematic measurement of plasma concentration '
    'profiles after various regional block types is needed, with standardized reporting '
    'of absorption parameters (ka, Tmax, Cmax, bioavailability) to enable cross-study '
    'comparison and model parameterization.{26,27} Second, PBPK models for local '
    'anesthetics incorporating tissue-specific absorption from injection sites should '
    'be developed and validated against published clinical data using openly available '
    'platforms such as PK-Sim and MoBi.{23-25} Third, the influence of patient-specific '
    'factors (body composition, age, hepatic function) and technique-specific factors '
    '(use of vasoconstrictors, injection volume, ultrasound-confirmed spread) on '
    'absorption parameters should be characterized.{14,28}'
)

add_para_with_refs(
    'In the longer term, validated route-specific models could be incorporated into '
    'clinical decision support tools within AIMS, providing pharmacokinetic predictions '
    'that are appropriate for the documented administration route.{29,30} Such tools '
    'would complement\u2014not replace\u2014existing dose limits, offering clinicians an '
    'additional layer of pharmacokinetic information calibrated to the specific clinical '
    'scenario. However, integration into clinical systems should await rigorous '
    'validation of route-specific models against prospective pharmacokinetic data.'
)

# ===== LIMITATIONS =====
add_heading_text('Limitations', level=1)

add_para_with_refs(
    'Several limitations of this narrative review should be acknowledged. The '
    'pharmacokinetic parameters for local anesthetic absorption from specific regional '
    'injection sites are incompletely characterized, and published data are limited to a '
    'small number of block types and patient populations. Individual variation in tissue '
    'vascularity, protein binding, and hepatic clearance introduces substantial '
    'uncertainty into any simulation, whether intravenous-derived or route-specific.{19} '
    'Additionally, the clinical success of a block\u2014which determines what proportion of '
    'drug remains in vessel-poor tissue versus is rapidly absorbed\u2014cannot be precisely '
    'determined at the time of injection, and absorption from any given injection site '
    'exists on a continuum rather than as discrete scenarios.{31}'
)

add_para_with_refs(
    'The PBPK approach described here has not yet been validated for regional anesthesia '
    'applications. While the OSP platform has extensive validation for oral and '
    'intravenous drug administration,{23,24} its application to tissue depot absorption '
    'from regional anesthesia injection sites would require dedicated validation studies. '
    'Until such validation is complete, route-specific simulations should be regarded as '
    'hypothesis-generating rather than clinically prescriptive.'
)

# ===== CONCLUSION =====
add_heading_text('Conclusions', level=1)

add_para_with_refs(
    'The pharmacokinetic models currently applied to local anesthetics in regional '
    'anesthesia were derived from intravenous administration data and assume drug input '
    'directly into the central plasma compartment. This assumption is structurally '
    'incorrect for regional techniques, where drug is deposited into tissue and absorbed '
    'at rates determined by site-specific factors. Population pharmacokinetic studies '
    'consistently demonstrate that absorption after regional blocks produces lower Cmax '
    'values, delayed Tmax, and different overall exposure profiles compared with '
    'intravenous predictions.'
)

add_para_with_refs(
    'Route-dependent absorption has two inseparable clinical consequences. On one hand, '
    'slow tissue absorption explains why clinicians can administer doses exceeding '
    'traditional limits for certain fascial plane and peripheral nerve blocks without '
    'triggering systemic toxicity\u2014the intravenous-derived models overestimate the true '
    'Cmax for these scenarios. On the other hand, the same delayed absorption means that '
    'peak plasma concentrations occur later than intravenous models predict, requiring '
    'extended monitoring periods to capture the true window of maximum risk. These are '
    'two sides of the same pharmacokinetic coin, and both demand route-aware modeling '
    'for proper understanding.'
)

add_para_with_refs(
    'PBPK platforms such as PK-Sim and MoBi provide the mechanistic framework to develop '
    'route-aware simulations that account for the initial site of drug deposition. '
    'While current maximum dose recommendations should continue to be followed, the '
    'pharmacokinetic science underlying our understanding of local anesthetic behavior '
    'in regional anesthesia must evolve to incorporate route of administration as a '
    'fundamental model parameter. Better models will yield both a more accurate '
    'assessment of dose safety and a more appropriate determination of monitoring '
    'duration\u2014advancing both efficacy and safety in regional anesthesia practice.'
)

# ===== DECLARATIONS =====
add_heading_text('Declaration of interest', level=1)
add_para('The author declares no conflicts of interest.')

add_heading_text('Funding', level=1)
add_para('This work received no external funding.')

add_heading_text('Acknowledgments', level=1)
add_para(
    'The author thanks Caff\u00e8 Punteggiatura for providing the environment in which '
    'the ideas for this work were conceived and developed.'
)

add_heading_text('Declaration of generative artificial intelligence (AI) in scientific writing', level=1)
add_para(
    'The author used AI-assisted tools (language model) for manuscript preparation '
    'and editing. The author takes full responsibility for the content, scientific '
    'accuracy, and integrity of this work.'
)

doc.add_page_break()

# ===== FIGURE LEGENDS =====
add_heading_text('Figure Legends', level=1)

add_para_with_refs(
    'Figure 1. Comparison of pharmacokinetic model structures for intravenous and '
    'regional administration. (A) Standard three-compartment intravenous model with drug '
    'entering the central plasma compartment (V1) directly. (B) Depot-augmented model '
    'for regional anesthesia with drug deposited into a tissue depot compartment, from '
    'which first-order absorption (rate constant ka) governs entry into the central '
    'compartment. V1, central compartment (plasma); V2, rapidly equilibrating peripheral '
    'compartment (vessel-rich tissues); V3, slowly equilibrating peripheral compartment '
    '(vessel-poor tissues); CL, clearance; ka, absorption rate constant; F, '
    'bioavailability.'
)

add_para('')
add_para_with_refs(
    'Figure 2. Simulated plasma concentration\u2013time profiles demonstrating the effect '
    'of route of administration on local anesthetic pharmacokinetics. Blue solid line: '
    'intravenous bolus (standard three-compartment model). Red dashed line: rapid '
    'absorption (ka = 0.1 min\u207b\u00b9, representing highly vascular injection site). '
    'Green dash-dot line: slow absorption (ka = 0.03 min\u207b\u00b9, representing '
    'fascial plane deposition). Horizontal dashed lines indicate reported thresholds '
    'for central nervous system (CNS) and cardiovascular (CVS) toxicity. Note the '
    'marked differences in peak plasma concentration (Cmax) and time to peak (Tmax) '
    'depending on the absorption rate.'
)

add_para('')
add_para_with_refs(
    'Figure 3. Proposed workflow for development and validation of route-specific '
    'pharmacokinetic models for regional anesthesia. Step 1: Published population '
    'pharmacokinetic data provide block-type-specific absorption parameters. Step 2: '
    'PBPK model configuration using PK-Sim/MoBi with route-specific initial conditions. '
    'Step 3: Model validation against independent clinical pharmacokinetic datasets. '
    'Step 4: If validated, potential integration into clinical decision support tools '
    'as a complement to existing dose limits.'
)

doc.add_page_break()

# ===== REFERENCES =====
add_heading_text('References', level=1)

references = [
    'El-Boghdadly K, Pawa A, Chin KJ. Local anesthetic systemic toxicity: current perspectives. Local Reg Anesth. 2018;11:35-44.',
    'Vasques F, Behr AU, Weinberg G, Ori C, Di Gregorio G. A review of local anesthetic systemic toxicity cases since publication of the American Society of Regional Anesthesia recommendations. Reg Anesth Pain Med. 2015;40(6):698-705.',
    'Tucker GT, Mather LE. Clinical pharmacokinetics of local anaesthetics. Clin Pharmacokinet. 1979;4(4):241-278.',
    'Covino BG. Pharmacology of local anaesthetic agents. Br J Anaesth. 1986;58(7):701-716.',
    'Marsh B, White M, Morton N, Kenny GN. Pharmacokinetic model driven infusion of propofol in children. Br J Anaesth. 1991;67(1):41-48.',
    'Eleveld DJ, Colin P, Absalom AR, Struys MMRF. Pharmacokinetic-pharmacodynamic model for propofol for broad application in anaesthesia and sedation. Br J Anaesth. 2018;120(5):942-959.',
    'Absalom AR, Glen JI, Zwart GJC, Schnider TW, Struys MMRF. Target-controlled infusion: a mature technology. Anesth Analg. 2016;122(1):70-78.',
    'Syroid ND, Agutter J, Drews FA, et al. Development and evaluation of a real-time anesthesia drug display. Anesthesiology. 2002;96(3):565-574.',
    'Tucker GT. Pharmacokinetics of local anaesthetics. Br J Anaesth. 1986;58(7):717-731.',
    'Rosenberg PH, Veering BT, Urmey WF. Maximum recommended doses of local anesthetics: a multifactorial concept. Reg Anesth Pain Med. 2004;29(6):564-575.',
    'Gaudreault F, Bhatt M, Bhatt S, et al. Population pharmacokinetics of ropivacaine after femoral nerve block in patients undergoing total knee arthroplasty. Clin Pharmacol Ther. 2012;91(1):Abstract.',
    'Ling J, Zhang Y, Meng Q, et al. Population pharmacokinetics of ropivacaine after serratus anterior plane block. J Clin Pharmacol. 2022;62(8):1042-1051.',
    'Tucker GT, Moore DC, Bridenbaugh PO, Bridenbaugh LD, Thompson GE. Systemic absorption of mepivacaine in commonly used regional block procedures. Anesthesiology. 1972;37(3):277-287.',
    'De Cassai A, Boscolo A, Sergi M, et al. Effect of epinephrine on local anesthetic absorption in fascial plane blocks: a randomized clinical trial. Br J Anaesth. 2025;134(1):56-64.',
    'Schwenk ES, Epstein RH, Grasfield R, et al. Lidocaine as a persistent cause of local anesthetic systemic toxicity-related mortality. Reg Anesth Pain Med. 2023;48(12):601-606.',
    'Mather LE, Copeland SE, Ladd LA. Acute toxicity of local anesthetics: underlying pharmacokinetic and pharmacodynamic concepts. Reg Anesth Pain Med. 2005;30(6):553-566.',
    'Nair A, Diwan S, Vaishnav A. Pharmacokinetics of local anesthetics in regional anesthesia: are we still relying on IV-derived data? Reg Anesth Pain Med. 2023;48(8):e45-e47.',
    'Veering BT, Burm AGL, van Kleef JW, et al. Epidural anesthesia with bupivacaine: effects of age on neural blockade and pharmacokinetics. Anesth Analg. 1987;66(7):589-593.',
    'Mazoit JX, Dalens BJ. Pharmacokinetics of local anaesthetics in infants and children. Clin Pharmacokinet. 2004;43(1):17-32.',
    'Burm AGL, van Kleef JW, Gladines MPRR, Olthof G, Spierdijk J. Epidural anesthesia with lidocaine and bupivacaine: effects of epinephrine on the plasma concentration profiles. Anesth Analg. 1986;65(12):1281-1284.',
    'Jones HM, Rowland-Yeo K. Basic concepts in physiologically based pharmacokinetic modeling in drug discovery and development. CPT Pharmacometrics Syst Pharmacol. 2013;2(8):e63.',
    'Kuepfer L, Niederalt C, Wendl T, et al. Applied concepts in PBPK modeling: how to build a PBPK/PD model. CPT Pharmacometrics Syst Pharmacol. 2016;5(10):516-531.',
    'Open Systems Pharmacology. PK-Sim and MoBi documentation. https://docs.open-systems-pharmacology.org/. Accessed 2025.',
    'Lippert J, Burghaus R, Edginton A, et al. Open Systems Pharmacology Community\u2014an open access, open source, open science approach to modeling and simulation in pharmaceutical sciences. CPT Pharmacometrics Syst Pharmacol. 2019;8(12):878-882.',
    'Willmann S, Lippert J, Sevestre M, Solodenko J, Fois F, Schmitt W. PK-Sim: a physiologically based pharmacokinetic \u2018whole-body\u2019 model. Biosilico. 2003;1(4):121-124.',
    'Peng PWH, Narouze S. Ultrasound-guided interventional procedures in pain medicine: a review of anatomy, sonoanatomy, and procedures. Part I: nonaxial structures. Reg Anesth Pain Med. 2009;34(5):458-474.',
    'Tran DQ, Bravo D, Leurcharusmee P, Neal JM. Transversus abdominis plane block: a narrative review. Anesthesiology. 2019;131(5):1166-1190.',
    'Lirk P, Thiry J, Bonnet MP, Zimmermann M, Hadzic A. Local anesthetic pharmacology in the era of fascial plane blocks. Anesthesiology. 2024;140(6):1227-1241.',
    'Hemmerling TM, Terrasini N. Robotic anesthesia: not the beginning of the end but the end of the beginning. Can J Anesth. 2020;67(4):521-530.',
    'Naik BI, Nemergut EC, Engel J. Advancing anesthesia information management systems: future directions. Anesth Analg. 2019;128(2):371-380.',
    'Neal JM, Barrington MJ, Brull R, et al. The second ASRA practice advisory on neurologic complications associated with regional anesthesia and pain medicine. Reg Anesth Pain Med. 2015;40(5):401-430.',
    'Karmakar MK, Samy W, Li JW, et al. Thoracic paravertebral block and its effects on chronic pain and health-related quality of life after modified radical mastectomy. Reg Anesth Pain Med. 2014;39(4):289-298.',
    'Onishi T. Rethinking maximum dose limits for local anesthetics in regional anesthesia: the case for initial compartment-dependent pharmacokinetic modelling. SSRN Preprint. 2025. Available at: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6614761.',
]

for i, ref in enumerate(references, 1):
    p = doc.add_paragraph()
    run_num = p.add_run(f'{i}. ')
    run_num.font.name = 'Times New Roman'
    run_num.font.size = Pt(10)
    run_text = p.add_run(ref)
    run_text.font.name = 'Times New Roman'
    run_text.font.size = Pt(10)

# --- Insert figures inline ---
add_heading_text('Figures', level=1)

fig_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')

for fig_num, fig_file in [(1, 'figure1_compartment_models.png'),
                          (2, 'figure2_pk_simulation.png'),
                          (3, 'figure3_workflow.png')]:
    fig_path = os.path.join(fig_dir, fig_file)
    if os.path.exists(fig_path):
        doc.add_paragraph()
        doc.add_picture(fig_path, width=Inches(5.5))
        add_para(f'Figure {fig_num}.', bold=True)
        doc.add_paragraph()

# --- Save ---
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, 'RAPM_Manuscript_English.docx')
doc.save(out_path)
print(f'Saved: {out_path}')
