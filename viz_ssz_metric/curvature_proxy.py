# -*- coding: utf-8 -*-
"""
Curvature Proxy for SSZ Metric

Provides a simplified curvature measure without full tensor calculations.
Formula from Windsurf prompt: K_proxy = (A'/r)² + ((1-A)/r²)²

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import numpy as np
from typing import Union


def K_proxy(r: Union[float, np.ndarray], metric) -> Union[float, np.ndarray]:
    """
    Calculate curvature proxy from metric function A(r).
    
    Formula: K_proxy = (A'/r)² + ((1-A)/r²)²
    
    This provides a quick estimate of spacetime curvature without computing
    the full Kretschmann scalar K = R_μνρσ R^μνρσ.
    
    Args:
        r: Radial coordinate (can be scalar or array)
        metric: UnifiedSSZMetric instance
    
    Returns:
        K_proxy value(s)
    """
    # Ensure array for consistent handling
    is_scalar = np.isscalar(r)
    r_arr = np.atleast_1d(r)
    
    # Get A(r)
    A_vals = np.array([metric.metric_function_A(r_val) for r_val in r_arr])
    
    # Numerical derivative A'(r)
    dr = r_arr * 1e-7  # Relative step
    A_plus = np.array([metric.metric_function_A(r_val + dr_val) 
                       for r_val, dr_val in zip(r_arr, dr)])
    A_minus = np.array([metric.metric_function_A(r_val - dr_val) 
                        for r_val, dr_val in zip(r_arr, dr)])
    A_prime = (A_plus - A_minus) / (2 * dr)
    
    # K_proxy formula
    term1 = (A_prime / r_arr)**2
    term2 = ((1.0 - A_vals) / r_arr**2)**2
    
    K = term1 + term2
    
    # Return scalar if input was scalar
    if is_scalar:
        return K[0]
    return K


def K_kretschmann_full(r: float, metric) -> float:
    """
    Full Kretschmann scalar for comparison.
    
    Uses the full tensor calculation from kretschmann_weyl module.
    
    Args:
        r: Radial coordinate
        metric: UnifiedSSZMetric instance
    
    Returns:
        K = R_μνρσ R^μνρσ
    """
    # Delegate to full calculation
    return metric.kretschmann_scalar(r, theta=np.pi/2)


def compare_proxy_vs_full(r_values: np.ndarray, metric) -> dict:
    """
    Compare proxy vs full Kretschmann scalar.
    
    Args:
        r_values: Array of radial values
        metric: UnifiedSSZMetric instance
    
    Returns:
        Dictionary with proxy, full, and relative difference
    """
    K_proxy_vals = K_proxy(r_values, metric)
    K_full_vals = np.array([K_kretschmann_full(r, metric) for r in r_values])
    
    # Relative difference
    rel_diff = np.abs(K_proxy_vals - K_full_vals) / (K_full_vals + 1e-30)
    
    return {
        'r': r_values,
        'K_proxy': K_proxy_vals,
        'K_full': K_full_vals,
        'relative_difference': rel_diff,
        'max_rel_diff': np.max(rel_diff),
        'mean_rel_diff': np.mean(rel_diff)
    }


def demo():
    """Demonstrate curvature proxy calculation."""
    from .unified_metric import UnifiedSSZMetric
    import matplotlib.pyplot as plt
    
    M_sun = 1.98847e30
    metric = UnifiedSSZMetric(mass=M_sun)
    
    # Test points
    r_vals = np.linspace(1.1 * metric.r_s, 20 * metric.r_s, 100)
    
    print("\n" + "="*80)
    print("CURVATURE PROXY vs FULL KRETSCHMANN")
    print("="*80)
    
    comparison = compare_proxy_vs_full(r_vals, metric)
    
    print(f"\nStatistics:")
    print(f"  Max relative difference: {comparison['max_rel_diff']:.2%}")
    print(f"  Mean relative difference: {comparison['mean_rel_diff']:.2%}")
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    
    # Curvature comparison
    ax1.semilogy(r_vals/metric.r_s, comparison['K_proxy'], 
                 label='K_proxy', lw=2)
    ax1.semilogy(r_vals/metric.r_s, comparison['K_full'], 
                 label='K_full (Kretschmann)', lw=2, ls='--', alpha=0.7)
    ax1.set(xlabel='r/r_s', ylabel='K', 
            title='Curvature Proxy vs Full Kretschmann')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Relative difference
    ax2.plot(r_vals/metric.r_s, comparison['relative_difference'] * 100, lw=2)
    ax2.set(xlabel='r/r_s', ylabel='Relative Difference (%)',
            title='Proxy Accuracy')
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print("="*80)


if __name__ == "__main__":
    demo()
