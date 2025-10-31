"""
Test Shadow Radius implementation.

Tests shadow_radius() and EHT comparison methods.
"""

import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

M_SUN = 1.98847e30


def test_shadow_coordinate():
    """Test coordinate shadow radius."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    b_crit = metric.shadow_radius()
    
    # Should be ~ √27/2 × r_s ≈ 2.6 r_s
    b_expected = np.sqrt(27) / 2 * metric.r_s
    
    assert 0.8 * b_expected < b_crit < 1.2 * b_expected
    print(f"✓ Shadow radius: {b_crit/metric.r_s:.3f} r_s")


def test_shadow_angular():
    """Test angular shadow size."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    # At 10 kpc distance
    distance_kpc = 10.0
    shadow = metric.shadow_angular_size_microarcsec(distance_kpc)
    
    # Should be positive and reasonable
    assert shadow > 0
    assert shadow < 1000  # Less than 1 mas
    
    print(f"✓ Shadow at 10 kpc: {shadow:.2f} μas")


def test_shadow_sgr_a_star():
    """
    Sgr A* Shadow (EHT 2022).
    
    Observed: 51.8 ± 2.3 (stat) ± 6.9 (sys) μas
    Distance: 8.277 kpc
    Mass: 4.15 × 10^6 Msun
    """
    M_sgr_a = 4.15e6 * M_SUN
    distance_kpc = 8.277
    observed = 51.8  # μas
    
    metric = UnifiedSSZMetric(mass=M_sgr_a)
    
    comparison = metric.compare_with_EHT(
        observed_microarcsec=observed,
        distance_kpc=distance_kpc
    )
    
    print(f"\n✓ Sgr A* Shadow Comparison:")
    print(f"  Predicted: {comparison['predicted_microarcsec']:.1f} μas")
    print(f"  Observed:  {comparison['observed_microarcsec']:.1f} μas")
    print(f"  Residual:  {comparison['relative_residual']:.1%}")
    
    assert comparison['passes'], "Shadow nicht innerhalb 15% von EHT!"
    
    # Additional checks
    assert 40 < comparison['predicted_microarcsec'] < 65
    print(f"  ✓ Within EHT uncertainty range")


def test_shadow_mass_scaling():
    """Shadow should scale linearly with mass."""
    m1 = UnifiedSSZMetric(mass=M_SUN)
    m2 = UnifiedSSZMetric(mass=10*M_SUN)
    
    distance = 10.0  # kpc
    
    shadow1 = m1.shadow_angular_size_microarcsec(distance)
    shadow2 = m2.shadow_angular_size_microarcsec(distance)
    
    ratio = shadow2 / shadow1
    
    # Should be ~10 (linear with mass)
    assert 9 < ratio < 11
    print(f"✓ Shadow scaling: θ(10M) / θ(M) = {ratio:.2f} (expect ~10)")


def test_shadow_distance_scaling():
    """Shadow should scale as 1/distance."""
    metric = UnifiedSSZMetric(mass=4.15e6 * M_SUN)
    
    shadow_10kpc = metric.shadow_angular_size_microarcsec(10.0)
    shadow_20kpc = metric.shadow_angular_size_microarcsec(20.0)
    
    ratio = shadow_10kpc / shadow_20kpc
    
    # Should be ~2 (inverse with distance)
    assert 1.8 < ratio < 2.2
    print(f"✓ Distance scaling: θ(10kpc) / θ(20kpc) = {ratio:.2f} (expect ~2)")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SHADOW RADIUS TESTS")
    print("="*60 + "\n")
    
    test_shadow_coordinate()
    test_shadow_angular()
    test_shadow_sgr_a_star()
    test_shadow_mass_scaling()
    test_shadow_distance_scaling()
    
    print("\n✅ ALL SHADOW RADIUS TESTS PASSED!\n")
