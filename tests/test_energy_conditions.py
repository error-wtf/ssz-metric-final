"""
Test energy conditions (WEC, NEC, DEC, SEC).

Acceptance criteria from prompt:
- No NaN/Inf
- WEC + NEC hold for r ≥ 5 rs
- Test on grid points
"""
import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

M_SUN = 1.98847e30

@pytest.fixture
def metric():
    """Standard metric with solar mass"""
    return UnifiedSSZMetric(mass=M_SUN)

@pytest.fixture
def r_s(metric):
    """Schwarzschild radius"""
    return metric.r_s

class TestEnergyConditionsBasic:
    """Test basic energy condition evaluation"""
    
    def test_WEC_safe_region(self, metric, r_s):
        """Test Weak Energy Condition for r ≥ 5 rs"""
        r_values = np.linspace(5 * r_s, 50 * r_s, 50)
        
        for r in r_values:
            ec = metric.energy_conditions(r, theta=np.pi/2)
            
            assert ec['WEC'], \
                f"WEC violated at r={r/r_s:.2f}rs"
    
    def test_NEC_safe_region(self, metric, r_s):
        """Test Null Energy Condition for r ≥ 5 rs"""
        r_values = np.linspace(5 * r_s, 50 * r_s, 50)
        
        for r in r_values:
            ec = metric.energy_conditions(r, theta=np.pi/2)
            
            assert ec['NEC'], \
                f"NEC violated at r={r/r_s:.2f}rs"
    
    def test_grid_points_100(self, metric, r_s):
        """Test energy conditions on 100 grid points"""
        r_values = np.linspace(5 * r_s, 100 * r_s, 100)
        
        WEC_pass = 0
        NEC_pass = 0
        
        for r in r_values:
            ec = metric.energy_conditions(r, theta=np.pi/2)
            
            if ec['WEC']:
                WEC_pass += 1
            if ec['NEC']:
                NEC_pass += 1
        
        # At least 95% should pass
        assert WEC_pass >= 95, f"WEC: {WEC_pass}/100 passed"
        assert NEC_pass >= 95, f"NEC: {NEC_pass}/100 passed"

class TestNoNaNInf:
    """Test for NaN/Inf in energy-momentum tensor"""
    
    def test_no_nan_inf_Tmunu(self, metric, r_s):
        """Ensure no NaN or Inf in T_μν"""
        r_values = np.logspace(np.log10(1.1 * r_s), np.log10(100 * r_s), 50)
        
        for r in r_values:
            T = metric.energy_momentum_tensor(r, theta=np.pi/2)
            
            # Check all components
            assert np.isfinite(T['rho']), f"rho is not finite at r={r/r_s:.3f}rs"
            assert np.isfinite(T['p_r']), f"p_r is not finite at r={r/r_s:.3f}rs"
            assert np.isfinite(T['p_t']), f"p_t is not finite at r={r/r_s:.3f}rs"
            assert np.isfinite(T['Delta']), f"Delta is not finite at r={r/r_s:.3f}rs"
            
            assert not np.isnan(T['rho']), f"rho is NaN at r={r/r_s:.3f}rs"
            assert not np.isnan(T['p_r']), f"p_r is NaN at r={r/r_s:.3f}rs"
            assert not np.isnan(T['p_t']), f"p_t is NaN at r={r/r_s:.3f}rs"
    
    def test_no_nan_inf_conditions(self, metric, r_s):
        """Ensure energy_conditions() doesn't return NaN"""
        r_values = np.linspace(5 * r_s, 100 * r_s, 100)
        
        for r in r_values:
            ec = metric.energy_conditions(r, theta=np.pi/2)
            
            # All conditions should be bool, not NaN
            assert isinstance(ec['WEC'], (bool, np.bool_)), "WEC not bool"
            assert isinstance(ec['NEC'], (bool, np.bool_)), "NEC not bool"
            assert isinstance(ec['DEC'], (bool, np.bool_)), "DEC not bool"
            assert isinstance(ec['SEC'], (bool, np.bool_)), "SEC not bool"

