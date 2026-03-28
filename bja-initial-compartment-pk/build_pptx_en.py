#!/usr/bin/env python3
"""Generate English PPTX with 1 figure/table per slide.
- Figures 1, 2: embedded as PNG images (code-generated)
- Figure 3: editable PowerPoint shapes (workflow diagram)
- Figure 4: editable PowerPoint shapes (AIMS schematic)
- Table 1: editable PowerPoint table
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

BLUE = RGBColor(0x21, 0x96, 0xF3)
RED = RGBColor(0xF4, 0x43, 0x36)
GREEN = RGBColor(0x4C, 0xAF, 0x50)
ORANGE = RGBColor(0xFF, 0x98, 0x00)
GREY = RGBColor(0x9E, 0x9E, 0x9E)
PURPLE = RGBColor(0x9C, 0x27, 0xB0)
DARK = RGBColor(0x37, 0x47, 0x4F)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
LIGHT_BLUE = RGBColor(0xE3, 0xF2, 0xFD)
LIGHT_GREEN = RGBColor(0xE8, 0xF5, 0xE9)
LIGHT_RED = RGBColor(0xFC, 0xE4, 0xEC)
LIGHT_ORANGE = RGBColor(0xFF, 0xF3, 0xE0)
LIGHT_PURPLE = RGBColor(0xF3, 0xE5, 0xF5)
LIGHT_GREY = RGBColor(0xF5, 0xF5, 0xF5)
TEAL = RGBColor(0x00, 0x69, 0x7C)
INDIGO = RGBColor(0x3F, 0x51, 0xB5)

def add_title_textbox(slide, text, left, top, width, height, font_size=24, bold=True, color=DARK):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = PP_ALIGN.CENTER
    return txBox

def add_textbox(slide, text, left, top, width, height, font_size=11, bold=False, color=BLACK, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return txBox

def add_rounded_rect(slide, left, top, width, height, fill_color, line_color=None, text='', font_size=11, font_color=BLACK, bold=False, text_align=PP_ALIGN.CENTER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = text_align
    if text:
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(font_size)
            p.font.color.rgb = font_color
            p.font.bold = bold
            p.alignment = text_align
    shape.text_frame.auto_size = None
    shape.text_frame.word_wrap = True
    return shape

def add_connector(slide, start_x, start_y, end_x, end_y, color=DARK, width=Pt(2)):
    connector = slide.shapes.add_connector(1, start_x, start_y, end_x, end_y)  # 1 = straight
    connector.line.color.rgb = color
    connector.line.width = width
    return connector

def add_arrow_shape(slide, left, top, width, height, color=DARK):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_down_arrow(slide, left, top, width, height, color=DARK):
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

# ============================================================
# SLIDE 1: Figure 1 (PNG image)
# ============================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_title_textbox(slide1, 'Figure 1. Comparison of Compartment Models for Three Clinical Scenarios',
                  Inches(0.5), Inches(0.2), Inches(12.3), Inches(0.6), font_size=20)
fig1_path = '/home/ubuntu/manuscript/figures/figure1_compartment_models.png'
if os.path.exists(fig1_path):
    slide1.shapes.add_picture(fig1_path, Inches(0.5), Inches(1.0), Inches(12.3), Inches(5.5))
add_textbox(slide1, '(A) Traditional IV model  |  (B) Successful regional block (BPT start)  |  (C) Failed block / Intravascular (Plasma/BRT start)',
            Inches(0.5), Inches(6.7), Inches(12.3), Inches(0.5), font_size=12, color=DARK, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 2: Figure 2 (PNG image)
# ============================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_textbox(slide2, 'Figure 2. Simulated Plasma Concentration-Time Profiles\nby Initial Compartment of Drug Deposition',
                  Inches(0.5), Inches(0.1), Inches(12.3), Inches(0.8), font_size=20)
fig2_path = '/home/ubuntu/manuscript/figures/figure2_pk_simulation.png'
if os.path.exists(fig2_path):
    slide2.shapes.add_picture(fig2_path, Inches(1.5), Inches(1.0), Inches(10.3), Inches(6.0))

# ============================================================
# SLIDE 3: Figure 3 (EDITABLE workflow diagram)
# ============================================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_textbox(slide3, 'Figure 3. Proposed PBPK-Based Workflow for Maximum Dose Reassessment\nin Regional Anaesthesia',
                  Inches(0.3), Inches(0.1), Inches(12.7), Inches(0.8), font_size=20)

# Step boxes across top
step_w = Inches(3.2)
step_h = Inches(1.0)
y_top = Inches(1.2)

# Step 1
add_rounded_rect(slide3, Inches(0.5), y_top, step_w, step_h,
                 RGBColor(0x5C, 0x6B, 0xC0), line_color=RGBColor(0x3F, 0x51, 0xB5),
                 text='Step 1\nClinical Assessment', font_size=14, font_color=WHITE, bold=True)

# Arrow 1->2
add_arrow_shape(slide3, Inches(3.8), Inches(1.45), Inches(0.7), Inches(0.3), color=GREY)

# Step 2
add_rounded_rect(slide3, Inches(4.6), y_top, step_w, step_h,
                 ORANGE, line_color=RGBColor(0xE6, 0x51, 0x00),
                 text='Step 2\nInitial Compartment Selection', font_size=14, font_color=WHITE, bold=True)

# Arrow 2->3
add_arrow_shape(slide3, Inches(7.9), Inches(1.45), Inches(0.7), Inches(0.3), color=GREY)

# Step 3
add_rounded_rect(slide3, Inches(8.7), y_top, step_w, step_h,
                 PURPLE, line_color=RGBColor(0x6A, 0x1B, 0x9A),
                 text='Step 3\nPBPK Simulation\n(PK-Sim / MoBi)', font_size=14, font_color=WHITE, bold=True)

# Down arrows from Step 2
y_mid = Inches(2.5)
add_down_arrow(slide3, Inches(2.0), y_mid, Inches(0.3), Inches(0.5), color=GREEN)
add_down_arrow(slide3, Inches(6.0), y_mid, Inches(0.3), Inches(0.5), color=ORANGE)
add_down_arrow(slide3, Inches(10.0), y_mid, Inches(0.3), Inches(0.5), color=RED)

# Three scenario boxes
sc_w = Inches(3.5)
sc_h = Inches(1.5)
y_sc = Inches(3.2)

# Successful block
add_rounded_rect(slide3, Inches(0.3), y_sc, sc_w, sc_h,
                 LIGHT_GREEN, line_color=GREEN,
                 text='Successful Block\nBPT Start\n\nLower Cmax\nHigher safe dose', font_size=12, font_color=RGBColor(0x2E, 0x7D, 0x32), bold=False)

# Partial block
add_rounded_rect(slide3, Inches(4.5), y_sc, sc_w, sc_h,
                 LIGHT_ORANGE, line_color=ORANGE,
                 text='Partial Block\nMixed Start\n\nIntermediate Cmax', font_size=12, font_color=RGBColor(0xE6, 0x51, 0x00), bold=False)

# Failed block
add_rounded_rect(slide3, Inches(8.7), y_sc, sc_w, sc_h,
                 LIGHT_RED, line_color=RED,
                 text='Failed Block\nPlasma/BRT Start\n\nHigher Cmax\nLower safe dose', font_size=12, font_color=RGBColor(0xC6, 0x28, 0x28), bold=False)

# Down arrows to Step 4
add_down_arrow(slide3, Inches(2.0), Inches(4.9), Inches(0.3), Inches(0.5), color=GREEN)
add_down_arrow(slide3, Inches(6.0), Inches(4.9), Inches(0.3), Inches(0.5), color=ORANGE)
add_down_arrow(slide3, Inches(10.0), Inches(4.9), Inches(0.3), Inches(0.5), color=RED)

# Step 4 large box
add_rounded_rect(slide3, Inches(0.5), Inches(5.6), Inches(12.0), Inches(1.2),
                 RGBColor(0x00, 0x69, 0x7C), line_color=TEAL,
                 text='Step 4: Context-Sensitive Maximum Dose Recommendation\n\nIndividualised, scenario-dependent maximum dose based on predicted plasma concentration profile',
                 font_size=14, font_color=WHITE, bold=True)

# Annotation
add_textbox(slide3, 'Block type, site, success probability, patient factors',
            Inches(0.3), Inches(2.3), Inches(3.0), Inches(0.4), font_size=9, color=GREY)
add_textbox(slide3, 'Simulation results',
            Inches(11.5), Inches(4.5), Inches(1.5), Inches(0.4), font_size=9, color=PURPLE)

# ============================================================
# SLIDE 4: Figure 4 (EDITABLE AIMS schematic)
# ============================================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_textbox(slide4, 'Figure 4. Route-Adaptive PKPD Simulation in AIMS',
                  Inches(0.3), Inches(0.1), Inches(12.7), Inches(0.5), font_size=20)

# Outer AIMS box
aims_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(0.7), Inches(12.7), Inches(6.5))
aims_box.fill.solid()
aims_box.fill.fore_color.rgb = LIGHT_GREY
aims_box.line.color.rgb = DARK
aims_box.line.width = Pt(2)
tf = aims_box.text_frame
p = tf.paragraphs[0]
p.text = 'Anaesthesia Information Management System (AIMS)'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK
p.alignment = PP_ALIGN.CENTER

# Drug Administration Record
add_rounded_rect(slide4, Inches(0.6), Inches(1.3), Inches(4.0), Inches(1.5),
                 LIGHT_BLUE, line_color=RGBColor(0x15, 0x65, 0xC0),
                 text='Drug Administration Record\n\nRoute: IV / Regional (block type)\nDrug: Bupivacaine 150 mg',
                 font_size=11, font_color=RGBColor(0x15, 0x65, 0xC0), bold=False)

# Arrow DAR -> Route Detection
add_arrow_shape(slide4, Inches(4.7), Inches(1.8), Inches(0.8), Inches(0.3), color=DARK)

# Route Detection
add_rounded_rect(slide4, Inches(5.6), Inches(1.3), Inches(3.5), Inches(1.5),
                 LIGHT_ORANGE, line_color=RGBColor(0xE6, 0x51, 0x00),
                 text='Route Detection\n\nIF route = IV:\n  -> Standard 3-compartment\nIF route = Regional:\n  -> Depot-augmented model',
                 font_size=10, font_color=RGBColor(0xE6, 0x51, 0x00), bold=False)

# IV Model box
add_rounded_rect(slide4, Inches(0.6), Inches(3.2), Inches(4.0), Inches(1.8),
                 LIGHT_GREEN, line_color=RGBColor(0x2E, 0x7D, 0x32),
                 text='IV Model\n\n3-Compartment (Plasma start)\nV1 -> V2 (BRT) + V3 (BPT)\n\nStandard Marsh / Schnider / Eleveld',
                 font_size=11, font_color=RGBColor(0x2E, 0x7D, 0x32), bold=False)

# Regional Model box
add_rounded_rect(slide4, Inches(5.2), Inches(3.2), Inches(4.5), Inches(1.8),
                 LIGHT_RED, line_color=RGBColor(0xC6, 0x28, 0x28),
                 text='Regional Model (Route-Adaptive)\n\nDepot + 3-Compartment (BPT start)\nDepot(ka, F) -> V1 -> V2 + V3\n\nBlock-type-specific ka values\n(TAP, ESP, FNB, Epidural, etc.)',
                 font_size=10, font_color=RGBColor(0xC6, 0x28, 0x28), bold=False)

# Block Success Feedback
add_rounded_rect(slide4, Inches(10.2), Inches(3.4), Inches(2.5), Inches(1.3),
                 LIGHT_PURPLE, line_color=RGBColor(0x6A, 0x1B, 0x9A),
                 text='Block Success\nFeedback\n\nAdjust ka in real time',
                 font_size=10, font_color=RGBColor(0x6A, 0x1B, 0x9A), bold=False)

# Arrows from Route Detection down to models
add_down_arrow(slide4, Inches(2.4), Inches(2.85), Inches(0.25), Inches(0.35), color=RGBColor(0x2E, 0x7D, 0x32))
add_textbox(slide4, 'IV', Inches(2.0), Inches(2.85), Inches(0.5), Inches(0.3), font_size=10, bold=True, color=RGBColor(0x2E, 0x7D, 0x32))

add_down_arrow(slide4, Inches(7.3), Inches(2.85), Inches(0.25), Inches(0.35), color=RGBColor(0xC6, 0x28, 0x28))
add_textbox(slide4, 'Regional', Inches(7.6), Inches(2.85), Inches(1.0), Inches(0.3), font_size=10, bold=True, color=RGBColor(0xC6, 0x28, 0x28))

# Arrow from Regional Model to Block Success Feedback
add_arrow_shape(slide4, Inches(9.8), Inches(3.9), Inches(0.4), Inches(0.2), color=RGBColor(0x6A, 0x1B, 0x9A))

# Real-Time AIMS Display box
add_rounded_rect(slide4, Inches(0.6), Inches(5.3), Inches(12.0), Inches(1.7),
                 WHITE, line_color=DARK,
                 text='', font_size=12, font_color=DARK, bold=True)

add_textbox(slide4, 'Real-Time AIMS Display', Inches(4.5), Inches(5.35), Inches(4.0), Inches(0.35),
            font_size=14, bold=True, color=DARK, align=PP_ALIGN.CENTER)

# Left side: predicted curves description
add_textbox(slide4, 'Predicted Plasma Concentration\n\n'
            '--- IV model: rapid peak, fast decline\n'
            '--- Regional model: low, delayed Cmax\n'
            '--- Toxicity threshold line',
            Inches(0.8), Inches(5.7), Inches(4.5), Inches(1.2),
            font_size=10, color=DARK)

# Right side: dose guidance
add_textbox(slide4, 'Dose Guidance Panel\n\n'
            'Current dose: 150 mg bupivacaine\n'
            'Route: TAP block (bilateral)\n'
            'Predicted Cmax: 0.8 ug/mL (safe)\n'
            'Remaining margin: 68% below threshold',
            Inches(6.5), Inches(5.7), Inches(5.5), Inches(1.2),
            font_size=10, color=DARK)

# Down arrows from model boxes to display
add_down_arrow(slide4, Inches(2.4), Inches(5.05), Inches(0.25), Inches(0.25), color=DARK)
add_down_arrow(slide4, Inches(7.3), Inches(5.05), Inches(0.25), Inches(0.25), color=DARK)

# ============================================================
# SLIDE 5: Table 1 (EDITABLE table)
# ============================================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_title_textbox(slide5, 'Table 1. Proposed Context-Sensitive Maximum Dose Framework\nfor Local Anaesthetics in Regional Anaesthesia',
                  Inches(0.5), Inches(0.2), Inches(12.3), Inches(0.8), font_size=20)

rows = 5
cols = 4
tbl_w = Inches(11.5)
tbl_h = Inches(4.5)
left = Inches(0.9)
top = Inches(1.3)

table_shape = slide5.shapes.add_table(rows, cols, left, top, tbl_w, tbl_h)
table = table_shape.table

# Column widths
col_widths = [Inches(3.2), Inches(3.0), Inches(2.3), Inches(3.0)]
for i, w in enumerate(col_widths):
    table.columns[i].width = w

headers = ['Scenario', 'Initial Compartment', 'Expected Cmax', 'Dose Adjustment']
header_colors = [RGBColor(0x26, 0x32, 0x38)] * 4

data = [
    ['Successful block\n(perineural / fascial)', 'BPT (V3)\nVessel-poor tissue', 'Low, delayed', 'Higher dose may be safe'],
    ['Partial block', 'Mixed\n(BPT + BRT / Plasma)', 'Intermediate', 'Standard dose limit applies'],
    ['Failed block\n(tissue misplacement)', 'BRT (V2)\nVessel-rich tissue', 'Moderate-high, early', 'Lower dose may be needed'],
    ['Intravascular injection', 'Plasma (V1)', 'Very high, immediate', 'Traditional IV limits apply'],
]

row_colors = [
    LIGHT_GREEN,
    LIGHT_ORANGE,
    LIGHT_RED,
    RGBColor(0xFF, 0xCD, 0xD2),
]

for i, h in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = h
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.size = Pt(14)
        paragraph.font.bold = True
        paragraph.font.color.rgb = WHITE
        paragraph.alignment = PP_ALIGN.CENTER
    cell.fill.solid()
    cell.fill.fore_color.rgb = DARK
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE

for r, row_data in enumerate(data):
    for c, val in enumerate(row_data):
        cell = table.cell(r + 1, c)
        cell.text = val
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(12)
            paragraph.font.color.rgb = BLACK
            paragraph.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = row_colors[r]
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

# Save
out = '/home/ubuntu/manuscript/BJA_Figures_English.pptx'
prs.save(out)
print(f'English PPTX saved: {out}')
