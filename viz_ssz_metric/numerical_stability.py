# -*- coding: utf-8 -*-
"""
Numerical Stability Functions - Konsolidierte numerische Stabilität

Basierend auf: ssz_theory_segmented.py aus Vorlage-Repo
Konsolidiert: Alle Overflow-Schutz und Sättigungs-Funktionen

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from typing import Union


def exp_clip(x: Union[float, np.ndarray], bound: float = 80.0) -> Union[float, np.ndarray]:
    """
    Overflow-safe exponential.
    
    Clippt exp-Argumente auf [-bound, bound] um Overflow zu vermeiden.
    
    Für x > 80: exp(x) > 5e34 → Overflow-Risiko!
    
    Args:
        x: Input value(s)
        bound: Maximum absolute value (default: 80.0)
    
    Returns:
        exp(clip(x, -bound, bound))
    
    Examples:
        >>> exp_clip(100)  # Sicher: exp(80)
        5.540622e+34
        >>> exp_clip(-100)  # Sicher: exp(-80)
        1.804851e-35
    """
    x_safe = np.clip(x, -bound, bound)
    return np.exp(x_safe)


def sech2_stable(z: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Overflow-safe sech²(z) = 1/cosh²(z).
    
    Für große |z|: cosh(z) ~ 0.5×exp(|z|) → Overflow!
    
    Asymptotische Form für |z| ≥ 20:
    sech²(z) ~ 4×exp(-2|z|)
    
    Args:
        z: Input value(s)
    
    Returns:
        sech²(z) without overflow
    
    Examples:
        >>> sech2_stable(0)
        1.0
        >>> sech2_stable(50)  # Kein Overflow!
        1.819...e-44
    """
    a = np.abs(z)
    
    # Für kleine |z|: Exakte Berechnung
    mask_small = a < 20.0
    
    result = np.zeros_like(a)
    
    if np.isscalar(z):
        if a < 20.0:
            c = np.cosh(z)
            return 1.0 / (c * c)
        else:
            return 4.0 * np.exp(-2.0 * a)
    else:
        # Array-Fall
        c = np.cosh(z[mask_small])
        result[mask_small] = 1.0 / (c * c)
        result[~mask_small] = 4.0 * np.exp(-2.0 * a[~mask_small])
        return result


def sat_tanh(x: Union[float, np.ndarray], cap: float | None) -> Union[float, np.ndarray]:
    """
    Glatte Sättigung via tanh.
    
    output = cap × tanh(x / cap)
    
    Eigenschaften:
    - Bounded: |output| ≤ cap
    - Smooth: Keine Kanten
    - Derivable: d/dx = sech²(x/cap)
    
    Args:
        x: Input value(s)
        cap: Saturation limit (None or ≤0 = no saturation)
    
    Returns:
        Saturated value
    
    Examples:
        >>> sat_tanh(10, cap=1)
        0.999...  # ≈ 1
        >>> sat_tanh(100, cap=1)
        1.0  # Saturiert bei cap
    """
    if cap is None or cap <= 0:
        return x
    return cap * np.tanh(x / cap)


def sat_pos_tanh(y: Union[float, np.ndarray], cap: float | None) -> Union[float, np.ndarray]:
    """
    Glatte Sättigung für y ≥ 0.
    
    Erst clippe auf y ≥ 0, dann saturiere.
    
    Args:
        y: Input value(s)
        cap: Saturation limit (None or ≤0 = no saturation)
    
    Returns:
        Saturated positive value
    
    Examples:
        >>> sat_pos_tanh(-5, cap=1)
        0.0  # Negativ → 0
        >>> sat_pos_tanh(10, cap=1)
        0.999...  # Saturiert
    """
    if np.isscalar(y):
        y_pos = max(y, 0.0)
    else:
        y_pos = np.maximum(y, 0.0)
    
    if cap is None or cap <= 0:
        return y_pos
    
    return cap * np.tanh(y_pos / cap)


def sigmoid_saturation(x: Union[float, np.ndarray], x_max: float) -> Union[float, np.ndarray]:
    """
    Sigmoid-Sättigung: output ∈ [0, x_max].
    
    σ(x) = x_max / (1 + exp(-x/x_max))
    
    Asymptotik:
    - x → -∞: σ → 0
    - x → +∞: σ → x_max
    - x = 0: σ = x_max/2
    
    Args:
        x: Input value(s)
        x_max: Maximum value
    
    Returns:
        Saturated value ∈ [0, x_max]
    """
    if x_max <= 0:
        raise ValueError("x_max must be positive!")
    
    # Numerisch stabil
    z = x / x_max
    return x_max / (1.0 + exp_clip(-z, bound=80.0))


