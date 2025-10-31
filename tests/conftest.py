# -*- coding: utf-8 -*-
"""
pytest Configuration and Fixtures for SSZ Tests

Provides standard fixtures for all tests.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from viz_ssz_metric.unified_metric import UnifiedSSZMetric, UnifiedMetricParameters
    from viz_ssz_metric.scalar_action_theory import ScalarActionTheory, ScalarParams
    HAS_MODULES = True
except ImportError:
    HAS_MODULES = False


# Physical Constants
M_SUN = 1.98847e30  # kg
M_EARTH = 5.972e24  # kg
M_JUPITER = 1.898e27  # kg


@pytest.fixture
def solar_mass_metric():
    """
    Standard test fixture: Sonnenmasse.
    
    Returns:
        UnifiedSSZMetric instance with solar mass
    """
    if not HAS_MODULES:
        pytest.skip("unified_metric not available")
    
    return UnifiedSSZMetric(mass=M_SUN)


@pytest.fixture
def earth_mass_metric():
    """
    Test fixture: Erdmasse.
    
    Returns:
        UnifiedSSZMetric instance with Earth mass
    """
    if not HAS_MODULES:
        pytest.skip("unified_metric not available")
    
    return UnifiedSSZMetric(mass=M_EARTH)


@pytest.fixture
def jupiter_mass_metric():
    """
    Test fixture: Jupiter-Masse.
    
    Returns:
        UnifiedSSZMetric instance with Jupiter mass
    """
    if not HAS_MODULES:
        pytest.skip("unified_metric not available")
    
    return UnifiedSSZMetric(mass=M_JUPITER)


@pytest.fixture
def scalar_theory():
    """
    Standard scalar action theory.
    
    Returns:
        ScalarActionTheory instance with default parameters
    """
    if not HAS_MODULES:
        pytest.skip("scalar_action_theory not available")
    
    return ScalarActionTheory()


@pytest.fixture
def scalar_theory_custom():
    """
    Custom scalar action theory (for parameterized tests).
    
    Returns:
        Function that creates ScalarActionTheory with custom params
    """
    if not HAS_MODULES:
        pytest.skip("scalar_action_theory not available")
    
    def _create(Z0=1.0, alpha=0.1, beta=0.01, m_phi=0.1, lambda_=0.001):
        return ScalarActionTheory(
            ScalarParams(Z0=Z0, alpha=alpha, beta=beta, m_phi=m_phi, lambda_=lambda_)
        )
    return _create


@pytest.fixture
def r_values_solar(solar_mass_metric):
    """
    Standard r-values for solar mass tests.
    
    Returns:
        Array of r values from r_phi to 100*r_s
    """
    return np.logspace(
        np.log10(solar_mass_metric.r_phi),
        np.log10(100 * solar_mass_metric.r_s),
        100
    )


@pytest.fixture
def theta_values():
    """
    Standard theta values (polar angle).
    
    Returns:
        Array of theta from 0 to π
    """
    return np.linspace(0, np.pi, 50)


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "validation: marks tests as validation tests (require data)"
    )


# Helper functions for tests
def approx_equal(a, b, rel=1e-6, abs=1e-12):
    """
    Check if two values are approximately equal.
    
    Args:
        a, b: Values to compare
        rel: Relative tolerance
        abs: Absolute tolerance
    
    Returns:
        bool: True if approximately equal
    """
    return np.abs(a - b) <= max(rel * max(np.abs(a), np.abs(b)), abs)


def check_finite(value, name="value"):
    """
    Check if value is finite (not NaN or Inf).
    
    Args:
        value: Value to check
        name: Name for error message
    
    Raises:
        AssertionError: If value is not finite
    """
    if not np.isfinite(value):
        raise AssertionError(f"{name} is not finite: {value}")


def check_bounded(value, lower, upper, name="value"):
    """
    Check if value is within bounds.
    
    Args:
        value: Value to check
        lower: Lower bound
        upper: Upper bound
        name: Name for error message
    
    Raises:
        AssertionError: If value is out of bounds
    """
    if not (lower <= value <= upper):
        raise AssertionError(f"{name}={value} not in [{lower}, {upper}]")


# Export helper functions
__all__ = [
    'solar_mass_metric',
    'earth_mass_metric',
    'jupiter_mass_metric',
    'scalar_theory',
    'scalar_theory_custom',
    'r_values_solar',
    'theta_values',
    'approx_equal',
    'check_finite',
    'check_bounded',
    'M_SUN',
    'M_EARTH',
    'M_JUPITER'
]
