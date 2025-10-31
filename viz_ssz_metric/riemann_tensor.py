# -*- coding: utf-8 -*-
"""
PHASE 12: Riemann-Krümmungstensor R^μ_νρσ

Berechnet den Riemann-Tensor aus Christoffel-Symbolen:

R^μ_νρσ = ∂_ρ Γ^μ_νσ - ∂_σ Γ^μ_νρ + Γ^μ_λρ Γ^λ_νσ - Γ^μ_λσ Γ^λ_νρ

Für sphärische Symmetrie gibt es Vereinfachungen!

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
import math
from typing import Tuple
from .christoffel_symbols import christoffel_nonzero, dA_dr_numerical, dB_dr_numerical
from .ssz_mirror_metric import metric_functions_pn, schwarzschild_radius


def d_Gamma_dr(mass: float, r: float, theta: float, 
               symbol_name: str, dr: float = 1e-3) -> float:
    """Numerische Ableitung eines Christoffel-Symbols nach r.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
        symbol_name: Name des Symbols (z.B. 'Gamma^t_tr')
        dr: Finite-difference Schritt
    
    Returns:
        ∂Γ/∂r
    """
    gamma_plus = christoffel_nonzero(mass, r + dr, theta)
    gamma_minus = christoffel_nonzero(mass, r - dr, theta)
    
    return (gamma_plus[symbol_name] - gamma_minus[symbol_name]) / (2 * dr)


def riemann_nonzero_components(mass: float, r: float, theta: float) -> dict:
    """Berechne nicht-triviale Komponenten des Riemann-Tensors.
    
    Für statische, sphärisch-symmetrische Metrik sind wichtigste:
    
    - R^r_trt (zeitartig-radial)
    - R^θ_rθr (radial-polar)
    - R^φ_rφr (radial-azimuthal)
    - R^φ_θφθ (polar-azimuthal)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        dict mit nicht-trivialen Riemann-Komponenten
    """
    A, B = metric_functions_pn(mass, r)
    dA = dA_dr_numerical(mass, r)
    dB = dB_dr_numerical(mass, r)
    
    # Zweite Ableitungen (numerisch)
    dr_step = 1e-3
    d2A = (dA_dr_numerical(mass, r + dr_step) - dA_dr_numerical(mass, r - dr_step)) / (2 * dr_step)
    
    gamma = christoffel_nonzero(mass, r, theta)
    
    # R^r_trt (wichtigste Komponente - Zeitdilatationsgrad)
    # R^r_trt = ∂_r Γ^r_tt - ∂_t Γ^r_tr + Γ^r_λr Γ^λ_tt - Γ^r_λt Γ^λ_tr
    # Da statisch: ∂_t = 0
    # Vereinfacht: R^r_trt ≈ ∂_r(A'/2B) + (A'/2A)²
    
    d_Gamma_r_tt = d_Gamma_dr(mass, r, theta, 'Gamma^r_tt', dr_step)
    
    R_r_trt = d_Gamma_r_tt + (gamma['Gamma^t_tr'])**2
    
    # R^θ_rθr (radial-polar Krümmung)
    # R^θ_rθr ≈ -d/dr(1/r) = 1/r²
    R_th_rthr = 1.0 / (r**2)
    
    # R^φ_rφr (radial-azimuthal)
    # Ähnlich wie R^θ_rθr
    R_ph_rphr = 1.0 / (r**2)
    
    # R^φ_θφθ (polar-azimuthal)
    # R^φ_θφθ ≈ sin²θ / r²
    R_ph_thphth = (math.sin(theta)**2) / (r**2)
    
    return {
        'R^r_trt': R_r_trt,
        'R^th_rthr': R_th_rthr,
        'R^ph_rphr': R_ph_rphr,
        'R^ph_thphth': R_ph_thphth,
    }


def ricci_scalar_approximation(mass: float, r: float) -> float:
    """Ricci-Skalar R = g^μν R_μν (Approximation).
    
    Für schwaches Feld:
    R ≈ ∇²A / A (Laplace von A)
    
    Exakte Berechnung erfordert alle Riemann-Komponenten (Phase 14).
    
    Args:
        mass: Masse in kg
        r: Radius in m
    
    Returns:
        R (Ricci-Skalar, approximativ)
    """
    A, _ = metric_functions_pn(mass, r)
    
    # Zweite radiale Ableitung
    dr = 1e-3
    d2A = (dA_dr_numerical(mass, r + dr) - dA_dr_numerical(mass, r - dr)) / (2 * dr)
    
    # Approximation: R ≈ -d²A/dr² / A
    return -d2A / A


def kretschmann_scalar(mass: float, r: float, theta: float) -> float:
    """Kretschmann-Skalar K = R_μνρσ R^μνρσ.
    
    Invariante Krümmungsgröße (unabhängig von Koordinaten).
    
    Für Schwarzschild: K = 48(GM)²/(c⁴r⁶) = 12r_s²/r⁶
    
    SSZ-Korrektur wird hier approximiert.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        K (Kretschmann-Skalar)
    """
    rs = schwarzschild_radius(mass)
    
    # GR-Wert (Baseline)
    K_GR = 12 * (rs**2) / (r**6)
    
    # SSZ-Korrektur (aus Riemann-Komponenten)
    riemann = riemann_nonzero_components(mass, r, theta)
    
    # Approximative Beiträge (vollständig: summiere alle R_μνρσ R^μνρσ)
    K_correction = abs(riemann['R^r_trt'])**2 + abs(riemann['R^th_rthr'])**2
    
    return K_GR + K_correction


def tidal_force_tensor(mass: float, r: float, theta: float, 
                       separation: float = 1.0) -> Tuple[float, float, float]:
    """Gezeitenkraft-Tensor (Tidal Force) aus Riemann-Tensor.
    
    F_tidal^i = -R^i_t0t · separation
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
        separation: Trennung der Testmassen (m)
    
    Returns:
        Tuple (F_r, F_theta, F_phi) Gezeitenkräfte
    """
    riemann = riemann_nonzero_components(mass, r, theta)
    
    # Radiale Gezeitenkraft
    F_r = -riemann['R^r_trt'] * separation
    
    # Tangentiale Gezeitenkräfte (kleiner)
    F_theta = -riemann['R^th_rthr'] * separation / 10
    F_phi = -riemann['R^ph_rphr'] * separation / 10
    
    return F_r, F_theta, F_phi


def demo():
    """Demo: Riemann-Tensor für Sonnenmasse."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r_arr = np.linspace(2*rs, 20*rs, 100)
    theta_test = math.pi / 2  # Äquator
    
    # Berechne Riemann-Komponenten
    R_r_trt_arr = []
    K_arr = []
    
    for r in r_arr:
        riemann = riemann_nonzero_components(M_sun, r, theta_test)
        R_r_trt_arr.append(riemann['R^r_trt'])
        K_arr.append(kretschmann_scalar(M_sun, r, theta_test))
    
    R_r_trt_arr = np.array(R_r_trt_arr)
    K_arr = np.array(K_arr)
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Top: R^r_trt
    ax1.plot(r_arr/rs, R_r_trt_arr * (rs**2), lw=2.5, color='#1f77b4')
    ax1.set_ylabel('r_s² · R^r_trt')
    ax1.set_title('Riemann-Tensor Komponenten (SSZ-Metrik, 1 M☉)')
    ax1.grid(alpha=0.3)
    ax1.axhline(0, ls='--', color='gray', alpha=0.5)
    
    # Bottom: Kretschmann-Skalar
    ax2.semilogy(r_arr/rs, K_arr * (rs**4), lw=2.5, color='#d62728')
    ax2.set_xlabel('r/r_s')
    ax2.set_ylabel('r_s⁴ · K')
    ax2.set_title('Kretschmann-Skalar (Krümmungsinvariante)')
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/riemann_tensor.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/riemann_tensor.png")
    
    # Tabelle
    print("\n" + "="*80)
    print("RIEMANN-TENSOR bei r=2r_s, θ=π/2")
    print("="*80)
    
    riemann = riemann_nonzero_components(M_sun, 2*rs, math.pi/2)
    for key, value in sorted(riemann.items()):
        value_norm = value * (rs**2)
        print(f"  {key:<20}: {value_norm:>15.6e} · r_s⁻²")
    
    print(f"\n  Kretschmann K       : {kretschmann_scalar(M_sun, 2*rs, math.pi/2):.6e}")
    print(f"  Ricci R (approx)    : {ricci_scalar_approximation(M_sun, 2*rs):.6e}")
    
    # Gezeitenkräfte
    sep = 1.0  # 1 m Trennung
    F_r, F_th, F_ph = tidal_force_tensor(M_sun, 2*rs, math.pi/2, sep)
    print(f"\n  Gezeitenkraft (1m sep):")
    print(f"    F_r     : {F_r:.6e} m/s²")
    print(f"    F_theta : {F_th:.6e} m/s²")
    print(f"    F_phi   : {F_ph:.6e} m/s²")
    
    print("="*80)


if __name__ == "__main__":
    demo()
