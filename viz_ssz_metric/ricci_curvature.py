# -*- coding: utf-8 -*-
"""
PHASE 13 & 14: Ricci-Tensor R_μν und Ricci-Skalar R

Ricci-Tensor: R_μν = R^λ_μλν (Kontraktion des Riemann-Tensors)
Ricci-Skalar: R = g^μν R_μν (Spur des Ricci-Tensors)

Diese sind zentral für die Einstein-Feldgleichungen!

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
import math
from typing import Tuple
from .ssz_mirror_metric import metric_functions_pn, schwarzschild_radius
from .christoffel_symbols import dA_dr_numerical, dB_dr_numerical


def ricci_tensor_diagonal(mass: float, r: float, theta: float) -> Tuple[float, float, float, float]:
    """Berechne diagonale Komponenten des Ricci-Tensors.
    
    Für sphärische Symmetrie ist R_μν diagonal:
    R_μν = diag(R_tt, R_rr, R_θθ, R_φφ)
    
    Formeln (aus Christoffel-Symbolen):
    R_tt = -A'' / (2B) + A' / (4B) (A'/A + B'/B) + A' / (rB)
    R_rr = -A'' / (2A) + A' / (4A) (A'/A + B'/B) - B' / (rB)
    R_θθ = 1 - (1/B) + r/(2B) (A'/A - B'/B)
    R_φφ = sin²θ · R_θθ
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        Tuple (R_tt, R_rr, R_θθ, R_φφ)
    """
    A, B = metric_functions_pn(mass, r)
    
    # Erste Ableitungen
    dr = 1e-3
    A_prime = dA_dr_numerical(mass, r, dr)
    B_prime = dB_dr_numerical(mass, r, dr)
    
    # Zweite Ableitungen (numerisch)
    A_prime_plus = dA_dr_numerical(mass, r + dr, dr)
    A_prime_minus = dA_dr_numerical(mass, r - dr, dr)
    A_double_prime = (A_prime_plus - A_prime_minus) / (2 * dr)
    
    # R_tt
    R_tt = (-A_double_prime / (2*B) + 
            (A_prime / (4*B)) * (A_prime/A + B_prime/B) + 
            A_prime / (r*B))
    
    # R_rr
    R_rr = (-A_double_prime / (2*A) + 
            (A_prime / (4*A)) * (A_prime/A + B_prime/B) - 
            B_prime / (r*B))
    
    # R_θθ
    R_thth = 1.0 - (1.0/B) + (r / (2*B)) * (A_prime/A - B_prime/B)
    
    # R_φφ = sin²θ · R_θθ
    R_phph = (math.sin(theta)**2) * R_thth
    
    return R_tt, R_rr, R_thth, R_phph


def ricci_scalar(mass: float, r: float, theta: float) -> float:
    """Berechne Ricci-Skalar R = g^μν R_μν.
    
    R = g^tt R_tt + g^rr R_rr + g^θθ R_θθ + g^φφ R_φφ
      = -R_tt/A + R_rr/B + R_θθ/r² + R_φφ/(r²sin²θ)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        R (Ricci-Skalar)
    """
    A, B = metric_functions_pn(mass, r)
    R_tt, R_rr, R_thth, R_phph = ricci_tensor_diagonal(mass, r, theta)
    
    # Inverse Metrik
    g_inv_tt = -1.0 / A
    g_inv_rr = 1.0 / B
    g_inv_thth = 1.0 / (r**2)
    g_inv_phph = 1.0 / (r**2 * math.sin(theta)**2)
    
    # Kontraktion
    R = (g_inv_tt * R_tt + 
         g_inv_rr * R_rr + 
         g_inv_thth * R_thth + 
         g_inv_phph * R_phph)
    
    return R


def vacuum_deviation(mass: float, r: float, theta: float) -> float:
    """Abweichung von Vakuum-Lösung (R_μν - (1/2)g_μν R).
    
    In Vakuum (GR): R_μν = 0 → R = 0
    In SSZ: R_μν ≠ 0 wegen Segment-Dichte
    
    Misst "effektive Materie" der Segmente.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        ||R_μν - (1/2)g_μν R||² (Frobenius-Norm²)
    """
    R = ricci_scalar(mass, r, theta)
    R_tt, R_rr, R_thth, R_phph = ricci_tensor_diagonal(mass, r, theta)
    A, B = metric_functions_pn(mass, r)
    
    # Einstein-Tensor Komponenten G_μν = R_μν - (1/2)g_μν R
    G_tt = R_tt - (1.0/2.0) * (-A) * R
    G_rr = R_rr - (1.0/2.0) * B * R
    G_thth = R_thth - (1.0/2.0) * (r**2) * R
    G_phph = R_phph - (1.0/2.0) * (r**2 * math.sin(theta)**2) * R
    
    # Norm² (summiere |G_μμ|²)
    norm_sq = (abs(G_tt)**2 + abs(G_rr)**2 + 
               abs(G_thth)**2 + abs(G_phph)**2)
    
    return norm_sq


def demo():
    """Demo: Ricci-Tensor und Ricci-Skalar."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r_arr = np.linspace(2*rs, 20*rs, 100)
    theta_test = math.pi / 2  # Äquator
    
    # Berechne Ricci-Größen
    R_scalar_arr = []
    R_tt_arr = []
    R_rr_arr = []
    vacuum_dev_arr = []
    
    for r in r_arr:
        R_scalar_arr.append(ricci_scalar(M_sun, r, theta_test))
        R_tt, R_rr, _, _ = ricci_tensor_diagonal(M_sun, r, theta_test)
        R_tt_arr.append(R_tt)
        R_rr_arr.append(R_rr)
        vacuum_dev_arr.append(vacuum_deviation(M_sun, r, theta_test))
    
    R_scalar_arr = np.array(R_scalar_arr)
    R_tt_arr = np.array(R_tt_arr)
    R_rr_arr = np.array(R_rr_arr)
    vacuum_dev_arr = np.array(vacuum_dev_arr)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Top-left: Ricci-Skalar
    axes[0,0].plot(r_arr/rs, R_scalar_arr * (rs**2), lw=2.5, color='#1f77b4')
    axes[0,0].set_ylabel('r_s² · R')
    axes[0,0].set_title('Ricci-Skalar (SSZ-Metrik)')
    axes[0,0].grid(alpha=0.3)
    axes[0,0].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[0,0].set_xlabel('r/r_s')
    
    # Top-right: R_tt
    axes[0,1].plot(r_arr/rs, R_tt_arr * (rs**2), lw=2.5, color='#ff7f0e')
    axes[0,1].set_ylabel('r_s² · R_tt')
    axes[0,1].set_title('Ricci-Tensor R_tt')
    axes[0,1].grid(alpha=0.3)
    axes[0,1].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[0,1].set_xlabel('r/r_s')
    
    # Bottom-left: R_rr
    axes[1,0].plot(r_arr/rs, R_rr_arr * (rs**2), lw=2.5, color='#2ca02c')
    axes[1,0].set_ylabel('r_s² · R_rr')
    axes[1,0].set_title('Ricci-Tensor R_rr')
    axes[1,0].grid(alpha=0.3)
    axes[1,0].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[1,0].set_xlabel('r/r_s')
    
    # Bottom-right: Vacuum Deviation
    axes[1,1].semilogy(r_arr/rs, vacuum_dev_arr * (rs**4), lw=2.5, color='#d62728')
    axes[1,1].set_ylabel('r_s⁴ · ||G_μν||²')
    axes[1,1].set_title('Vakuum-Abweichung (Segment-Effekt)')
    axes[1,1].grid(alpha=0.3)
    axes[1,1].set_xlabel('r/r_s')
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/ricci_curvature.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/ricci_curvature.png")
    
    # Tabelle
    print("\n" + "="*80)
    print("RICCI-KRÜMMUNG bei verschiedenen Radien (θ=π/2)")
    print("="*80)
    print(f"{'r/r_s':>8} {'R [r_s⁻²]':>15} {'R_tt [r_s⁻²]':>15} {'R_rr [r_s⁻²]':>15} {'||G||² [r_s⁻⁴]':>18}")
    print("-"*80)
    
    for r_mult in [2, 3, 5, 10, 20]:
        r = r_mult * rs
        R_val = ricci_scalar(M_sun, r, math.pi/2)
        R_tt, R_rr, _, _ = ricci_tensor_diagonal(M_sun, r, math.pi/2)
        vac_dev = vacuum_deviation(M_sun, r, math.pi/2)
        
        print(f"{r_mult:>8} {R_val*(rs**2):>15.6e} {R_tt*(rs**2):>15.6e} "
              f"{R_rr*(rs**2):>15.6e} {vac_dev*(rs**4):>18.6e}")
    
    print("="*80)
    
    # Interpretation
    print("\nPhysikalische Interpretation:")
    print("  • In GR-Vakuum: R = 0 (Schwarzschild)")
    print("  • In SSZ: R ≠ 0 wegen Segment-Dichte Ξ(r)")
    print("  • ||G||² misst 'effektive Materie' der Segmente")
    print("  • ||G||² → 0 für r → ∞ (GR-Limit)")


if __name__ == "__main__":
    demo()
