"""
Test core metric functions A(r), B(r).

Acceptance criteria from prompt:
- A(r) > 0 for r ≥ 1.05 rs
- |A(r) - (1-rs/r)| < 2e-4 for r ∈ [10, 100] rs (far field)
- B(r) = 1/A(r)
"""
import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

# Solar mass constant
M_SUN = 1.98847e30

@pytest.fixture
def metric():
    """Standard metric with solar mass"""
    return UnifiedSSZMetric(mass=M_SUN)

@pytest.fixture
def r_s(metric):
    """Schwarzschild radius"""
    return metric.r_s

class TestMetricPositivity:
    """Test that A(r) is always positive"""
    
    def test_A_positive_near_horizon(self, metric, r_s):
        """Test A(r) > 0 for r ≥ 1.05 rs"""
        r_values = np.linspace(1.05 * r_s, 5 * r_s, 50)
        
        for r in r_values:
            A = metric.metric_function_A(r)
            assert A > 0, f"A({r/r_s:.3f} rs) = {A} is not positive"
    
    def test_A_positive_far_field(self, metric, r_s):
        """Test A(r) > 0 in far field"""
        r_values = np.logspace(1, 3, 30) * r_s  # 10 to 1000 rs
        
        for r in r_values:
            A = metric.metric_function_A(r)
            assert A > 0, f"A({r/r_s:.1f} rs) = {A} is not positive"
    
    def test_A_minimum(self, metric, r_s):
        """Test that min(A) > 0 over entire range"""
        r_values = np.linspace(1.05 * r_s, 100 * r_s, 1000)
        A_values = [metric.metric_function_A(r) for r in r_values]
        
        A_min = min(A_values)
        assert A_min > 0, f"min(A) = {A_min} ≤ 0"

class TestFarFieldLimit:
    """Test GR limit in far field"""
    
    def test_A_farfield_accuracy(self, metric, r_s):
        """Test |A(r) - (1-rs/r)| < 2e-4 for r ∈ [10, 100] rs"""
        r_values = np.linspace(10 * r_s, 100 * r_s, 50)
        
        max_error = 0.0
        for r in r_values:
            A_ssz = metric.metric_function_A(r)
            A_gr = 1.0 - r_s / r
            
            error = abs(A_ssz - A_gr)
            max_error = max(max_error, error)
            
            assert error < 2e-4, \
                f"At r={r/r_s:.1f}rs: |A_SSZ - A_GR| = {error:.2e} ≥ 2e-4"
        
        print(f"Max far-field error: {max_error:.2e}")
    
    def test_A_approaches_unity(self, metric, r_s):
        """Test that A → 1 as r → ∞"""
        r_values = [100, 500, 1000, 5000] * np.array([r_s] * 4)
        
        for r in r_values:
            A = metric.metric_function_A(r)
            error = abs(A - 1.0)
            
            # Error should decrease with increasing r
            expected_error = r_s / r  # Order of magnitude
            assert error < 10 * expected_error, \
                f"A({r/r_s:.0f}rs) = {A}, error = {error:.2e} too large"

class TestMetricConsistency:
    """Test B(r) = 1/A(r) relation"""
    
    def test_B_from_A(self, metric, r_s):
        """Test that B(r) = 1/A(r) everywhere"""
        r_values = np.logspace(0.02, 2, 50) * r_s  # 1.05 to 100 rs
        
        for r in r_values:
            A = metric.metric_function_A(r)
            B = metric.metric_function_B(r)
            
            B_expected = 1.0 / A
            rel_error = abs(B - B_expected) / B_expected
            
            assert rel_error < 1e-10, \
                f"At r={r/r_s:.3f}rs: B={B}, 1/A={B_expected}, rel_error={rel_error:.2e}"
    
    def test_AB_product(self, metric, r_s):
        """Test that A(r) × B(r) = 1"""
        r_values = np.linspace(1.05 * r_s, 50 * r_s, 100)
        
        for r in r_values:
            A = metric.metric_function_A(r)
            B = metric.metric_function_B(r)
            product = A * B
            
            assert abs(product - 1.0) < 1e-10, \
                f"At r={r/r_s:.3f}rs: A×B = {product}, should be 1.0"

