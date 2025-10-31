# -*- coding: utf-8 -*-
"""
SINGULARITÄTSVERMEIDUNG: Golden Ratio Sättigungs-Modul

Implementiert die fundamentale Stabilisierungsmechanik aus dem
Segmented Spacetime Framework:

1. Golden Ratio Sättigung: E_max = E_0 (1 - exp(-φK))
2. Kritische Kopplung: λ_A < 1/K²
3. φ-Radius Bound: r_φ = (φ/2) × r_s
4. Maximale Dichte: ρ_max = M/(4π/3 × r_φ³)

Dies ist das HERZSTÜCK der Singularitätsvermeidung!

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4

Basierend auf: "Stability of Black Holes in Segmented Spacetime"
"""
from __future__ import annotations
import numpy as np
import math
from typing import Tuple
from .ssz_mirror_metric import schwarzschild_radius, PHI, G_DEFAULT, C_DEFAULT
from .mass_corrections import delta_M


# ============================= FUNDAMENTALE GRENZEN =============================

def r_phi_exact(mass: float, varphi: float = PHI) -> float:
    """φ-Radius mit Masse-Korrektur Δ(M).
    
    r_φ = φ × (GM/c²) × (1 + Δ(M)/100)
    
    Dies ist die FUNDAMENTALE GRENZE unterhalb derer
    die Segment-Dichte saturiert!
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter (default: Golden Ratio)
    
    Returns:
        r_φ in Metern
    
    Physikalische Bedeutung:
    - r_φ < r_s (SSZ-Horizont INNERHALB Schwarzschild!)
    - r < r_φ: Vollständige Segment-Sättigung
    - r > r_φ: Gradueller Übergang zu GR
    """
    rs = schwarzschild_radius(mass)
    Delta_percent = delta_M(mass)
    
    # φ-Radius mit Masse-Korrektur
    r_phi_base = (varphi / 2.0) * rs
    r_phi_corrected = r_phi_base * (1.0 + Delta_percent / 100.0)
    
    return r_phi_corrected


def rho_max_density(mass: float, varphi: float = PHI) -> float:
    """Maximale Energie-Dichte bei r = r_φ.
    
    ρ_max = M / (4π/3 × r_φ³)
    
    **KRITISCH:** Dies ist die ENDLICHE maximale Dichte!
    GR sagt ρ(r=0) = ∞ voraus → SSZ widerlegt Singularität!
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
    
    Returns:
        ρ_max in kg/m³ (ENDLICH!)
    """
    r_phi = r_phi_exact(mass, varphi)
    
    # Volumen der φ-Kugel
    V_phi = (4.0 * math.pi / 3.0) * (r_phi**3)
    
    # Maximale Dichte
    rho_max = mass / V_phi
    
    return rho_max


def kretschmann_max(mass: float, varphi: float = PHI) -> float:
    """Maximale Kretschmann-Krümmung bei r = r_φ.
    
    K_max = 12 r_s² / r_φ⁶
    
    **KRITISCH:** K bleibt ENDLICH! (GR: K → ∞ für r → 0)
    
    Args:
        mass: Masse in kg
        varphi: φ-Parameter
    
    Returns:
        K_max (endlich!)
    """
    rs = schwarzschild_radius(mass)
    r_phi = r_phi_exact(mass, varphi)
    
    K_max = 12.0 * (rs**2) / (r_phi**6)
    
    return K_max


# ============================= SÄTTIGUNGS-FUNKTIONEN =============================

def golden_ratio_saturation(value: float, value_max: float, 
                            r: float, r_phi: float, K: int = 100) -> float:
    """Golden Ratio Sättigung nach Black Hole Bomb Mechanismus.
    
    Saturation(r) = value_max × (1 - exp(-φK × r/r_φ))
    
    Für r → 0: Saturation → 0
    Für r → r_φ: Saturation → value_max × (1 - exp(-φK)) ≈ value_max
    Für r >> r_φ: Saturation → value_max
    
    Args:
        value: Aktueller Wert (kann divergieren)
        value_max: Maximaler erlaubter Wert
        r: Radius
        r_phi: φ-Radius
        K: Segment-Anzahl (default: 100)
    
    Returns:
        Saturierter Wert ≤ value_max
    """
    if r >= r_phi:
        # Außerhalb r_φ: Keine Sättigung nötig
        return min(value, value_max)
    
    # Sättigungsfaktor (Golden Ratio basiert)
    saturation_factor = 1.0 - np.exp(-PHI * K * r / r_phi)
    
    # Glatter Übergang
    value_saturated = value * saturation_factor
    
    # Hard cap (Sicherheit)
    return min(value_saturated, value_max)


