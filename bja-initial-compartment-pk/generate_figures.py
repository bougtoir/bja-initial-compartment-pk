#!/usr/bin/env python3
"""Generate color figures for the BJA manuscript."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import os

OUTPUT_DIR = "/home/ubuntu/manuscript/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'figure.dpi': 300,
})

COLORS = {
    'plasma': '#2196F3',       # Blue
    'brt': '#F44336',          # Red
    'bpt': '#4CAF50',          # Green
    'depot': '#FF9800',        # Orange
    'elimination': '#9E9E9E',  # Grey
    'effect': '#9C27B0',       # Purple
    'arrow': '#37474F',        # Dark grey
    'bg_light': '#FAFAFA',
    'success': '#4CAF50',
    'failure': '#F44336',
    'partial': '#FF9800',
}

def draw_box(ax, xy, w, h, label, color, fontsize=11, bold=True):
    """Draw a rounded rectangle with centered label."""
    box = FancyBboxPatch(xy, w, h,
                         boxstyle="round,pad=0.1",
                         facecolor=color, edgecolor='black',
                         linewidth=1.5, alpha=0.85)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(xy[0] + w/2, xy[1] + h/2, label,
            ha='center', va='center', fontsize=fontsize,
            fontweight=weight, color='white' if color not in ['#FF9800', '#FAFAFA', '#E0E0E0'] else 'black')

def draw_arrow(ax, start, end, color='#37474F', style='->', lw=2, connectionstyle="arc3,rad=0"):
    arrow = FancyArrowPatch(start, end,
                            arrowstyle=style,
                            connectionstyle=connectionstyle,
                            color=color, linewidth=lw,
                            mutation_scale=15)
    ax.add_patch(arrow)

# ============================================================
# FIGURE 1: Comparison of Traditional vs Regional Anesthesia
#            Compartment Models (3 panels)
# ============================================================
def figure1():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
    
    # --- Panel A: Traditional IV model ---
    ax = axes[0]
    ax.set_title('A. Traditional IV Administration', fontsize=13, fontweight='bold', pad=10)
    
    # Syringe icon (simplified)
    ax.annotate('IV Bolus', xy=(5, 9.2), fontsize=10, ha='center', fontstyle='italic', color='#555')
    ax.annotate('', xy=(5, 8.6), xytext=(5, 9.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['arrow'], lw=2.5))
    
    # Plasma (V1)
    draw_box(ax, (2.5, 6.8), 5, 1.5, 'Plasma (V1)', COLORS['plasma'])
    
    # BRT (V2)
    draw_box(ax, (0.3, 3.5), 4, 1.3, 'BRT (V2)\nVessel-rich', COLORS['brt'], fontsize=9)
    
    # BPT (V3)
    draw_box(ax, (5.7, 3.5), 4, 1.3, 'BPT (V3)\nVessel-poor', COLORS['bpt'], fontsize=9)
    
    # Elimination
    draw_box(ax, (3.2, 0.8), 3.6, 1.0, 'Elimination (CL)', COLORS['elimination'], fontsize=9)
    
    # Arrows
    draw_arrow(ax, (3.5, 6.8), (2.3, 4.8), COLORS['brt'])
    draw_arrow(ax, (2.3, 4.8), (3.5, 6.8), COLORS['brt'], style='->')
    ax.text(1.3, 5.9, 'k$_{12}$/k$_{21}$', fontsize=8, color=COLORS['brt'])
    
    draw_arrow(ax, (6.5, 6.8), (7.7, 4.8), COLORS['bpt'])
    draw_arrow(ax, (7.7, 4.8), (6.5, 6.8), COLORS['bpt'], style='->')
    ax.text(7.8, 5.9, 'k$_{13}$/k$_{31}$', fontsize=8, color=COLORS['bpt'])
    
    draw_arrow(ax, (5, 6.8), (5, 1.8), COLORS['elimination'])
    
    # Highlight: drug enters plasma first
    ax.add_patch(plt.Circle((5, 7.55), 0.3, color='yellow', alpha=0.4, zorder=0))
    ax.text(5, 7.55, '', fontsize=14, ha='center', va='center')
    
    # --- Panel B: Successful Regional Block ---
    ax = axes[1]
    ax.set_title('B. Successful Regional Block', fontsize=13, fontweight='bold', pad=10, color=COLORS['success'])
    
    # Injection into tissue depot
    ax.annotate('Perineural\nInjection', xy=(7.7, 9.0), fontsize=9, ha='center', fontstyle='italic', color='#555')
    ax.annotate('', xy=(7.7, 8.0), xytext=(7.7, 8.7),
                arrowprops=dict(arrowstyle='->', color=COLORS['success'], lw=2.5))
    
    # Depot compartment (near BPT)
    draw_box(ax, (5.7, 6.3), 4, 1.5, 'Depot\n(near BPT)', COLORS['depot'], fontsize=10)
    
    # Plasma (V1)
    draw_box(ax, (2.5, 3.5), 5, 1.3, 'Plasma (V1)', COLORS['plasma'])
    
    # BRT
    draw_box(ax, (0.3, 0.8), 4, 1.2, 'BRT (V2)', COLORS['brt'], fontsize=9)
    
    # Elimination
    draw_box(ax, (5.7, 0.8), 4, 1.2, 'Elimination (CL)', COLORS['elimination'], fontsize=9)
    
    # Slow absorption arrow (depot -> plasma)
    draw_arrow(ax, (6.5, 6.3), (5.5, 4.8), COLORS['depot'], lw=1.5)
    ax.text(4.8, 5.7, 'k$_a$ (slow)', fontsize=9, color=COLORS['depot'], fontweight='bold')
    
    # Plasma <-> BRT
    draw_arrow(ax, (3.5, 3.5), (2.3, 2.0), COLORS['brt'])
    draw_arrow(ax, (2.3, 2.0), (3.5, 3.5), COLORS['brt'], style='->')
    
    # Plasma -> Elimination
    draw_arrow(ax, (6.5, 3.5), (7.7, 2.0), COLORS['elimination'])
    
    # Key annotation
    ax.text(5, 9.8, 'Drug starts in vessel-poor tissue',
            fontsize=9, ha='center', color=COLORS['success'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor=COLORS['success']))
    
    # --- Panel C: Failed Block / Intravascular Injection ---
    ax = axes[2]
    ax.set_title('C. Failed Block / Intravascular', fontsize=13, fontweight='bold', pad=10, color=COLORS['failure'])
    
    # Injection directly into bloodstream
    ax.annotate('Inadvertent\nIV Injection', xy=(5, 9.2), fontsize=9, ha='center', fontstyle='italic', color='#555')
    ax.annotate('', xy=(5, 8.5), xytext=(5, 8.9),
                arrowprops=dict(arrowstyle='->', color=COLORS['failure'], lw=2.5))
    
    # Plasma (V1) - highlighted as starting point
    draw_box(ax, (2.5, 6.8), 5, 1.5, 'Plasma (V1)', COLORS['plasma'])
    ax.add_patch(plt.Rectangle((2.3, 6.6), 5.4, 1.9, fill=False,
                               edgecolor=COLORS['failure'], linewidth=3, linestyle='--'))
    
    # BRT (V2) - rapid distribution
    draw_box(ax, (0.3, 3.5), 4, 1.3, 'BRT (V2)\nRapid uptake', COLORS['brt'], fontsize=9)
    
    # BPT (V3)
    draw_box(ax, (5.7, 3.5), 4, 1.3, 'BPT (V3)', COLORS['bpt'], fontsize=9)
    
    # Elimination
    draw_box(ax, (3.2, 0.8), 3.6, 1.0, 'Elimination (CL)', COLORS['elimination'], fontsize=9)
    
    # Arrows - fast to BRT
    draw_arrow(ax, (3.5, 6.8), (2.3, 4.8), COLORS['brt'], lw=3)
    draw_arrow(ax, (2.3, 4.8), (3.5, 6.8), COLORS['brt'], style='->')
    ax.text(0.8, 5.9, 'Fast', fontsize=9, color=COLORS['failure'], fontweight='bold')
    
    draw_arrow(ax, (6.5, 6.8), (7.7, 4.8), COLORS['bpt'], lw=1)
    draw_arrow(ax, (7.7, 4.8), (6.5, 6.8), COLORS['bpt'], style='->')
    
    draw_arrow(ax, (5, 6.8), (5, 1.8), COLORS['elimination'])
    
    # Key annotation
    ax.text(5, 9.8, 'Drug starts in plasma/BRT',
            fontsize=9, ha='center', color=COLORS['failure'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFEBEE', edgecolor=COLORS['failure']))
    
    plt.tight_layout(pad=1.0)
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure1_compartment_models.png'),
                dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure1_compartment_models.tiff'),
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("Figure 1 saved.")


# ============================================================
# FIGURE 2: Simulated Plasma Concentration–Time Curves
# ============================================================
def figure2():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    t = np.linspace(0, 480, 1000)  # 0 to 480 min (8 hours)
    
    # --- Scenario A: Traditional IV bolus (into plasma) ---
    # Three-compartment model: C(t) = A*exp(-alpha*t) + B*exp(-beta*t) + C0*exp(-gamma*t)
    # Typical parameters for bupivacaine-like LA
    A_iv = 3.0; alpha = 0.15   # rapid distribution
    B_iv = 1.5; beta = 0.02    # slow distribution
    C_iv = 0.5; gamma = 0.003  # terminal elimination
    Cp_iv = A_iv * np.exp(-alpha * t) + B_iv * np.exp(-beta * t) + C_iv * np.exp(-gamma * t)
    
    # --- Scenario B: Failed block (drug into BRT, rapid absorption) ---
    # Modeled as first-order absorption from BRT with ka_fast
    ka_fast = 0.08
    F_fast = 0.95
    dose_factor = 4.0
    Cp_failed = dose_factor * F_fast * (
        (ka_fast / (ka_fast - alpha)) * (np.exp(-alpha * t) - np.exp(-ka_fast * t)) * 0.5 +
        (ka_fast / (ka_fast - beta)) * (np.exp(-beta * t) - np.exp(-ka_fast * t)) * 0.35 +
        (ka_fast / (ka_fast - gamma)) * (np.exp(-gamma * t) - np.exp(-ka_fast * t)) * 0.15
    )
    Cp_failed = np.maximum(Cp_failed, 0)
    
    # --- Scenario C: Successful block (drug into BPT, slow absorption) ---
    ka_slow = 0.008
    F_slow = 0.65
    Cp_success = dose_factor * F_slow * (
        (ka_slow / (ka_slow - alpha)) * (np.exp(-alpha * t) - np.exp(-ka_slow * t)) * 0.5 +
        (ka_slow / (ka_slow - beta)) * (np.exp(-beta * t) - np.exp(-ka_slow * t)) * 0.35 +
        (ka_slow / (ka_slow - gamma)) * (np.exp(-gamma * t) - np.exp(-ka_slow * t)) * 0.15
    )
    Cp_success = np.maximum(Cp_success, 0)
    
    # --- Scenario D: Partial block (mixed) ---
    frac_depot = 0.6
    frac_plasma = 0.4
    Cp_partial = frac_depot * Cp_success + frac_plasma * Cp_failed
    
    # Plot
    ax.plot(t, Cp_iv, color=COLORS['plasma'], linewidth=2.5, label='IV bolus (traditional model)', linestyle='-')
    ax.plot(t, Cp_failed, color=COLORS['failure'], linewidth=2.5, label='Failed block (BRT/plasma start)', linestyle='--')
    ax.plot(t, Cp_success, color=COLORS['success'], linewidth=2.5, label='Successful block (BPT start)', linestyle='-.')
    ax.plot(t, Cp_partial, color=COLORS['partial'], linewidth=2.0, label='Partial block (mixed)', linestyle=':')
    
    # Toxicity threshold
    ax.axhline(y=2.0, color='red', linewidth=1.5, linestyle='--', alpha=0.6)
    ax.text(400, 2.15, 'CNS toxicity threshold', fontsize=9, color='red', alpha=0.8)
    ax.axhline(y=4.0, color='darkred', linewidth=1.5, linestyle='--', alpha=0.6)
    ax.text(400, 4.15, 'Cardiovascular toxicity threshold', fontsize=9, color='darkred', alpha=0.8)
    
    ax.set_xlabel('Time (min)', fontsize=12)
    ax.set_ylabel('Plasma Concentration (arbitrary units)', fontsize=12)
    ax.set_title('Simulated Plasma Concentration-Time Profiles\nby Initial Compartment of Drug Deposition',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax.set_xlim(0, 480)
    ax.set_ylim(0, 5.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3)
    
    # Annotation arrows
    # Peak for failed block
    idx_peak_fail = np.argmax(Cp_failed)
    ax.annotate(f'Cmax = {Cp_failed[idx_peak_fail]:.1f}\nt = {t[idx_peak_fail]:.0f} min',
                xy=(t[idx_peak_fail], Cp_failed[idx_peak_fail]),
                xytext=(t[idx_peak_fail]+40, Cp_failed[idx_peak_fail]+0.6),
                fontsize=8, color=COLORS['failure'],
                arrowprops=dict(arrowstyle='->', color=COLORS['failure'], lw=1.2))
    
    # Peak for successful block
    idx_peak_succ = np.argmax(Cp_success)
    ax.annotate(f'Cmax = {Cp_success[idx_peak_succ]:.1f}\nt = {t[idx_peak_succ]:.0f} min',
                xy=(t[idx_peak_succ], Cp_success[idx_peak_succ]),
                xytext=(t[idx_peak_succ]+40, Cp_success[idx_peak_succ]+0.5),
                fontsize=8, color=COLORS['success'],
                arrowprops=dict(arrowstyle='->', color=COLORS['success'], lw=1.2))
    
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure2_pk_simulation.png'),
                dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure2_pk_simulation.tiff'),
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("Figure 2 saved.")


# ============================================================
# FIGURE 3: Proposed Workflow for PBPK-Based Maximum Dose
#            Reassessment
# ============================================================
def figure3():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Proposed PBPK-Based Workflow for Maximum Dose Reassessment\nin Regional Anaesthesia',
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Step 1: Clinical Assessment
    draw_box(ax, (0.5, 7.3), 3.5, 1.3, 'Step 1\nClinical Assessment', '#5C6BC0', fontsize=10)
    ax.text(2.25, 6.6, 'Block type, site, success\nprobability, patient factors',
            ha='center', va='top', fontsize=8, color='#555', fontstyle='italic')
    
    # Step 2: Initial Compartment Selection
    draw_box(ax, (5.25, 7.3), 3.5, 1.3, 'Step 2\nInitial Compartment\nSelection', COLORS['depot'], fontsize=10)
    
    # Branch arrows from Step 2
    # Success path
    draw_box(ax, (0.5, 4.3), 3.2, 1.2, 'Successful Block\nBPT Start', COLORS['success'], fontsize=9)
    # Partial path
    draw_box(ax, (4.4, 4.3), 3.2, 1.2, 'Partial Block\nMixed Start', COLORS['partial'], fontsize=9)
    # Failure path
    draw_box(ax, (8.3, 4.3), 3.2, 1.2, 'Failed Block\nPlasma/BRT Start', COLORS['failure'], fontsize=9)
    
    # Arrows from Step 1 -> Step 2
    draw_arrow(ax, (4.0, 7.95), (5.25, 7.95), COLORS['arrow'], lw=2)
    
    # Arrows from Step 2 -> branches
    draw_arrow(ax, (6.0, 7.3), (2.1, 5.5), COLORS['success'], lw=1.5)
    draw_arrow(ax, (7.0, 7.3), (6.0, 5.5), COLORS['partial'], lw=1.5)
    draw_arrow(ax, (8.0, 7.3), (9.9, 5.5), COLORS['failure'], lw=1.5)
    
    # Step 3: PBPK Simulation
    draw_box(ax, (10.0, 7.3), 3.5, 1.3, 'Step 3\nPBPK Simulation\n(PK-Sim / MoBi)', '#7B1FA2', fontsize=10)
    
    # Arrow from Step 2 -> Step 3
    draw_arrow(ax, (8.75, 7.95), (10.0, 7.95), COLORS['arrow'], lw=2)
    
    # Arrows from branches -> Step 4
    draw_arrow(ax, (2.1, 4.3), (4.5, 2.6), COLORS['success'], lw=1.5)
    draw_arrow(ax, (6.0, 4.3), (6.5, 2.6), COLORS['partial'], lw=1.5)
    draw_arrow(ax, (9.9, 4.3), (8.5, 2.6), COLORS['failure'], lw=1.5)
    
    # Step 4: Context-Sensitive Maximum Dose
    draw_box(ax, (3.5, 1.2), 7, 1.4, 'Step 4: Context-Sensitive Maximum Dose Recommendation', '#00695C', fontsize=11)
    
    # Annotations for each scenario
    ax.text(2.1, 3.8, 'Lower Cmax\nHigher safe dose', ha='center', fontsize=7.5, color=COLORS['success'], fontweight='bold')
    ax.text(6.0, 3.8, 'Intermediate\nCmax', ha='center', fontsize=7.5, color='#E65100', fontweight='bold')
    ax.text(9.9, 3.8, 'Higher Cmax\nLower safe dose', ha='center', fontsize=7.5, color=COLORS['failure'], fontweight='bold')
    
    # Arrow from Step 3 down
    draw_arrow(ax, (11.75, 7.3), (11.75, 3.0), '#7B1FA2', lw=1.5)
    ax.text(12.0, 5.2, 'Simulation\nresults', fontsize=8, color='#7B1FA2', fontstyle='italic')
    draw_arrow(ax, (11.75, 3.0), (10.5, 2.6), '#7B1FA2', lw=1.5)
    
    # Bottom note
    ax.text(7, 0.5, 'Outcome: Individualised, scenario-dependent maximum dose\nbased on predicted plasma concentration profile',
            ha='center', fontsize=9, color='#333', fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#E0F2F1', edgecolor='#00695C', alpha=0.8))
    
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure3_workflow.png'),
                dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure3_workflow.tiff'),
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("Figure 3 saved.")


if __name__ == '__main__':
    figure1()
    figure2()
    figure3()
    print("All figures generated successfully.")
