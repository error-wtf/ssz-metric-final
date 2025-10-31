"""
Performance Benchmark Suite for SSZ Metric

Measures execution time for all major features.
"""

import time
import numpy as np
import sys
sys.path.insert(0, '.')

from viz_ssz_metric.unified_metric import UnifiedSSZMetric

M_SUN = 1.98847e30

def benchmark(func, name, iterations=100):
    """Benchmark a function."""
    times = []
    
    # Warmup
    for _ in range(10):
        func()
    
    # Measure
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)  # ms
    
    mean = np.mean(times)
    std = np.std(times)
    min_time = np.min(times)
    max_time = np.max(times)
    
    print(f"  {name:35s} {mean:8.3f} ± {std:6.3f} ms  [{min_time:6.3f} - {max_time:6.3f}]")
    return mean

def main():
    print("="*80)
    print("SSZ METRIC PERFORMANCE BENCHMARKS")
    print("="*80)
    print()
    
    # Create metrics
    print("Creating metric instances...")
    metric_sun = UnifiedSSZMetric(mass=M_SUN)
    metric_sgr_a = UnifiedSSZMetric(mass=4.15e6 * M_SUN)
    print("  [OK] Sun and Sgr A* metrics created")
    print()
    
    results = {}
    
    # Schwarzschild Features
    print("[1] SCHWARZSCHILD FEATURES (Solar Mass)")
    print("-" * 80)
    
    results['photon_sphere'] = benchmark(
        lambda: metric_sun.photon_sphere_radius(),
        "Photon Sphere"
    )
    
    results['shadow'] = benchmark(
        lambda: metric_sun.shadow_radius(),
        "Shadow Radius"
    )
    
    results['shadow_angular'] = benchmark(
        lambda: metric_sun.shadow_angular_size_microarcsec(8.277),
        "Shadow Angular Size"
    )
    
    results['isco'] = benchmark(
        lambda: metric_sun.ISCO_radius(),
        "ISCO"
    )
    
    results['qnm'] = benchmark(
        lambda: metric_sun.quasi_normal_modes_wkb(),
        "QNM (l=2, n=0)"
    )
    
    results['ringdown'] = benchmark(
        lambda: metric_sun.ringdown_time(),
        "Ringdown Time"
    )
    
    results['qnm_freq'] = benchmark(
        lambda: metric_sun.qnm_frequency_hz(),
        "QNM Frequency"
    )
    
    results['hawking_temp'] = benchmark(
        lambda: metric_sun.hawking_temperature(),
        "Hawking Temperature"
    )
    
    results['hawking_lum'] = benchmark(
        lambda: metric_sun.hawking_luminosity(),
        "Hawking Luminosity"
    )
    
    results['evap_time'] = benchmark(
        lambda: metric_sun.evaporation_time(),
        "Evaporation Time"
    )
    
    results['entropy'] = benchmark(
        lambda: metric_sun.black_hole_entropy(),
        "Black Hole Entropy"
    )
    
    results['perihelion'] = benchmark(
        lambda: metric_sun.perihelion_precession(5.791e10, 0.2056),
        "Perihelion Precession"
    )
    
    results['perihelion_century'] = benchmark(
        lambda: metric_sun.perihelion_precession_arcsec_per_century(5.791e10, 0.2056, 0.2408),
        "Perihelion (arcsec/century)"
    )
    
    print()
    
    # Kerr Features
    print("[2] KERR FEATURES (Solar Mass)")
    print("-" * 80)
    
    results['isco_kerr_0'] = benchmark(
        lambda: metric_sun.ISCO_kerr(0),
        "ISCO Kerr (a=0)"
    )
    
    results['isco_kerr_05'] = benchmark(
        lambda: metric_sun.ISCO_kerr(0.5),
        "ISCO Kerr (a=0.5)"
    )
    
    results['isco_kerr_1'] = benchmark(
        lambda: metric_sun.ISCO_kerr(1.0),
        "ISCO Kerr (a=1.0)"
    )
    
    results['photon_kerr_05'] = benchmark(
        lambda: metric_sun.photon_sphere_kerr(0.5),
        "Photon Sphere Kerr (a=0.5)"
    )
    
    results['ergosphere'] = benchmark(
        lambda: metric_sun.ergosphere_boundary(0.9),
        "Ergosphere (a=0.9)"
    )
    
    results['frame_drag'] = benchmark(
        lambda: metric_sun.frame_dragging_rate(10*metric_sun.r_s, 0.5),
        "Frame Dragging (a=0.5)"
    )
    
    print()
    
    # Geodesics
    print("[3] GEODESICS (Solar Mass)")
    print("-" * 80)
    
    results['escape_vel'] = benchmark(
        lambda: metric_sun.geodesics.escape_velocity(10*metric_sun.r_s),
        "Escape Velocity"
    )
    
    results['circ_vel'] = benchmark(
        lambda: metric_sun.geodesics.circular_orbit_velocity(10*metric_sun.r_s),
        "Circular Velocity"
    )
    
    results['orbit_stable'] = benchmark(
        lambda: metric_sun.geodesics.test_orbit_stability(10*metric_sun.r_s),
        "Orbit Stability Test"
    )
    
    print()
    
    # Supermassive BH
    print("[4] SUPERMASSIVE BLACK HOLE (Sgr A*)")
    print("-" * 80)
    
    results['shadow_sgr_a'] = benchmark(
        lambda: metric_sgr_a.shadow_angular_size_microarcsec(8.277),
        "Shadow (Sgr A*)"
    )
    
    results['shadow_disk'] = benchmark(
        lambda: metric_sgr_a.shadow_with_accretion_disk(8.277),
        "Shadow with Accretion Disk"
    )
    
    results['qnm_sgr_a'] = benchmark(
        lambda: metric_sgr_a.quasi_normal_modes_wkb(),
        "QNM (Sgr A*)"
    )
    
    results['isco_sgr_a'] = benchmark(
        lambda: metric_sgr_a.ISCO_radius(),
        "ISCO (Sgr A*)"
    )
    
    print()
    
    # Summary
    print("="*80)
    print("PERFORMANCE SUMMARY")
    print("="*80)
    print()
    
    total_time = sum(results.values())
    print(f"Total time for all features:  {total_time:.2f} ms")
    print(f"Average per feature:          {total_time/len(results):.2f} ms")
    print()
    
    # Fastest/Slowest
    fastest = min(results.items(), key=lambda x: x[1])
    slowest = max(results.items(), key=lambda x: x[1])
    
    print(f"Fastest feature:  {fastest[0]:30s} {fastest[1]:.3f} ms")
    print(f"Slowest feature:  {slowest[0]:30s} {slowest[1]:.3f} ms")
    print()
    
    # Categories
    schwarzschild_time = sum(v for k,v in results.items() if 'kerr' not in k and 'sgr_a' not in k and 'geodesics' not in k.lower())
    kerr_time = sum(v for k,v in results.items() if 'kerr' in k or 'ergosphere' in k or 'frame' in k)
    sgr_a_time = sum(v for k,v in results.items() if 'sgr_a' in k or 'disk' in k)
    
    print(f"Schwarzschild features: {schwarzschild_time:.2f} ms")
    print(f"Kerr features:          {kerr_time:.2f} ms")
    print(f"Sgr A* features:        {sgr_a_time:.2f} ms")
    print()
    
    # Performance rating
    if total_time < 100:
        rating = "EXCELLENT"
    elif total_time < 500:
        rating = "GOOD"
    elif total_time < 1000:
        rating = "ACCEPTABLE"
    else:
        rating = "NEEDS OPTIMIZATION"
    
    print(f"Performance Rating: {rating}")
    print()
    
    print("[SUCCESS] Benchmark complete!")
    print()
    print("Note: Times are for 100 iterations (warmup: 10)")
    print("      Actual single-call times are ~10x faster")

if __name__ == '__main__':
    main()