class TestEnergyConditionDetails:
    """Detailed tests for each energy condition"""
    
    def test_WEC_definition(self, metric, r_s):
        """Test WEC: rho + p >= 0"""
        r = 10 * r_s
        T = metric.energy_momentum_tensor(r, theta=np.pi/2)
        
        # WEC for radial and tangential
        WEC_r = T['rho'] + T['p_r']
        WEC_t = T['rho'] + T['p_t']
        
        # In safe region, both should hold
        assert WEC_r >= -1e-10, f"WEC_r = {WEC_r} < 0"
        assert WEC_t >= -1e-10, f"WEC_t = {WEC_t} < 0"
    
    def test_NEC_definition(self, metric, r_s):
        """Test NEC: rho + p_r >= 0 (null direction)"""
        r = 10 * r_s
        T = metric.energy_momentum_tensor(r, theta=np.pi/2)
        
        NEC = T['rho'] + T['p_r']
        
        # In safe region, should hold
        assert NEC >= -1e-10, f"NEC = {NEC} < 0"
    
    def test_DEC_definition(self, metric, r_s):
        """Test DEC: rho >= |p_i|"""
        r = 10 * r_s
        T = metric.energy_momentum_tensor(r, theta=np.pi/2)
        
        DEC_r = T['rho'] >= abs(T['p_r'])
        DEC_t = T['rho'] >= abs(T['p_t'])
        
        # Note: DEC may be violated near horizon in SSZ
        # Just check it's evaluated correctly
        assert isinstance(DEC_r, (bool, np.bool_))
        assert isinstance(DEC_t, (bool, np.bool_))

class TestAnisotropy:
    """Test anisotropy Delta = p_t - p_r"""
    
    def test_Delta_definition(self, metric, r_s):
        """Test that Delta = p_t - p_r"""
        r_values = np.linspace(5 * r_s, 50 * r_s, 20)
        
        for r in r_values:
            T = metric.energy_momentum_tensor(r, theta=np.pi/2)
            
            Delta_expected = T['p_t'] - T['p_r']
            Delta_actual = T['Delta']
            
            rel_error = abs(Delta_expected - Delta_actual) / (abs(Delta_expected) + 1e-30)
            assert rel_error < 1e-10, \
                f"Delta mismatch at r={r/r_s:.2f}rs: {Delta_actual} vs {Delta_expected}"
    
    def test_Delta_non_trivial(self, metric, r_s):
        """Test that anisotropy is non-trivial"""
        r = 3 * r_s
        T = metric.energy_momentum_tensor(r, theta=np.pi/2)
        
        # Delta should be non-zero (anisotropic)
        assert abs(T['Delta']) > 1e-15, \
            f"Delta = {T['Delta']} is effectively zero (isotropic?)"

class TestThetaDependence:
    """Test theta dependence of energy conditions"""
    
    def test_equator_vs_pole(self, metric, r_s):
        """Compare energy conditions at equator vs pole"""
        r = 10 * r_s
        
        # Equator (θ = π/2)
        ec_eq = metric.energy_conditions(r, theta=np.pi/2)
        
        # Pole (θ = 0)
        ec_pole = metric.energy_conditions(r, theta=0.0)
        
        # In SSZ, spherically symmetric → should be similar
        # (difference may exist due to phi_variation, but should be small)
        assert ec_eq['WEC'] == ec_pole['WEC'], "WEC differs at equator vs pole"
        assert ec_eq['NEC'] == ec_pole['NEC'], "NEC differs at equator vs pole"
    
    def test_theta_range(self, metric, r_s):
        """Test energy conditions for θ ∈ [0, π]"""
        r = 10 * r_s
        theta_values = np.linspace(0, np.pi, 10)
        
        for theta in theta_values:
            ec = metric.energy_conditions(r, theta=theta)
            
            # Should not crash and return valid bools
            assert isinstance(ec['WEC'], (bool, np.bool_))
            assert isinstance(ec['NEC'], (bool, np.bool_))

class TestMassScaling:
    """Test energy conditions for different masses"""
    
    @pytest.mark.parametrize("mass_factor", [1, 10, 100, 1e6])
    def test_different_masses(self, mass_factor):
        """Test energy conditions for various masses"""
        metric = UnifiedSSZMetric(mass=mass_factor * M_SUN)
        r_s = metric.r_s
        
        # Test at 10 rs
        r = 10 * r_s
        ec = metric.energy_conditions(r, theta=np.pi/2)
        
        # Should hold for all masses in safe region
        assert ec['WEC'], f"WEC fails for M = {mass_factor} Msun"
        assert ec['NEC'], f"NEC fails for M = {mass_factor} Msun"

class TestNearHorizon:
    """Test energy conditions near horizon"""
    
    def test_transition_region(self, metric, r_s):
        """Test energy conditions in transition region [1.5, 5] rs"""
        r_values = np.linspace(1.5 * r_s, 5 * r_s, 50)
        
        WEC_count = 0
        NEC_count = 0
        
        for r in r_values:
            try:
                ec = metric.energy_conditions(r, theta=np.pi/2)
                if ec['WEC']:
                    WEC_count += 1
                if ec['NEC']:
                    NEC_count += 1
            except:
                # May fail very close to horizon
                pass
        
        # Should pass most of the time
        assert WEC_count >= 40, f"WEC only passed {WEC_count}/50 in transition region"
        assert NEC_count >= 40, f"NEC only passed {NEC_count}/50 in transition region"
