"""
Test Post-Newtonian parameters from PPNAnalysis.

Acceptance criteria from prompt:
- |γ - 1| < 1e-6
- |β - 1| < 1e-6

These tests verify that the SSZ metric reduces to GR in the weak-field limit
with correct PPN parameters.
"""
import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric
from viz_ssz_metric.ppn import PPNAnalysis

M_SUN = 1.98847e30

@pytest.fixture
def metric():
    """Standard metric with solar mass"""
    return UnifiedSSZMetric(mass=M_SUN)

@pytest.fixture
def ppn(metric):
    """PPN analysis instance"""
    return PPNAnalysis(metric)

class TestPPNParameters:
    """Test PPN parameter extraction"""
    
    def test_gamma_value(self, ppn):
        """Test that |γ - 1| < 1e-6"""
        gamma, _ = ppn.extract_gamma_beta()
        
        deviation = abs(gamma - 1.0)
        
        assert deviation < 1e-6, \
            f"|γ - 1| = {deviation:.2e} >= 1e-6"
    
    def test_beta_value(self, ppn):
        """Test that |β - 1| < 1e-6"""
        _, beta = ppn.extract_gamma_beta()
        
        deviation = abs(beta - 1.0)
        
        assert deviation < 1e-6, \
            f"|β - 1| = {deviation:.2e} >= 1e-6"
    
    def test_gamma_beta_together(self, ppn):
        """Test both parameters simultaneously"""
        gamma, beta = ppn.extract_gamma_beta()
        
        assert abs(gamma - 1.0) < 1e-6, f"γ = {gamma}"
        assert abs(beta - 1.0) < 1e-6, f"β = {beta}"
    
    def test_far_field_limit(self, ppn):
        """Test that γ, β → 1 in far field"""
        # Test at different distances
        test_radii = [50, 100, 500, 1000]
        
        for mult in test_radii:
            r_test = mult * ppn.metric.r_s
            gamma, beta = ppn.extract_gamma_beta(r_test)
            
            # Should approach 1.0 more closely at larger distances
            assert 0.99 < gamma < 1.01, f"γ = {gamma} at {mult}rs"
            assert 0.99 < beta < 1.01, f"β = {beta} at {mult}rs"

class TestIsotropicCoordinates:
    """Test isotropic coordinate transformations"""
    
    def test_roundtrip_conversion(self, ppn):
        """Test r_schw → r_iso → r_schw"""
        r_schw_orig = 10 * ppn.metric.r_s
        
        r_iso = ppn.iso_from_schw(r_schw_orig)
        r_schw_back = ppn.schw_from_iso(r_iso)
        
        rel_error = abs(r_schw_back - r_schw_orig) / r_schw_orig
        
        assert rel_error < 1e-6, \
            f"Roundtrip error: {rel_error:.2e}"
    
    def test_iso_smaller_than_schw(self, ppn):
        """Test that r_iso < r_schw (generally true)"""
        r_schw = 10 * ppn.metric.r_s
        r_iso = ppn.iso_from_schw(r_schw)
        
        # For r > rs, isotropic radius is smaller
        assert r_iso < r_schw, \
            f"r_iso = {r_iso}, r_schw = {r_schw}"
    
    def test_multiple_radii(self, ppn):
        """Test conversion for multiple radii"""
        test_radii = np.logspace(np.log10(2), np.log10(100), 20) * ppn.metric.r_s
        
        for r_schw in test_radii:
            r_iso = ppn.iso_from_schw(r_schw)
            
            assert r_iso > 0, f"r_iso = {r_iso} <= 0"
            assert np.isfinite(r_iso), f"r_iso not finite"

