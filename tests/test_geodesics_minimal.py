"""
Test minimal geodesics implementation.

Tests the GeodesicSolverMinimal class.
"""

import sys
sys.path.insert(0, 'E:/clone/ssz-full-metric')

from viz_ssz_metric.unified_metric import UnifiedSSZMetric
import numpy as np

M_SUN = 1.98847e30


def test_radial_infall():
    """Test radial geodesic (infall)."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    assert metric.geodesics is not None, "Geodesics not initialized!"
    
    r0 = 100 * metric.r_s
    v_r0 = -1000  # m/s inward
    
    tau, r_traj = metric.geodesics.integrate_radial_infall(r0, v_r0, tau_max=5.0)
    
    # r should decrease
    assert r_traj[-1] < r_traj[0], "Radius should decrease during infall"
    
    print(f"[OK] Infall: {r0/metric.r_s:.1f} -> {r_traj[-1]/metric.r_s:.1f} r_s")


def test_orbit_stability():
    """Test orbit stability check."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    # Stable at r > 3 r_s
    stable = metric.geodesics.test_orbit_stability(10 * metric.r_s)
    assert stable, "Orbit at 10 r_s should be stable"
    
    print("[OK] Orbit at 10 r_s: STABLE")
    
    # Unstable at r < 3 r_s
    unstable = not metric.geodesics.test_orbit_stability(2 * metric.r_s)
    assert unstable, "Orbit at 2 r_s should be unstable"
    
    print("[OK] Orbit at 2 r_s: UNSTABLE")


def test_escape_velocity():
    """Test escape velocity calculation."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r_test = 10 * metric.r_s
    v_esc = metric.geodesics.escape_velocity(r_test)
    
    # Should be positive and less than c
    assert 0 < v_esc < metric.params.c
    
    print(f"[OK] Escape velocity at 10 r_s: {v_esc/1000:.1f} km/s")


def test_circular_velocity():
    """Test circular orbit velocity."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r_test = 10 * metric.r_s
    v_circ = metric.geodesics.circular_orbit_velocity(r_test)
    
    # Should be positive and less than c
    assert 0 < v_circ < metric.params.c
    
    # Should be less than escape velocity
    v_esc = metric.geodesics.escape_velocity(r_test)
    assert v_circ < v_esc, "Circular velocity should be less than escape velocity"
    
    print(f"[OK] Circular velocity at 10 r_s: {v_circ/1000:.1f} km/s")


def test_velocity_ratio():
    """Test that v_esc/v_circ ~ sqrt(2) (Newtonian limit)."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r_test = 100 * metric.r_s  # Far from horizon (Newtonian)
    
    v_esc = metric.geodesics.escape_velocity(r_test)
    v_circ = metric.geodesics.circular_orbit_velocity(r_test)
    
    ratio = v_esc / v_circ
    
    # Should be close to sqrt(2) ≈ 1.414
    assert 1.3 < ratio < 1.5, f"Ratio {ratio:.3f} not close to sqrt(2)"
    
    print(f"[OK] v_esc/v_circ = {ratio:.3f} (expect ~1.414)")


def test_orbital_energy():
    """Test orbital energy calculation."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r_test = 10 * metric.r_s
    v_circ = metric.geodesics.circular_orbit_velocity(r_test)
    
    # Circular orbit: v_r = 0, v_tangent = v_circ / r
    E = metric.geodesics.orbital_energy(r_test, v_r=0, v_tangent=v_circ/r_test)
    
    # Energy should be negative (bound orbit)
    assert E < 0, "Circular orbit should have negative energy"
    
    print(f"[OK] Orbital energy: {E:.3e} J/kg (negative = bound)")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("GEODESICS MINIMAL TESTS")
    print("="*70 + "\n")
    
    test_radial_infall()
    test_orbit_stability()
    test_escape_velocity()
    test_circular_velocity()
    test_velocity_ratio()
    test_orbital_energy()
    
    print("\n[PASS] ALL GEODESICS TESTS PASSED!\n")
