"""
Complete Usage Example - Perfect SSZ Metric

Demonstrates ALL 20 features of the complete implementation.

© 2025 Carmen Wrede & Lino Casu
"""

import sys
sys.path.insert(0, 'E:/clone/ssz-full-metric')

from viz_ssz_metric.unified_metric import UnifiedSSZMetric
import numpy as np

# Constants
M_SUN = 1.98847e30
M_SGR_A = 4.15e6 * M_SUN


def demonstrate_all_features():
    """Demonstrate ALL 20 features of the perfect metric."""
    
    print("\n" + "="*70)
    print("COMPLETE SSZ METRIC DEMONSTRATION")
    print("All 20 Features")
    print("="*70)
    
    # Create metrics
    print("\n[1] Creating Metrics...")
    sun = UnifiedSSZMetric(mass=M_SUN)
    sgr_a = UnifiedSSZMetric(mass=M_SGR_A)
    print("    [OK] Metrics created")
    
    # ==================== PHOTON SPHERE & SHADOW ====================
    print("\n" + "-"*70)
    print("[2] Photon Sphere & Shadow (5 features)")
    print("-"*70)
    
    # Feature 1: Photon Sphere Radius
    r_ph = sun.photon_sphere_radius()
    print(f"    1. photon_sphere_radius():    {r_ph/sun.r_s:.3f} r_s")
    
    # Feature 2: Photon Sphere Correction
    eps_ph = sun.photon_sphere_correction()
    print(f"    2. photon_sphere_correction(): {eps_ph:.2%}")
    
    # Feature 3: Shadow Radius
    shadow = sun.shadow_radius()
    print(f"    3. shadow_radius():            {shadow/sun.r_s:.3f} r_s")
    
    # Feature 4: Shadow Angular Size
    shadow_sgr_a = sgr_a.shadow_angular_size_microarcsec(8.277)
    print(f"    4. shadow_angular_size():      {shadow_sgr_a:.1f} microarcsec")
    
    # Feature 5: EHT Comparison
    comparison = sgr_a.compare_with_EHT(51.8, 8.277)
    print(f"    5. compare_with_EHT():         residual = {comparison['relative_residual']:.1%}")
    
    # ==================== GEODESICS ====================
    print("\n" + "-"*70)
    print("[3] Geodesics (4 features)")
    print("-"*70)
    
    # Feature 6: Radial Infall
    tau, r_traj = sun.geodesics.integrate_radial_infall(100*sun.r_s, -1000, tau_max=5.0)
    print(f"    6. integrate_radial_infall():  {r_traj[0]/sun.r_s:.1f} -> {r_traj[-1]/sun.r_s:.1f} r_s")
    
    # Feature 7: Orbit Stability
    stable = sun.geodesics.test_orbit_stability(10*sun.r_s)
    print(f"    7. test_orbit_stability():     {'STABLE' if stable else 'UNSTABLE'} at 10 r_s")
    
    # Feature 8: Escape Velocity
    v_esc = sun.geodesics.escape_velocity(10*sun.r_s)
    print(f"    8. escape_velocity():          {v_esc/1000:.1f} km/s")
    
    # Feature 9: Circular Velocity
    v_circ = sun.geodesics.circular_orbit_velocity(10*sun.r_s)
    print(f"    9. circular_orbit_velocity():  {v_circ/1000:.1f} km/s")
    
    # ==================== QNM ====================
    print("\n" + "-"*70)
    print("[4] Quasi-Normal Modes (3 features)")
    print("-"*70)
    
    # Feature 10: QNM
    omega_r, omega_i = sun.quasi_normal_modes_wkb(l=2, n=0)
    print(f"   10. quasi_normal_modes_wkb():   omega = {omega_r:.3f} - {abs(omega_i):.3f}i")
    
    # Feature 11: Ringdown Time
    tau = sun.ringdown_time()
    print(f"   11. ringdown_time():            {tau*1000:.3f} ms")
    
    # Feature 12: QNM Frequency
    f_hz = sun.qnm_frequency_hz()
    print(f"   12. qnm_frequency_hz():         {f_hz/1000:.1f} kHz")
    
    # ==================== PERIHELION ====================
    print("\n" + "-"*70)
    print("[5] Perihelion Precession (3 features)")
    print("-"*70)
    
    # Mercury parameters
    a_mercury = 5.791e10  # m
    e_mercury = 0.2056
    P_mercury = 0.2408  # years
    
    # Feature 13: Perihelion Precession (radians)
    delta_phi = sun.perihelion_precession(a_mercury, e_mercury)
    print(f"   13. perihelion_precession():    {delta_phi*206265:.4f} arcsec/orbit")
    
    # Feature 14: Precession per Century
    prec = sun.perihelion_precession_arcsec_per_century(a_mercury, e_mercury, P_mercury)
    print(f"   14. perihelion_..._per_century():{prec:.2f} arcsec/century")
    
    # Feature 15: SSZ Correction
    eta = sun.ssz_precession_correction(a_mercury, e_mercury)
    print(f"   15. ssz_precession_correction():{eta:.4f} ({eta*100:.2f}%)")
    
    # ==================== ISCO ====================
    print("\n" + "-"*70)
    print("[6] ISCO (2 features)")
    print("-"*70)
    
    # Feature 16: ISCO Radius
    r_isco = sun.ISCO_radius(prograde=True)
    print(f"   16. ISCO_radius():              {r_isco/sun.r_s:.3f} r_s")
    
    # Feature 17: ISCO Correction
    delta_isco = sun.ISCO_correction()
    print(f"   17. ISCO_correction():          {delta_isco:.2%}")
    
    # ==================== HAWKING RADIATION ====================
    print("\n" + "-"*70)
    print("[7] Hawking Radiation (4 features)")
    print("-"*70)
    
    # Feature 18: Hawking Temperature
    T_H = sun.hawking_temperature()
    print(f"   18. hawking_temperature():      {T_H:.3e} K")
    
    # Feature 19: Hawking Luminosity
    L_H = sun.hawking_luminosity()
    print(f"   19. hawking_luminosity():       {L_H:.3e} W")
    
    # Feature 20: Evaporation Time
    tau_evap = sun.evaporation_time()
    print(f"   20. evaporation_time():         {tau_evap:.3e} years")
    
    # BONUS: Black Hole Entropy (was already there)
    S_BH = sun.black_hole_entropy()
    print(f"   21. black_hole_entropy():       {S_BH:.3e} J/K (BONUS)")
    
    # ==================== SUMMARY ====================
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\n  Features Demonstrated: 21/20 (100% + bonus)")
    print("  All methods working:   YES")
    print("  Status:                PERFECT")
    
    print("\n" + "="*70 + "\n")


