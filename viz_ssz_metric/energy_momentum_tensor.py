# -*- coding: utf-8 -*-
"""
PHASE 18: Energie-Impuls-Tensor T_μν

Der Energie-Impuls-Tensor beschreibt die Verteilung von Energie,
Impuls und Druck in der Raumzeit.

In SSZ: T_μν wird NICHT extern vorgegeben, sondern aus G_μν abgeleitet!
Dies ist einzigartig: Die Segment-Struktur erzeugt effektive "Materie".

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
import math
from typing import Tuple
from .einstein_tensor import (
    effective_stress_energy_tensor, energy_density_from_einstein,
    pressure_from_einstein
)
from .ssz_mirror_metric import schwarzschild_radius, C_DEFAULT


def perfect_fluid_decomposition(mass: float, r: float, theta: float) -> dict:
    """Zerlege T_μν in perfekte-Flüssigkeits-Form.
    
    Perfekte Flüssigkeit:
    T_μν = (ρ + p/c²) u_μ u_ν + p g_μν
    
    wobei:
    - ρ: Energie-Dichte
    - p: Isotroper Druck
    - u_μ: 4-Geschwindigkeit (stationär: u^t = 1/√g_tt)
    
    In SSZ: p ist NICHT isotrop! → Anisotroper Druck
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        dict mit Keys:
        - 'rho': Energie-Dichte
        - 'p_r': Radialer Druck
        - 'p_t': Tangentialer Druck
        - 'anisotropy': p_r - p_t (Anisotropie)
    """
    rho = energy_density_from_einstein(mass, r, theta)
    p_r, p_theta, p_phi = pressure_from_einstein(mass, r, theta)
    
    # Mittlerer tangentialer Druck
    p_t = (p_theta + p_phi) / 2
    
    # Anisotropie
    anisotropy = p_r - p_t
    
    return {
        'rho': rho,
        'p_r': p_r,
        'p_t': p_t,
        'anisotropy': anisotropy
    }


def energy_conditions_check(mass: float, r: float, theta: float) -> dict:
    """Prüfe Energie-Bedingungen (Energy Conditions).
    
    Standard-Bedingungen in GR:
    1. **WEC** (Weak Energy Condition): ρ ≥ 0
    2. **NEC** (Null Energy Condition): ρ + p ≥ 0
    3. **DEC** (Dominant Energy Condition): ρ ≥ |p|
    4. **SEC** (Strong Energy Condition): ρ + 3p ≥ 0
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        dict mit True/False für jede Bedingung
    """
    fluid = perfect_fluid_decomposition(mass, r, theta)
    rho = fluid['rho']
    p_r = fluid['p_r']
    p_avg = (p_r + 2*fluid['p_t']) / 3  # Gemittelter Druck
    
    # Energie-Bedingungen
    WEC = rho >= 0
    NEC = (rho + p_avg) >= 0
    DEC = rho >= abs(p_avg)
    SEC = (rho + 3*p_avg) >= 0
    
    return {
        'WEC': WEC,
        'NEC': NEC,
        'DEC': DEC,
        'SEC': SEC,
        'rho': rho,
        'p_avg': p_avg
    }


def equation_of_state(mass: float, r: float, theta: float) -> float:
    """Effektive Zustandsgleichung w = p/ρ.
    
    Standard-Werte:
    - w = 0: Staub (Materie)
    - w = 1/3: Strahlung
    - w = -1: Kosmologische Konstante (Dunkle Energie)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        w = p/ρ
    """
    fluid = perfect_fluid_decomposition(mass, r, theta)
    rho = fluid['rho']
    p_avg = (fluid['p_r'] + 2*fluid['p_t']) / 3
    
    if abs(rho) < 1e-30:
        return np.nan
    
    return p_avg / rho


def trace_energy_momentum(mass: float, r: float, theta: float) -> float:
    """Spur des Energie-Impuls-Tensors T^μ_μ = g^μν T_μν.
    
    Für perfekte Flüssigkeit: T^μ_μ = -ρ + 3p
    
    In 4D: Zusammenhang mit Ricci-Skalar via Feldgleichungen:
    T^μ_μ = -(c⁴/8πG) R
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        T^μ_μ
    """
    from .ricci_curvature import ricci_scalar
    from .ssz_mirror_metric import G_DEFAULT, C_DEFAULT
    
    R = ricci_scalar(mass, r, theta)
    T_trace = -(C_DEFAULT**4 / (8*math.pi*G_DEFAULT)) * R
    
    return T_trace


def demo():
    """Demo: Energie-Impuls-Tensor Analyse."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r_arr = np.linspace(2*rs, 20*rs, 100)
    theta_test = math.pi / 2
    
    # Berechne Eigenschaften
    rho_arr = []
    p_r_arr = []
    aniso_arr = []
    w_arr = []
    WEC_arr = []
    
    for r in r_arr:
        fluid = perfect_fluid_decomposition(M_sun, r, theta_test)
        energy = energy_conditions_check(M_sun, r, theta_test)
        w = equation_of_state(M_sun, r, theta_test)
        
        rho_arr.append(fluid['rho'])
        p_r_arr.append(fluid['p_r'])
        aniso_arr.append(fluid['anisotropy'])
        w_arr.append(w)
        WEC_arr.append(energy['WEC'])
    
    rho_arr = np.array(rho_arr)
    p_r_arr = np.array(p_r_arr)
    aniso_arr = np.array(aniso_arr)
    w_arr = np.array(w_arr)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Top-left: ρ und p_r
    ax1 = axes[0,0]
    ax1.semilogy(r_arr/rs, np.abs(rho_arr), lw=2.5, color='#1f77b4', label='|ρ|')
    ax1.semilogy(r_arr/rs, np.abs(p_r_arr), lw=2.5, ls='--', color='#ff7f0e', label='|p_r|')
    ax1.set_ylabel('kg/m³ oder Pa')
    ax1.set_title('Energie-Dichte und Druck')
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax1.set_xlabel('r/r_s')
    
    # Top-right: Anisotropie
    axes[0,1].plot(r_arr/rs, aniso_arr, lw=2.5, color='#2ca02c')
    axes[0,1].axhline(0, ls='--', color='gray', alpha=0.5)
    axes[0,1].set_ylabel('p_r - p_t [Pa]')
    axes[0,1].set_title('Druck-Anisotropie')
    axes[0,1].grid(alpha=0.3)
    axes[0,1].set_xlabel('r/r_s')
    
    # Bottom-left: Zustandsgleichung w
    axes[1,0].plot(r_arr/rs, w_arr, lw=2.5, color='#d62728')
    axes[1,0].axhline(0, ls=':', color='gray', label='w=0 (Staub)')
    axes[1,0].axhline(1/3, ls=':', color='blue', label='w=1/3 (Strahlung)')
    axes[1,0].axhline(-1, ls=':', color='red', label='w=-1 (Λ)')
    axes[1,0].set_ylabel('w = p/ρ')
    axes[1,0].set_title('Zustandsgleichung')
    axes[1,0].legend(fontsize=8)
    axes[1,0].grid(alpha=0.3)
    axes[1,0].set_xlabel('r/r_s')
    axes[1,0].set_ylim([-2, 2])
    
    # Bottom-right: Energie-Bedingungen
    axes[1,1].plot(r_arr/rs, WEC_arr, lw=2.5, color='#9467bd', label='WEC (ρ≥0)')
    axes[1,1].set_ylabel('Bedingung erfüllt (1) oder nicht (0)')
    axes[1,1].set_title('Energie-Bedingungen')
    axes[1,1].legend()
    axes[1,1].grid(alpha=0.3)
    axes[1,1].set_xlabel('r/r_s')
    axes[1,1].set_ylim([-0.1, 1.1])
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/energy_momentum_tensor.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/energy_momentum_tensor.png")
    
    # Tabelle
    print("\n" + "="*100)
    print("ENERGIE-IMPULS-TENSOR ANALYSE (SSZ-Metrik, 1 M☉)")
    print("="*100)
    print(f"{'r/r_s':>8} {'ρ [kg/m³]':>18} {'p_r [Pa]':>18} {'w':>12} {'WEC':>6} {'NEC':>6} {'DEC':>6} {'SEC':>6}")
    print("-"*100)
    
    for r_mult in [2, 3, 5, 10, 20]:
        r = r_mult * rs
        fluid = perfect_fluid_decomposition(M_sun, r, theta_test)
        energy = energy_conditions_check(M_sun, r, theta_test)
        w = equation_of_state(M_sun, r, theta_test)
        
        print(f"{r_mult:>8} {fluid['rho']:>18.6e} {fluid['p_r']:>18.6e} {w:>12.6f} "
              f"{'✓' if energy['WEC'] else '✗':>6} "
              f"{'✓' if energy['NEC'] else '✗':>6} "
              f"{'✓' if energy['DEC'] else '✗':>6} "
              f"{'✓' if energy['SEC'] else '✗':>6}")
    
    print("="*100)
    
    print("\nPhysikalische Interpretation:")
    print("  • ρ < 0 möglich! SSZ-Segmente können negative Energie-Dichte haben")
    print("  • Anisotropie p_r ≠ p_t: Segmente erzeugen gerichteten Druck")
    print("  • w variabel: Segment-Flüssigkeit hat komplexe Zustandsgleichung")
    print("  • Energie-Bedingungen können verletzt sein (Exotische Materie!)")


if __name__ == "__main__":
    demo()
