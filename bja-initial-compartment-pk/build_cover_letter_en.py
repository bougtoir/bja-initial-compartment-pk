#!/usr/bin/env python3
"""Generate English cover letter for RAPM submission as .docx"""
import re
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
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
pf.space_after = Pt(6)
pf.line_spacing = 1.5


def add_para(text, bold=False, italic=False, space_after=Pt(6)):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = space_after
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p


# Date
add_para('[Date]')
add_para('')

# Addressee
add_para('Editor-in-Chief')
add_para('Regional Anesthesia & Pain Medicine')
add_para('')

# Salutation
add_para('Dear Editor,')
add_para('')

# Subject line
add_para(
    'Re: Submission of Narrative Review \u2014 '
    '"Are Intravenous Pharmacokinetic Models Fit for Purpose in Regional Anesthesia? '
    'The Case for Route-Aware Simulation of Local Anesthetic Absorption"',
    bold=True
)
add_para('')

# Body
add_para(
    'I am pleased to submit the above manuscript for consideration as a Narrative '
    'Review in Regional Anesthesia & Pain Medicine.'
)

add_para(
    'This review addresses a question of direct relevance to every clinician who '
    'administers local anesthetics for regional blocks: can pharmacokinetic models '
    'derived from intravenous administration data produce meaningful plasma concentration '
    'predictions when applied to tissue-based deposition routes? I argue that they cannot, '
    'because they lack the absorption compartment and route-specific parameters that '
    'govern drug entry into the systemic circulation after regional injection.'
)

# KEY INSIGHT - monitoring window (emphasized per user request)
add_para(
    'The central clinical insight of this review is that route-dependent absorption '
    'has two inseparable consequences for patient safety:',
    bold=True
)

add_para(
    '(1) Slow tissue absorption explains why clinicians can safely administer doses '
    'that approach or exceed traditional maximum limits for fascial plane and peripheral '
    'nerve blocks\u2014the actual peak plasma concentration (Cmax) is substantially lower '
    'than intravenous-derived models predict.'
)

add_para(
    '(2) However, the same mechanism that provides this safety margin\u2014delayed '
    'absorption\u2014simultaneously shifts the time to peak plasma concentration (Tmax) '
    'to well beyond the traditional monitoring window. Population pharmacokinetic studies '
    'report Tmax values of 30\u201360 minutes or longer after fascial plane blocks, yet '
    'conventional LAST monitoring is often focused on the first 15\u201330 minutes after '
    'injection. This means clinicians may be terminating observation before the period '
    'of maximum pharmacokinetic risk has even begun.',
    bold=True
)

add_para(
    'This dual consequence\u2014explaining dose safety while simultaneously demanding '
    'extended monitoring\u2014distinguishes this work from a unidirectional argument for '
    'dose liberalization. The review explicitly states that current maximum dose '
    'recommendations should continue to be followed, and instead focuses on the need '
    'for route-aware pharmacokinetic understanding to inform both dose interpretation '
    'and monitoring duration.'
)

add_para(
    'The manuscript discusses physiologically based pharmacokinetic (PBPK) platforms '
    '(PK-Sim, MoBi) as tools for developing route-specific simulations, and proposes '
    'a validation workflow. A preprint describing the initial framework is archived on '
    'SSRN (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6614761); this '
    'submission represents a substantially restructured and refocused version with '
    'the monitoring window implication as its central clinical contribution.'
)

add_para(
    'I believe this review is well suited to the readership of RAPM, who encounter '
    'these pharmacokinetic questions daily\u2014particularly in the context of multisite '
    'blocks for polytrauma, bilateral fascial plane blocks, and other high-dose '
    'regional anesthesia scenarios.'
)

add_para(
    'This manuscript is not under consideration elsewhere and has not been published '
    'previously (other than the preprint noted above). The author has no conflicts of '
    'interest to declare. AI-assisted tools were used for manuscript preparation, as '
    'disclosed in the manuscript per BMJ policy.'
)

add_para('')
add_para('Yours sincerely,')
add_para('')
add_para('[Author name]')
add_para('[Affiliation]')
add_para('[Email]')

# Save
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, 'RAPM_Cover_Letter_English.docx')
doc.save(out_path)
print(f'Saved: {out_path}')
