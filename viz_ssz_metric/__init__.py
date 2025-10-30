# -*- coding: utf-8 -*-
"""
SSZ Full Metric - Singularitätenfreie Metrik für Segmented Spacetime

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
__version__ = "1.0.0"
__authors__ = ["Carmen Wrede", "Lino Casu"]

from .ssz_mirror_metric import (
    PHI,
    schwarzschild_radius,
    Xi,
    D_SSZ,
    A_SSZ,
    A_GR,
    solve_r_star,
    A_safe,
    B_safe,
    D_from_A,
    redshift_from_A,
    curvature_proxy,
)

__all__ = [
    "PHI",
    "schwarzschild_radius",
    "Xi",
    "D_SSZ",
    "A_SSZ",
    "A_GR",
    "solve_r_star",
    "A_safe",
    "B_safe",
    "D_from_A",
    "redshift_from_A",
    "curvature_proxy",
]
