# -*- coding: utf-8 -*-
"""
PHASE 11: Christoffel-Symbole Γ^μ_νρ

Berechnet die Christoffel-Symbole der zweiten Art für die SSZ-Metrik:

Γ^μ_νρ = (1/2) g^μσ (∂g_σρ/∂x^ν + ∂g_σν/∂x^ρ - ∂g_νρ/∂x^σ)

Für sphärische Symmetrie (statisch, diagonal) sind die meisten Null!

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
import math
from typing import Tuple
from .ssz_mirror_metric import (
    metric_functions_pn, schwarzschild_radius, G_DEFAULT, C_DEFAULT
)


def dA_dr_numerical(mass: float, r: float, dr: float = 1e-3) -> float:
    """Numerische Ableitung von A(r).
    
    dA/dr ≈ (A(r+dr) - A(r-dr)) / (2·dr)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        dr: Finite-difference Schritt
    
    Returns:
        dA/dr
    """
    A_plus, _ = metric_functions_pn(mass, r + dr)
    A_minus, _ = metric_functions_pn(mass, r - dr)
    return (A_plus - A_minus) / (2 * dr)


def dB_dr_numerical(mass: float, r: float, dr: float = 1e-3) -> float:
    """Numerische Ableitung von B(r) = 1/A(r).
    
    dB/dr = -dA/dr / A²
    
    Args:
        mass: Masse in kg
        r: Radius in m
        dr: Finite-difference Schritt
    
    Returns:
        dB/dr
    """
    A, _ = metric_functions_pn(mass, r)
    dA = dA_dr_numerical(mass, r, dr)
    return -dA / (A**2)


def christoffel_nonzero(mass: float, r: float, theta: float) -> dict:
    """Berechne nicht-triviale Christoffel-Symbole für SSZ-Metrik.
    
    Für statische, sphärisch-symmetrische Metrik g_μν = diag(-A, B, r², r²sin²θ)
    sind nur folgende Komponenten nicht-Null:
    
    Zeitartige (t):
    - Γ^t_tr = dA/dr / (2A) = A'/2A
    - Γ^r_tt = A'/2B
    
    Radiale (r):
    - Γ^r_rr = dB/dr / (2B) = B'/2B
    - Γ^r_θθ = -r/B
    - Γ^r_φφ = -r sin²θ / B
    
    Polare (θ):
    - Γ^θ_rθ = 1/r
    - Γ^θ_φφ = -sinθ cosθ
    
    Azimuthale (φ):
    - Γ^φ_rφ = 1/r
    - Γ^φ_θφ = cotθ = cosθ/sinθ
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel in Radiant
    
    Returns:
        dict mit Christoffel-Symbolen
    """
    A, B = metric_functions_pn(mass, r)
    dA = dA_dr_numerical(mass, r)
    dB = dB_dr_numerical(mass, r)
    
    # Zeitartige
    Gamma_t_tr = dA / (2 * A)
    Gamma_r_tt = dA / (2 * B)
    
    # Radiale
    Gamma_r_rr = dB / (2 * B)
    Gamma_r_thth = -r / B
    Gamma_r_phph = -r * (math.sin(theta)**2) / B
    
    # Polare
    Gamma_th_rth = 1.0 / r
    Gamma_th_phph = -math.sin(theta) * math.cos(theta)
    
    # Azimuthale
    Gamma_ph_rph = 1.0 / r
    cot_theta = math.cos(theta) / math.sin(theta) if math.sin(theta) > 1e-10 else 0
    Gamma_ph_thph = cot_theta
    
    return {
        # Zeitartige (t-Komponenten)
        'Gamma^t_tr': Gamma_t_tr,
        'Gamma^t_rt': Gamma_t_tr,  # Symmetrie
        'Gamma^r_tt': Gamma_r_tt,
        
        # Radiale (r-Komponenten)
        'Gamma^r_rr': Gamma_r_rr,
        'Gamma^r_thth': Gamma_r_thth,
        'Gamma^r_phph': Gamma_r_phph,
        
        # Polare (θ-Komponenten)
        'Gamma^th_rth': Gamma_th_rth,
        'Gamma^th_thr': Gamma_th_rth,  # Symmetrie
        'Gamma^th_phph': Gamma_th_phph,
        
        # Azimuthale (φ-Komponenten)
        'Gamma^ph_rph': Gamma_ph_rph,
        'Gamma^ph_phr': Gamma_ph_rph,  # Symmetrie
        'Gamma^ph_thph': Gamma_ph_thph,
        'Gamma^ph_phth': Gamma_ph_thph,  # Symmetrie
    }


def geodesic_acceleration(mass: float, r: float, theta: float, 
                         v_r: float, v_theta: float, v_phi: float) -> Tuple[float, float, float]:
    """Berechne Beschleunigung entlang Geodäte.
    
    Geodätengleichung: d²x^μ/dλ² = -Γ^μ_νρ (dx^ν/dλ)(dx^ρ/dλ)
    
    Args:
        mass: Masse in kg
        r, theta: Position (m, rad)
        v_r, v_theta, v_phi: Geschwindigkeiten (m/s, rad/s, rad/s)
    
    Returns:
        Tuple (a_r, a_theta, a_phi) Beschleunigungen
    """
    gamma = christoffel_nonzero(mass, r, theta)
    
    # Radiale Beschleunigung
    a_r = -(
        gamma['Gamma^r_rr'] * v_r * v_r +
        gamma['Gamma^r_thth'] * v_theta * v_theta +
        gamma['Gamma^r_phph'] * v_phi * v_phi
    )
    
    # Polare Beschleunigung
    a_theta = -(
        2 * gamma['Gamma^th_rth'] * v_r * v_theta +
        gamma['Gamma^th_phph'] * v_phi * v_phi
    )
    
    # Azimuthale Beschleunigung
    a_phi = -(
        2 * gamma['Gamma^ph_rph'] * v_r * v_phi +
        2 * gamma['Gamma^ph_thph'] * v_theta * v_phi
    )
    
    return a_r, a_theta, a_phi


def demo():
    """Demo: Christoffel-Symbole für Sonnenmasse."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r_arr = np.linspace(2*rs, 10*rs, 100)
    theta_test = math.pi / 4  # 45°
    
    # Berechne wichtige Christoffel-Symbole
    Gamma_t_tr_arr = []
    Gamma_r_tt_arr = []
    Gamma_r_thth_arr = []
    
    for r in r_arr:
        gamma = christoffel_nonzero(M_sun, r, theta_test)
        Gamma_t_tr_arr.append(gamma['Gamma^t_tr'])
        Gamma_r_tt_arr.append(gamma['Gamma^r_tt'])
        Gamma_r_thth_arr.append(gamma['Gamma^r_thth'])
    
    Gamma_t_tr_arr = np.array(Gamma_t_tr_arr)
    Gamma_r_tt_arr = np.array(Gamma_r_tt_arr)
    Gamma_r_thth_arr = np.array(Gamma_r_thth_arr)
    
    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    
    # Top: Γ^t_tr
    axes[0].plot(r_arr/rs, Gamma_t_tr_arr * rs, lw=2.5, color='#1f77b4')
    axes[0].set_ylabel('r_s · Γ^t_tr')
    axes[0].set_title('Christoffel-Symbole für SSZ-Metrik (1 M☉)')
    axes[0].grid(alpha=0.3)
    axes[0].axhline(0, ls='--', color='gray', alpha=0.5)
    
    # Middle: Γ^r_tt
    axes[1].plot(r_arr/rs, Gamma_r_tt_arr / rs, lw=2.5, color='#ff7f0e')
    axes[1].set_ylabel('Γ^r_tt / r_s')
    axes[1].grid(alpha=0.3)
    axes[1].axhline(0, ls='--', color='gray', alpha=0.5)
    
    # Bottom: Γ^r_θθ
    axes[2].plot(r_arr/rs, Gamma_r_thth_arr / rs, lw=2.5, color='#2ca02c')
    axes[2].set_xlabel('r/r_s')
    axes[2].set_ylabel('Γ^r_θθ / r_s')
    axes[2].grid(alpha=0.3)
    axes[2].axhline(0, ls='--', color='gray', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/christoffel_symbols.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/christoffel_symbols.png")
    
    # Tabelle
    print("\n" + "="*80)
    print("CHRISTOFFEL-SYMBOLE bei r=2r_s, θ=π/4")
    print("="*80)
    
    gamma = christoffel_nonzero(M_sun, 2*rs, math.pi/4)
    
    for key, value in sorted(gamma.items()):
        # Normalisiere
        if 'r_tt' in key or 'r_thth' in key or 'r_phph' in key:
            value_norm = value / rs
            unit = '1/r_s'
        elif 't_tr' in key:
            value_norm = value * rs
            unit = 'r_s'
        else:
            value_norm = value
            unit = ''
        
        print(f"  {key:<20}: {value_norm:>12.6e} {unit}")
    
    print("="*80)


if __name__ == "__main__":
    demo()
