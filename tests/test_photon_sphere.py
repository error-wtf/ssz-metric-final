"""
Test Photon Sphere implementation.

Tests the photon_sphere_radius() method with SSZ corrections.
"""

import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

M_SUN = 1.98847e30


def test_photon_sphere_exists():
    """Check photon sphere radius is calculated."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    r_ph = metric.photon_sphere_radius()
    
    # Should be near 1.5 × r_s
    assert 1.4 * metric.r_s < r_ph < 1.6 * metric.r_s
    print(f"✓ Photon Sphere: {r_ph/metric.r_s:.3f} r_s")


def test_photon_sphere_above_schwarzschild():
    """Photon sphere must be outside Schwarzschild radius."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    r_ph = metric.photon_sphere_radius()
    
    assert r_ph > metric.r_s
    print(f"✓ r_ph ({r_ph/metric.r_s:.3f} r_s) > r_s ✓")


def test_photon_sphere_correction_small():
    """SSZ correction should be small."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    epsilon = metric.photon_sphere_correction()
    
    # SSZ correction < 10%
    assert abs(epsilon) < 0.1
    print(f"✓ SSZ correction: {epsilon:.2%}")


def test_photon_sphere_mass_scaling():
    """Photon sphere should scale linearly with mass."""
    m1 = UnifiedSSZMetric(mass=M_SUN)
    m2 = UnifiedSSZMetric(mass=10*M_SUN)
    
    r_ph1 = m1.photon_sphere_radius()
    r_ph2 = m2.photon_sphere_radius()
    
    ratio = r_ph2 / r_ph1
    
    # Should be ~10 (linear with mass)
    assert 9 < ratio < 11
    print(f"✓ Scaling: r_ph(10M) / r_ph(M) = {ratio:.2f} (expect ~10)")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PHOTON SPHERE TESTS")
    print("="*60 + "\n")
    
    test_photon_sphere_exists()
    test_photon_sphere_above_schwarzschild()
    test_photon_sphere_correction_small()
    test_photon_sphere_mass_scaling()
    
    print("\n✅ ALL PHOTON SPHERE TESTS PASSED!\n")
