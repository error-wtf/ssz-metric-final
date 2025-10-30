# -*- coding: utf-8 -*-
"""
Tests für SSZ Mirror Metric

Validiert:
- Schnittpunkt r* bei φ = 1.0 und φ = φ (Golden Ratio)
- A_safe > 0 überall (keine Singularitäten)
- Fernfeld-Übereinstimmung mit GR (PPN-Limit)
- Krümmungs-Proxy ist endlich

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
import pytest
from viz_ssz_metric.ssz_mirror_metric import (
    A_GR, A_SSZ, A_safe, solve_r_star, curvature_proxy, PHI
)


def test_intersection_phi_1():
    """Test: Schnittpunkt bei φ = 1.0
    
    Referenzwerte aus SSZ-Theorie:
    - u* = r*/r_s ≈ 1.4689714056
    - D* ≈ 0.5650235
    """
    rs = 1.0
    varphi = 1.0
    
    # Berechne Schnittpunkt
    rstar = solve_r_star(rs, varphi)
    u_star = rstar / rs
    
    # Berechne D* aus A*
    A_val, _ = A_safe(np.array([rstar]), rs, varphi=varphi)
    D_star = float(np.sqrt(A_val)[0])
    
    print(f"\n✅ Test φ=1.0:")
    print(f"   u* = {u_star:.10f} (expected: 1.4689714056)")
    print(f"   D* = {D_star:.10f} (expected: 0.5650235)")
    
    # Assertions mit Toleranz
    assert abs(u_star - 1.4689714056) < 5e-4, f"u* = {u_star} weicht zu stark ab!"
    assert abs(D_star - 0.5650235) < 5e-4, f"D* = {D_star} weicht zu stark ab!"


def test_intersection_phi_golden():
    """Test: Schnittpunkt bei φ = Golden Ratio
    
    Referenzwerte aus SSZ-Theorie:
    - u* ≈ 1.3866 (±0.01)
    - D* ≈ 0.5280 (±0.02)
    """
    rs = 1.0
    varphi = PHI  # ≈ 1.618033988749...
    
    rstar = solve_r_star(rs, varphi)
    u_star = rstar / rs
    
    A_val, _ = A_safe(np.array([rstar]), rs, varphi=varphi)
    D_star = float(np.sqrt(A_val)[0])
    
    print(f"\n✅ Test φ={PHI:.10f}:")
    print(f"   u* = {u_star:.10f} (expected: ~1.3866)")
    print(f"   D* = {D_star:.10f} (expected: ~0.5280)")
    
    assert 1.36 < u_star < 1.41, f"u* = {u_star} außerhalb erwarteter Range!"
    assert 0.50 < D_star < 0.56, f"D* = {D_star} außerhalb erwarteter Range!"


def test_A_safe_positive_and_farfield():
    """Test: A_safe > 0 überall UND Fernfeld-Konvergenz zu GR"""
    rs = 1.0
    varphi = 1.0
    
    # 1. Test: A_safe > 0 im Nahfeld
    r_near = np.linspace(1.05*rs, 6.0*rs, 400)
    A, rstar = A_safe(r_near, rs, varphi=varphi)
    
    print(f"\n✅ Test A_safe Positivität:")
    print(f"   min(A) = {A.min():.10f} (must be > 0)")
    print(f"   r* = {rstar/rs:.6f} r_s")
    
    assert np.all(A > 0.0), "A_safe hat negative Werte! (Singularität)"
    
    # 2. Test: Fernfeld → GR
    r_far = np.linspace(10*rs, 100*rs, 10)
    A_mirror, _ = A_safe(r_far, rs, varphi=varphi)
    A_gr = A_GR(r_far, rs)
    
    # PPN-Limit Test (tolerant wegen Softplus-Floor)
    max_diff = np.max(np.abs(A_mirror - A_gr))
    print(f"   Fernfeld max|A_safe - A_GR| = {max_diff:.6e} (should be < 2e-4)")
    
    assert np.allclose(A_mirror, A_gr, rtol=0, atol=2e-4), \
        f"Fernfeld-Abweichung zu groß: {max_diff}"


def test_curvature_proxy_finite():
    """Test: Krümmungs-Proxy bleibt endlich (keine NaN/Inf)"""
    rs = 1.0
    varphi = PHI
    
    r = np.linspace(1.05*rs, 6.0*rs, 500)
    A, _ = A_safe(r, rs, varphi=varphi)
    K = curvature_proxy(r, A)
    
    print(f"\n✅ Test Curvature Proxy:")
    print(f"   max(K) = {K.max():.6e}")
    print(f"   min(K) = {K.min():.6e}")
    print(f"   NaN count = {np.sum(np.isnan(K))}")
    print(f"   Inf count = {np.sum(np.isinf(K))}")
    
    assert not np.any(np.isnan(K)), "Krümmungs-Proxy enthält NaN!"
    assert not np.any(np.isinf(K)), "Krümmungs-Proxy enthält Inf!"
    assert K.max() < 1e10, f"Krümmungs-Proxy zu groß: {K.max()}"


def test_mirror_blend_smoothness():
    """Test: Mirror-Blend ist glatt am Übergang r*"""
    rs = 1.0
    varphi = PHI
    
    rstar = solve_r_star(rs, varphi)
    
    # Sample um r* herum (±5% Breite)
    r = np.linspace(rstar * 0.95, rstar * 1.05, 200)
    A, _ = A_safe(r, rs, varphi=varphi)
    
    # Berechne numerische Ableitung
    dr = r[1] - r[0]
    dA = np.gradient(A, dr)
    d2A = np.gradient(dA, dr)
    
    print(f"\n✅ Test Mirror-Blend Glätte bei r*:")
    print(f"   max|dA/dr| = {np.max(np.abs(dA)):.6e}")
    print(f"   max|d²A/dr²| = {np.max(np.abs(d2A)):.6e}")
    
    # Glattheit: Ableitungen dürfen nicht springen
    assert np.max(np.abs(dA)) < 10, "Erste Ableitung zu steil!"
    assert np.max(np.abs(d2A)) < 100, "Zweite Ableitung zu steil!"


def test_SSZ_vs_GR_values_at_rstar():
    """Test: Am Schnittpunkt r* sind SSZ und GR tatsächlich gleich"""
    rs = 1.0
    varphi = PHI
    
    rstar = solve_r_star(rs, varphi)
    
    # SSZ-Wert
    A_ssz_val = A_SSZ(rstar, rs, varphi)
    D_ssz = np.sqrt(A_ssz_val)
    
    # GR-Wert
    A_gr_val = A_GR(rstar, rs)
    D_gr = np.sqrt(A_gr_val)
    
    print(f"\n✅ Test SSZ=GR bei r*={rstar/rs:.6f}:")
    print(f"   D_SSZ = {D_ssz:.10f}")
    print(f"   D_GR  = {D_gr:.10f}")
    print(f"   |Diff| = {abs(D_ssz - D_gr):.2e}")
    
    # Sie sollten identisch sein (bis auf numerische Fehler)
    assert abs(D_ssz - D_gr) < 1e-8, f"SSZ≠GR am Schnittpunkt! Diff={abs(D_ssz-D_gr)}"


if __name__ == "__main__":
    # Kann auch direkt ausgeführt werden
    print("="*80)
    print("SSZ MIRROR METRIC TESTS")
    print("="*80)
    
    test_intersection_phi_1()
    test_intersection_phi_golden()
    test_A_safe_positive_and_farfield()
    test_curvature_proxy_finite()
    test_mirror_blend_smoothness()
    test_SSZ_vs_GR_values_at_rstar()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED!")
    print("="*80)
