"""Comprehensive validation suite for all observables."""

import sys
sys.path.insert(0, 'E:/clone/ssz-full-metric')

from viz_ssz_metric.unified_metric import UnifiedSSZMetric
import numpy as np

M_SUN = 1.98847e30


def test_all_methods_exist():
    """Check all observable methods exist."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    required_methods = [
        'photon_sphere_radius',
        'photon_sphere_correction',
        'shadow_radius',
        'shadow_angular_size_microarcsec',
        'compare_with_EHT',
        'quasi_normal_modes_wkb',
        'ringdown_time',
        'qnm_frequency_hz',
        'perihelion_precession',
        'perihelion_precession_arcsec_per_century',
        'ssz_precession_correction',
        'ISCO_radius',
        'ISCO_correction',
        'geodesics'
    ]
    
    missing = []
    for method in required_methods:
        if not hasattr(metric, method):
            missing.append(method)
    
    assert len(missing) == 0, f"Missing methods: {missing}"
    print(f"[OK] All {len(required_methods)} methods present")


def test_sgr_a_star_observables():
    """Test all observables for Sgr A*."""
    M_sgr_a = 4.15e6 * M_SUN
    metric = UnifiedSSZMetric(mass=M_sgr_a)
    
    print("\n" + "-"*60)
    print("Sgr A* Observables (M = 4.15e6 M_sun)")
    print("-"*60)
    
    # Photon Sphere
    r_ph = metric.photon_sphere_radius()
    print(f"  Photon Sphere:   {r_ph/metric.r_s:.3f} r_s")
    assert r_ph > metric.r_s
    
    # Shadow
    shadow = metric.shadow_angular_size_microarcsec(8.277)
    print(f"  Shadow:          {shadow:.1f} microarcsec")
    print(f"  (EHT observed:   51.8 +/- 7 microarcsec)")
    assert 10 < shadow < 100
    
    # QNM
    omega_r, omega_i = metric.quasi_normal_modes_wkb()
    f_hz = metric.qnm_frequency_hz()
    tau = metric.ringdown_time()
    print(f"  QNM:             omega = {omega_r:.3f} - {abs(omega_i):.3f}i")
    print(f"  Frequency:       {f_hz:.1f} Hz")
    print(f"  Ringdown time:   {tau:.3f} s")
    assert omega_r > 0 and omega_i < 0
    
    # ISCO
    r_isco = metric.ISCO_radius()
    print(f"  ISCO:            {r_isco/metric.r_s:.3f} r_s")
    assert 2.5 * metric.r_s < r_isco < 4 * metric.r_s
    
    print("[OK] All Sgr A* observables computed")


def test_solar_system_observables():
    """Test observables for Solar System (Sun + Mercury)."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    print("\n" + "-"*60)
    print("Solar System Observables")
    print("-"*60)
    
    # Mercury perihelion
    prec = metric.perihelion_precession_arcsec_per_century(
        5.791e10, 0.2056, 0.2408
    )
    print(f"  Mercury precession:  {prec:.2f} arcsec/century")
    print(f"  (Observed:           43.13 arcsec/century)")
    assert 40 < prec < 45
    
    # Solar QNM
    f_hz = metric.qnm_frequency_hz()
    tau = metric.ringdown_time()
    print(f"  QNM frequency:       {f_hz/1000:.1f} kHz")
    print(f"  Ringdown time:       {tau*1000:.3f} ms")
    assert f_hz > 1e3
    
    # ISCO
    r_isco = metric.ISCO_radius()
    print(f"  ISCO:                {r_isco/metric.r_s:.3f} r_s")
    
    print("[OK] All Solar System observables computed")


def test_geodesics_integration():
    """Test geodesics work with observables."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    print("\n" + "-"*60)
    print("Geodesics Integration Test")
    print("-"*60)
    
    # Check geodesics exist
    assert metric.geodesics is not None
    
    # ISCO stability
    r_isco = metric.ISCO_radius()
    stable_above = metric.geodesics.test_orbit_stability(r_isco * 1.1)
    unstable_below = not metric.geodesics.test_orbit_stability(r_isco * 0.9)
    
    print(f"  Orbit at 1.1 × ISCO:  {'STABLE' if stable_above else 'UNSTABLE'}")
    print(f"  Orbit at 0.9 × ISCO:  {'UNSTABLE' if unstable_below else 'STABLE'}")
    
    assert stable_above, "Orbit above ISCO should be stable"
    assert unstable_below, "Orbit below ISCO should be unstable"
    
    # Escape velocity
    v_esc = metric.geodesics.escape_velocity(10 * metric.r_s)
    print(f"  Escape velocity:      {v_esc/1000:.1f} km/s at 10 r_s")
    
    print("[OK] Geodesics integrated with observables")


def test_ssz_corrections_summary():
    """Summary of all SSZ corrections."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    print("\n" + "-"*60)
    print("SSZ Corrections Summary")
    print("-"*60)
    
    # Photon sphere
    eps_ph = metric.photon_sphere_correction()
    print(f"  Photon sphere:      {eps_ph:+.2%}")
    
    # ISCO
    eps_isco = metric.ISCO_correction()
    print(f"  ISCO:               {eps_isco:+.2%}")
    
    # Perihelion (Mercury)
    eps_prec = metric.ssz_precession_correction(5.791e10, 0.2056)
    print(f"  Perihelion:         {eps_prec:+.2%}")
    
    # QNM (indirect via A_ph/A_GR)
    r_ph = metric.photon_sphere_radius()
    A_ph_SSZ = metric.metric_function_A(r_ph)
    A_ph_GR = 1 - metric.r_s / r_ph if r_ph > metric.r_s else 0.333
    eps_qnm = (A_ph_SSZ - A_ph_GR) / A_ph_GR if A_ph_GR > 0 else 0
    print(f"  QNM (via A_ph):     {eps_qnm:+.2%}")
    
    print(f"\n  Average correction: {np.mean([abs(eps_ph), abs(eps_isco), abs(eps_prec)]):.2%}")
    print("[OK] SSZ corrections computed")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPREHENSIVE OBSERVABLES VALIDATION")
    print("="*70)
    
    test_all_methods_exist()
    test_sgr_a_star_observables()
    test_solar_system_observables()
    test_geodesics_integration()
    test_ssz_corrections_summary()
    
    print("\n" + "="*70)
    print("[PASS] ALL COMPREHENSIVE TESTS PASSED!")
    print("="*70 + "\n")
