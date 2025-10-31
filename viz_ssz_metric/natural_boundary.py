# -*- coding: utf-8 -*-
"""
PHASE 8: Natürliche Grenze r_φ

Physikalische Interpretation des φ-Radius als fundamentale Grenze
in der Segmented Spacetime Theorie.

r_φ < r_s → SSZ-Horizont liegt INNERHALB des Schwarzschild-Horizonts!

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from .mass_corrections import r_phi, delta_M, r_phi_vs_r_s_ratio
from .ssz_mirror_metric import schwarzschild_radius, Xi, PHI


def natural_horizon_comparison(mass: float, varphi: float = PHI):
    """Vergleiche SSZ-Horizont (r_φ) mit GR-Horizont (r_s).
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
    
    Returns:
        dict mit Keys:
        - 'r_s': Schwarzschild-Radius
        - 'r_phi': φ-Radius
        - 'ratio': r_φ/r_s
        - 'Delta_%': Masse-Korrektur
        - 'inside': True wenn r_φ < r_s
    """
    rs = schwarzschild_radius(mass)
    rphi = r_phi(mass, varphi)
    ratio = rphi / rs
    Delta = delta_M(mass)
    
    return {
        'r_s': rs,
        'r_phi': rphi,
        'ratio': ratio,
        'Delta_%': Delta,
        'inside': rphi < rs
    }


def segment_saturation_radius(mass: float, varphi: float = PHI, threshold: float = 0.99):
    """Radius bei dem Segment-Dichte 99% der Sättigung erreicht.
    
    Löse: Ξ(r_sat) = threshold
    → 1 - exp(-φ·r_sat/r_s) = threshold
    → r_sat = -(r_s/φ)·ln(1-threshold)
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
        threshold: Sättigungsschwelle (default: 0.99 = 99%)
    
    Returns:
        r_sat in Metern
    """
    rs = schwarzschild_radius(mass)
    return -(rs / varphi) * np.log(1.0 - threshold)


def surface_gravity_at_phi(mass: float, varphi: float = PHI):
    """Oberflächen-Gravitation bei r = r_φ.
    
    g(r_φ) ≈ GM/r_φ² · (korrekturfaktor aus SSZ)
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
    
    Returns:
        g in m/s²
    """
    from .ssz_mirror_metric import G_DEFAULT, C_DEFAULT
    
    rphi = r_phi(mass, varphi)
    
    # Newtonsche Gravitation
    g_newton = G_DEFAULT * mass / (rphi ** 2)
    
    # SSZ-Korrektur (Segment-Dichte reduziert effektive Gravitation)
    rs = schwarzschild_radius(mass)
    Xi_phi = Xi(rphi, rs, varphi)
    correction = 1.0 / (1.0 + Xi_phi)  # Zeitdilatations-Faktor
    
    return g_newton * correction


def escape_velocity_at_phi(mass: float, varphi: float = PHI):
    """Fluchtgeschwindigkeit bei r = r_φ.
    
    v_esc(r_φ) = √(2GM/r_φ) · √correction
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
    
    Returns:
        v_esc in m/s
    """
    from .ssz_mirror_metric import G_DEFAULT, C_DEFAULT
    
    rphi = r_phi(mass, varphi)
    rs = schwarzschild_radius(mass)
    
    # Newtonsche v_esc
    v_esc_newton = np.sqrt(2 * G_DEFAULT * mass / rphi)
    
    # SSZ-Korrektur
    Xi_phi = Xi(rphi, rs, varphi)
    correction = 1.0 / (1.0 + Xi_phi)
    
    return v_esc_newton * np.sqrt(correction)


def demo():
    """Demo: Physikalische Eigenschaften bei r_φ."""
    import matplotlib.pyplot as plt
    
    # Verschiedene Massen
    masses = {
        'Sonne': 1.98847e30,
        '3 M☉ (NS)': 3 * 1.98847e30,
        '10 M☉ (BH)': 10 * 1.98847e30,
        'Sgr A*': 4.3e6 * 1.98847e30,
    }
    
    print("\n" + "="*100)
    print("NATÜRLICHE GRENZE r_φ: PHYSIKALISCHE EIGENSCHAFTEN")
    print("="*100)
    print(f"{'Objekt':<15} {'r_s (km)':>12} {'r_φ (km)':>12} {'r_φ/r_s':>10} "
          f"{'g(r_φ) [m/s²]':>15} {'v_esc(r_φ) [c]':>15}")
    print("-"*100)
    
    from .ssz_mirror_metric import C_DEFAULT
    
    for name, M in masses.items():
        comp = natural_horizon_comparison(M)
        g_phi = surface_gravity_at_phi(M)
        v_esc_phi = escape_velocity_at_phi(M)
        
        print(f"{name:<15} {comp['r_s']/1e3:>12.3e} {comp['r_phi']/1e3:>12.3e} "
              f"{comp['ratio']:>10.6f} {g_phi:>15.3e} {v_esc_phi/C_DEFAULT:>15.6f}")
    
    print("="*100)
    
    # Vergleich r_φ vs. r_s für verschiedene φ
    phi_values = [1.0, PHI, 2.0]
    M_sun = 1.98847e30
    mass_range = np.logspace(29, 39, 200)  # 0.5 M☉ bis 5e9 M☉
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: r_φ/r_s vs. M
    for phi_val in phi_values:
        ratios = [r_phi_vs_r_s_ratio(M, phi_val) for M in mass_range]
        ax1.semilogx(mass_range / M_sun, ratios, lw=2, label=f'φ={phi_val:.3f}')
    
    ax1.axhline(1.0, ls='--', color='red', alpha=0.5, label='r_φ = r_s')
    ax1.set_xlabel('M/M☉')
    ax1.set_ylabel('r_φ/r_s')
    ax1.set_title('SSZ-Horizont vs. GR-Horizont')
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax1.set_ylim([0.8, 1.1])
    
    # Right: Segment-Dichte bei r_φ
    Xi_at_phi = []
    for M in mass_range:
        rs = schwarzschild_radius(M)
        rphi = r_phi(M, PHI)
        Xi_val = Xi(rphi, rs, PHI)
        Xi_at_phi.append(Xi_val)
    
    ax2.semilogx(mass_range / M_sun, Xi_at_phi, lw=2.5, color='#2ca02c')
    ax2.set_xlabel('M/M☉')
    ax2.set_ylabel('Ξ(r_φ)')
    ax2.set_title('Segment-Dichte am φ-Horizont')
    ax2.grid(alpha=0.3)
    ax2.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/natural_boundary.png', dpi=150)
    print("\n✅ Saved: viz_ssz_metric/out/natural_boundary.png")
    
    # Sättigungsradius
    print("\nSegment-Sättigungsradius (99%):")
    for name, M in masses.items():
        rs = schwarzschild_radius(M)
        r_sat = segment_saturation_radius(M, PHI, 0.99)
        print(f"  {name:<15}: r_sat = {r_sat/rs:.3f} r_s = {r_sat/1e3:.3e} km")


if __name__ == "__main__":
    demo()
