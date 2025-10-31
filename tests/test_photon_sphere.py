"""
Test Photon Sphere implementation.

Tests the photon_sphere_radius() method with SSZ corrections.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

M_SUN = 1.98847e30


def test_photon_sphere_exists():
    """Check photon sphere radius is calculated."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    r_ph = metric.photon_sphere_radius()
    
    # SSZ gives ~1.338 r_s (GR: 1.5 r_s)
    # Allow range for SSZ modification
    assert 1.2 * metric.r_s < r_ph < 1.5 * metric.r_s
    print(f"[OK] Photon Sphere: {r_ph/metric.r_s:.3f} r_s")


def test_photon_sphere_above_schwarzschild():
    """Photon sphere must be outside Schwarzschild radius."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    r_ph = metric.photon_sphere_radius()
    
    assert r_ph > metric.r_s
    print(f"[OK] r_ph ({r_ph/metric.r_s:.3f} r_s) > r_s [OK]")


def test_photon_sphere_correction_small():
    """SSZ correction should be measurable but not huge."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    epsilon = metric.photon_sphere_correction()
    
    # SSZ correction ~-10.8% (expected for SSZ near horizon)
    assert abs(epsilon) < 0.15  # Allow up to 15%
    print(f"[OK] SSZ correction: {epsilon:.2%}")


def test_photon_sphere_mass_scaling():
    """Photon sphere should scale linearly with mass."""
    m1 = UnifiedSSZMetric(mass=M_SUN)
    m2 = UnifiedSSZMetric(mass=10*M_SUN)
    
    r_ph1 = m1.photon_sphere_radius()
    r_ph2 = m2.photon_sphere_radius()
    
    ratio = r_ph2 / r_ph1
    
    # Should be ~10 (linear with mass)
    assert 9 < ratio < 11
    print(f"[OK] Scaling: r_ph(10M) / r_ph(M) = {ratio:.2f} (expect ~10)")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PHOTON SPHERE TESTS")
    print("="*60 + "\n")
    
    test_photon_sphere_exists()
    test_photon_sphere_above_schwarzschild()
    test_photon_sphere_correction_small()
    test_photon_sphere_mass_scaling()
    
    print("\n✅ ALL PHOTON SPHERE TESTS PASSED!\n")
