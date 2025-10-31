"""Test Quasi-Normal Modes implementation."""

import sys
sys.path.insert(0, 'E:/clone/ssz-full-metric')

from viz_ssz_metric.unified_metric import UnifiedSSZMetric
import numpy as np

M_SUN = 1.98847e30


def test_qnm_positive():
    """QNM should have positive real, negative imaginary part."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    omega_r, omega_i = metric.quasi_normal_modes_wkb(l=2, n=0)
    
    assert omega_r > 0, "Real part should be positive"
    assert omega_i < 0, "Imaginary part should be negative (damping)"
    
    print(f"[OK] QNM: omega = {omega_r:.3f} - i*{abs(omega_i):.3f}")


def test_ringdown_time_physical():
    """Ringdown time should be physical."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    tau = metric.ringdown_time(l=2, n=0)
    
    # For M_sun: tau ~ 0.1 ms
    assert 1e-5 < tau < 1e-2, f"Ringdown time {tau:.2e}s unphysical"
    
    print(f"[OK] Ringdown time: {tau*1000:.3f} ms")


def test_qnm_frequency():
    """QNM frequency should be in kHz-MHz range for solar mass."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    f_hz = metric.qnm_frequency_hz(l=2, n=0)
    
    # For M_sun: f ~ 100 kHz - few MHz
    assert 1e3 < f_hz < 1e7, f"Frequency {f_hz:.2e} Hz unphysical"
    
    if f_hz > 1e6:
        print(f"[OK] QNM frequency: {f_hz/1e6:.2f} MHz")
    else:
        print(f"[OK] QNM frequency: {f_hz/1000:.1f} kHz")


def test_qnm_mass_scaling():
    """QNM should scale with mass: f ~ 1/M."""
    m1 = UnifiedSSZMetric(mass=M_SUN)
    m2 = UnifiedSSZMetric(mass=10*M_SUN)
    
    f1 = m1.qnm_frequency_hz()
    f2 = m2.qnm_frequency_hz()
    
    ratio = f1 / f2
    expected_ratio = 10  # f ~ 1/M
    
    assert 8 < ratio < 12, f"Scaling {ratio:.1f} not ~10"
    
    print(f"[OK] Scaling: f(M) / f(10M) = {ratio:.2f} (expect ~10)")


def test_qnm_overtones():
    """Higher overtones should have stronger damping."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    _, omega_i_0 = metric.quasi_normal_modes_wkb(l=2, n=0)
    _, omega_i_1 = metric.quasi_normal_modes_wkb(l=2, n=1)
    
    # n=1 should be more damped (more negative)
    assert omega_i_1 < omega_i_0, "Higher overtones should be more damped"
    
    print(f"[OK] Damping: n=0: {abs(omega_i_0):.3f}, n=1: {abs(omega_i_1):.3f}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("QNM TESTS")
    print("="*70 + "\n")
    
    test_qnm_positive()
    test_ringdown_time_physical()
    test_qnm_frequency()
    test_qnm_mass_scaling()
    test_qnm_overtones()
    
    print("\n[PASS] ALL QNM TESTS PASSED!\n")