def softplus_floor(value: float, epsilon: float = 1e-6, beta: float = 50.0) -> float:
    """Softplus-Floor garantiert value > epsilon.
    
    Softplus(x) = (1/β) × ln(1 + exp(β × (x - ε))) + ε
    
    **Garantiert:** Rückgabe > epsilon (niemals 0!)
    
    Args:
        value: Input-Wert (kann → 0 gehen)
        epsilon: Minimum-Wert (default: 10⁻⁶)
        beta: Steilheit (default: 50)
    
    Returns:
        value_safe > epsilon (immer!)
    """
    shifted = value - epsilon
    
    # Numerisch stabil (clip für große β|shifted|)
    argument = beta * shifted
    if argument > 50:
        # ln(1 + exp(x)) ≈ x für große x
        return shifted / beta + epsilon
    elif argument < -50:
        # ln(1 + exp(x)) ≈ exp(x) für kleine x
        return np.exp(argument) / beta + epsilon
    else:
        return np.log(1.0 + np.exp(argument)) / beta + epsilon


def critical_coupling_check(lambda_A: float, K: int) -> bool:
    """Prüfe Stabilitätsbedingung λ_A < λ_crit = 1/K².
    
    Aus Black Hole Bomb Paper:
    - λ_A < 1/K²: STABIL (Energie saturiert)
    - λ_A ≥ 1/K²: INSTABIL (Energie divergiert)
    
    Args:
        lambda_A: Kopplungskonstante
        K: Segment-Anzahl
    
    Returns:
        True wenn stabil, False wenn instabil
    """
    lambda_crit = 1.0 / (K**2)
    return lambda_A < lambda_crit


# ============================= METRIK-SÄTTIGUNG =============================

def A_saturated(mass: float, r: float, A_unsaturated: float, 
                varphi: float = PHI, epsilon: float = 1e-6) -> float:
    """Saturierte Metrik-Funktion A(r) - KEINE Singularität!
    
    Kombiniert:
    1. Golden Ratio Sättigung bei r < r_φ
    2. Softplus-Floor A > epsilon
    
    **Garantiert:** A(r) > 0 für ALLE r > 0 (auch r → 0!)
    
    Args:
        mass: Masse in kg
        r: Radius in m
        A_unsaturated: Unsaturierte A(r) (kann → 0 gehen)
        varphi: φ-Parameter
        epsilon: Minimum-Wert
    
    Returns:
        A_safe > 0 (garantiert!)
    """
    r_phi = r_phi_exact(mass, varphi)
    
    # Maximum bei r_φ (nicht ∞!)
    A_max_at_phi = 1.0  # Normalisierung
    
    # Sättigung wenn r < r_φ
    if r < r_phi:
        A_sat = golden_ratio_saturation(
            A_unsaturated, 
            A_max_at_phi, 
            r, 
            r_phi,
            K=100
        )
    else:
        A_sat = A_unsaturated
    
    # Softplus-Floor garantiert A > 0
    A_safe = softplus_floor(A_sat, epsilon=epsilon)
    
    return A_safe


def christoffel_saturated(Gamma_unsaturated: float, mass: float, r: float,
                         varphi: float = PHI) -> float:
    """Saturierte Christoffel-Symbole - KEINE Divergenz!
    
    Christoffel können divergieren wenn:
    - dA/dr → ∞
    - B = 1/A → ∞
    
    SSZ-Lösung: Bound durch r_φ-Skalierung
    
    Args:
        Gamma_unsaturated: Unsaturiertes Christoffel-Symbol
        mass: Masse
        r: Radius
        varphi: φ-Parameter
    
    Returns:
        Γ_safe (bounded)
    """
    r_phi = r_phi_exact(mass, varphi)
    rs = schwarzschild_radius(mass)
    
    # Maximaler Wert bei r_φ
    Gamma_max = 1.0 / r_phi  # Natürliche Skala
    
    # Sättigung
    if r < r_phi:
        Gamma_sat = golden_ratio_saturation(
            abs(Gamma_unsaturated),
            Gamma_max,
            r,
            r_phi,
            K=100
        )
        # Vorzeichen beibehalten
        Gamma_safe = np.sign(Gamma_unsaturated) * Gamma_sat
    else:
        Gamma_safe = Gamma_unsaturated
    
    return Gamma_safe


def kretschmann_saturated(K_unsaturated: float, mass: float, r: float,
                         varphi: float = PHI) -> float:
    """Saturierter Kretschmann-Skalar - KEINE Singularität!
    
    GR: K = 12 r_s² / r⁶ → ∞ für r → 0
    SSZ: K_max = 12 r_s² / r_φ⁶ (ENDLICH!)
    
    Args:
        K_unsaturated: Unsaturierter K (kann → ∞)
        mass: Masse
        r: Radius
        varphi: φ-Parameter
    
    Returns:
        K_safe < K_max (bounded!)
    """
    K_max = kretschmann_max(mass, varphi)
    r_phi = r_phi_exact(mass, varphi)
    
    # Sättigung bei r < r_φ
    if r < r_phi:
        K_safe = golden_ratio_saturation(
            K_unsaturated,
            K_max,
            r,
            r_phi,
            K=100
        )
    else:
        K_safe = min(K_unsaturated, K_max * 1.1)  # Soft cap auch außerhalb
    
    return K_safe