class TestLightDeflection:
    """Test light deflection calculations"""
    
    def test_sun_deflection(self, ppn):
        """Test light deflection at Sun's surface"""
        R_sun = 6.96e8  # m
        
        angle_rad = ppn.light_deflection_angle(R_sun)
        angle_arcsec = angle_rad * 206265
        
        # Einstein value: 1.75 arcsec
        # SSZ should be very close in weak field
        assert 1.70 < angle_arcsec < 1.80, \
            f"Deflection = {angle_arcsec:.3f} arcsec, expected ~1.75"
    
    def test_deflection_scales_inverse(self, ppn):
        """Test that deflection ∝ 1/b"""
        b1 = 1e9  # m
        b2 = 2e9  # m
        
        angle1 = ppn.light_deflection_angle(b1)
        angle2 = ppn.light_deflection_angle(b2)
        
        # angle1/angle2 should be ≈ b2/b1 = 2
        ratio = angle1 / angle2
        
        assert 1.9 < ratio < 2.1, \
            f"Scaling ratio = {ratio}, expected ~2.0"
    
    def test_positive_deflection(self, ppn):
        """Test that deflection is always positive"""
        test_b = [1e8, 1e9, 1e10, 1e11]
        
        for b in test_b:
            angle = ppn.light_deflection_angle(b)
            
            assert angle > 0, f"Angle = {angle} at b = {b}"
            assert np.isfinite(angle), "Angle not finite"

class TestPerihelionPrecession:
    """Test perihelion precession"""
    
    def test_mercury_precession(self, ppn):
        """Test Mercury perihelion precession"""
        a_mercury = 5.79e10  # m
        e_mercury = 0.206
        
        Delta_rad = ppn.perihelion_precession(a_mercury, e_mercury)
        Delta_arcsec = Delta_rad * 206265
        
        # Observed: ~0.1038 arcsec/orbit
        # 415 orbits/century → ~43 arcsec/century
        assert 0.08 < Delta_arcsec < 0.13, \
            f"Precession = {Delta_arcsec:.6f} arcsec/orbit"
    
    def test_circular_orbit_zero(self, ppn):
        """Test that circular orbit (e=0) still has precession"""
        a = 1e11  # m
        e = 0.0
        
        Delta = ppn.perihelion_precession(a, e)
        
        # Even circular orbit has frame-dragging precession
        assert Delta > 0, "Circular orbit should still precess"
    
    def test_precession_scales_inverse(self, ppn):
        """Test that precession ∝ 1/a"""
        a1 = 5e10
        a2 = 10e10
        e = 0.2
        
        Delta1 = ppn.perihelion_precession(a1, e)
        Delta2 = ppn.perihelion_precession(a2, e)
        
        # Delta1/Delta2 ≈ a2/a1 = 2
        ratio = Delta1 / Delta2
        
        assert 1.9 < ratio < 2.1, \
            f"Scaling ratio = {ratio}, expected ~2.0"

class TestShapiroDelay:
    """Test Shapiro time delay"""
    
    def test_positive_delay(self, ppn):
        """Test that delay is always positive"""
        r_closest = 1e9  # m
        
        delay = ppn.shapiro_delay(r_closest)
        
        assert delay > 0, f"Delay = {delay} <= 0"
        assert np.isfinite(delay), "Delay not finite"
    
    def test_delay_magnitude(self, ppn):
        """Test typical Shapiro delay magnitude"""
        R_sun = 6.96e8
        distance = 1.496e11  # 1 AU
        
        delay = ppn.shapiro_delay(R_sun, distance)
        
        # Should be microseconds for Solar System
        assert 1e-7 < delay < 1e-3, \
            f"Delay = {delay:.2e} s seems unrealistic"
    
    def test_delay_increases_with_mass(self):
        """Test that delay increases with mass"""
        m1 = UnifiedSSZMetric(mass=M_SUN)
        m2 = UnifiedSSZMetric(mass=10*M_SUN)
        
        ppn1 = PPNAnalysis(m1)
        ppn2 = PPNAnalysis(m2)
        
        r = 1e9
        delay1 = ppn1.shapiro_delay(r)
        delay2 = ppn2.shapiro_delay(r)
        
        # Delay ∝ M, so delay2 ≈ 10 × delay1
        ratio = delay2 / delay1
        
        assert 9 < ratio < 11, f"Mass scaling: {ratio:.2f}"

