#!/usr/bin/env python3
"""Generate color figures for the RAPM manuscript.

Target: Regional Anesthesia & Pain Medicine
Figures 1-3 only (Figure 4 removed in restructuring).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
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
    text_color = 'white' if color not in ['#FF9800', '#FAFAFA', '#E0E0E0'] else 'black'
    ax.text(xy[0] + w/2, xy[1] + h/2, label,
            ha='center', va='center', fontsize=fontsize,
            fontweight=weight, color=text_color)

def draw_arrow(ax, start, end, color='#37474F', style='->', lw=2, connectionstyle="arc3,rad=0"):
    arrow = FancyArrowPatch(start, end,
                            arrowstyle=style,
                            connectionstyle=connectionstyle,
                            color=color, linewidth=lw,
                            mutation_scale=15)
    ax.add_patch(arrow)

# ============================================================
# FIGURE 1: Comparison of IV vs Depot-Augmented Models (2 panels)
# ============================================================
def figure1():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')

    # --- Panel A: Standard IV Three-Compartment Model ---
    ax = axes[0]
    ax.set_title('A. Standard IV Three-Compartment Model',
                 fontsize=13, fontweight='bold', pad=10)

    # IV input
    ax.annotate('IV Bolus\n(drug enters plasma directly)',
                xy=(5, 9.2), fontsize=9, ha='center', fontstyle='italic', color='#555')
    ax.annotate('', xy=(5, 8.6), xytext=(5, 9.0),
                arrowprops=dict(arrowstyle='->', color=COLORS['arrow'], lw=2.5))

    # Plasma (V1)
    draw_box(ax, (2.5, 6.8), 5, 1.5, 'V1: Plasma\n(Central)', COLORS['plasma'])

    # BRT (V2)
    draw_box(ax, (0.3, 3.5), 4, 1.3, 'V2: Vessel-Rich\nTissues (BRT)', COLORS['brt'], fontsize=9)

    # BPT (V3)
    draw_box(ax, (5.7, 3.5), 4, 1.3, 'V3: Vessel-Poor\nTissues (BPT)', COLORS['bpt'], fontsize=9)

    # Elimination
    draw_box(ax, (3.2, 0.8), 3.6, 1.0, 'Elimination (CL)', COLORS['elimination'], fontsize=9)

    # Arrows
    draw_arrow(ax, (3.5, 6.8), (2.3, 4.8), COLORS['brt'])
    draw_arrow(ax, (2.3, 4.8), (3.5, 6.8), COLORS['brt'], style='->')
    ax.text(1.0, 5.9, 'k$_{12}$ / k$_{21}$', fontsize=8, color=COLORS['brt'])

    draw_arrow(ax, (6.5, 6.8), (7.7, 4.8), COLORS['bpt'])
    draw_arrow(ax, (7.7, 4.8), (6.5, 6.8), COLORS['bpt'], style='->')
    ax.text(7.8, 5.9, 'k$_{13}$ / k$_{31}$', fontsize=8, color=COLORS['bpt'])

    draw_arrow(ax, (5, 6.8), (5, 1.8), COLORS['elimination'])

    # Highlight input point
    ax.add_patch(plt.Circle((5, 7.55), 0.3, color='yellow', alpha=0.4, zorder=0))

    # Key point
    ax.text(5, 0.1, 'No absorption compartment;\nassumes instantaneous plasma input',
            ha='center', fontsize=9, color='#C62828', fontstyle='italic')

    # --- Panel B: Depot-Augmented Model for Regional Anesthesia ---
    ax = axes[1]
    ax.set_title('B. Depot-Augmented Model for Regional Anesthesia',
                 fontsize=13, fontweight='bold', pad=10, color=COLORS['depot'])

    # Regional injection
    ax.annotate('Regional Injection\n(tissue deposition)',
                xy=(7.5, 9.2), fontsize=9, ha='center', fontstyle='italic', color='#555')
    ax.annotate('', xy=(7.5, 8.5), xytext=(7.5, 8.9),
                arrowprops=dict(arrowstyle='->', color=COLORS['depot'], lw=2.5))

    # Depot compartment
    draw_box(ax, (5.5, 6.8), 4, 1.5, 'Depot\n(Tissue at injection site)', COLORS['depot'], fontsize=10)

    # Plasma (V1)
    draw_box(ax, (2.5, 3.8), 5, 1.3, 'V1: Plasma (Central)', COLORS['plasma'])

    # Elimination
    draw_box(ax, (0.3, 1.0), 4, 1.0, 'V2/V3:\nPeripheral', '#78909C', fontsize=9)
    draw_box(ax, (5.7, 1.0), 4, 1.0, 'Elimination (CL)', COLORS['elimination'], fontsize=9)

    # Depot -> Plasma (slow absorption)
    draw_arrow(ax, (6.5, 6.8), (5.5, 5.1), COLORS['depot'], lw=2.5)
    ax.text(4.5, 6.0, 'k$_a$ (absorption)\nF (bioavailability)',
            fontsize=9, color=COLORS['depot'], fontweight='bold')

    # Plasma <-> Peripheral
    draw_arrow(ax, (3.5, 3.8), (2.3, 2.0), '#78909C')
    draw_arrow(ax, (2.3, 2.0), (3.5, 3.8), '#78909C', style='->')

    # Plasma -> Elimination
    draw_arrow(ax, (6.5, 3.8), (7.7, 2.0), COLORS['elimination'])

    # Key point
    ax.text(5, 0.1, 'Absorption rate (k$_a$) and bioavailability (F)\nare route-specific and block-type-dependent',
            ha='center', fontsize=9, color='#E65100', fontstyle='italic')

    # Annotation: ka varies
    ax.text(1.0, 6.0, 'k$_a$ varies by:\n\u2022 Block type\n\u2022 Tissue vascularity\n\u2022 Vasoconstrictor use',
            fontsize=8, color='#555', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3E0', edgecolor=COLORS['depot'], alpha=0.8))

    plt.tight_layout(pad=1.5)
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure1_compartment_models.png'),
                dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure1_compartment_models.tiff'),
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("Figure 1 saved.")


# ============================================================
# FIGURE 2: Simulated Plasma Concentration-Time Curves
# ============================================================
def figure2():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    t = np.linspace(0, 480, 1000)  # 0 to 480 min (8 hours)

    # --- Scenario A: IV bolus (into plasma) ---
    A_iv = 3.0; alpha = 0.15
    B_iv = 1.5; beta = 0.02
    C_iv = 0.5; gamma = 0.003
    Cp_iv = A_iv * np.exp(-alpha * t) + B_iv * np.exp(-beta * t) + C_iv * np.exp(-gamma * t)

    # --- Scenario B: Rapid absorption (high vascularity, ka=0.1) ---
    ka_fast = 0.1
    F_fast = 0.95
    dose_factor = 4.0
    Cp_rapid = dose_factor * F_fast * (
        (ka_fast / (ka_fast - alpha)) * (np.exp(-alpha * t) - np.exp(-ka_fast * t)) * 0.5 +
        (ka_fast / (ka_fast - beta)) * (np.exp(-beta * t) - np.exp(-ka_fast * t)) * 0.35 +
        (ka_fast / (ka_fast - gamma)) * (np.exp(-gamma * t) - np.exp(-ka_fast * t)) * 0.15
    )
    Cp_rapid = np.maximum(Cp_rapid, 0)

    # --- Scenario C: Slow absorption (fascial plane, ka=0.03) ---
    ka_slow = 0.03
    F_slow = 0.70
    Cp_slow = dose_factor * F_slow * (
        (ka_slow / (ka_slow - alpha)) * (np.exp(-alpha * t) - np.exp(-ka_slow * t)) * 0.5 +
        (ka_slow / (ka_slow - beta)) * (np.exp(-beta * t) - np.exp(-ka_slow * t)) * 0.35 +
        (ka_slow / (ka_slow - gamma)) * (np.exp(-gamma * t) - np.exp(-ka_slow * t)) * 0.15
    )
    Cp_slow = np.maximum(Cp_slow, 0)

    # Plot
    ax.plot(t, Cp_iv, color=COLORS['plasma'], linewidth=2.5,
            label='IV bolus (standard 3-compartment model)', linestyle='-')
    ax.plot(t, Cp_rapid, color=COLORS['failure'], linewidth=2.5,
            label='Rapid absorption (k$_a$ = 0.1 min$^{-1}$)', linestyle='--')
    ax.plot(t, Cp_slow, color=COLORS['success'], linewidth=2.5,
            label='Slow absorption (k$_a$ = 0.03 min$^{-1}$, fascial plane)', linestyle='-.')

    # Toxicity thresholds
    ax.axhline(y=2.0, color='red', linewidth=1.5, linestyle='--', alpha=0.6)
    ax.text(400, 2.15, 'CNS toxicity threshold', fontsize=9, color='red', alpha=0.8)
    ax.axhline(y=4.0, color='darkred', linewidth=1.5, linestyle='--', alpha=0.6)
    ax.text(400, 4.15, 'CVS toxicity threshold', fontsize=9, color='darkred', alpha=0.8)

    # Monitoring window annotations
    # Traditional monitoring window
    ax.axvspan(0, 30, alpha=0.08, color='blue', label='_nolegend_')
    ax.text(15, 5.2, 'Traditional\nmonitoring\nwindow', fontsize=8, ha='center',
            color='blue', alpha=0.7, fontstyle='italic')

    # Delayed Tmax window for slow absorption
    idx_peak_slow = np.argmax(Cp_slow)
    tmax_slow = t[idx_peak_slow]
    ax.axvspan(tmax_slow - 15, tmax_slow + 15, alpha=0.08, color='green', label='_nolegend_')
    ax.annotate(f'True Tmax\n({tmax_slow:.0f} min)',
                xy=(tmax_slow, Cp_slow[idx_peak_slow]),
                xytext=(tmax_slow + 50, Cp_slow[idx_peak_slow] + 0.6),
                fontsize=9, color=COLORS['success'], fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['success'], lw=1.5))

    # Peak for rapid absorption
    idx_peak_rapid = np.argmax(Cp_rapid)
    ax.annotate(f'Cmax = {Cp_rapid[idx_peak_rapid]:.1f}\nt = {t[idx_peak_rapid]:.0f} min',
                xy=(t[idx_peak_rapid], Cp_rapid[idx_peak_rapid]),
                xytext=(t[idx_peak_rapid] + 40, Cp_rapid[idx_peak_rapid] + 0.5),
                fontsize=8, color=COLORS['failure'],
                arrowprops=dict(arrowstyle='->', color=COLORS['failure'], lw=1.2))

    ax.set_xlabel('Time (min)', fontsize=12)
    ax.set_ylabel('Plasma Concentration (arbitrary units)', fontsize=12)
    ax.set_title('Simulated Plasma Concentration-Time Profiles\nby Route of Administration',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax.set_xlim(0, 480)
    ax.set_ylim(0, 5.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure2_pk_simulation.png'),
                dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(OUTPUT_DIR, 'figure2_pk_simulation.tiff'),
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("Figure 2 saved.")


# ============================================================
# FIGURE 3: Route-Specific PBPK Model Development and
#            Validation Workflow
# ============================================================
def figure3():
    fig, ax = plt.subplots(1, 1, figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Proposed Workflow for Route-Specific Pharmacokinetic Model\nDevelopment and Validation',
            ha='center', va='center', fontsize=14, fontweight='bold')

    # Step 1: Published PopPK Data
    draw_box(ax, (0.5, 7.0), 3.0, 1.5, 'Step 1\nPublished\nPopulation PK Data', '#5C6BC0', fontsize=10)
    ax.text(2.0, 6.4, 'ka, F, Tmax, Cmax\nfor each block type',
            ha='center', va='top', fontsize=8, color='#555', fontstyle='italic')

    # Step 2: PBPK Model Configuration
    draw_box(ax, (5.0, 7.0), 3.5, 1.5, 'Step 2\nPBPK Model\nConfiguration\n(PK-Sim / MoBi)', '#7B1FA2', fontsize=9)

    # Step 3: Model Validation
    draw_box(ax, (10.0, 7.0), 3.5, 1.5, 'Step 3\nModel Validation\nvs. Independent\nClinical Data', '#00695C', fontsize=9)

    # Arrow: Step 1 -> Step 2
    draw_arrow(ax, (3.5, 7.75), (5.0, 7.75), COLORS['arrow'], lw=2.5)
    ax.text(4.25, 8.1, 'Parameterize', fontsize=8, ha='center', color='#555')

    # Arrow: Step 2 -> Step 3
    draw_arrow(ax, (8.5, 7.75), (10.0, 7.75), COLORS['arrow'], lw=2.5)
    ax.text(9.25, 8.1, 'Predict', fontsize=8, ha='center', color='#555')

    # Validation outcome: branch
    # Pass
    draw_box(ax, (9.5, 4.2), 2.5, 1.0, 'Validated', '#4CAF50', fontsize=10)
    # Fail
    draw_box(ax, (12.5, 4.2), 1.3, 1.0, 'Refine', '#F44336', fontsize=9)

    draw_arrow(ax, (11.0, 7.0), (10.7, 5.2), '#4CAF50', lw=1.5)
    draw_arrow(ax, (12.2, 7.0), (13.1, 5.2), '#F44336', lw=1.5)

    # Refine loops back to Step 2
    draw_arrow(ax, (13.1, 5.2), (13.5, 6.5), '#F44336', lw=1.2,
               connectionstyle="arc3,rad=-0.3")
    draw_arrow(ax, (13.5, 6.5), (8.5, 7.4), '#F44336', lw=1.2,
               connectionstyle="arc3,rad=-0.2")

    # Step 4: Clinical Decision Support (future)
    draw_box(ax, (4.0, 1.5), 5.5, 1.5, 'Step 4 (Future)\nIntegration into Clinical Decision Support\n(complement to existing dose limits)',
             '#37474F', fontsize=10)

    # Arrow from Validated -> Step 4
    draw_arrow(ax, (10.7, 4.2), (9.5, 3.0), '#4CAF50', lw=2)

    # Block type examples feeding into Step 1
    block_types = ['Fascial plane\nblocks', 'Peripheral\nnerve blocks', 'Epidural']
    positions = [(0.5, 4.5), (0.5, 3.3), (0.5, 2.1)]
    for pos, label in zip(positions, block_types):
        draw_box(ax, pos, 2.5, 0.9, label, '#E3F2FD', fontsize=8, bold=False)

    # Arrows from block types to Step 1
    for pos in positions:
        draw_arrow(ax, (pos[0] + 2.5, pos[1] + 0.8), (1.5, 7.0), '#5C6BC0', lw=1.0,
                   connectionstyle="arc3,rad=0.2")

    # Safety note at bottom
    ax.text(7, 0.4,
            'Note: Current maximum dose recommendations remain in effect throughout.\n'
            'Route-specific models complement (do not replace) existing safety limits.',
            ha='center', fontsize=9, color='#C62828', fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFEBEE', edgecolor='#C62828', alpha=0.8))

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
