# -*- coding: utf-8 -*-
"""
PHASE 7: Masse-abhängige Korrekturen Δ(M)

Implementiert die empirische Formel aus dem archivierten Repo:
Δ(M) = 98.01 · exp(-27000 · r_s(M)) + 2.01

Diese Korrektur modifiziert r_φ, den natürlichen φ-Radius.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Tuple
from .ssz_mirror_metric import schwarzschild_radius, PHI, G_DEFAULT, C_DEFAULT


# Empirische Parameter (aus Theorie-Fit an Daten)
DELTA_A = 98.01   # Amplitude (Prozent)
DELTA_B = 2.01    # Offset (Prozent)
DELTA_LAMBDA = 27000.0  # Charakteristische Skala (1/m)


def delta_M(mass: float, G: float = G_DEFAULT, c: float = C_DEFAULT) -> float:
    """Masse-abhängige Korrektur Δ(M) in Prozent.
    
    Formel: Δ(M) = A · exp(-λ · r_s(M)) + B
    
    Args:
        mass: Masse in kg
        G, c: Physikalische Konstanten
    
    Returns:
        Δ(M) in Prozent (0 bis 100)
    
    Physikalische Bedeutung:
    - Kleine Massen (r_s → 0): Δ → 100% (maximale Segment-Korrektur)
    - Große Massen (r_s → ∞): Δ → 2% (minimale Korrektur, GR-Näherung)
    """
    rs = schwarzschild_radius(mass, G, c)
    return DELTA_A * np.exp(-DELTA_LAMBDA * rs) + DELTA_B


def r_phi(mass: float, varphi: float = PHI, 
          G: float = G_DEFAULT, c: float = C_DEFAULT) -> float:
    """Natürlicher φ-Radius mit Masse-Korrektur.
    
    r_φ = φ · (GM/c²) · (1 + Δ(M)/100)
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter (default: Golden Ratio)
        G, c: Physikalische Konstanten
    
    Returns:
        r_φ in Metern
    
    Vergleich mit r_s:
    - r_φ/r_s = φ/2 · (1 + Δ/100) ≈ 0.809 · (1 + Δ/100)
    - Für Δ=2%: r_φ ≈ 0.825 r_s (SSZ-Horizont INNERHALB GR-Horizont)
    """
    Delta = delta_M(mass, G, c)
    r_phi_base = varphi * (G * mass) / (c * c)
    return r_phi_base * (1.0 + Delta / 100.0)


def r_phi_vs_r_s_ratio(mass: float, varphi: float = PHI) -> float:
    """Verhältnis r_φ/r_s.
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
    
    Returns:
        r_φ/r_s (dimensionslos)
    """
    rs = schwarzschild_radius(mass)
    rphi = r_phi(mass, varphi)
    return rphi / rs


def segment_density_max(mass: float, varphi: float = PHI, N_0: float = 1.0) -> float:
    """Maximale Segment-Dichte bei r = r_φ.
    
    N_max = N_0 · Ξ(r_φ) = N_0 · (1 - exp(-φ · r_φ/r_s))
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
        N_0: Normalisierungsfaktor
    
    Returns:
        N_max (Segmente pro Volumen)
    """
    from .ssz_mirror_metric import Xi
    
    rs = schwarzschild_radius(mass)
    rphi = r_phi(mass, varphi)
    
    Xi_max = Xi(rphi, rs, varphi)
    return N_0 * Xi_max


def demo():
    """Demo: Δ(M) für verschiedene Massen."""
    import matplotlib.pyplot as plt
    
    # Massen von Planeten bis Schwarze Löcher
    masses = {
        'Erde': 5.972e24,
        'Jupiter': 1.898e27,
        'Sonne': 1.98847e30,
        '10 M☉': 10 * 1.98847e30,
        'Sgr A*': 4.3e6 * 1.98847e30,
        'M87*': 6.5e9 * 1.98847e30,
    }
    
    # Berechne für jede Masse
    results = {}
    for name, M in masses.items():
        rs = schwarzschild_radius(M)
        Delta = delta_M(M)
        rphi = r_phi(M)
        ratio = r_phi_vs_r_s_ratio(M)
        N_max = segment_density_max(M)
        
        results[name] = {
            'mass': M,
            'r_s_km': rs / 1000,
            'Delta_%': Delta,
            'r_phi_km': rphi / 1000,
            'r_phi/r_s': ratio,
            'N_max': N_max
        }
    
    # Tabelle
    print("\n" + "="*90)
    print("MASSE-ABHÄNGIGE KORREKTUREN Δ(M)")
    print("="*90)
    print(f"{'Objekt':<12} {'M/M☉':>10} {'r_s (km)':>12} {'Δ(%)':>8} {'r_φ (km)':>12} {'r_φ/r_s':>10} {'N_max':>10}")
    print("-"*90)
    
    M_sun = 1.98847e30
    for name, data in results.items():
        print(f"{name:<12} {data['mass']/M_sun:>10.2e} {data['r_s_km']:>12.3e} "
              f"{data['Delta_%']:>8.3f} {data['r_phi_km']:>12.3e} "
              f"{data['r_phi/r_s']:>10.6f} {data['N_max']:>10.6f}")
    
    print("="*90)
    
    # Plot: Δ(M) vs. r_s
    r_s_arr = np.logspace(-5, 15, 500)  # von μm bis 10^9 km
    Delta_arr = DELTA_A * np.exp(-DELTA_LAMBDA * r_s_arr) + DELTA_B
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Top: Δ(M) vs. r_s
    ax1.semilogx(r_s_arr / 1000, Delta_arr, lw=2.5, color='#2ca02c')
    for name, data in results.items():
        ax1.plot(data['r_s_km'], data['Delta_%'], 'o', markersize=8, label=name)
    ax1.axhline(100, ls='--', color='gray', alpha=0.5, label='Max (100%)')
    ax1.axhline(2.01, ls='--', color='red', alpha=0.5, label='Min (2.01%)')
    ax1.set_xlabel('r_s (km)')
    ax1.set_ylabel('Δ(M) [%]')
    ax1.set_title('Masse-abhängige Korrektur')
    ax1.legend(fontsize=8, ncol=2)
    ax1.grid(alpha=0.3)
    
    # Bottom: r_φ/r_s vs. r_s
    ratio_arr = (PHI / 2) * (1 + Delta_arr / 100)
    ax2.semilogx(r_s_arr / 1000, ratio_arr, lw=2.5, color='#ff7f0e')
    for name, data in results.items():
        ax2.plot(data['r_s_km'], data['r_phi/r_s'], 'o', markersize=8, label=name)
    ax2.axhline(PHI/2, ls='--', color='gray', alpha=0.5, label='φ/2 (ohne Δ)')
    ax2.set_xlabel('r_s (km)')
    ax2.set_ylabel('r_φ/r_s')
    ax2.set_title('SSZ-Horizont relativ zu GR-Horizont')
    ax2.legend(fontsize=8, ncol=2)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/mass_corrections.png', dpi=150)
    print("\n✅ Saved: viz_ssz_metric/out/mass_corrections.png")


if __name__ == "__main__":
    demo()
