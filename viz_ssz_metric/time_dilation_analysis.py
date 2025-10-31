# -*- coding: utf-8 -*-
"""
PHASE 10: Zeitdilatation D(r) - Vollständige Analyse

Vergleicht zwei Formulierungen der Zeitdilatation:
1. D_PN = √A(r) - aus Post-Newtonscher Metrik
2. D_SSZ = 1/(1+Ξ) - aus Segment-Dichte

Analysiert Differenzen und physikalische Interpretation.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Tuple
from .ssz_mirror_metric import (
    schwarzschild_radius, D_SSZ, Xi, proper_time_dilation,
    metric_functions_pn, PHI, G_DEFAULT, C_DEFAULT
)


def D_from_metric(mass: float, r: float) -> float:
    """Zeitdilatation aus Post-Newtonscher Metrik.
    
    D_PN = √|g_tt| = √A(r)
    
    Args:
        mass: Masse in kg
        r: Radius in m
    
    Returns:
        D_PN ∈ (0, 1]
    """
    return proper_time_dilation(mass, r)


def D_from_segments(mass: float, r: float, varphi: float = PHI) -> float:
    """Zeitdilatation aus Segment-Dichte.
    
    D_SSZ = 1/(1 + Ξ(r))
    
    Args:
        mass: Masse in kg
        r: Radius in m
        varphi: φ-Parameter
    
    Returns:
        D_SSZ ∈ (0, 1]
    """
    rs = schwarzschild_radius(mass)
    return D_SSZ(r, rs, varphi)


def time_dilation_comparison(mass: float, r: float, varphi: float = PHI) -> dict:
    """Vergleiche beide Zeitdilatations-Formulierungen.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        varphi: φ-Parameter
    
    Returns:
        dict mit Keys:
        - 'D_PN': aus Metrik
        - 'D_SSZ': aus Segmenten
        - 'Delta': Absolute Differenz
        - 'Delta_%': Relative Differenz in Prozent
    """
    D_pn = D_from_metric(mass, r)
    D_ssz = D_from_segments(mass, r, varphi)
    
    delta_abs = D_pn - D_ssz
    delta_rel = 100 * delta_abs / D_pn if D_pn > 0 else np.nan
    
    return {
        'D_PN': D_pn,
        'D_SSZ': D_ssz,
        'Delta': delta_abs,
        'Delta_%': delta_rel
    }


def proper_time_elapsed(mass: float, r: float, dt_coordinate: float, 
                        method: str = 'PN') -> float:
    """Berechne verstrichene Eigenzeit für gegebene Koordinatenzeit.
    
    dτ = D(r) · dt
    
    Args:
        mass: Masse in kg
        r: Radius in m
        dt_coordinate: Koordinatenzeit-Intervall (Sekunden)
        method: 'PN' (Metrik) oder 'SSZ' (Segmente)
    
    Returns:
        dτ (Eigenzeit in Sekunden)
    
    Beispiel:
        Für einen stationären Beobachter bei r=2r_s läuft die Uhr
        langsamer als in unendlicher Entfernung.
    """
    if method == 'PN':
        D = D_from_metric(mass, r)
    elif method == 'SSZ':
        D = D_from_segments(mass, r)
    else:
        raise ValueError(f"Unbekannte Methode: {method}")
    
    return D * dt_coordinate


def gravitational_redshift(mass: float, r: float, method: str = 'PN') -> float:
    """Gravitationsrotverschiebung z = 1/D - 1.
    
    Für Licht von r nach ∞:
    λ_∞/λ_r = 1/D(r) = 1 + z
    
    Args:
        mass: Masse in kg
        r: Radius in m
        method: 'PN' oder 'SSZ'
    
    Returns:
        z (dimensionslos, z>0 für Rotverschiebung)
    """
    if method == 'PN':
        D = D_from_metric(mass, r)
    elif method == 'SSZ':
        D = D_from_segments(mass, r)
    else:
        raise ValueError(f"Unbekannte Methode: {method}")
    
    return 1.0/D - 1.0


def clock_experiment_prediction(mass: float, r1: float, r2: float, 
                                dt_coordinate: float = 3600.0) -> dict:
    """Vorhersage für Uhren-Experiment (GPS-ähnlich).
    
    Zwei Uhren bei r1 und r2, Vergleich nach dt_coordinate Sekunden.
    
    Args:
        mass: Masse in kg
        r1, r2: Radien der beiden Uhren
        dt_coordinate: Koordinatenzeit-Intervall (default: 1 Stunde)
    
    Returns:
        dict mit Keys:
        - 'dtau_1_PN', 'dtau_2_PN': Eigenzeiten (PN-Metrik)
        - 'dtau_1_SSZ', 'dtau_2_SSZ': Eigenzeiten (Segment-Dichte)
        - 'diff_PN', 'diff_SSZ': Zeitdifferenzen in Sekunden
    """
    dtau_1_pn = proper_time_elapsed(mass, r1, dt_coordinate, 'PN')
    dtau_2_pn = proper_time_elapsed(mass, r2, dt_coordinate, 'PN')
    
    dtau_1_ssz = proper_time_elapsed(mass, r1, dt_coordinate, 'SSZ')
    dtau_2_ssz = proper_time_elapsed(mass, r2, dt_coordinate, 'SSZ')
    
    return {
        'dtau_1_PN': dtau_1_pn,
        'dtau_2_PN': dtau_2_pn,
        'diff_PN': dtau_1_pn - dtau_2_pn,
        'dtau_1_SSZ': dtau_1_ssz,
        'dtau_2_SSZ': dtau_2_ssz,
        'diff_SSZ': dtau_1_ssz - dtau_2_ssz,
    }


def demo():
    """Demo: Zeitdilatations-Vergleich."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Radius-Bereich
    r = np.linspace(1.5*rs, 20*rs, 500)
    
    # Berechne beide Formulierungen
    D_pn = np.array([D_from_metric(M_sun, r_val) for r_val in r])
    D_ssz = np.array([D_from_segments(M_sun, r_val, PHI) for r_val in r])
    D_gr = np.sqrt(1 - rs/r)  # GR zum Vergleich
    
    delta = D_pn - D_ssz
    delta_percent = 100 * delta / D_pn
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Top: D(r) Vergleich
    ax1.plot(r/rs, D_gr, 'k--', lw=1.5, alpha=0.5, label='GR (Schwarzschild)')
    ax1.plot(r/rs, D_pn, lw=2.5, color='#1f77b4', label='D_PN (aus Metrik)')
    ax1.plot(r/rs, D_ssz, lw=2.5, ls='--', color='#ff7f0e', label='D_SSZ (aus Segmenten)')
    ax1.set_ylabel('D(r)')
    ax1.set_title('Zeitdilatation: Post-Newtonsche Metrik vs. Segment-Dichte')
    ax1.legend(loc='lower right')
    ax1.grid(alpha=0.3)
    ax1.set_ylim([0, 1.05])
    
    # Bottom: Differenz
    ax2.plot(r/rs, delta_percent, lw=2.5, color='#2ca02c')
    ax2.axhline(0, ls='--', color='gray', alpha=0.5)
    ax2.set_xlabel('r/r_s')
    ax2.set_ylabel('Δ = (D_PN - D_SSZ) / D_PN [%]')
    ax2.set_title('Relative Differenz')
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/time_dilation_comparison.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/time_dilation_comparison.png")
    
    # Uhren-Experiment
    print("\n" + "="*80)
    print("UHREN-EXPERIMENT: GPS-ähnliche Konfiguration")
    print("="*80)
    
    # GPS-Satellit bei ~20.000 km (≈3.4 r_Earth)
    # Vereinfacht: verwende Sonnenmasse als Test
    r1 = 2 * rs   # Innere Uhr (starke Gravitation)
    r2 = 10 * rs  # Äußere Uhr (schwache Gravitation)
    dt_coord = 86400.0  # 1 Tag in Sekunden
    
    result = clock_experiment_prediction(M_sun, r1, r2, dt_coord)
    
    print(f"\nRadien:")
    print(f"  r1 = {r1/rs:.2f} r_s (innere Uhr)")
    print(f"  r2 = {r2/rs:.2f} r_s (äußere Uhr)")
    print(f"  Koordinatenzeit: {dt_coord/3600:.1f} Stunden")
    
    print(f"\nPost-Newtonsche Metrik:")
    print(f"  Eigenzeit r1: {result['dtau_1_PN']/3600:.6f} Stunden")
    print(f"  Eigenzeit r2: {result['dtau_2_PN']/3600:.6f} Stunden")
    print(f"  Differenz: {result['diff_PN']:.6f} Sekunden")
    
    print(f"\nSegment-Dichte:")
    print(f"  Eigenzeit r1: {result['dtau_1_SSZ']/3600:.6f} Stunden")
    print(f"  Eigenzeit r2: {result['dtau_2_SSZ']/3600:.6f} Stunden")
    print(f"  Differenz: {result['diff_SSZ']:.6f} Sekunden")
    
    print("="*80)
    
    # Rotverschiebung
    print("\nGravitationsrotverschiebung:")
    for r_mult in [2, 3, 5, 10]:
        r_test = r_mult * rs
        z_pn = gravitational_redshift(M_sun, r_test, 'PN')
        z_ssz = gravitational_redshift(M_sun, r_test, 'SSZ')
        print(f"  r = {r_mult}r_s: z_PN = {z_pn:.6f}, z_SSZ = {z_ssz:.6f}, Δz = {z_pn-z_ssz:.6e}")


if __name__ == "__main__":
    demo()
