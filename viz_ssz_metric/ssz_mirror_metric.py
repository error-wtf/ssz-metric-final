# -*- coding: utf-8 -*-
"""
Vollständige SSZ-Metrik: Post-Newtonsche Serie + Mirror-Blend.

Dieses Modul implementiert ZWEI komplementäre Ansätze für die SSZ-Metrik:

1. **Post-Newtonsche Serie** (schwaches Feld, analytisch):
   A(r) = 1 - 2U + 2U² + ε₃U³ + ...
   wobei U = GM/(c²r) und ε₃ = -24/5

2. **Mirror-Blend** (starkes Feld, numerisch):
   Glatter Übergang SSZ ↔ GR am Schnittpunkt r* mit Softplus-Floor

Basierend auf der Segmented Spacetime Theorie von Carmen Wrede & Lino Casu.

Linienelement (sphärisch symmetrisch, statisch):
    ds² = -A(r)dt² + B(r)dr² + r²dθ² + r²sin²θ dφ²

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import math
from typing import Tuple, Optional
import numpy as np
from scipy.optimize import brentq

try:
    import mpmath as mp
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False

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


# ============================================================================
# POST-NEWTONSCHE SERIE (Analytische Lösung im schwachen Feld)
# ============================================================================

def weak_field_parameter(mass: float, r: float, G: float = G_DEFAULT, c: float = C_DEFAULT) -> float:
    """Dimensionsloser Schwachfeldparameter U(r) = GM/(c²r) = r_s/(2r).
    
    Args:
        mass: Masse in kg
        r: Radialer Koordinatenwert in m
        G: Gravitationskonstante (SI)
        c: Lichtgeschwindigkeit (SI)
    
    Returns:
        U(r) dimensionslos
    """
    return (G * mass) / (c * c * r)


def metric_functions_pn(mass: float, r: float, 
                        G: float = G_DEFAULT, 
                        c: float = C_DEFAULT,
                        epsilon3: float = -24.0/5.0) -> Tuple[float, float]:
    """Post-Newtonsche Serie A(r) und B(r) = 1/A(r).
    
    SSZ-Metrik (schwaches Feld):
        A(r) = 1 - 2U + 2U² + ε₃U³ + O(U⁴)
        B(r) = 1/A(r)
    
    mit U = GM/(c²r) und ε₃ = -24/5.
    
    Diese Serie trunciert bei O(U³). Für starke Felder (r ≈ r_s) sollte
    die Mirror-Blend-Funktion A_safe() verwendet werden.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        G: Gravitationskonstante
        c: Lichtgeschwindigkeit
        epsilon3: Kubischer Koeffizient (default: -24/5)
    
    Returns:
        Tuple (A(r), B(r))
    
    Raises:
        ValueError: wenn A(r) ≤ 0 (Metrik-Singularität)
    """
    U = weak_field_parameter(mass, r, G, c)
    
    # Post-Newtonsche Serie
    A = 1.0 - 2.0 * U + 2.0 * (U ** 2) + epsilon3 * (U ** 3)
    
    # Höhere Ordnungen können hier ergänzt werden:
    # A += epsilon4 * (U ** 4) + ...
    
    if A <= 0:
        raise ValueError(
            f"Metrik-Singularität: A(r) = {A:.3e} ≤ 0 bei r = {r:.3e} m. "
            f"Verwende A_safe() für starke Felder."
        )
    
    B = 1.0 / A
    return A, B


def metric_tensor(mass: float, r: float, theta: float,
                  G: float = G_DEFAULT, 
                  c: float = C_DEFAULT) -> Tuple[Tuple[float, float, float, float], ...]:
    """Vollständiger diagonaler metrischer Tensor g_μν(r,θ) im SSZ-Modell.
    
    Linienelement:
        ds² = -A(r)dt² + B(r)dr² + r²dθ² + r²sin²θ dφ²
    
    Signatur: (-,+,+,+)
    Koordinaten: (t, r, θ, φ)
    
    Args:
        mass: Masse in kg
        r: Radialer Koordinatenwert in m
        theta: Polwinkel θ in Radiant
        G: Gravitationskonstante
        c: Lichtgeschwindigkeit
    
    Returns:
        4×4 Matrix des metrischen Tensors als nested tuple:
        ((g_tt, 0, 0, 0),
         (0, g_rr, 0, 0),
         (0, 0, g_θθ, 0),
         (0, 0, 0, g_φφ))
    """
    A, B = metric_functions_pn(mass, r, G, c)
    
    # Diagonale Komponenten
    g_tt = -A
    g_rr = B
    g_thth = r ** 2
    g_phph = (r ** 2) * (math.sin(theta) ** 2)
    
    # 4×4 Tensor (Off-diagonal = 0 für sphärische Symmetrie)
    return (
        (g_tt, 0.0, 0.0, 0.0),
        (0.0, g_rr, 0.0, 0.0),
        (0.0, 0.0, g_thth, 0.0),
        (0.0, 0.0, 0.0, g_phph),
    )


def proper_time_dilation(mass: float, r: float,
                         G: float = G_DEFAULT,
                         c: float = C_DEFAULT) -> float:
    """Eigenzeit-Dilatation D(r) = √|g_tt| für stationäre Beobachter.
    
    Gibt an, wie viele Eigenzeit-Sekunden pro Koordinatenzeit-Sekunde
    für einen ruhenden Beobachter bei Radius r vergehen.
    
    Dies basiert auf der Post-Newtonschen A(r), NICHT auf der 
    vereinfachten 1/(1+Ξ)-Formel.
    
    Args:
        mass: Masse in kg
        r: Radius in m
        G: Gravitationskonstante
        c: Lichtgeschwindigkeit
    
    Returns:
        D(r) ∈ (0, 1] (1 = unendlich fern, →0 am Horizont)
    """
    A, _ = metric_functions_pn(mass, r, G, c)
    # g_tt = -A, daher |g_tt| = A (falls A > 0)
    return math.sqrt(abs(A))


# ============================================================================
# INTERSECTION POINT (high-precision mit mpmath)
# ============================================================================

def intersection_time_dilation(varphi: float = PHI, 
                               tol: float = 1e-12) -> dict:
    """Berechne Schnittpunkt u* und D* zwischen GR und SSZ (high precision).
    
    Löst: sqrt(1 - 1/u) = 1/(2 - exp(-φ·u))
    
    wobei u = r/r_s (dimensionslos).
    
    Args:
        varphi: φ-Parameter (default: Golden Ratio)
        tol: Relative Toleranz für Root-Finding (default: 1e-12)
    
    Returns:
        dict mit Keys:
            - 'u': Dimensionsloser Schnittpunkt u* = r*/r_s
            - 'D': Gemeinsame Zeitdilatation D* = D_GR(r*) = D_SSZ(r*)
    
    Beispiel:
        >>> result = intersection_time_dilation(varphi=1.0)
        >>> print(f"u* = {result['u']:.10f}, D* = {result['D']:.10f}")
        u* = 1.4689714056, D* = 0.5650234996
    
    Raises:
        RuntimeError: wenn keine Konvergenz erreicht wird
        ImportError: wenn mpmath nicht verfügbar (Fallback zu scipy)
    """
    if HAS_MPMATH:
        # High-precision mit mpmath
        def f(u):
            return mp.sqrt(1.0 - 1.0 / u) - 1.0 / (2.0 - mp.e ** (-varphi * u))
        
        # Versuche mehrere Startpunkte
        guesses = [1.2, 1.3, 1.4, 1.5, 2.0]
        root = None
        
        for guess in guesses:
            try:
                root = mp.findroot(f, guess)
                u = float(mp.re(root))
                if u > 1.0:
                    break
            except Exception:
                continue
        
        if root is None or u <= 1.0:
            raise RuntimeError(
                f"mpmath findroot failed for varphi={varphi}. "
                f"Try different initial guesses."
            )
        
        # Berechne D* bei u*
        D_val = math.sqrt(1.0 - 1.0 / u)
        
        return {"u": u, "D": D_val}
    
    else:
        # Fallback zu scipy (niedrigere Präzision)
        def equation(u):
            return math.sqrt(1.0 - 1.0 / u) - 1.0 / (2.0 - math.exp(-varphi * u))
        
        try:
            u = brentq(equation, 1.01, 3.0, xtol=tol)
            D_val = math.sqrt(1.0 - 1.0 / u)
            return {"u": u, "D": D_val}
        except ValueError as e:
            raise RuntimeError(
                f"scipy brentq failed for varphi={varphi}: {e}"
            )
