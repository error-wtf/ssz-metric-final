# -*- coding: utf-8 -*-
"""
PHASE 6: φ-Abhängigkeit in der Metrik

Analysiert wie der Golden-Ratio-Parameter φ die metrischen Funktionen
beeinflusst und bestimmt optimale φ-Werte für verschiedene Massen.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Callable, Tuple
from .ssz_mirror_metric import (
    schwarzschild_radius, D_SSZ, A_SSZ, solve_r_star, PHI, G_DEFAULT, C_DEFAULT
)


def epsilon_3_phi(varphi: float) -> float:
    """Koeffizient ε₃ als Funktion von φ.
    
    Aus SSZ-Theorie: ε₃(φ) = -24/5 · (φ/φ₀)^α
    mit φ₀ = (1+√5)/2 und α ≈ 0.618 (reciprocal φ)
    
    Args:
        varphi: φ-Parameter
    
    Returns:
        ε₃(φ)
    """
    phi_0 = PHI
    alpha = 1.0 / PHI  # ≈ 0.618034
    base = -24.0 / 5.0
    
    return base * (varphi / phi_0) ** alpha


def A_SSZ_phi_dependent(r, rs, varphi: float) -> float:
    """A_SSZ mit φ-abhängigem Korrekturfaktor.
    
    A_SSZ = D²_SSZ · f(φ)
    
    wobei f(φ) = 1 + (φ-φ₀)/φ₀² · correction
    
    Args:
        r: Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
    
    Returns:
        A_SSZ(r, φ)
    """
    from .ssz_mirror_metric import A_SSZ as A_SSZ_base
    
    # Basis-Wert
    A_base = A_SSZ_base(r, rs, varphi)
    
    # φ-Korrektur
    delta_phi = varphi - PHI
    correction = 1.0 + (delta_phi / (PHI**2)) * 0.1  # 10% max Korrektur
    
    return A_base * correction


def sensitivity_dA_dphi(r, rs, varphi: float, dphi: float = 1e-6) -> float:
    """Sensitivität ∂A/∂φ via finite difference.
    
    Args:
        r: Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
        dphi: Finite difference step
    
    Returns:
        dA/dφ
    """
    A_plus = A_SSZ_phi_dependent(r, rs, varphi + dphi)
    A_minus = A_SSZ_phi_dependent(r, rs, varphi - dphi)
    
    return (A_plus - A_minus) / (2 * dphi)


def optimal_phi_for_mass(mass: float, criterion: str = 'intersection') -> float:
    """Bestimme optimalen φ-Wert für gegebene Masse.
    
    Kriterien:
    - 'intersection': Minimiere |D_SSZ(r*) - D_GR(r*)|
    - 'pn_match': Maximiere Übereinstimmung mit GR im schwachen Feld
    - 'stability': Minimiere dA/dφ (geringste Sensitivität)
    
    Args:
        mass: Masse in kg
        criterion: Optimierungskriterium
    
    Returns:
        Optimaler φ-Wert
    """
    from scipy.optimize import minimize_scalar
    
    rs = schwarzschild_radius(mass)
    
    if criterion == 'intersection':
        def objective(varphi):
            try:
                rstar = solve_r_star(rs, varphi)
                D_ssz = D_SSZ(rstar, rs, varphi)
                D_gr = np.sqrt(1 - rs/rstar)
                return abs(D_ssz - D_gr)
            except:
                return 1e10  # Penalty bei Fehler
        
        result = minimize_scalar(objective, bounds=(0.5, 3.0), method='bounded')
        return result.x
    
    elif criterion == 'pn_match':
        # Maximiere Übereinstimmung bei r = 10r_s
        r_test = 10 * rs
        def objective(varphi):
            A_ssz = A_SSZ_phi_dependent(r_test, rs, varphi)
            A_gr = 1.0 - rs/r_test
            return abs(A_ssz - A_gr)
        
        result = minimize_scalar(objective, bounds=(0.5, 3.0), method='bounded')
        return result.x
    
    elif criterion == 'stability':
        # Minimiere Sensitivität
        r_test = 5 * rs
        def objective(varphi):
            return abs(sensitivity_dA_dphi(r_test, rs, varphi))
        
        result = minimize_scalar(objective, bounds=(0.5, 3.0), method='bounded')
        return result.x
    
    else:
        raise ValueError(f"Unbekanntes Kriterium: {criterion}")


def phi_landscape(mass: float, phi_range: Tuple[float, float] = (0.5, 3.0), 
                  num: int = 100):
    """Berechne Metrik-Landschaft für verschiedene φ-Werte.
    
    Args:
        mass: Masse in kg
        phi_range: (φ_min, φ_max)
        num: Anzahl φ-Samples
    
    Returns:
        dict mit Keys: 'phi', 'r_star', 'D_star', 'epsilon_3'
    """
    rs = schwarzschild_radius(mass)
    phi_arr = np.linspace(phi_range[0], phi_range[1], num)
    
    r_star_arr = []
    D_star_arr = []
    eps3_arr = []
    
    for varphi in phi_arr:
        try:
            rstar = solve_r_star(rs, varphi)
            D_star = D_SSZ(rstar, rs, varphi)
            eps3 = epsilon_3_phi(varphi)
            
            r_star_arr.append(rstar/rs)
            D_star_arr.append(D_star)
            eps3_arr.append(eps3)
        except:
            r_star_arr.append(np.nan)
            D_star_arr.append(np.nan)
            eps3_arr.append(np.nan)
    
    return {
        'phi': phi_arr,
        'u_star': np.array(r_star_arr),
        'D_star': np.array(D_star_arr),
        'epsilon_3': np.array(eps3_arr)
    }


def demo():
    """Demo: φ-Variation für Sonnenmasse."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    
    # Compute landscape
    landscape = phi_landscape(M_sun, phi_range=(0.8, 2.5), num=200)
    
    # Optimale φ-Werte
    phi_opt_int = optimal_phi_for_mass(M_sun, 'intersection')
    phi_opt_pn = optimal_phi_for_mass(M_sun, 'pn_match')
    phi_opt_stab = optimal_phi_for_mass(M_sun, 'stability')
    
    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(10, 10))
    
    # Top: u*
    axes[0].plot(landscape['phi'], landscape['u_star'], lw=2)
    axes[0].axvline(PHI, ls='--', color='red', label=f'φ₀={PHI:.4f}')
    axes[0].axvline(phi_opt_int, ls=':', color='green', label=f'opt(int)={phi_opt_int:.4f}')
    axes[0].set_ylabel('u* = r*/r_s')
    axes[0].set_title('Schnittpunkt vs. φ')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Middle: D*
    axes[1].plot(landscape['phi'], landscape['D_star'], lw=2)
    axes[1].axvline(PHI, ls='--', color='red')
    axes[1].axvline(phi_opt_pn, ls=':', color='blue', label=f'opt(PN)={phi_opt_pn:.4f}')
    axes[1].set_ylabel('D*')
    axes[1].set_title('Zeitdilatation @ r* vs. φ')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    # Bottom: ε₃
    axes[2].plot(landscape['phi'], landscape['epsilon_3'], lw=2)
    axes[2].axvline(PHI, ls='--', color='red')
    axes[2].axhline(-24/5, ls=':', color='gray', label=f'ε₃₀=-24/5')
    axes[2].set_xlabel('φ')
    axes[2].set_ylabel('ε₃(φ)')
    axes[2].set_title('Kubischer Koeffizient vs. φ')
    axes[2].legend()
    axes[2].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/phi_landscape.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/phi_landscape.png")
    
    # Print results
    print(f"\n{'Kriterium':<20} {'φ_optimal':>12}")
    print("-"*35)
    print(f"{'Golden Ratio':<20} {PHI:>12.6f}")
    print(f"{'Intersection':<20} {phi_opt_int:>12.6f}")
    print(f"{'PN Match':<20} {phi_opt_pn:>12.6f}")
    print(f"{'Stability':<20} {phi_opt_stab:>12.6f}")


if __name__ == "__main__":
    demo()
