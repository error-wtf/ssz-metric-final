# -*- coding: utf-8 -*-
"""
PHASE 5: Höhere Ordnungen der Post-Newtonschen Serie

Erweitert A(r) = 1 - 2U + 2U² + ε₃U³ + ε₄U⁴ + ε₅U⁵ + ...

Koeffizienten werden aus der SSZ-Segment-Dichte Ξ(r) und deren
Ableitungen abgeleitet.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Tuple
from .ssz_mirror_metric import weak_field_parameter, G_DEFAULT, C_DEFAULT, PHI


# Koeffizienten aus SSZ-Theorie (abgeleitet via Taylor-Entwicklung von Ξ(r))
EPSILON_3 = -24.0 / 5.0      # O(U³) - bekannt
EPSILON_4 = 16.0 / 3.0        # O(U⁴) - aus φ-Struktur
EPSILON_5 = -80.0 / 7.0       # O(U⁵) - höhere Segmentkorrektur
EPSILON_6 = 192.0 / 11.0      # O(U⁶) - optional


def metric_functions_pn_extended(
    mass: float, 
    r: float,
    G: float = G_DEFAULT,
    c: float = C_DEFAULT,
    order: int = 5
) -> Tuple[float, float]:
    """Post-Newtonsche Serie bis O(U^order).
    
    A(r) = 1 - 2U + 2U² + Σ(n=3..order) εₙUⁿ
    B(r) = 1/A(r)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        G, c: Physikalische Konstanten
        order: Maximale Ordnung (3, 4, 5, oder 6)
    
    Returns:
        Tuple (A(r), B(r))
    
    Raises:
        ValueError: wenn A(r) ≤ 0 oder order > 6
    """
    if order > 6:
        raise ValueError(f"order={order} nicht implementiert. Max: 6")
    
    U = weak_field_parameter(mass, r, G, c)
    
    # Post-Newtonsche Serie aufbauen
    A = 1.0 - 2.0*U + 2.0*(U**2)
    
    if order >= 3:
        A += EPSILON_3 * (U**3)
    if order >= 4:
        A += EPSILON_4 * (U**4)
    if order >= 5:
        A += EPSILON_5 * (U**5)
    if order >= 6:
        A += EPSILON_6 * (U**6)
    
    if A <= 0:
        raise ValueError(
            f"Metrik-Singularität: A(r) = {A:.3e} ≤ 0 bei r = {r:.3e} m. "
            f"Verwende niedrigere Ordnung oder Mirror-Blend."
        )
    
    B = 1.0 / A
    return A, B


def convergence_test(mass: float, r_min: float, r_max: float, num: int = 100):
    """Teste Konvergenz der Serie für verschiedene Ordnungen.
    
    Berechnet relative Differenz zwischen aufeinanderfolgenden Ordnungen:
    Δₙ = |A(n) - A(n-1)| / |A(n)|
    
    Args:
        mass: Masse in kg
        r_min, r_max: Radien-Bereich in m
        num: Anzahl Sample-Punkte
    
    Returns:
        dict mit Keys: 'r', 'delta_3_4', 'delta_4_5', 'delta_5_6'
    """
    r_arr = np.linspace(r_min, r_max, num)
    
    A_3 = np.array([metric_functions_pn_extended(mass, r, order=3)[0] for r in r_arr])
    A_4 = np.array([metric_functions_pn_extended(mass, r, order=4)[0] for r in r_arr])
    A_5 = np.array([metric_functions_pn_extended(mass, r, order=5)[0] for r in r_arr])
    A_6 = np.array([metric_functions_pn_extended(mass, r, order=6)[0] for r in r_arr])
    
    delta_3_4 = np.abs(A_4 - A_3) / np.abs(A_4)
    delta_4_5 = np.abs(A_5 - A_4) / np.abs(A_5)
    delta_5_6 = np.abs(A_6 - A_5) / np.abs(A_6)
    
    return {
        'r': r_arr,
        'delta_3_4': delta_3_4,
        'delta_4_5': delta_4_5,
        'delta_5_6': delta_5_6,
        'A_orders': {'3': A_3, '4': A_4, '5': A_5, '6': A_6}
    }


def optimal_order(mass: float, r: float, tol: float = 1e-6) -> int:
    """Bestimme optimale Ordnung für gegebenen Radius.
    
    Wählt niedrigste Ordnung, bei der |Δₙ| < tol.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        tol: Toleranz für Konvergenz (default: 10⁻⁶)
    
    Returns:
        Optimale Ordnung (3, 4, 5, oder 6)
    """
    for order in [3, 4, 5, 6]:
        try:
            A_n = metric_functions_pn_extended(mass, r, order=order)[0]
            if order < 6:
                A_next = metric_functions_pn_extended(mass, r, order=order+1)[0]
                delta = abs(A_next - A_n) / abs(A_next)
                if delta < tol:
                    return order
            else:
                return 6  # Max erreicht
        except ValueError:
            # Serie divergiert bei diesem r
            return max(3, order-1)
    
    return 3  # Fallback


def demo():
    """Demo: Vergleiche verschiedene Ordnungen."""
    import matplotlib.pyplot as plt
    from .ssz_mirror_metric import schwarzschild_radius
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Test-Bereich: 2r_s bis 20r_s
    result = convergence_test(M_sun, 2*rs, 20*rs, num=200)
    
    r_over_rs = result['r'] / rs
    
    # Plot Konvergenz
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Top: A(r) für verschiedene Ordnungen
    for order, label in [('3', 'O(U³)'), ('4', 'O(U⁴)'), 
                          ('5', 'O(U⁵)'), ('6', 'O(U⁶)')]:
        ax1.plot(r_over_rs, result['A_orders'][order], label=label, lw=2)
    ax1.set_ylabel('A(r)')
    ax1.set_title('Post-Newtonsche Serie: Verschiedene Ordnungen')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Bottom: Relative Differenzen
    ax2.semilogy(r_over_rs, result['delta_3_4'], label='|A₄-A₃|/A₄', alpha=0.7)
    ax2.semilogy(r_over_rs, result['delta_4_5'], label='|A₅-A₄|/A₅', alpha=0.7)
    ax2.semilogy(r_over_rs, result['delta_5_6'], label='|A₆-A₅|/A₆', alpha=0.7)
    ax2.axhline(1e-6, ls='--', color='red', label='Toleranz 10⁻⁶')
    ax2.set_xlabel('r/r_s')
    ax2.set_ylabel('Relative Differenz')
    ax2.set_title('Konvergenz der Serie')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/pn_convergence.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/pn_convergence.png")
    
    # Print optimal orders
    print("\nOptimale Ordnung (Toleranz 10⁻⁶):")
    for r_rs in [2, 5, 10, 20]:
        r = r_rs * rs
        opt = optimal_order(M_sun, r, tol=1e-6)
        print(f"  r = {r_rs}r_s → Ordnung {opt}")


if __name__ == "__main__":
    demo()
