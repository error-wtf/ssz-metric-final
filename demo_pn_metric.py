#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Post-Newtonsche SSZ-Metrik

Zeigt die Verwendung der vollständigen metrischen Funktionen und
des 4×4 Tensors für verschiedene Radien.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import os
import sys
import math

# UTF-8 encoding für Windows
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        import io
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

from viz_ssz_metric import (
    schwarzschild_radius,
    weak_field_parameter,
    metric_functions_pn,
    metric_tensor,
    proper_time_dilation,
    intersection_time_dilation,
)

def demo_table(mass: float, r_min: float, r_max: float, num: int = 8) -> None:
    """Tabellen-Output der Post-Newtonschen Metrik-Koeffizienten."""
    rs = schwarzschild_radius(mass)
    
    print("\n" + "="*80)
    print("POST-NEWTONSCHE SSZ-METRIK: A(r) = 1 - 2U + 2U² + ε₃U³")
    print("="*80)
    print(f"Masse: {mass:.3e} kg")
    print(f"r_s = {rs/1000:.3f} km")
    print(f"ε₃ = -24/5 = {-24/5:.6f}")
    print("-"*80)
    print(f"{'r/r_s':>8} {'U(r)':>12} {'A(r)':>14} {'B(r)':>14} {'D_PN(r)':>14} {'D_GR(r)':>14}")
    print("-"*80)
    
    for i in range(num):
        r = r_min + (r_max - r_min) * i / (num - 1)
        U = weak_field_parameter(mass, r)
        A, B = metric_functions_pn(mass, r)
        D_pn = proper_time_dilation(mass, r)
        D_gr = math.sqrt(max(0.0, 1.0 - rs / r))
        
        print(f"{r/rs:8.4f} {U:12.6e} {A:14.10f} {B:14.10f} {D_pn:14.10f} {D_gr:14.10f}")
    
    print("="*80)


def demo_tensor() -> None:
    """Demonstriere vollständigen 4×4 metrischen Tensor."""
    M_sun = 1.98847e30  # 1 Sonnenmasse
    rs = schwarzschild_radius(M_sun)
    r = 5 * rs
    theta = math.pi / 4  # 45°
    
    g = metric_tensor(M_sun, r, theta)
    
    print("\n" + "="*80)
    print("VOLLSTÄNDIGER METRISCHER TENSOR g_μν")
    print("="*80)
    print(f"Linienelement: ds² = -A(r)dt² + B(r)dr² + r²dθ² + r²sin²θ dφ²")
    print(f"Position: r = {r/rs:.2f} r_s, θ = {theta:.4f} rad = {math.degrees(theta):.1f}°")
    print(f"Signatur: (-,+,+,+)")
    print("-"*80)
    print("4×4 Matrix (nur Diagonale, Off-diagonal = 0):")
    print()
    for i, label in enumerate(['t', 'r', 'θ', 'φ']):
        row_str = "  "
        for j in range(4):
            if i == j:
                row_str += f"{g[i][j]:14.6f}  "
            else:
                row_str += f"{0.0:14.6f}  "
        print(f"  {label}:  [{row_str}]")
    print()
    print(f"g_tt = {g[0][0]:.6f}  (< 0, Zeitkomponente)")
    print(f"g_rr = {g[1][1]:.6f}  (> 0, Radialkomponente)")
    print(f"g_θθ = {g[2][2]:.6f}  (= r²)")
    print(f"g_φφ = {g[3][3]:.6f}  (= r²sin²θ)")
    print("="*80)


def demo_intersection() -> None:
    """Zeige Schnittpunkt zwischen SSZ und GR."""
    print("\n" + "="*80)
    print("SCHNITTPUNKT SSZ ↔ GR (High-Precision mit mpmath)")
    print("="*80)
    
    for varphi in [1.0, (1 + math.sqrt(5)) / 2]:
        result = intersection_time_dilation(varphi)
        u_star = result['u']
        D_star = result['D']
        
        print(f"\nφ = {varphi:.10f}")
        print(f"  u* = r*/r_s = {u_star:.12f}")
        print(f"  D* = {D_star:.12f}")
        
        # Physikalische Distanz für verschiedene Massen
        M_sun = 1.98847e30
        rs_sun = schwarzschild_radius(M_sun)
        r_star_sun = u_star * rs_sun
        
        print(f"  Für 1 M☉:")
        print(f"    r_s = {rs_sun/1000:.3f} km")
        print(f"    r* = {r_star_sun/1000:.3f} km")
    
    print("="*80)


def main():
    """Hauptfunktion: Demonstriere alle Features."""
    # 1. Post-Newtonsche Serie für 1 Sonnenmasse
    M_sun = 1.98847e30  # kg
    rs_sun = schwarzschild_radius(M_sun)
    demo_table(M_sun, 1.2 * rs_sun, 10.0 * rs_sun, num=8)
    
    # 2. Vollständiger metrischer Tensor
    demo_tensor()
    
    # 3. Schnittpunkt SSZ ↔ GR
    demo_intersection()
    
    print("\n✅ Demo abgeschlossen!")
    print("Tipp: Für starke Felder (r ≈ r_s) verwende A_safe() statt metric_functions_pn().\n")


if __name__ == "__main__":
    main()