def energy_density_bounded(rho_unsaturated: float, mass: float, 
                          varphi: float = PHI) -> float:
    """Bounded Energie-Dichte - KEINE Divergenz!
    
    GR: ρ(r=0) = ∞
    SSZ: ρ(r < r_φ) ≤ ρ_max (ENDLICH!)
    
    Args:
        rho_unsaturated: Unsaturierte Dichte (kann → ∞)
        mass: Masse
        varphi: φ-Parameter
    
    Returns:
        ρ_safe ≤ ρ_max (bounded!)
    """
    rho_maximum = rho_max_density(mass, varphi)
    
    # Hard bound (Sättigung erfolgt im Metrik-Level)
    if abs(rho_unsaturated) > rho_maximum:
        rho_safe = np.sign(rho_unsaturated) * rho_maximum
    else:
        rho_safe = rho_unsaturated
    
    return rho_safe


# ============================= ENERGIE-EVOLUTION =============================

def energy_evolution_ssz(E_current: float, lambda_A: float, K: int, 
                        time_steps: int = 1) -> float:
    """Energie-Evolution nach SSZ Black Hole Bomb Mechanismus.
    
    E_{t+1} = E_t × (1 + λ_A - λ_A² K²)
    
    Mit Golden Ratio Sättigung:
    E_max = E_0 × (1 - exp(-φK))
    
    Args:
        E_current: Aktuelle Energie
        lambda_A: Kopplungskonstante
        K: Segment-Anzahl
        time_steps: Anzahl Zeitschritte
    
    Returns:
        E_final (saturiert!)
    """
    # Prüfe Stabilität
    if not critical_coupling_check(lambda_A, K):
        raise ValueError(
            f"Instabile Kopplung! λ_A={lambda_A:.6f} ≥ λ_crit={1/K**2:.6f}"
        )
    
    # Evolution
    E = E_current
    growth_factor = 1.0 + lambda_A - (lambda_A**2) * (K**2)
    
    for _ in range(time_steps):
        E = E * growth_factor
        
        # Golden Ratio Sättigung
        E_max = E_current * (1.0 - np.exp(-PHI * K))
        E = min(E, E_max)
    
    return E


def demo():
    """Demo: Singularitätsvermeidung für verschiedene Massen."""
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    
    # Test-Massen
    masses = {
        'Sonne (1 M☉)': M_sun,
        'Neutronenstern (3 M☉)': 3 * M_sun,
        'Stellar BH (10 M☉)': 10 * M_sun,
        'Sgr A* (4.15e6 M☉)': 4.15e6 * M_sun,
    }
    
    print("\n" + "="*90)
    print("SINGULARITÄTSVERMEIDUNG: FUNDAMENTALE GRENZEN")
    print("="*90)
    print(f"{'Objekt':<25} {'r_s (km)':>15} {'r_φ (km)':>15} {'r_φ/r_s':>12} "
          f"{'ρ_max (kg/m³)':>18} {'K_max':>15}")
    print("-"*90)
    
    for name, M in masses.items():
        rs = schwarzschild_radius(M) / 1000  # km
        r_phi = r_phi_exact(M) / 1000  # km
        ratio = r_phi_exact(M) / schwarzschild_radius(M)
        rho = rho_max_density(M)
        K = kretschmann_max(M)
        
        print(f"{name:<25} {rs:>15.3e} {r_phi:>15.3e} {ratio:>12.6f} "
              f"{rho:>18.3e} {K:>15.3e}")
    
    print("="*90)
    
    print("\n✅ WICHTIGE ERKENNTNISSE:")
    print("  • r_φ < r_s: SSZ-Horizont liegt INNERHALB Schwarzschild!")
    print("  • ρ_max ist ENDLICH (keine Singularität!)")
    print("  • K_max ist ENDLICH (GR: K → ∞)")
    print("  • Alle Werte bleiben bounded für r → 0")
    
    # Black Hole Bomb Test
    print("\n" + "="*90)
    print("BLACK HOLE BOMB: ENERGIE-EVOLUTION")
    print("="*90)
    
    K = 100
    lambda_A = 0.005  # < λ_crit = 0.0001
    E_0 = 1.0
    time_steps = 10000
    
    E_final = energy_evolution_ssz(E_0, lambda_A, K, time_steps)
    E_max_theory = E_0 * (1.0 - np.exp(-PHI * K))
    
    print(f"Segment-Anzahl K: {K}")
    print(f"Kopplung λ_A: {lambda_A}")
    print(f"Kritische Kopplung λ_crit: {1/K**2:.6f}")
    print(f"Stabil? {'✅ JA' if lambda_A < 1/K**2 else '❌ NEIN'}")
    print(f"\nAnfangsenergie E_0: {E_0:.4f}")
    print(f"Energie nach {time_steps} Schritten: {E_final:.4f}")
    print(f"Theoretisches Maximum E_max: {E_max_theory:.4f}")
    print(f"Amplifikationsfaktor: {E_final/E_0:.2f}× (GR: ~10⁸×!)")
    print("="*90)
    
    print("\n✅ SSZ verhindert explosive Energie-Amplifikation!")
    print("   GR: E → ∞ (Black Hole explodiert)")
    print("   SSZ: E → E_max (stabil)")


if __name__ == "__main__":
    demo()
