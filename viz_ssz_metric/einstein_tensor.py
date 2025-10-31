# -*- coding: utf-8 -*-
"""
PHASE 17: Einstein-Tensor G_μν

Der Einstein-Tensor ist das Herzstück der Einstein'schen Feldgleichungen:

G_μν = R_μν - (1/2) g_μν R = (8πG/c⁴) T_μν

Linke Seite (Geometrie) = Rechte Seite (Materie/Energie)

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
import math
from typing import Tuple
from .ricci_curvature import ricci_tensor_diagonal, ricci_scalar
from .ssz_mirror_metric import metric_functions_pn, schwarzschild_radius, G_DEFAULT, C_DEFAULT


def einstein_tensor_diagonal(mass: float, r: float, theta: float) -> Tuple[float, float, float, float]:
    """Berechne Einstein-Tensor G_μν = R_μν - (1/2) g_μν R.
    
    Dies ist die linke Seite der Einstein-Feldgleichungen.
    
    Für sphärische Symmetrie ist G_μν diagonal:
    G_μν = diag(G_tt, G_rr, G_θθ, G_φφ)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        Tuple (G_tt, G_rr, G_θθ, G_φφ)
    """
    # Metrik
    A, B = metric_functions_pn(mass, r)
    
    # Ricci-Größen
    R_tt, R_rr, R_thth, R_phph = ricci_tensor_diagonal(mass, r, theta)
    R = ricci_scalar(mass, r, theta)
    
    # Einstein-Tensor G_μν = R_μν - (1/2) g_μν R
    G_tt = R_tt - (1.0/2.0) * (-A) * R     # g_tt = -A
    G_rr = R_rr - (1.0/2.0) * B * R        # g_rr = B
    G_thth = R_thth - (1.0/2.0) * (r**2) * R  # g_θθ = r²
    G_phph = R_phph - (1.0/2.0) * (r**2 * math.sin(theta)**2) * R  # g_φφ = r²sin²θ
    
    return G_tt, G_rr, G_thth, G_phph


def einstein_tensor_trace(mass: float, r: float, theta: float) -> float:
    """Spur des Einstein-Tensors G^μ_μ = g^μν G_μν.
    
    In 4D: G^μ_μ = -R (aus Kontraktion)
    
    Wichtig: In Vakuum (T_μν=0) ist G_μν=0, also auch G^μ_μ=0.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        G^μ_μ (Spur)
    """
    R = ricci_scalar(mass, r, theta)
    return -R


def effective_stress_energy_tensor(mass: float, r: float, theta: float) -> Tuple[float, float, float, float]:
    """Effektiver Energie-Impuls-Tensor T_μν aus Einstein-Gleichungen.
    
    T_μν = (c⁴/8πG) G_μν
    
    Dies ist die "Materie"-Seite, die durch Segmente induziert wird!
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        Tuple (T_tt, T_rr, T_θθ, T_φφ)
    """
    G_tt, G_rr, G_thth, G_phph = einstein_tensor_diagonal(mass, r, theta)
    
    # Kopplungskonstante c⁴/(8πG)
    coupling = (C_DEFAULT**4) / (8 * math.pi * G_DEFAULT)
    
    T_tt = coupling * G_tt
    T_rr = coupling * G_rr
    T_thth = coupling * G_thth
    T_phph = coupling * G_phph
    
    return T_tt, T_rr, T_thth, T_phph


def energy_density_from_einstein(mass: float, r: float, theta: float) -> float:
    """Energie-Dichte ρ aus Einstein-Tensor.
    
    ρ = (c⁴/8πG) G_tt / c² = (c²/8πG) G_tt
    
    (In Einheiten kg/m³)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        ρ (Energie-Dichte in kg/m³)
    """
    G_tt, _, _, _ = einstein_tensor_diagonal(mass, r, theta)
    
    # ρ = (c²/8πG) G_tt
    rho = ((C_DEFAULT**2) / (8 * math.pi * G_DEFAULT)) * G_tt
    
    return rho


def pressure_from_einstein(mass: float, r: float, theta: float) -> Tuple[float, float, float]:
    """Druck-Komponenten aus Einstein-Tensor.
    
    p_r = (c⁴/8πG) G_rr  (radialer Druck)
    p_t = (c⁴/8πG) G_θθ  (tangentialer Druck)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        Tuple (p_r, p_theta, p_phi) in Pascal
    """
    _, G_rr, G_thth, G_phph = einstein_tensor_diagonal(mass, r, theta)
    
    coupling = (C_DEFAULT**4) / (8 * math.pi * G_DEFAULT)
    
    p_r = coupling * G_rr
    p_theta = coupling * G_thth / (r**2)  # Normalisiert
    p_phi = coupling * G_phph / (r**2 * math.sin(theta)**2)  # Normalisiert
    
    return p_r, p_theta, p_phi


def demo():
    """Demo: Einstein-Tensor und abgeleitete Größen."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r_arr = np.linspace(2*rs, 20*rs, 100)
    theta_test = math.pi / 2
    
    # Berechne Einstein-Tensor
    G_tt_arr = []
    G_rr_arr = []
    rho_arr = []
    p_r_arr = []
    
    for r in r_arr:
        G_tt, G_rr, _, _ = einstein_tensor_diagonal(M_sun, r, theta_test)
        G_tt_arr.append(G_tt)
        G_rr_arr.append(G_rr)
        
        rho = energy_density_from_einstein(M_sun, r, theta_test)
        p_r, _, _ = pressure_from_einstein(M_sun, r, theta_test)
        rho_arr.append(rho)
        p_r_arr.append(p_r)
    
    G_tt_arr = np.array(G_tt_arr)
    G_rr_arr = np.array(G_rr_arr)
    rho_arr = np.array(rho_arr)
    p_r_arr = np.array(p_r_arr)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Top-left: G_tt
    axes[0,0].plot(r_arr/rs, G_tt_arr * (rs**2), lw=2.5, color='#1f77b4')
    axes[0,0].set_ylabel('r_s² · G_tt')
    axes[0,0].set_title('Einstein-Tensor G_tt')
    axes[0,0].grid(alpha=0.3)
    axes[0,0].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[0,0].set_xlabel('r/r_s')
    
    # Top-right: G_rr
    axes[0,1].plot(r_arr/rs, G_rr_arr * (rs**2), lw=2.5, color='#ff7f0e')
    axes[0,1].set_ylabel('r_s² · G_rr')
    axes[0,1].set_title('Einstein-Tensor G_rr')
    axes[0,1].grid(alpha=0.3)
    axes[0,1].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[0,1].set_xlabel('r/r_s')
    
    # Bottom-left: Energie-Dichte
    axes[1,0].semilogy(r_arr/rs, np.abs(rho_arr), lw=2.5, color='#2ca02c')
    axes[1,0].set_ylabel('ρ [kg/m³]')
    axes[1,0].set_title('Effektive Energie-Dichte (aus G_tt)')
    axes[1,0].grid(alpha=0.3)
    axes[1,0].set_xlabel('r/r_s')
    
    # Bottom-right: Radialer Druck
    axes[1,1].plot(r_arr/rs, p_r_arr, lw=2.5, color='#d62728')
    axes[1,1].set_ylabel('p_r [Pa]')
    axes[1,1].set_title('Radialer Druck (aus G_rr)')
    axes[1,1].grid(alpha=0.3)
    axes[1,1].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[1,1].set_xlabel('r/r_s')
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/einstein_tensor.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/einstein_tensor.png")
    
    # Tabelle
    print("\n" + "="*90)
    print("EINSTEIN-TENSOR UND ENERGIE-IMPULS-TENSOR (SSZ-Metrik, 1 M☉)")
    print("="*90)
    print(f"{'r/r_s':>8} {'G_tt':>15} {'G_rr':>15} {'ρ [kg/m³]':>18} {'p_r [Pa]':>18}")
    print("-"*90)
    
    for r_mult in [2, 3, 5, 10, 20]:
        r = r_mult * rs
        G_tt, G_rr, _, _ = einstein_tensor_diagonal(M_sun, r, theta_test)
        rho = energy_density_from_einstein(M_sun, r, theta_test)
        p_r, _, _ = pressure_from_einstein(M_sun, r, theta_test)
        
        print(f"{r_mult:>8} {G_tt*(rs**2):>15.6e} {G_rr*(rs**2):>15.6e} "
              f"{rho:>18.6e} {p_r:>18.6e}")
    
    print("="*90)
    
    # Vergleich mit Kerndichte
    print("\nVergleich mit bekannten Dichten:")
    rho_nuclear = 2.3e17  # kg/m³ (Neutronenstern-Kern)
    rho_ssz_2rs = abs(energy_density_from_einstein(M_sun, 2*rs, theta_test))
    print(f"  ρ_SSZ(2r_s)  = {rho_ssz_2rs:.3e} kg/m³")
    print(f"  ρ_nuclear    = {rho_nuclear:.3e} kg/m³")
    print(f"  Verhältnis   = {rho_ssz_2rs/rho_nuclear:.3e}")
    
    print("\n⚠️  WICHTIG: Dies ist die EFFEKTIVE Dichte der Segment-Struktur,")
    print("   nicht materielle Dichte! Segmente sind geometrische Objekte.")


if __name__ == "__main__":
    demo()
