# -*- coding: utf-8 -*-
"""
SSZ Full Metric - Vollständige singularitätenfreie Metrik für Segmented Spacetime

Enthält BEIDE Ansätze:
1. Post-Newtonsche Serie (analytisch, schwaches Feld)
2. Mirror-Blend (numerisch, starkes Feld)

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
__version__ = "2.0.0"
__authors__ = ["Carmen Wrede", "Lino Casu"]

from .ssz_mirror_metric import (
    # Konstanten
    PHI,
    G_DEFAULT,
    C_DEFAULT,
    
    # Basis-Funktionen
    schwarzschild_radius,
    Xi,
    D_SSZ,
    A_SSZ,
    A_GR,
    
    # Mirror-Blend (starkes Feld)
    solve_r_star,
    A_safe,
    B_safe,
    
    # Post-Newtonsche Serie (schwaches Feld)
    weak_field_parameter,
    metric_functions_pn,
    metric_tensor,
    proper_time_dilation,
    
    # Intersection Point
    intersection_time_dilation,
    
    # Utilities
    D_from_A,
    redshift_from_A,
    curvature_proxy,
)

__all__ = [
    # Konstanten
    "PHI",
    "G_DEFAULT",
    "C_DEFAULT",
    
    # Basis
    "schwarzschild_radius",
    "Xi",
    "D_SSZ",
    "A_SSZ",
    "A_GR",
    
    # Mirror-Blend
    "solve_r_star",
    "A_safe",
    "B_safe",
    
    # Post-Newtonsche Serie
    "weak_field_parameter",
    "metric_functions_pn",
    "metric_tensor",
    "proper_time_dilation",
    
    # Intersection
    "intersection_time_dilation",
    
    # Utilities
    "D_from_A",
    "redshift_from_A",
    "curvature_proxy",
]