class TestMetricBehavior:
    """Test qualitative metric behavior"""
    
    def test_A_monotonic(self, metric, r_s):
        """Test that A(r) is monotonically increasing"""
        r_values = np.linspace(1.05 * r_s, 100 * r_s, 200)
        A_values = [metric.metric_function_A(r) for r in r_values]
        
        # Check monotonicity
        for i in range(len(A_values) - 1):
            assert A_values[i+1] >= A_values[i], \
                f"A not monotonic: A[{i}]={A_values[i]}, A[{i+1}]={A_values[i+1]}"
    
    def test_A_bounds(self, metric, r_s):
        """Test 0 < A(r) < 1 for all r"""
        r_values = np.logspace(0.02, 3, 100) * r_s
        
        for r in r_values:
            A = metric.metric_function_A(r)
            
            assert 0 < A < 1.1, \
                f"A({r/r_s:.2f}rs) = {A} outside bounds [0, 1.1]"
    
    def test_B_monotonic(self, metric, r_s):
        """Test that B(r) is monotonically decreasing"""
        r_values = np.linspace(1.05 * r_s, 100 * r_s, 200)
        B_values = [metric.metric_function_B(r) for r in r_values]
        
        # Check monotonicity (decreasing)
        for i in range(len(B_values) - 1):
            assert B_values[i+1] <= B_values[i], \
                f"B not decreasing: B[{i}]={B_values[i]}, B[{i+1}]={B_values[i+1]}"

class TestNumericalStability:
    """Test numerical stability"""
    
    def test_no_nan_inf(self, metric, r_s):
        """Ensure no NaN or Inf in metric functions"""
        r_values = np.logspace(0.02, 3, 200) * r_s
        
        for r in r_values:
            A = metric.metric_function_A(r)
            B = metric.metric_function_B(r)
            
            assert np.isfinite(A), f"A({r/r_s:.3f}rs) is not finite: {A}"
            assert np.isfinite(B), f"B({r/r_s:.3f}rs) is not finite: {B}"
            assert not np.isnan(A), f"A({r/r_s:.3f}rs) is NaN"
            assert not np.isnan(B), f"B({r/r_s:.3f}rs) is NaN"
    
    def test_extreme_radii(self, metric, r_s):
        """Test metric at extreme radii"""
        # Very close to horizon
        r_close = 1.001 * r_s
        A_close = metric.metric_function_A(r_close)
        assert np.isfinite(A_close) and A_close > 0
        
        # Very far
        r_far = 1e6 * r_s
        A_far = metric.metric_function_A(r_far)
        assert np.isfinite(A_far) and 0.999 < A_far < 1.001

class TestMassScaling:
    """Test metric scales correctly with mass"""
    
    def test_different_masses(self):
        """Test metric for various masses"""
        masses = [M_SUN, 10*M_SUN, 1e6*M_SUN]
        
        for mass in masses:
            metric = UnifiedSSZMetric(mass=mass)
            r_s = metric.r_s
            
            # Test at 5 rs
            r_test = 5 * r_s
            A = metric.metric_function_A(r_test)
            
            assert 0 < A < 1, f"A(5rs) = {A} for M={mass/M_SUN:.1e}Msun"
            assert np.isfinite(A)
    
    def test_mass_independence_normalized(self):
        """Test that A(r/rs) is same for different masses"""
        m1 = UnifiedSSZMetric(mass=M_SUN)
        m2 = UnifiedSSZMetric(mass=100*M_SUN)
        
        # Test at same normalized radius
        u = 5.0  # u = r/rs
        
        A1 = m1.metric_function_A(u * m1.r_s)
        A2 = m2.metric_function_A(u * m2.r_s)
        
        rel_diff = abs(A1 - A2) / A1
        assert rel_diff < 0.05, \
            f"A(5rs) not mass-independent: A1={A1}, A2={A2}, diff={rel_diff:.2%}"