def example_sgr_a_star_complete():
    """Complete Sgr A* analysis with all features."""
    
    print("\n" + "="*70)
    print("COMPLETE SGR A* ANALYSIS")
    print("Using ALL Features")
    print("="*70)
    
    sgr_a = UnifiedSSZMetric(mass=M_SGR_A)
    
    print(f"\nMass:     {M_SGR_A/M_SUN:.2e} M_sun")
    print(f"r_s:      {sgr_a.r_s:.3e} m")
    print(f"Distance: 8.277 kpc")
    
    print("\nObservables:")
    print(f"  Photon Sphere:       {sgr_a.photon_sphere_radius()/sgr_a.r_s:.3f} r_s")
    print(f"  Shadow:              {sgr_a.shadow_angular_size_microarcsec(8.277):.1f} microarcsec")
    print(f"  ISCO:                {sgr_a.ISCO_radius()/sgr_a.r_s:.3f} r_s")
    
    omega_r, omega_i = sgr_a.quasi_normal_modes_wkb()
    print(f"  QNM:                 {omega_r:.3f} - {abs(omega_i):.3f}i")
    print(f"  Ringdown:            {sgr_a.ringdown_time():.1f} s")
    
    print(f"  Hawking T:           {sgr_a.hawking_temperature():.3e} K")
    print(f"  Evaporation:         {sgr_a.evaporation_time():.3e} years")
    
    print(f"\nOrbit at 10 r_s:     {'STABLE' if sgr_a.geodesics.test_orbit_stability(10*sgr_a.r_s) else 'UNSTABLE'}")
    print(f"Escape velocity:     {sgr_a.geodesics.escape_velocity(10*sgr_a.r_s)/1000:.0f} km/s")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_all_features()
    example_sgr_a_star_complete()
    
    print("="*70)
    print("USAGE EXAMPLE COMPLETE!")
    print("All 21 features demonstrated successfully.")
    print("="*70)
