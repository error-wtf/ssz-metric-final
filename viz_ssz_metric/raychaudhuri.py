# -*- coding: utf-8 -*-
"""
PHASE 20: Raychaudhuri-Gleichung

Die Raychaudhuri-Gleichung beschreibt die Fokussierung geodätischer Kongruenzen:

dθ/dλ = -(1/3)θ² - σ²_ab + ω²_ab - R_ab u^a u^b

wobei:
- θ: Expansion (Divergenz des Geschwindigkeitsfelds)
- σ_ab: Scherung (Shear)
- ω_ab: Rotation (Vortizität)
- R_ab u^a u^b: Ricci-fokussierung

Wichtig für: Singularitäts-Theoreme (Penrose-Hawking)

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Tuple
from .ricci_curvature import ricci_tensor_diagonal
from .ssz_mirror_metric import metric_functions_pn, schwarzschild_radius


def expansion_scalar(mass: float, r: float, v_r: float) -> float:
    """Expansions-Skalar θ = ∇_a u^a für radiale Geodäte.
    
    Für radial einfallende Materie (u^r ≠ 0, u^θ = u^φ = 0):
    θ ≈ (2/r) + (1/√B) d√B/dr · v_r
    
    Args:
        mass: Masse in kg
        r: Radius in m
        v_r: Radiale Geschwindigkeit (m/s)
    
    Returns:
        θ (Expansion in 1/s)
    """
    from .christoffel_symbols import dB_dr_numerical
    
    A, B = metric_functions_pn(mass, r)
    dB = dB_dr_numerical(mass, r)
    
    # Expansion für radiale Bewegung
    theta = (2.0 / r) + (1.0 / (2*np.sqrt(B))) * dB * v_r / np.sqrt(B)
    
    return theta


def shear_scalar(mass: float, r: float, v_r: float) -> float:
    """Scherungs-Skalar σ² = σ_ab σ^ab.
    
    Scherung misst nicht-isotrope Deformation der Kongruenz.
    
    Für sphärische Symmetrie (radiale Bewegung): σ² = 0
    
    Args:
        mass: Masse in kg
        r: Radius in m
        v_r: Radiale Geschwindigkeit
    
    Returns:
        σ² (Scherung²)
    """
    # In exakter sphärischer Symmetrie: keine Scherung!
    return 0.0


def rotation_scalar(mass: float, r: float) -> float:
    """Rotations-Skalar ω² = ω_ab ω^ab.
    
    Rotation misst Wirbelstärke der Kongruenz.
    
    Für statische, sphärisch-symmetrische Metrik: ω² = 0
    
    Args:
        mass: Masse in kg
        r: Radius in m
    
    Returns:
        ω² (Rotation²)
    """
    # Statisch → keine Rotation
    return 0.0


def ricci_focusing_term(mass: float, r: float, theta: float, u_t: float, u_r: float) -> float:
    """Ricci-Fokussierungs-Term R_ab u^a u^b.
    
    Dies ist der Materie-Beitrag zur Fokussierung.
    
    Für zeitartige Geodäte mit 4-Geschwindigkeit u^μ = (u^t, u^r, 0, 0):
    R_ab u^a u^b = R_tt (u^t)² + R_rr (u^r)²
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
        u_t: Zeitliche 4-Geschwindigkeit
        u_r: Radiale 4-Geschwindigkeit
    
    Returns:
        R_ab u^a u^b
    """
    R_tt, R_rr, _, _ = ricci_tensor_diagonal(mass, r, theta)
    
    # Normierung: u_a u^a = -1 (zeitartig)
    A, B = metric_functions_pn(mass, r)
    
    # Ricci-Fokussierung
    R_focus = (-A * R_tt * (u_t**2)) + (B * R_rr * (u_r**2))
    
    return R_focus


def raychaudhuri_equation(mass: float, r: float, theta: float, 
                          v_r: float, u_t: float = 1.0) -> float:
    """Berechne Raychaudhuri-Gleichung dθ/dλ.
    
    dθ/dλ = -(1/3)θ² - σ² + ω² - R_ab u^a u^b
    
    Für radiale, zeitartige Geodäte in SSZ-Metrik.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
        v_r: Radiale Geschwindigkeit (m/s)
        u_t: Zeitliche 4-Geschwindigkeit (normalisiert)
    
    Returns:
        dθ/dλ (Änderungsrate der Expansion)
    """
    # Komponenten
    theta_exp = expansion_scalar(mass, r, v_r)
    sigma_sq = shear_scalar(mass, r, v_r)
    omega_sq = rotation_scalar(mass, r)
    
    # 4-Geschwindigkeit (normalisiert für u_a u^a = -1)
    A, _ = metric_functions_pn(mass, r)
    u_r = v_r / np.sqrt(A)  # Approximation
    
    R_focus = ricci_focusing_term(mass, r, theta, u_t, u_r)
    
    # Raychaudhuri-Gleichung
    dtheta_dlambda = -(1.0/3.0) * (theta_exp**2) - sigma_sq + omega_sq - R_focus
    
    return dtheta_dlambda


def focusing_theorem_check(mass: float, r: float, theta: float, v_r: float) -> dict:
    """Prüfe Fokussierungs-Theorem (Penrose-Hawking).
    
    Bedingung: Wenn R_ab u^a u^b ≥ 0 (Energie-Bedingung)
    und θ < 0 an einem Punkt, dann θ → -∞ in endlicher Zeit
    → Singularität unvermeidbar!
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
        v_r: Radiale Geschwindigkeit
    
    Returns:
        dict mit Analyse-Ergebnissen
    """
    theta_exp = expansion_scalar(mass, r, v_r)
    dtheta = raychaudhuri_equation(mass, r, theta, v_r)
    
    A, _ = metric_functions_pn(mass, r)
    u_t = 1.0
    u_r = v_r / np.sqrt(A)
    R_focus = ricci_focusing_term(mass, r, theta, u_t, u_r)
    
    # Prüfe Bedingungen
    energy_condition_satisfied = R_focus >= 0
    expansion_negative = theta_exp < 0
    diverging = (dtheta < 0) and expansion_negative
    
    # Zeit bis zur Singularität (wenn θ → -∞)
    if diverging and abs(theta_exp) > 1e-10:
        time_to_singularity = -3.0 / theta_exp  # λ_sing ≈ -3/θ₀
    else:
        time_to_singularity = np.inf
    
    return {
        'theta': theta_exp,
        'dtheta/dlambda': dtheta,
        'R_focus': R_focus,
        'energy_condition_OK': energy_condition_satisfied,
        'focusing': diverging,
        'time_to_singularity': time_to_singularity
    }


def demo():
    """Demo: Raychaudhuri-Gleichung für freien Fall."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r_arr = np.linspace(2*rs, 10*rs, 100)
    theta_test = np.pi / 2
    
    # Verschiedene Geschwindigkeiten
    velocities = {
        'langsam': -1e5,    # -100 km/s
        'mittel': -1e6,     # -1000 km/s
        'schnell': -1e7,    # -10000 km/s
    }
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    for label, v_r in velocities.items():
        theta_arr = []
        dtheta_arr = []
        R_focus_arr = []
        
        for r in r_arr:
            theta_exp = expansion_scalar(M_sun, r, v_r)
            dtheta = raychaudhuri_equation(M_sun, r, theta_test, v_r)
            
            A, _ = metric_functions_pn(M_sun, r)
            u_r = v_r / np.sqrt(A)
            R_focus = ricci_focusing_term(M_sun, r, theta_test, 1.0, u_r)
            
            theta_arr.append(theta_exp)
            dtheta_arr.append(dtheta)
            R_focus_arr.append(R_focus)
        
        theta_arr = np.array(theta_arr)
        dtheta_arr = np.array(dtheta_arr)
        R_focus_arr = np.array(R_focus_arr)
        
        # Plot einzelne Komponenten
        axes[0,0].plot(r_arr/rs, theta_arr * rs, lw=2, label=label)
        axes[0,1].plot(r_arr/rs, dtheta_arr * (rs**2), lw=2, label=label)
        axes[1,0].plot(r_arr/rs, R_focus_arr * (rs**2), lw=2, label=label)
    
    # Top-left: Expansion θ
    axes[0,0].set_ylabel('r_s · θ')
    axes[0,0].set_title('Expansion-Skalar')
    axes[0,0].legend()
    axes[0,0].grid(alpha=0.3)
    axes[0,0].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[0,0].set_xlabel('r/r_s')
    
    # Top-right: dθ/dλ
    axes[0,1].set_ylabel('r_s² · dθ/dλ')
    axes[0,1].set_title('Raychaudhuri dθ/dλ')
    axes[0,1].legend()
    axes[0,1].grid(alpha=0.3)
    axes[0,1].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[0,1].set_xlabel('r/r_s')
    
    # Bottom-left: Ricci-Fokussierung
    axes[1,0].set_ylabel('r_s² · R_ab u^a u^b')
    axes[1,0].set_title('Ricci-Fokussierungs-Term')
    axes[1,0].legend()
    axes[1,0].grid(alpha=0.3)
    axes[1,0].axhline(0, ls='--', color='red', alpha=0.5)
    axes[1,0].set_xlabel('r/r_s')
    
    # Bottom-right: Fokussierungs-Theorem
    axes[1,1].remove()
    axes[1,1] = fig.add_subplot(2, 2, 4)
    axes[1,1].axis('off')
    
    # Tabelle mit Fokussierungs-Analyse
    print("\n" + "="*80)
    print("RAYCHAUDHURI & FOKUSSIERUNGS-THEOREM")
    print("="*80)
    print(f"{'r/r_s':>8} {'v_r [km/s]':>12} {'θ [1/s]':>15} {'dθ/dλ':>15} {'Fokussierung':>15}")
    print("-"*80)
    
    text_lines = []
    for r_mult in [2, 3, 5]:
        r = r_mult * rs
        for label, v_r in velocities.items():
            result = focusing_theorem_check(M_sun, r, theta_test, v_r)
            
            focus_str = "JA" if result['focusing'] else "NEIN"
            
            print(f"{r_mult:>8} {v_r/1e3:>12.0f} {result['theta']:>15.6e} "
                  f"{result['dtheta/dlambda']:>15.6e} {focus_str:>15}")
            
            if r_mult == 2 and result['focusing']:
                time_str = f"{result['time_to_singularity']:.3e} s" if np.isfinite(result['time_to_singularity']) else "∞"
                text_lines.append(f"• {label}: Zeit bis Singularität ≈ {time_str}")
    
    print("="*80)
    
    # Text in Plot
    text_content = "FOKUSSIERUNGS-ANALYSE (r=2r_s):\n\n" + "\n".join(text_lines)
    text_content += "\n\n⚠️  Negative θ + dθ/dλ < 0\n    → Unvermeidbare Singularität!"
    axes[1,1].text(0.05, 0.95, text_content, transform=axes[1,1].transAxes,
                   fontsize=10, verticalalignment='top', family='monospace',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/raychaudhuri.png', dpi=150)
    print("\n✅ Saved: viz_ssz_metric/out/raychaudhuri.png")


if __name__ == "__main__":
    demo()