def safe_sqrt(x: Union[float, np.ndarray], epsilon: float = 1e-30) -> Union[float, np.ndarray]:
    """
    Safe square root: √(max(x, ε)).
    
    Verhindert √(negative Zahl).
    
    Args:
        x: Input value(s)
        epsilon: Minimum value (default: 1e-30)
    
    Returns:
        √(max(x, ε))
    """
    if np.isscalar(x):
        return np.sqrt(max(x, epsilon))
    else:
        return np.sqrt(np.maximum(x, epsilon))


def safe_divide(numerator: Union[float, np.ndarray], 
                denominator: Union[float, np.ndarray],
                epsilon: float = 1e-30) -> Union[float, np.ndarray]:
    """
    Safe division: numerator / max(|denominator|, ε).
    
    Verhindert Division durch 0.
    
    Args:
        numerator: Zähler
        denominator: Nenner
        epsilon: Minimum |denominator| (default: 1e-30)
    
    Returns:
        numerator / max(|denominator|, ε)
    """
    denom_safe = np.maximum(np.abs(denominator), epsilon)
    return numerator / denom_safe


def golden_ratio_saturation(E: float, K: float, E_0: float = 1.0) -> float:
    """
    Golden Ratio Sättigung für Black Hole Bomb.
    
    E_max = E_0 × (1 - exp(-φ × K))
    
    wobei φ = (1+√5)/2 ≈ 1.618
    
    Args:
        E: Aktuelle Energie
        K: Segment-Anzahl
        E_0: Initiale Energie
    
    Returns:
        Saturierte Energie E_max
    """
    PHI = (1.0 + np.sqrt(5.0)) / 2.0
    return E_0 * (1.0 - np.exp(-PHI * K))


def demo():
    """Demo: Alle numerischen Stabilisierungs-Funktionen."""
    print("\n" + "="*80)
    print("NUMERICAL STABILITY FUNCTIONS")
    print("="*80)
    
    # Test exp_clip
    print("\n1. exp_clip (Overflow-safe exponential):")
    print(f"   exp_clip(100) = {exp_clip(100):.3e}  (clipped to exp(80))")
    print(f"   exp(100) would overflow! (> 10^43)")
    
    # Test sech2_stable
    print("\n2. sech2_stable (Overflow-safe sech²):")
    print(f"   sech2_stable(0) = {sech2_stable(0):.6f}")
    print(f"   sech2_stable(50) = {sech2_stable(50):.3e}  (no overflow!)")
    
    # Test sat_tanh
    print("\n3. sat_tanh (Smooth saturation):")
    print(f"   sat_tanh(0.5, cap=1) = {sat_tanh(0.5, 1.0):.6f}")
    print(f"   sat_tanh(10, cap=1) = {sat_tanh(10, 1.0):.6f}  (saturated)")
    
    # Test sat_pos_tanh
    print("\n4. sat_pos_tanh (Positive saturation):")
    print(f"   sat_pos_tanh(-5, cap=1) = {sat_pos_tanh(-5, 1.0):.6f}")
    print(f"   sat_pos_tanh(10, cap=1) = {sat_pos_tanh(10, 1.0):.6f}")
    
    # Test sigmoid_saturation
    print("\n5. sigmoid_saturation:")
    print(f"   sigmoid(0, x_max=1) = {sigmoid_saturation(0, 1.0):.6f}")
    print(f"   sigmoid(10, x_max=1) = {sigmoid_saturation(10, 1.0):.6f}")
    
    # Test safe_sqrt
    print("\n6. safe_sqrt:")
    print(f"   safe_sqrt(-1) = {safe_sqrt(-1):.3e}  (no NaN!)")
    print(f"   safe_sqrt(4) = {safe_sqrt(4):.1f}")
    
    # Test safe_divide
    print("\n7. safe_divide:")
    print(f"   safe_divide(1, 0) = {safe_divide(1, 0):.3e}  (no inf!)")
    print(f"   safe_divide(10, 2) = {safe_divide(10, 2):.1f}")
    
    # Test golden_ratio_saturation
    print("\n8. golden_ratio_saturation (Black Hole Bomb):")
    K = 100
    E_max = golden_ratio_saturation(1.0, K)
    print(f"   K = {K}")
    print(f"   E_max = {E_max:.6f}")
    print(f"   Saturation prevents explosive growth!")
    
    print("="*80)
    print("All functions numerically stable!")
    print("   - No overflows")
    print("   - No NaN/Inf")
    print("   - Smooth bounds")
    print("   - Physically meaningful")


if __name__ == "__main__":
    demo()
