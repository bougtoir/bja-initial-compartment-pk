#!/usr/bin/env python3
"""Generate Figure 4: AIMS route-adaptive PKPD schematic"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(7, 9.5, 'Route-Adaptive PKPD Simulation in AIMS', fontsize=16, fontweight='bold',
        ha='center', va='center')

# AIMS System box
aims_box = FancyBboxPatch((0.5, 0.5), 13, 8.5, boxstyle="round,pad=0.3",
                           facecolor='#F5F5F5', edgecolor='#333333', linewidth=2)
ax.add_patch(aims_box)
ax.text(7, 8.7, 'Anaesthesia Information Management System (AIMS)', fontsize=12,
        fontweight='bold', ha='center', va='center', color='#333333')

# Drug Administration Record
dar_box = FancyBboxPatch((1, 6.8), 4, 1.5, boxstyle="round,pad=0.15",
                          facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.5)
ax.add_patch(dar_box)
ax.text(3, 7.85, 'Drug Administration Record', fontsize=10, fontweight='bold',
        ha='center', va='center', color='#1565C0')
ax.text(3, 7.35, 'Route: IV / Regional (block type)', fontsize=8,
        ha='center', va='center', color='#333')
ax.text(3, 7.0, 'Drug: Bupivacaine 150 mg', fontsize=8,
        ha='center', va='center', color='#333')

# Route Detection Logic
route_box = FancyBboxPatch((6, 6.8), 3.5, 1.5, boxstyle="round,pad=0.15",
                            facecolor='#FFF3E0', edgecolor='#E65100', linewidth=1.5)
ax.add_patch(route_box)
ax.text(7.75, 7.85, 'Route Detection', fontsize=10, fontweight='bold',
        ha='center', va='center', color='#E65100')
ax.text(7.75, 7.35, 'IF route = IV:', fontsize=8, ha='center', va='center', color='#333')
ax.text(7.75, 7.1, '  \u2192 Standard 3-compartment', fontsize=7.5, ha='center', va='center', color='#333')
ax.text(7.75, 6.85, 'IF route = Regional:', fontsize=8, ha='center', va='center', color='#333')

# Arrow from DAR to Route Detection
ax.annotate('', xy=(6, 7.55), xytext=(5, 7.55),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

# PK Model Selection
# IV model
iv_box = FancyBboxPatch((1, 4.3), 3.5, 2, boxstyle="round,pad=0.15",
                         facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.5)
ax.add_patch(iv_box)
ax.text(2.75, 5.9, 'IV Model', fontsize=10, fontweight='bold',
        ha='center', va='center', color='#2E7D32')
ax.text(2.75, 5.4, '3-Compartment (Plasma start)', fontsize=8,
        ha='center', va='center', color='#333')
ax.text(2.75, 5.05, 'V1 \u2192 V2 (BRT) + V3 (BPT)', fontsize=8,
        ha='center', va='center', color='#333')
ax.text(2.75, 4.7, 'Standard Marsh/Schnider/Eleveld', fontsize=7.5,
        ha='center', va='center', color='#666')

# Regional model
reg_box = FancyBboxPatch((5.5, 4.3), 5, 2, boxstyle="round,pad=0.15",
                          facecolor='#FCE4EC', edgecolor='#C62828', linewidth=1.5)
ax.add_patch(reg_box)
ax.text(8, 5.9, 'Regional Model (Route-Adaptive)', fontsize=10, fontweight='bold',
        ha='center', va='center', color='#C62828')
ax.text(8, 5.4, 'Depot + 3-Compartment (BPT start)', fontsize=8,
        ha='center', va='center', color='#333')
ax.text(8, 5.05, 'Depot(ka, F) \u2192 V1 \u2192 V2 + V3', fontsize=8,
        ha='center', va='center', color='#333')
ax.text(8, 4.7, 'Block-type-specific ka values', fontsize=7.5,
        ha='center', va='center', color='#666')
ax.text(8, 4.4, '(TAP, ESP, FNB, Epidural, etc.)', fontsize=7.5,
        ha='center', va='center', color='#666')

# Block success feedback
feedback_box = FancyBboxPatch((10.8, 4.8), 2.5, 1.2, boxstyle="round,pad=0.15",
                               facecolor='#F3E5F5', edgecolor='#6A1B9A', linewidth=1.5)
ax.add_patch(feedback_box)
ax.text(12.05, 5.6, 'Block Success', fontsize=9, fontweight='bold',
        ha='center', va='center', color='#6A1B9A')
ax.text(12.05, 5.2, 'Feedback', fontsize=9, fontweight='bold',
        ha='center', va='center', color='#6A1B9A')
ax.text(12.05, 4.9, 'Adjust ka in real time', fontsize=7.5,
        ha='center', va='center', color='#666')

# Arrows from route detection to models
ax.annotate('', xy=(2.75, 6.3), xytext=(7, 6.8),
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5))
ax.text(4.5, 6.8, 'IV', fontsize=9, fontweight='bold', color='#2E7D32')

ax.annotate('', xy=(8, 6.3), xytext=(8, 6.8),
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.5))
ax.text(8.5, 6.65, 'Regional', fontsize=9, fontweight='bold', color='#C62828')

# Arrow from feedback to regional model
ax.annotate('', xy=(10.5, 5.3), xytext=(10.8, 5.3),
            arrowprops=dict(arrowstyle='<->', color='#6A1B9A', lw=1.2))

# AIMS Display
display_box = FancyBboxPatch((2, 1), 10, 2.8, boxstyle="round,pad=0.15",
                              facecolor='#FFFFFF', edgecolor='#37474F', linewidth=2)
ax.add_patch(display_box)
ax.text(7, 3.5, 'Real-Time AIMS Display', fontsize=11, fontweight='bold',
        ha='center', va='center', color='#37474F')

# Mini PK curves inside display
t = np.linspace(0, 5, 100)
# IV curve
y_iv = 5 * np.exp(-0.8 * t)
# Regional curve
y_reg = 2 * (np.exp(-0.15 * t) - np.exp(-0.5 * t))

# Plot mini curves
ax_mini = fig.add_axes([0.22, 0.14, 0.25, 0.2])
ax_mini.plot(t, y_iv, 'b-', linewidth=2, label='IV predicted')
ax_mini.plot(t, y_reg, 'r--', linewidth=2, label='Regional predicted')
ax_mini.axhline(y=3, color='red', linestyle=':', alpha=0.5, linewidth=1)
ax_mini.text(4, 3.2, 'Toxicity', fontsize=6, color='red', alpha=0.7)
ax_mini.set_xlabel('Time', fontsize=7)
ax_mini.set_ylabel('Cp', fontsize=7)
ax_mini.set_title('Predicted Plasma Conc.', fontsize=8)
ax_mini.legend(fontsize=6, loc='upper right')
ax_mini.tick_params(labelsize=6)
ax_mini.set_xlim(0, 5)
ax_mini.set_ylim(0, 5.5)

# Dose guidance panel
ax.text(8.5, 2.6, 'Dose Guidance Panel', fontsize=9, fontweight='bold',
        ha='center', va='center', color='#37474F')
ax.text(8.5, 2.2, 'Current dose: 150 mg bupivacaine', fontsize=8,
        ha='center', va='center', color='#333')
ax.text(8.5, 1.85, 'Route: TAP block (bilateral)', fontsize=8,
        ha='center', va='center', color='#333')
ax.text(8.5, 1.5, 'Predicted Cmax: 0.8 \u00b5g/mL (safe)', fontsize=8,
        ha='center', va='center', color='#2E7D32')
ax.text(8.5, 1.15, 'Remaining margin: 68% below threshold', fontsize=8,
        ha='center', va='center', color='#2E7D32')

# Arrows from models to display
ax.annotate('', xy=(5, 3.8), xytext=(2.75, 4.3),
            arrowprops=dict(arrowstyle='->', color='#37474F', lw=1.5))
ax.annotate('', xy=(9, 3.8), xytext=(8, 4.3),
            arrowprops=dict(arrowstyle='->', color='#37474F', lw=1.5))

plt.tight_layout()

fig_dir = '/home/ubuntu/manuscript/figures'
fig.savefig(os.path.join(fig_dir, 'figure4_aims.png'), dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
fig.savefig(os.path.join(fig_dir, 'figure4_aims.tiff'), dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('Figure 4 saved.')
plt.close()
