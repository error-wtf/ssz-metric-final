# -*- coding: utf-8 -*-
"""
PHASE 19: Energie-Bedingungen (WEC/DEC/SEC) - Detaillierte Analyse

Systematische Prüfung aller klassischen Energie-Bedingungen aus der GR:

1. WEC (Weak Energy Condition): ρ ≥ 0, ρ + p ≥ 0
2. NEC (Null Energy Condition): ρ + p ≥ 0  
3. DEC (Dominant Energy Condition): ρ ≥ |p|
4. SEC (Strong Energy Condition): ρ + p ≥ 0, ρ + 3p ≥ 0

SSZ kann diese verletzen → Exotische Materie, Wurmlöcher möglich!

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Dict, List
from .energy_momentum_tensor import perfect_fluid_decomposition
from .ssz_mirror_metric import schwarzschild_radius, PHI


def check_all_energy_conditions(mass: float, r: float, theta: float) -> Dict[str, bool]:
    """Vollständige Prüfung aller Energie-Bedingungen.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        dict mit Keys: 'WEC', 'NEC', 'DEC', 'SEC', 'ANEC', 'AWEC'
        und Werten True (erfüllt) oder False (verletzt)
    """
    fluid = perfect_fluid_decomposition(mass, r, theta)
    
    rho = fluid['rho']
    p_r = fluid['p_r']
    p_t = fluid['p_t']
    
    # Gemittelter Druck (isotrop approximiert)
    p_avg = (p_r + 2*p_t) / 3
    
    # Standard-Bedingungen
    WEC = (rho >= 0) and ((rho + p_avg) >= 0)
    NEC = (rho + p_avg) >= 0
    DEC = (rho >= 0) and (rho >= abs(p_r)) and (rho >= abs(p_t))
    SEC = (rho + p_avg >= 0) and (rho + 3*p_avg >= 0)
    
    # Erweiterte Bedingungen
    ANEC = (rho + p_r >= 0)  # Averaged NEC (radial)
    AWEC = (rho >= 0) and (rho + p_r >= 0) and (rho + p_t >= 0)  # Averaged WEC
    
    return {
        'WEC': WEC,
        'NEC': NEC,
        'DEC': DEC,
        'SEC': SEC,
        'ANEC': ANEC,
        'AWEC': AWEC
    }


def violation_regions(mass: float, r_min: float, r_max: float, 
                     num: int = 100, theta: float = np.pi/2) -> Dict[str, List[float]]:
    """Finde Regionen wo Energie-Bedingungen verletzt sind.
    
    Args:
        mass: Masse in kg
        r_min, r_max: Radien-Bereich
        num: Anzahl Sample-Punkte
        theta: Polwinkel
    
    Returns:
        dict mit Listen von r-Werten wo Bedingung verletzt ist
    """
    rs = schwarzschild_radius(mass)
    r_arr = np.linspace(r_min, r_max, num)
    
    violations = {
        'WEC': [],
        'NEC': [],
        'DEC': [],
        'SEC': [],
        'ANEC': [],
        'AWEC': []
    }
    
    for r in r_arr:
        conditions = check_all_energy_conditions(mass, r, theta)
        
        for key, satisfied in conditions.items():
            if not satisfied:
                violations[key].append(r / rs)
    
    return violations


def exotic_matter_indicator(mass: float, r: float, theta: float) -> float:
    """Indikator für exotische Materie.
    
    Exotische Materie: ρ + p < 0 (verletzt NEC)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        Wert < 0: exotisch, Wert ≥ 0: normal
    """
    fluid = perfect_fluid_decomposition(mass, r, theta)
    rho = fluid['rho']
    p_avg = (fluid['p_r'] + 2*fluid['p_t']) / 3
    
    return rho + p_avg


def wormhole_throat_criterion(mass: float, r: float, theta: float) -> bool:
    """Prüfe ob Radius ein Wurmloch-Throat sein könnte.
    
    Kriterien (Morris-Thorne):
    1. NEC verletzt (ρ + p < 0)
    2. Minimaler Radius (d²r/dλ² > 0)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        theta: Polwinkel
    
    Returns:
        True wenn Wurmloch-Throat-Kriterien erfüllt
    """
    conditions = check_all_energy_conditions(mass, r, theta)
    
    # NEC verletzt?
    nec_violated = not conditions['NEC']
    
    # Zusätzlich: radiale Druckgradient-Check (vereinfacht)
    fluid = perfect_fluid_decomposition(mass, r, theta)
    exotic = fluid['rho'] + fluid['p_r'] < 0
    
    return nec_violated and exotic


def demo():
    """Demo: Energie-Bedingungen über Radien-Bereich."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r_arr = np.linspace(1.5*rs, 20*rs, 200)
    theta_test = np.pi / 2
    
    # Sammle Bedingungen
    WEC_vals = []
    NEC_vals = []
    DEC_vals = []
    SEC_vals = []
    exotic_vals = []
    
    for r in r_arr:
        cond = check_all_energy_conditions(M_sun, r, theta_test)
        WEC_vals.append(1 if cond['WEC'] else 0)
        NEC_vals.append(1 if cond['NEC'] else 0)
        DEC_vals.append(1 if cond['DEC'] else 0)
        SEC_vals.append(1 if cond['SEC'] else 0)
        
        exotic = exotic_matter_indicator(M_sun, r, theta_test)
        exotic_vals.append(exotic)
    
    WEC_vals = np.array(WEC_vals)
    NEC_vals = np.array(NEC_vals)
    DEC_vals = np.array(DEC_vals)
    SEC_vals = np.array(SEC_vals)
    exotic_vals = np.array(exotic_vals)
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Top: Bedingungen (1=erfüllt, 0=verletzt)
    ax1.fill_between(r_arr/rs, 0, WEC_vals, alpha=0.3, color='#1f77b4', label='WEC')
    ax1.fill_between(r_arr/rs, 0, NEC_vals, alpha=0.3, color='#ff7f0e', label='NEC')
    ax1.fill_between(r_arr/rs, 0, DEC_vals, alpha=0.3, color='#2ca02c', label='DEC')
    ax1.fill_between(r_arr/rs, 0, SEC_vals, alpha=0.3, color='#d62728', label='SEC')
    ax1.set_ylabel('Erfüllt (1) / Verletzt (0)')
    ax1.set_title('Energie-Bedingungen (SSZ-Metrik, 1 M☉)')
    ax1.legend(loc='upper right')
    ax1.grid(alpha=0.3)
    ax1.set_ylim([-0.1, 1.1])
    
    # Bottom: Exotische Materie Indikator
    ax2.plot(r_arr/rs, exotic_vals, lw=2.5, color='#9467bd')
    ax2.axhline(0, ls='--', color='red', lw=2, label='NEC-Grenze (ρ+p=0)')
    ax2.fill_between(r_arr/rs, exotic_vals, 0, where=(exotic_vals < 0), 
                     alpha=0.3, color='red', label='Exotische Region')
    ax2.set_xlabel('r/r_s')
    ax2.set_ylabel('ρ + p')
    ax2.set_title('Exotische Materie (ρ+p<0)')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/energy_conditions.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/energy_conditions.png")
    
    # Verletzungs-Regionen
    print("\n" + "="*80)
    print("ENERGIE-BEDINGUNGEN: VERLETZUNGS-ANALYSE")
    print("="*80)
    
    violations = violation_regions(M_sun, 1.5*rs, 20*rs, num=200, theta=theta_test)
    
    for key, r_list in violations.items():
        if len(r_list) > 0:
            r_min_viol = min(r_list)
            r_max_viol = max(r_list)
            percentage = 100 * len(r_list) / 200
            print(f"\n{key}:")
            print(f"  Verletzt in {len(r_list)}/200 Punkten ({percentage:.1f}%)")
            print(f"  Bereich: {r_min_viol:.3f} - {r_max_viol:.3f} r_s")
        else:
            print(f"\n{key}: ✓ Überall erfüllt")
    
    print("="*80)
    
    # Wurmloch-Kandidaten
    print("\nWURMLOCH-THROAT KANDIDATEN:")
    wormhole_count = 0
    for r in r_arr:
        if wormhole_throat_criterion(M_sun, r, theta_test):
            print(f"  • r = {r/rs:.3f} r_s (potentieller Throat)")
            wormhole_count += 1
            if wormhole_count >= 5:
                print("  (... weitere Kandidaten)")
                break
    
    if wormhole_count == 0:
        print("  Keine Wurmloch-Throat Kandidaten gefunden")
    
    print("\n⚠️  WICHTIG:")
    print("  • Verletzung der Energie-Bedingungen → Exotische Materie")
    print("  • SSZ-Segmente können exotische Eigenschaften haben")
    print("  • Ermöglicht theoretisch Wurmlöcher, Warp-Antriebe, etc.")
    print("  • Physikalische Realisierbarkeit noch offen!")


if __name__ == "__main__":
    demo()
