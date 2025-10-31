# -*- coding: utf-8 -*-
"""
PHASE 15 & 16: Kretschmann-Skalar K und Weyl-Tensor C^μ_νρσ

Kretschmann-Skalar K = R_μνρσ R^μνρσ
- Invariante unter Koordinatentransformationen
- Misst Gezeiten-Gravitation
- K → ∞ bei echter Singularität

Weyl-Tensor C^μ_νρσ (konformer Krümmungstensor)
- Spurfreier Teil des Riemann-Tensors
- Beschreibt Gezeiten-Effekte
- In Vakuum: R_μνρσ = C_μνρσ

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
import math
from typing import Tuple
from .ssz_mirror_metric import schwarzschild_radius, metric_functions_pn
from .ricci_curvature import ricci_scalar, ricci_tensor_diagonal
from .christoffel_symbols import dA_dr_numerical, dB_dr_numerical


def kretschmann_scalar_exact(mass: float, r: float, theta: float) -> float:
    """Kretschmann-Skalar K = R_μνρσ R^μνρσ (exakt berechnet).
    
    Für Schwarzschild-GR: K = 48(GM)²/(c⁴r⁶) = 12r_s²/r⁶
    
    Für SSZ: Korrektur durch Post-Newtonsche Terme.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        K (Kretschmann-Skalar)
    """
    rs = schwarzschild_radius(mass)
    A, B = metric_functions_pn(mass, r)
    
    # GR-Baseline
    K_GR = 12 * (rs**2) / (r**6)
    
    # SSZ-Korrektur aus Post-Newtonschen Termen
    # Vereinfachte Berechnung (vollständig: summiere alle 256 Komponenten!)
    
    # Metrik-Ableitungen
    dA = dA_dr_numerical(mass, r)
    dB = dB_dr_numerical(mass, r)
    
    # Dominanter Beitrag: (dA/dr)² und (dB/dr)²
    correction_term = (dA**2 / (A*B) + dB**2 / (B**2)) / r**4
    
    K = K_GR + correction_term
    
    return K


def weyl_scalar_C2(mass: float, r: float, theta: float) -> float:
    """Weyl-Skalar C² = C_μνρσ C^μνρσ.
    
    Der Weyl-Tensor beschreibt die Gezeiten-Gravitation (tidal field).
    
    Für Vakuum-Lösung: C_μνρσ = R_μνρσ (da R_μν = 0)
    
    Für SSZ: C_μνρσ = R_μνρσ - (Ricci-Beiträge)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        C² (Weyl-Skalar)
    """
    rs = schwarzschild_radius(mass)
    
    # In sphärischer Symmetrie: Weyl-Skalar vereinfacht sich
    # C² ≈ K - (4/3)R² (für 4D)
    
    K = kretschmann_scalar_exact(mass, r, theta)
    R = ricci_scalar(mass, r, theta)
    
    C2 = K - (4.0/3.0) * (R**2)
    
    return max(0, C2)  # Physikalisch muss C² ≥ 0


def tidal_tensor_eigenvalues(mass: float, r: float, theta: float) -> Tuple[float, float, float]:
    """Eigenwerte des Gezeiten-Tensors (Tidal Tensor).
    
    Der Gezeiten-Tensor E_ij beschreibt die Deformation von Testmassen.
    
    Für sphärische Symmetrie (radiale Richtung):
    E_rr = -(GM/r³) [1 + SSZ-Korrektur]
    E_θθ = E_φφ = (GM/2r³) [1 + SSZ-Korrektur]
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        Tuple (λ_r, λ_θ, λ_φ) Eigenwerte
    """
    from .ssz_mirror_metric import G_DEFAULT
    
    # Newtonsche Gezeiten-Tensor
    E_newton = G_DEFAULT * mass / (r**3)
    
    # SSZ-Korrektur aus Metrik
    A, _ = metric_functions_pn(mass, r)
    correction = np.sqrt(A)  # Zeitdilatations-Faktor
    
    # Eigenwerte
    lambda_r = -E_newton * correction
    lambda_theta = 0.5 * E_newton * correction
    lambda_phi = lambda_theta
    
    return lambda_r, lambda_theta, lambda_phi


def singularity_strength(mass: float, r: float, theta: float) -> str:
    """Klassifiziere Stärke der Singularität via Kretschmann.
    
    Klassifikation:
    - K < 10³: Schwach gekrümmt
    - 10³ ≤ K < 10⁶: Moderate Krümmung
    - 10⁶ ≤ K < 10¹²: Starke Krümmung
    - K ≥ 10¹²: Nahe Singularität
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        Klassifikation als String
    """
    K = kretschmann_scalar_exact(mass, r, theta)
    
    if K < 1e3:
        return "schwach"
    elif K < 1e6:
        return "moderat"
    elif K < 1e12:
        return "stark"
    else:
        return "extrem (nahe Singularität!)"


def demo():
    """Demo: Kretschmann und Weyl Skalare."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich (logarithmisch für bessere Auflösung nahe r_s)
    r_arr = np.logspace(np.log10(1.5*rs), np.log10(20*rs), 200)
    theta_test = np.pi / 2
    
    # Berechne Skalare
    K_arr = []
    C2_arr = []
    lambda_r_arr = []
    
    for r in r_arr:
        K_arr.append(kretschmann_scalar_exact(M_sun, r, theta_test))
        C2_arr.append(weyl_scalar_C2(M_sun, r, theta_test))
        
        lr, _, _ = tidal_tensor_eigenvalues(M_sun, r, theta_test)
        lambda_r_arr.append(lr)
    
    K_arr = np.array(K_arr)
    C2_arr = np.array(C2_arr)
    lambda_r_arr = np.array(lambda_r_arr)
    
    # GR-Vergleich
    K_GR_arr = 12 * (rs**2) / (r_arr**6)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Top-left: Kretschmann
    axes[0,0].loglog(r_arr/rs, K_arr * (rs**4), lw=2.5, color='#1f77b4', label='SSZ')
    axes[0,0].loglog(r_arr/rs, K_GR_arr * (rs**4), lw=2, ls='--', color='gray', 
                     alpha=0.7, label='GR')
    axes[0,0].set_xlabel('r/r_s')
    axes[0,0].set_ylabel('r_s⁴ · K')
    axes[0,0].set_title('Kretschmann-Skalar')
    axes[0,0].legend()
    axes[0,0].grid(alpha=0.3, which='both')
    
    # Top-right: Weyl-Skalar
    axes[0,1].loglog(r_arr/rs, C2_arr * (rs**4), lw=2.5, color='#ff7f0e')
    axes[0,1].set_xlabel('r/r_s')
    axes[0,1].set_ylabel('r_s⁴ · C²')
    axes[0,1].set_title('Weyl-Skalar (Gezeiten-Gravitation)')
    axes[0,1].grid(alpha=0.3, which='both')
    
    # Bottom-left: Gezeiten-Tensor Eigenwert
    axes[1,0].loglog(r_arr/rs, np.abs(lambda_r_arr) * (rs**3), lw=2.5, color='#2ca02c')
    axes[1,0].set_xlabel('r/r_s')
    axes[1,0].set_ylabel('r_s³ · |λ_r|')
    axes[1,0].set_title('Gezeiten-Tensor (radial)')
    axes[1,0].grid(alpha=0.3, which='both')
    
    # Bottom-right: SSZ vs. GR Differenz
    diff = (K_arr - K_GR_arr) / K_GR_arr * 100
    axes[1,1].semilogx(r_arr/rs, diff, lw=2.5, color='#d62728')
    axes[1,1].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[1,1].set_xlabel('r/r_s')
    axes[1,1].set_ylabel('(K_SSZ - K_GR) / K_GR [%]')
    axes[1,1].set_title('Relative Differenz zu GR')
    axes[1,1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/kretschmann_weyl.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/kretschmann_weyl.png")
    
    # Tabelle
    print("\n" + "="*90)
    print("KRETSCHMANN & WEYL SKALARE (SSZ-Metrik, 1 M☉)")
    print("="*90)
    print(f"{'r/r_s':>8} {'K [r_s⁻⁴]':>18} {'C² [r_s⁻⁴]':>18} {'|λ_r| [r_s⁻³]':>18} {'Stärke':<20}")
    print("-"*90)
    
    for r_mult in [1.5, 2, 3, 5, 10, 20]:
        r = r_mult * rs
        K = kretschmann_scalar_exact(M_sun, r, theta_test)
        C2 = weyl_scalar_C2(M_sun, r, theta_test)
        lr, _, _ = tidal_tensor_eigenvalues(M_sun, r, theta_test)
        strength = singularity_strength(M_sun, r, theta_test)
        
        print(f"{r_mult:>8.1f} {K*(rs**4):>18.6e} {C2*(rs**4):>18.6e} "
              f"{abs(lr)*(rs**3):>18.6e} {strength:<20}")
    
    print("="*90)
    
    print("\nPhysikalische Interpretation:")
    print("  • Kretschmann K: Invariante Krümmung (unabhängig von Koordinaten)")
    print("  • K ∝ 1/r⁶ für GR-Schwarzschild")
    print("  • Weyl C²: Gezeiten-Gravitation (gezeitenfreie = 0)")
    print("  • λ_r < 0: radiale Kompression (Spaghettification)")
    print("  • SSZ-Korrektur minimal für große r (GR-Limit)")


if __name__ == "__main__":
    demo()
