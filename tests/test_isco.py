"""Test ISCO implementation."""

import sys
sys.path.insert(0, 'E:/clone/ssz-full-metric')

from viz_ssz_metric.unified_metric import UnifiedSSZMetric
import numpy as np

M_SUN = 1.98847e30


def test_isco_prograde():
    """Test ISCO for prograde orbits."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r_isco = metric.ISCO_radius(prograde=True)
    
    # Should be near 3 r_s (Schwarzschild)
    assert 2.5 * metric.r_s < r_isco < 3.5 * metric.r_s
    
    print(f"[OK] ISCO (prograde): {r_isco/metric.r_s:.3f} r_s")


def test_isco_above_photon_sphere():
    """ISCO must be outside photon sphere."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r_isco = metric.ISCO_radius()
    r_ph = metric.photon_sphere_radius()
    
    assert r_isco > r_ph, "ISCO must be outside photon sphere"
    
    print(f"[OK] r_ISCO ({r_isco/metric.r_s:.3f} r_s) > r_ph ({r_ph/metric.r_s:.3f} r_s)")


def test_isco_correction():
    """SSZ correction should be reasonable."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    delta = metric.ISCO_correction(prograde=True)
    
    # Should be < 20%
    assert abs(delta) < 0.2, f"ISCO correction {delta:.2%} too large"
    
    print(f"[OK] SSZ ISCO correction: {delta:.2%}")


def test_isco_legacy_method():
    """Test that legacy method still works."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r_isco_legacy = metric.innermost_stable_circular_orbit()
    
    # Should be exactly 3 r_s (GR value)
    assert r_isco_legacy == 3.0 * metric.r_s
    
    print(f"[OK] Legacy ISCO: {r_isco_legacy/metric.r_s:.3f} r_s (GR)")


def test_isco_mass_scaling():
    """ISCO should scale linearly with mass."""
    m1 = UnifiedSSZMetric(mass=M_SUN)
    m2 = UnifiedSSZMetric(mass=10*M_SUN)
    
    r1 = m1.ISCO_radius()
    r2 = m2.ISCO_radius()
    
    ratio = r2 / r1
    
    # Should be ~10 (linear with mass)
    assert 9 < ratio < 11, f"Scaling {ratio:.1f} not ~10"
    
    print(f"[OK] Scaling: r_ISCO(10M) / r_ISCO(M) = {ratio:.2f}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ISCO TESTS")
    print("="*70 + "\n")
    
    test_isco_prograde()
    test_isco_above_photon_sphere()
    test_isco_correction()
    test_isco_legacy_method()
    test_isco_mass_scaling()
    
    print("\n[PASS] ALL ISCO TESTS PASSED!\n")
