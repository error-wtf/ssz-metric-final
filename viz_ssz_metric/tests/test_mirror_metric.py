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


def test_post_newtonian_series():
    """Test: Post-Newtonsche Serie A(r) = 1 - 2U + 2U² + ε₃U³"""
    from viz_ssz_metric.ssz_mirror_metric import (
        weak_field_parameter, metric_functions_pn, schwarzschild_radius
    )
    
    # Sonnenmasse
    M_sun = 1.98847e30  # kg
    rs = schwarzschild_radius(M_sun)
    
    # Schwaches Feld: r = 10 r_s
    r = 10 * rs
    U = weak_field_parameter(M_sun, r)
    A, B = metric_functions_pn(M_sun, r)
    
    print(f"\n✅ Test Post-Newtonsche Serie bei r = 10r_s:")
    print(f"   U = {U:.6e}")
    print(f"   A(r) = {A:.10f}")
    print(f"   B(r) = {B:.10f}")
    print(f"   ε₃ = -24/5 = {-24/5:.6f}")
    
    # Erwartete Werte (analytisch)
    A_expected = 1.0 - 2*U + 2*U**2 + (-24/5)*U**3
    
    assert abs(A - A_expected) < 1e-12, f"A-Serie fehlerhaft! {A} ≠ {A_expected}"
    assert B == pytest.approx(1/A), "B ≠ 1/A!"
    
    # Fernfeld: A → 1
    r_far = 1000 * rs
    A_far, _ = metric_functions_pn(M_sun, r_far)
    assert A_far > 0.999, f"Fernfeld: A({r_far/rs:.0f}r_s) = {A_far} sollte ≈1 sein"


def test_metric_tensor_components():
    """Test: Vollständiger 4×4 metrischer Tensor"""
    from viz_ssz_metric.ssz_mirror_metric import metric_tensor, schwarzschild_radius
    import math
    
    M = 1.98847e30  # 1 M☉
    rs = schwarzschild_radius(M)
    r = 5 * rs
    theta = math.pi / 4  # 45°
    
    g = metric_tensor(M, r, theta)
    
    print(f"\n✅ Test Metrischer Tensor bei r=5r_s, θ=π/4:")
    print(f"   g_tt = {g[0][0]:.6f} (sollte < 0 sein)")
    print(f"   g_rr = {g[1][1]:.6f} (sollte > 0 sein)")
    print(f"   g_θθ = {g[2][2]:.6f} (= r²)")
    print(f"   g_φφ = {g[3][3]:.6f} (= r²sin²θ)")
    
    # Signatur-Check
    assert g[0][0] < 0, "g_tt sollte negativ sein (Signatur -,+,+,+)"
    assert g[1][1] > 0, "g_rr sollte positiv sein"
    assert g[2][2] > 0, "g_θθ sollte positiv sein"
    assert g[3][3] > 0, "g_φφ sollte positiv sein"
    
    # Winkelkomponenten
    assert g[2][2] == pytest.approx(r**2), "g_θθ ≠ r²"
    assert g[3][3] == pytest.approx(r**2 * math.sin(theta)**2, rel=1e-10), "g_φφ ≠ r²sin²θ"
    
    # Off-diagonal = 0
    for i in range(4):
        for j in range(4):
            if i != j:
                assert g[i][j] == 0.0, f"Off-diagonal g[{i}][{j}] ≠ 0"


def test_proper_time_vs_coordinate_time():
    """Test: Eigenzeit-Dilatation D(r) = √|g_tt|"""
    from viz_ssz_metric.ssz_mirror_metric import proper_time_dilation, schwarzschild_radius
    
    M = 1.98847e30
    rs = schwarzschild_radius(M)
    
    # Bei r = ∞: D = 1 (keine Dilatation)
    r_far = 100 * rs
    D_far = proper_time_dilation(M, r_far)
    
    # Bei r = 2r_s: D < 1 (starke Dilatation)
    r_near = 2 * rs
    D_near = proper_time_dilation(M, r_near)
    
    print(f"\n✅ Test Eigenzeit-Dilatation:")
    print(f"   D(100r_s) = {D_far:.10f} (sollte ≈1 sein)")
    print(f"   D(2r_s) = {D_near:.10f} (sollte < 1 sein)")
    
    assert D_far > 0.99, f"Fernfeld-Dilatation zu groß: {D_far}"
    assert D_near < D_far, "Zeitdilatation sollte bei kleinerem r stärker sein"
    assert 0 < D_near < 1, f"D_near außerhalb physikalischem Bereich: {D_near}"


def test_intersection_high_precision():
    """Test: High-precision Schnittpunkt mit mpmath"""
    from viz_ssz_metric.ssz_mirror_metric import intersection_time_dilation, HAS_MPMATH
    
    if not HAS_MPMATH:
        print("\n⚠️  mpmath nicht verfügbar, überspringe high-precision Test")
        return
    
    # φ = 1.0
    result_1 = intersection_time_dilation(varphi=1.0)
    u1, D1 = result_1['u'], result_1['D']
    
    # φ = Golden Ratio
    result_phi = intersection_time_dilation(varphi=(1+5**0.5)/2)
    u_phi, D_phi = result_phi['u'], result_phi['D']
    
    print(f"\n✅ Test Intersection (mpmath high-precision):")
    print(f"   φ=1.0:  u* = {u1:.12f}, D* = {D1:.12f}")
    print(f"   φ=φ:    u* = {u_phi:.12f}, D* = {D_phi:.12f}")
    
    # Referenzwerte (aus Theorie)
    assert abs(u1 - 1.4689714056) < 1e-8, f"u*(φ=1.0) = {u1} weicht ab!"
    assert abs(D1 - 0.5650235) < 1e-6, f"D*(φ=1.0) = {D1} weicht ab!"
    
    assert 1.38 < u_phi < 1.40, f"u*(φ=φ) = {u_phi} außerhalb erwarteter Range"
    assert 0.52 < D_phi < 0.54, f"D*(φ=φ) = {D_phi} außerhalb erwarteter Range"


if __name__ == "__main__":
    # Kann auch direkt ausgeführt werden
    print("="*80)
    print("SSZ FULL METRIC TESTS (Mirror-Blend + Post-Newtonsche Serie)")
    print("="*80)
    
    # Original Mirror-Blend Tests
    test_intersection_phi_1()
    test_intersection_phi_golden()
    test_A_safe_positive_and_farfield()
    test_curvature_proxy_finite()
    test_mirror_blend_smoothness()
    test_SSZ_vs_GR_values_at_rstar()
    
    # Neue Post-Newtonsche Tests
    test_post_newtonian_series()
    test_metric_tensor_components()
    test_proper_time_vs_coordinate_time()
    test_intersection_high_precision()
    
    print("\n" + "="*80)
    print("✅ ALL 10 TESTS PASSED!")
    print("="*80)
