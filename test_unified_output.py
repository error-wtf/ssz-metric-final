#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Unified Metric Output
"""
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

print("="*80)
print("UNIFIED SSZ METRIC - OUTPUT TEST")
print("="*80)

# Create metric
metric = UnifiedSSZMetric(mass=1.98847e30)  # 1 solar mass
print("\n[OK] Metric created successfully")
print(f"   Mass: {metric.params.mass:.3e} kg")
print(f"   r_s: {metric.r_s:.3f} m")
print(f"   r_phi: {metric.r_phi:.3f} m")

# Test at different radii
radii = [3.0, 5.0, 10.0, 20.0]

print("\n" + "="*80)
print("COMPUTE_ALL() TEST AT DIFFERENT RADII")
print("="*80)

for r_factor in radii:
    r = r_factor * metric.r_s
    print(f"\n--- r = {r_factor:.1f} r_s = {r:.3e} m ---")
    
    try:
        result = metric.compute_all(r)
        
        print(f"  A(r) = {result['A']:.6f}")
        print(f"  Xi(r) = {result['Xi']:.6e}")
        print(f"  D(r) = {result['proper_time_dilation']:.6f}")
        print(f"  K_kretschmann = {result['K_kretschmann']:.6e}")
        
        # Energy-Momentum Tensor
        T = result['T_energy_momentum']
        print(f"  rho = {T['rho']:.6e}")
        print(f"  p_r = {T['p_r']:.6e}")
        print(f"  p_t = {T['p_t']:.6e}")
        print(f"  Delta = {T['Delta']:.6e}")
        
        # Singularity Check
        sing = result['singularity_free']
        print(f"  Singularity-free? {sing['all_clear']}")
        
    except Exception as e:
        print(f"  [ERROR]: {e}")

print("\n" + "="*80)
print("UNIFIED METRIC TEST COMPLETE")
print("="*80)
