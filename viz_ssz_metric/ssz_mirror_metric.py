# -*- coding: utf-8 -*-
"""
Singularitätenfreie SSZ–GR Mirror-Metrik (sphärisch symmetrisch, statisch).

Basierend auf der Segmented Spacetime Theorie von Carmen Wrede & Lino Casu.

Linienelement:
    ds² = -A_safe(r) dt² + B_safe(r) dr² + r²dΩ²

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import brentq

# Physikalische Konstanten
G_DEFAULT = 6.67430e-11  # m³/(kg·s²)
C_DEFAULT = 299_792_458.0  # m/s
PHI = (1 + np.sqrt(5)) / 2  # Golden Ratio ≈ 1.618033988749...


def schwarzschild_radius(M: float, G: float = G_DEFAULT, c: float = C_DEFAULT) -> float:
    """Schwarzschild-Radius r_s = 2GM/c²"""
    return 2.0 * G * M / (c * c)


def Xi(r, rs, varphi=PHI):
    """Segment-Dichte (KORREKTE exponential saturation form)
    
    Ξ(r) = Ξ_max * (1 - exp(-φ * r/r_s))
    
    Args:
        r: Radius (scalar or array)
        rs: Schwarzschild-Radius
        varphi: φ-Parameter (default: Golden Ratio)
    
    Returns:
        Segment density 0 ≤ Ξ(r) < 1
    """
    r = np.asarray(r, float)
    return 1.0 - np.exp(-varphi * r / rs)


def D_SSZ(r, rs, varphi=PHI):
    """SSZ-Zeitdilatation (KORREKTE Formel)
    
    D(r) = 1 / (1 + Ξ(r))
    
    Args:
        r: Radius
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
    
    Returns:
        Time dilation factor 0 < D(r) ≤ 1
    """
    return 1.0 / (1.0 + Xi(r, rs, varphi))


def A_SSZ(r, rs, varphi=PHI):
    """SSZ-Metrik-Koeffizient: A(r) = D²(r)"""
    D = D_SSZ(r, rs, varphi)
    return D * D


def A_GR(r, rs):
    """GR-Schwarzschild-Metrik: A(r) = 1 - r_s/r"""
    r = np.asarray(r, float)
    return 1.0 - (rs / r)


def solve_r_star(rs: float, varphi: float = PHI) -> float:
    """Löse SSZ = GR Schnittpunkt numerisch.
    
    Findet r* wo: D_SSZ(r*) = D_GR(r*)
    Äquivalent: sqrt(1 - r_s/r*) = 1/(1 + Ξ(r*))
    
    Args:
        rs: Schwarzschild-Radius
        varphi: φ-Parameter
    
    Returns:
        r_star: Schnittpunkt-Radius
    """
    def equation(r):
        D_ssz = D_SSZ(r, rs, varphi)
        D_gr = np.sqrt(1 - rs/r)
        return D_ssz - D_gr
    
    try:
        # Brentq für robuste root-finding
        r_star = brentq(equation, rs * 1.01, rs * 2.5)
        return r_star
    except ValueError:
        # Fallback: Bisection mit größerem Intervall
        r_star = brentq(equation, rs * 1.001, rs * 3.0)
        return r_star


def A_safe(r, rs, varphi: float = PHI, delta_ratio: float = 0.02,
           eps: float = 1e-6, beta: float = 50.0):
    """Glatter Mirror-Blend: SSZ (innen) ↔ GR (außen) am Schnittpunkt r*.
    
    Verwendet:
    - tanh-Übergang für C^∞ Glätte
    - Softplus-Floor zur Singularitätsvermeidung (A > 0 garantiert)
    
    Args:
        r: Radius (array)
        rs: Schwarzschild-Radius
        varphi: φ-Parameter (default: Golden Ratio)
        delta_ratio: Übergangsbreite relativ zu r* (default: 0.02)
        eps: Softplus-Floor-Offset (default: 10⁻⁶)
        beta: Softplus-Steilheit (default: 50)
    
    Returns:
        (A_safe, r_star): Metrik-Koeffizient und Schnittpunkt
    """
    r = np.asarray(r, float)
    
    # 1. Schnittpunkt berechnen
    r_star = solve_r_star(rs, varphi)
    
    # 2. Übergangsbreite
    delta = max(delta_ratio * r_star, 1e-9)
    
    # 3. Glatte Übergangsweiche (tanh)
    #    h = 1 bei r << r*  (innen → SSZ)
    #    h = 0 bei r >> r*  (außen → GR)
    h = 0.5 * (1.0 - np.tanh((r - r_star) / delta))
    
    # 4. Mirror-Blend
    A_mix = h * A_SSZ(r, rs, varphi) + (1.0 - h) * A_GR(r, rs)
    
    # 5. Softplus-Floor (garantiert A > 0)
    #    A_safe = ε + (1/β) * ln(1 + exp(β*(A_mix - ε)))
    A = eps + (1.0 / beta) * np.log1p(np.exp(beta * (A_mix - eps)))
    
    return A, r_star


def B_safe(r, rs, **kw):
    """Radial-Metrik-Koeffizient: B(r) = 1/A(r)"""
    A, _ = A_safe(r, rs, **kw)
    return 1.0 / A


def D_from_A(A):
    """Zeitdilatation aus Metrik-Koeffizient: D = sqrt(A)"""
    return np.sqrt(np.abs(A))


def redshift_from_A(A):
    """Gravitationsrotverschiebung: z = 1/D - 1"""
    D = D_from_A(A)
    return 1.0 / np.maximum(D, 1e-15) - 1.0


def curvature_proxy(r, A):
    """Einfacher dimensionsloser Krümmungs-Proxy.
    
    K ~ (A'/r)² + ((1-A)/r²)²
    
    Nicht exakt Kretschmann, aber qualitativ korrekt.
    """
    r = np.asarray(r, float)
    dr = r[1] - r[0]
    dA = np.gradient(A, dr)
    return (dA / np.maximum(r, 1e-12))**2 + ((1.0 - A) / np.maximum(r*r, 1e-12))**2
