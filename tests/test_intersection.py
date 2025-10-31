"""
Test intersection point r* where SSZ and GR metrics match.

Acceptance criteria from prompt:
- |u* - 1.38656| < 2e-3
- 0.50 < D* < 0.56
"""
import pytest
import numpy as np
from viz_ssz_metric.ssz_mirror_metric import (
    find_intersection_highprec,
    compute_proper_time_dilation,
    D_SSZ,
    D_GR
)

# Fixtures
@pytest.fixture
def phi_golden():
    """Golden ratio φ"""
    return (1 + np.sqrt(5)) / 2

@pytest.fixture
def phi_unity():
    """Unity value for comparison"""
    return 1.0

class TestIntersectionPhi1:
    """Tests for φ = 1.0 case"""
    
    def test_u_star_value_phi1(self, phi_unity):
        """Test that u* is close to expected value for φ=1.0"""
        u_star, D_star = find_intersection_highprec(phi_unity)
        
        # Reference: u* ≈ 1.468971 for φ=1.0
        expected = 1.468971
        tolerance = 2e-3  # From prompt
        
        assert abs(u_star - expected) < tolerance, \
            f"u* = {u_star:.6f}, expected ≈ {expected}, diff = {abs(u_star - expected):.6f}"
    
    def test_D_star_range_phi1(self, phi_unity):
        """Test that D* is in valid range for φ=1.0"""
        u_star, D_star = find_intersection_highprec(phi_unity)
        
        assert 0.50 < D_star < 0.56, \
            f"D* = {D_star:.6f} not in range [0.50, 0.56]"
    
    def test_intersection_equality_phi1(self, phi_unity):
        """Test that SSZ and GR agree at r*"""
        u_star, D_star = find_intersection_highprec(phi_unity)
        
        # At intersection, D_SSZ should equal D_GR
        D_ssz = D_SSZ(u_star, phi_unity)
        D_gr = D_GR(u_star)
        
        rel_diff = abs(D_ssz - D_gr) / D_gr
        assert rel_diff < 1e-5, \
            f"D_SSZ({u_star}) = {D_ssz:.8f}, D_GR = {D_gr:.8f}, rel_diff = {rel_diff:.2e}"

class TestIntersectionPhiGolden:
    """Tests for φ = golden ratio case"""
    
    def test_u_star_value_golden(self, phi_golden):
        """Test that u* is close to 1.38656 for φ=φ"""
        u_star, D_star = find_intersection_highprec(phi_golden)
        
        # Reference: u* ≈ 1.38656 for φ=φ
        expected = 1.38656
        tolerance = 2e-3  # From prompt
        
        assert abs(u_star - expected) < tolerance, \
            f"u* = {u_star:.6f}, expected ≈ {expected}, diff = {abs(u_star - expected):.6f}"
    
    def test_D_star_range_golden(self, phi_golden):
        """Test that D* is in valid range for φ=φ"""
        u_star, D_star = find_intersection_highprec(phi_golden)
        
        assert 0.50 < D_star < 0.56, \
            f"D* = {D_star:.6f} not in range [0.50, 0.56]"
    
    def test_intersection_equality_golden(self, phi_golden):
        """Test that SSZ and GR agree at r* for golden ratio"""
        u_star, D_star = find_intersection_highprec(phi_golden)
        
        D_ssz = D_SSZ(u_star, phi_golden)
        D_gr = D_GR(u_star)
        
        rel_diff = abs(D_ssz - D_gr) / D_gr
        assert rel_diff < 1e-5, \
            f"D_SSZ({u_star}) = {D_ssz:.8f}, D_GR = {D_gr:.8f}, rel_diff = {rel_diff:.2e}"

class TestPhiVariations:
    """Test intersection behavior for various φ values"""
    
    @pytest.mark.parametrize("phi_value", [1.0, 1.2, 1.4, 1.618, 1.8, 2.0])
    def test_phi_range(self, phi_value):
        """Test that intersection exists for φ ∈ [1.0, 2.0]"""
        try:
            u_star, D_star = find_intersection_highprec(phi_value)
            
            # Sanity checks
            assert u_star > 1.0, f"u* = {u_star} should be > 1.0"
            assert u_star < 3.0, f"u* = {u_star} should be < 3.0"
            assert D_star > 0.0, f"D* = {D_star} should be positive"
            assert D_star < 1.0, f"D* = {D_star} should be < 1.0"
            
        except Exception as e:
            pytest.fail(f"Intersection failed for φ = {phi_value}: {e}")
    
    def test_phi_monotonicity(self):
        """Test that u* decreases as φ increases"""
        phi_values = [1.0, 1.3, 1.618, 1.9]
        u_stars = []
        
        for phi in phi_values:
            u_star, _ = find_intersection_highprec(phi)
            u_stars.append(u_star)
        
        # u* should be monotonically decreasing
        for i in range(len(u_stars) - 1):
            assert u_stars[i] > u_stars[i+1], \
                f"u*({phi_values[i]}) = {u_stars[i]} should be > u*({phi_values[i+1]}) = {u_stars[i+1]}"

class TestRobustness:
    """Test numerical robustness of intersection finder"""
    
    def test_no_nan_inf(self, phi_golden):
        """Ensure no NaN or Inf in results"""
        u_star, D_star = find_intersection_highprec(phi_golden)
        
        assert np.isfinite(u_star), f"u* is not finite: {u_star}"
        assert np.isfinite(D_star), f"D* is not finite: {D_star}"
        assert not np.isnan(u_star), "u* is NaN"
        assert not np.isnan(D_star), "D* is NaN"
    
    def test_deterministic(self, phi_golden):
        """Test that result is deterministic (same every time)"""
        results = [find_intersection_highprec(phi_golden) for _ in range(5)]
        
        u_stars = [r[0] for r in results]
        D_stars = [r[1] for r in results]
        
        # All should be identical
        assert all(abs(u - u_stars[0]) < 1e-10 for u in u_stars), \
            f"u* not deterministic: {u_stars}"
        assert all(abs(D - D_stars[0]) < 1e-10 for D in D_stars), \
            f"D* not deterministic: {D_stars}"
