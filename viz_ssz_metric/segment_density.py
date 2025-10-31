# -*- coding: utf-8 -*-
"""
PHASE 9: Segment-Dichte Ξ(r) - Exakte Integration und Ableitungen

Präzise Berechnung der Segment-Dichte-Funktion, ihrer Ableitungen
und der totalen Segment-Anzahl durch räumliche Integration.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from scipy.integrate import quad
from typing import Callable
from .ssz_mirror_metric import Xi, schwarzschild_radius, PHI


def dXi_dr(r, rs, varphi: float = PHI) -> float:
    """Erste Ableitung der Segment-Dichte.
    
    Ξ(r) = 1 - exp(-φr/r_s)
    dΞ/dr = (φ/r_s) · exp(-φr/r_s)
    
    Args:
        r: Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
    
    Returns:
        dΞ/dr
    """
    r = np.asarray(r, float)
    return (varphi / rs) * np.exp(-varphi * r / rs)


def d2Xi_dr2(r, rs, varphi: float = PHI) -> float:
    """Zweite Ableitung der Segment-Dichte.
    
    d²Ξ/dr² = -(φ²/r_s²) · exp(-φr/r_s)
    
    Args:
        r: Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
    
    Returns:
        d²Ξ/dr²
    """
    r = np.asarray(r, float)
    return -(varphi**2 / rs**2) * np.exp(-varphi * r / rs)


def segment_number_density(r, rs, varphi: float = PHI, N_0: float = 1.0):
    """Absolute Segment-Anzahldichte N(r) = N_0 · Ξ(r).
    
    Args:
        r: Radius
        rs: Schwarzschild-Radius  
        varphi: φ-Parameter
        N_0: Normalisierungsfaktor (Segmente/m³)
    
    Returns:
        N(r) in Segmenten pro Volumen
    """
    return N_0 * Xi(r, rs, varphi)


def total_segments_spherical(r_max: float, rs, varphi: float = PHI, N_0: float = 1.0):
    """Totale Segment-Anzahl innerhalb Kugel mit Radius r_max.
    
    N_total = ∫₀^r_max 4πr² N(r) dr
            = 4π N_0 ∫₀^r_max r² Ξ(r) dr
    
    Args:
        r_max: Maximaler Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
        N_0: Normalisierungsfaktor
    
    Returns:
        Totale Segment-Anzahl (dimensionslos wenn N_0=1)
    """
    def integrand(r):
        return 4 * np.pi * r**2 * Xi(r, rs, varphi)
    
    result, error = quad(integrand, 0, r_max, limit=100)
    return N_0 * result


def total_segments_analytical(r_max: float, rs, varphi: float = PHI, N_0: float = 1.0):
    """Analytische Lösung der Segment-Integration (falls möglich).
    
    ∫ r² (1 - exp(-φr/r_s)) dr = r³/3 + (r_s/φ)³ exp(-φr/r_s) [r²(φ/r_s)² + 2r(φ/r_s) + 2]
    
    (Komplex, verwende numerisch für Genauigkeit)
    """
    # Für große r_max/rs approximiere als r³/3
    u = r_max / rs
    if u > 10:
        # Asymptotic: ∫ r² dr ≈ r³/3 (Ξ → 1)
        return N_0 * 4 * np.pi * (r_max**3) / 3
    else:
        # Verwende numerische Integration (präziser)
        return total_segments_spherical(r_max, rs, varphi, N_0)


def segment_mass_equivalent(r_max: float, rs, varphi: float = PHI, 
                           m_segment: float = 1.0):
    """Äquivalente Masse aller Segmente innerhalb r_max.
    
    M_seg = N_total · m_segment
    
    Args:
        r_max: Maximaler Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
        m_segment: Masse pro Segment (kg)
    
    Returns:
        M_seg in kg
    """
    N_total = total_segments_spherical(r_max, rs, varphi, N_0=1.0)
    return N_total * m_segment


def effective_density_profile(r, rs, varphi: float = PHI, rho_0: float = 1.0):
    """Effektive Massensdichte-Profil aus Segmenten.
    
    ρ_eff(r) = ρ_0 · Ξ(r) / r²
    
    (Annahme: Segmente tragen zur effektiven Dichte bei)
    
    Args:
        r: Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
        rho_0: Zentrale Dichte
    
    Returns:
        ρ_eff(r)
    """
    r = np.asarray(r, float)
    Xi_val = Xi(r, rs, varphi)
    return rho_0 * Xi_val / np.maximum(r**2, 1e-20)


def demo():
    """Demo: Segment-Dichte Analyse für Sonnenmasse."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r = np.linspace(0.5*rs, 10*rs, 500)
    
    # Berechne Funktionen
    Xi_vals = Xi(r, rs, PHI)
    dXi_vals = dXi_dr(r, rs, PHI)
    d2Xi_vals = d2Xi_dr2(r, rs, PHI)
    N_vals = segment_number_density(r, rs, PHI, N_0=1e40)  # 10^40 Segmente/m³
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Top-left: Ξ(r)
    axes[0,0].plot(r/rs, Xi_vals, lw=2.5, color='#1f77b4')
    axes[0,0].axhline(1.0, ls='--', color='gray', alpha=0.5)
    axes[0,0].set_xlabel('r/r_s')
    axes[0,0].set_ylabel('Ξ(r)')
    axes[0,0].set_title('Segment-Dichte')
    axes[0,0].grid(alpha=0.3)
    axes[0,0].set_ylim([0, 1.05])
    
    # Top-right: dΞ/dr
    axes[0,1].plot(r/rs, dXi_vals * rs, lw=2.5, color='#ff7f0e')
    axes[0,1].set_xlabel('r/r_s')
    axes[0,1].set_ylabel('r_s · dΞ/dr')
    axes[0,1].set_title('Erste Ableitung (normalisiert)')
    axes[0,1].grid(alpha=0.3)
    
    # Bottom-left: d²Ξ/dr²
    axes[1,0].plot(r/rs, d2Xi_vals * (rs**2), lw=2.5, color='#2ca02c')
    axes[1,0].set_xlabel('r/r_s')
    axes[1,0].set_ylabel('r_s² · d²Ξ/dr²')
    axes[1,0].set_title('Zweite Ableitung (normalisiert)')
    axes[1,0].grid(alpha=0.3)
    
    # Bottom-right: N(r)
    axes[1,1].semilogy(r/rs, N_vals, lw=2.5, color='#d62728')
    axes[1,1].set_xlabel('r/r_s')
    axes[1,1].set_ylabel('N(r) [Segmente/m³]')
    axes[1,1].set_title('Absolute Segment-Anzahldichte (N_0=10⁴⁰)')
    axes[1,1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/segment_density.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/segment_density.png")
    
    # Totale Segmente
    radii = [1, 2, 5, 10, 20]
    print("\n" + "="*70)
    print("TOTALE SEGMENT-ANZAHL (N_0 = 1)")
    print("="*70)
    print(f"{'r_max/r_s':>10} {'N_total (numerisch)':>25} {'N_total (analytisch)':>25}")
    print("-"*70)
    
    for r_mult in radii:
        r_max = r_mult * rs
        N_num = total_segments_spherical(r_max, rs, PHI, N_0=1.0)
        N_ana = total_segments_analytical(r_max, rs, PHI, N_0=1.0)
        print(f"{r_mult:>10} {N_num:>25.6e} {N_ana:>25.6e}")
    
    print("="*70)
    
    # Vergleich mit Kerndichte
    print("\nVergleich: Segment-Dichte vs. Nukleare Dichte")
    rho_nuclear = 2.3e17  # kg/m³ (Neutronenstern-Kern)
    m_segment_estimate = 1e-27  # kg (etwa Protonmasse)
    
    N_0_required = rho_nuclear / m_segment_estimate
    print(f"  ρ_nuclear = {rho_nuclear:.2e} kg/m³")
    print(f"  m_segment ≈ {m_segment_estimate:.2e} kg")
    print(f"  → N_0 ≈ {N_0_required:.2e} Segmente/m³")


if __name__ == "__main__":
    demo()