class TestGravitationalRedshift:
    """Test gravitational redshift"""
    
    def test_positive_redshift(self, ppn):
        """Test that redshift is positive (light loses energy)"""
        r_test = 10 * ppn.metric.r_s
        
        z = ppn.gravitational_redshift(r_test)
        
        assert z > 0, f"Redshift z = {z} <= 0"
    
    def test_redshift_decreases_with_r(self, ppn):
        """Test that z decreases with increasing r"""
        r1 = 5 * ppn.metric.r_s
        r2 = 10 * ppn.metric.r_s
        
        z1 = ppn.gravitational_redshift(r1)
        z2 = ppn.gravitational_redshift(r2)
        
        assert z1 > z2, f"z({r1}) = {z1} not > z({r2}) = {z2}"
    
    def test_weak_field_approximation(self, ppn):
        """Test z ≈ GM/(c²r) in weak field"""
        r_test = 100 * ppn.metric.r_s
        
        z_ssz = ppn.gravitational_redshift(r_test)
        z_newton = ppn.metric.r_s / (2 * r_test)
        
        rel_diff = abs(z_ssz - z_newton) / z_newton
        
        assert rel_diff < 0.01, \
            f"Weak field: z_ssz = {z_ssz:.2e}, z_N = {z_newton:.2e}"

class TestCoordinateSpeedOfLight:
    """Test coordinate speed of light"""
    
    def test_speed_less_than_c(self, ppn):
        """Test that coordinate speed <= c"""
        r_values = np.linspace(2*ppn.metric.r_s, 50*ppn.metric.r_s, 20)
        
        for r in r_values:
            c_coord = ppn.speed_of_light_coordinate(r)
            
            assert c_coord <= ppn.c * 1.01, \
                f"c_coord = {c_coord/ppn.c:.6f} c > c"
    
    def test_speed_approaches_c(self, ppn):
        """Test that c_coord → c as r → ∞"""
        r_far = 1000 * ppn.metric.r_s
        
        c_coord = ppn.speed_of_light_coordinate(r_far)
        
        rel_diff = abs(c_coord - ppn.c) / ppn.c
        
        assert rel_diff < 0.001, \
            f"c_coord/c - 1 = {rel_diff:.2e} at 1000 rs"

class TestSummary:
    """Test summary generation"""
    
    def test_summary_keys(self, ppn):
        """Test that summary has all expected keys"""
        summary = ppn.summary()
        
        expected_keys = [
            'gamma', 'beta',
            'gamma_deviation', 'beta_deviation',
            'light_deflection_sun_rad',
            'light_deflection_sun_arcsec',
            'perihelion_mercury_rad_per_orbit',
            'perihelion_mercury_arcsec_per_orbit',
            'shapiro_delay_1AU_seconds'
        ]
        
        for key in expected_keys:
            assert key in summary, f"Missing key: {key}"
    
    def test_summary_values_finite(self, ppn):
        """Test that all summary values are finite"""
        summary = ppn.summary()
        
        for key, value in summary.items():
            assert np.isfinite(value), \
                f"{key} = {value} is not finite"
    
    def test_acceptance_criteria_in_summary(self, ppn):
        """Test that summary shows acceptance criteria are met"""
        summary = ppn.summary()
        
        assert summary['gamma_deviation'] < 1e-6, \
            f"|γ-1| = {summary['gamma_deviation']:.2e} >= 1e-6"
        assert summary['beta_deviation'] < 1e-6, \
            f"|β-1| = {summary['beta_deviation']:.2e} >= 1e-6"

class TestMassScaling:
    """Test PPN parameters for different masses"""
    
    @pytest.mark.parametrize("mass_factor", [1, 10, 100])
    def test_gamma_beta_mass_independent(self, mass_factor):
        """Test that γ, β are independent of mass"""
        metric = UnifiedSSZMetric(mass=mass_factor * M_SUN)
        ppn = PPNAnalysis(metric)
        
        gamma, beta = ppn.extract_gamma_beta()
        
        # PPN parameters should be mass-independent
        assert abs(gamma - 1.0) < 1e-6
        assert abs(beta - 1.0) < 1e-6
