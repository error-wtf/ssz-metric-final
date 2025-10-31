# -*- coding: utf-8 -*-
"""
Tests for Scalar Action Theory

Tests the scientific correctness of the action-based formulation.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import pytest
import numpy as np
from conftest import scalar_theory, scalar_theory_custom, check_finite, check_bounded


def test_Z_parallel_at_zero(scalar_theory):
    """
    Test: Z_parallel(0) = Z0.
    
    At phi=0, the kinetic function should equal Z0.
    """
    result = scalar_theory.Z_parallel(0.0)
    
    assert result == pytest.approx(1.0, rel=1e-10)
    check_finite(result, "Z_parallel(0)")


def test_Z_parallel_positive(scalar_theory):
    """
    Test: Z_parallel(phi) > 0 for all phi.
    
    Kinetic function must be positive definite.
    """
    phi_values = np.linspace(-5, 5, 100)
    
    for phi in phi_values:
        Z = scalar_theory.Z_parallel(phi)
        assert Z > 0, f"Z_parallel({phi}) = {Z} is not positive!"
        check_finite(Z, f"Z_parallel({phi})")


def test_Z_parallel_bounded(scalar_theory):
    """
    Test: Z_parallel is bounded by Zmin and Zmax.
    
    The kinetic function has saturation bounds.
    """
    phi_values = np.linspace(-10, 10, 100)
    
    for phi in phi_values:
        Z = scalar_theory.Z_parallel(phi)
        check_bounded(Z, scalar_theory.params.Zmin, scalar_theory.params.Zmax, 
                     f"Z_parallel({phi})")


def test_U_potential_at_zero(scalar_theory):
    """
    Test: U(0) = 0.
    
    Potential should vanish at origin.
    """
    result = scalar_theory.U_potential(0.0)
    
    assert result == pytest.approx(0.0, abs=1e-15)
    check_finite(result, "U(0)")


def test_U_potential_positive_for_large_phi(scalar_theory):
    """
    Test: U(phi) > 0 for large |phi|.
    
    Potential should grow for large field values.
    """
    for phi in [5.0, -5.0, 10.0, -10.0]:
        U = scalar_theory.U_potential(phi)
        assert U > 0, f"U({phi}) = {U} is not positive!"
        check_finite(U, f"U({phi})")


def test_dZ_dphi_at_zero(scalar_theory):
    """
    Test: dZ/dphi at phi=0.
    
    Should match alpha parameter.
    """
    result = scalar_theory.dZ_dphi(0.0)
    
    expected = scalar_theory.params.Z0 * scalar_theory.params.alpha
    
    assert result == pytest.approx(expected, rel=1e-6)


def test_dU_dphi_at_zero(scalar_theory):
    """
    Test: dU/dphi at phi=0.
    
    Should vanish (U is even function near origin).
    """
    result = scalar_theory.dU_dphi(0.0)
    
    assert abs(result) < 1e-10


def test_stress_energy_tensor_shape(scalar_theory):
    """
    Test: stress_energy_tensor returns 4 values.
    
    Should return (rho, p_r, p_t, Delta).
    """
    phi, phi_prime, one_minus = 1.0, 0.1, 0.9
    
    result = scalar_theory.stress_energy_tensor(phi, phi_prime, one_minus)
    
    assert len(result) == 4
    rho, p_r, p_t, Delta = result
    
    # All should be finite
    check_finite(rho, "rho")
    check_finite(p_r, "p_r")
    check_finite(p_t, "p_t")
    check_finite(Delta, "Delta")


def test_anisotropy_formula(scalar_theory):
    """
    Test: Delta = p_t - p_r = -Z × X.
    
    CRITICAL: This is the fundamental anisotropy formula!
    """
    phi, phi_prime, one_minus = 1.0, 0.1, 0.9
    
    rho, p_r, p_t, Delta = scalar_theory.stress_energy_tensor(phi, phi_prime, one_minus)
    
    # Check Delta = p_t - p_r
    Delta_from_diff = p_t - p_r
    assert Delta == pytest.approx(Delta_from_diff, rel=1e-10)
    
    # Check Delta = -Z × X
    Z = scalar_theory.Z_parallel(phi)
    phi_p_sat = scalar_theory.sat_tanh(phi_prime, scalar_theory.params.phi_prime_cap)
    X = one_minus * phi_p_sat**2
    expected_Delta = -Z * X
    
    assert Delta == pytest.approx(expected_Delta, rel=0.01), \
        f"Delta={Delta} but expected={expected_Delta}"


def test_stress_energy_zero_field(scalar_theory):
    """
    Test: T_munu trivial wenn phi=0, phi'=0.
    
    Without scalar field, stress-energy should be ~zero.
    """
    phi, phi_prime, one_minus = 0.0, 0.0, 0.9
    
    rho, p_r, p_t, Delta = scalar_theory.stress_energy_tensor(phi, phi_prime, one_minus)
    
    # All should be approximately zero
    assert abs(rho) < 1e-10
    assert abs(p_r) < 1e-10
    assert abs(p_t) < 1e-10
    assert abs(Delta) < 1e-10


def test_stress_energy_bounds(scalar_theory):
    """
    Test: Stress-energy components are bounded.
    
    Physical bounds on rho, p_r, p_t.
    """
    phi, phi_prime, one_minus = 1.0, 0.1, 0.9
    
    rho, p_r, p_t, Delta = scalar_theory.stress_energy_tensor(phi, phi_prime, one_minus)
    
    # Energy density should be positive
    assert rho >= 0, f"rho={rho} is negative!"
    
    # All should be bounded (reasonable values)
    assert abs(rho) < 1e10
    assert abs(p_r) < 1e10
    assert abs(p_t) < 1e10
    assert abs(Delta) < 1e10


def test_scalar_eom_source(scalar_theory):
    """
    Test: Scalar equation of motion source term.
    
    Source = dU/dphi + (1/2) × (dZ/dphi) × X
    """
    phi, phi_prime, one_minus = 1.0, 0.1, 0.9
    
    source = scalar_theory.scalar_eom_source(phi, phi_prime, one_minus)
    
    # Should be finite
    check_finite(source, "EOM source")
    
    # Manual calculation
    dU = scalar_theory.dU_dphi(phi)
    dZ = scalar_theory.dZ_dphi(phi)
    phi_p_sat = scalar_theory.sat_tanh(phi_prime, scalar_theory.params.phi_prime_cap)
    X = one_minus * phi_p_sat**2
    expected_source = dU + 0.5 * dZ * X
    
    assert source == pytest.approx(expected_source, rel=1e-6)


@pytest.mark.parametrize("phi,phi_prime", [
    (0.0, 0.0),
    (0.5, 0.05),
    (1.0, 0.1),
    (2.0, 0.2),
    (-1.0, 0.1),
])
def test_stress_energy_various_values(scalar_theory, phi, phi_prime):
    """
    Test: Stress-energy for various phi, phi'.
    
    Should always produce finite, physically reasonable values.
    """
    one_minus = 0.9
    
    rho, p_r, p_t, Delta = scalar_theory.stress_energy_tensor(phi, phi_prime, one_minus)
    
    # All finite
    check_finite(rho, f"rho at phi={phi}, phi'={phi_prime}")
    check_finite(p_r, f"p_r at phi={phi}, phi'={phi_prime}")
    check_finite(p_t, f"p_t at phi={phi}, phi'={phi_prime}")
    check_finite(Delta, f"Delta at phi={phi}, phi'={phi_prime}")
    
    # Energy density non-negative
    assert rho >= 0


def test_numerical_stability_large_phi(scalar_theory):
    """
    Test: Numerische Stabilität bei großen phi.
    
    Saturation should prevent overflow.
    """
    phi_large = 100.0  # Very large field value
    phi_prime = 0.1
    one_minus = 0.9
    
    rho, p_r, p_t, Delta = scalar_theory.stress_energy_tensor(phi_large, phi_prime, one_minus)
    
    # Should still be finite (saturation works!)
    check_finite(rho, f"rho at phi={phi_large}")
    check_finite(p_r, f"p_r at phi={phi_large}")
    check_finite(p_t, f"p_t at phi={phi_large}")
    check_finite(Delta, f"Delta at phi={phi_large}")
    
    # Should be bounded
    assert abs(rho) < 1e10
    assert abs(Delta) < 1e10


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
