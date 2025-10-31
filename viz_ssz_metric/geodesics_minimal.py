"""
Minimale Geodäten-Integration für SSZ-Metrik.

Simplified geodesic solver - nur Basis-Features für Fahrplan 1.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import numpy as np
from scipy.integrate import odeint
from typing import Tuple


class GeodesicSolverMinimal:
    """
    Simplified Geodesic Solver - nur Basis-Features.
    
    Fokus auf:
    - Radiale Geodäten (Freifall)
    - Orbit-Stabilität (ISCO)
    """
    
    def __init__(self, metric):
        """
        Initialize with SSZ metric.
        
        Args:
            metric: UnifiedSSZMetric instance
        """
        self.metric = metric
        self.c = metric.params.c
    
    def integrate_radial_infall(self, r0: float, v_r0: float, 
                                tau_max: float = 10.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Integriere radiale Geodäte (vereinfacht, theta=pi/2 fixiert).
        
        Löst vereinfachte Geodäten-Gleichung für radialen Freifall:
        
        d²r/dτ² ≈ -(c²/2B) × dA/dr
        
        Args:
            r0: Start radius [m]
            v_r0: Initial radial velocity [m/s]
            tau_max: Max proper time [s]
        
        Returns:
            (tau, r_trajectory)
        """
        def equations(y, tau):
            """ODE system: y = [r, v_r]"""
            r, v_r = y
            
            # Safety: stop near horizon
            if r < 1.01 * self.metric.r_s:
                return [0, 0]
            
            # Metric functions
            A = self.metric.metric_function_A(r)
            B = self.metric.metric_function_B(r)
            
            # Numerical derivative dA/dr
            dr = r * 1e-6
            A_plus = self.metric.metric_function_A(r + dr)
            dA_dr = (A_plus - A) / dr
            
            # Simplified acceleration (from Christoffel symbols)
            # a_r ≈ -(c²/2B) × dA/dr
            a_r = -(self.c**2 / (2 * B)) * dA_dr
            
            return [v_r, a_r]
        
        # Initial conditions
        y0 = [r0, v_r0]
        
        # Integration
        tau = np.linspace(0, tau_max, 100)
        solution = odeint(equations, y0, tau)
        
        r_trajectory = solution[:, 0]
        
        return tau, r_trajectory
    
    def test_orbit_stability(self, r_orbit: float) -> bool:
        """
        Test ob Kreisbahn bei r stabil ist.
        
        Vereinfachtes Kriterium: r > r_ISCO ≈ 3 r_s
        
        Args:
            r_orbit: Orbital radius [m]
        
        Returns:
            True wenn stabil
        """
        # Simplified criterion: r > 3 r_s (ISCO for Schwarzschild)
        # In reality, should check d²V_eff/dr² > 0
        return r_orbit > 3 * self.metric.r_s
    
    def escape_velocity(self, r: float) -> float:
        """
        Fluchtgeschwindigkeit bei Radius r.
        
        v_esc = c × sqrt(1 - A(r))
        
        Args:
            r: Radius [m]
        
        Returns:
            v_esc [m/s]
        """
        A = self.metric.metric_function_A(r)
        
        # v_esc = c × sqrt(1 - A)
        v_esc = self.c * np.sqrt(1 - A)
        
        return v_esc
    
    def circular_orbit_velocity(self, r: float) -> float:
        """
        Kreisbahn-Geschwindigkeit bei Radius r.
        
        Vereinfacht: v_circ ≈ sqrt(GM/r)
        
        Args:
            r: Radius [m]
        
        Returns:
            v_circ [m/s]
        """
        # Newtonian approximation (valid for r >> r_s)
        G = self.metric.params.G
        M = self.metric.params.mass
        
        v_circ = np.sqrt(G * M / r)
        
        return v_circ
    
    def orbital_energy(self, r: float, v_r: float, v_tangent: float) -> float:
        """
        Orbital energy per unit mass.
        
        E/m = -A(r) × c² + B(r) × v_r² + r² × v_tangent²
        
        Args:
            r: Radius [m]
            v_r: Radial velocity [m/s]
            v_tangent: Tangential velocity [m/s]
        
        Returns:
            E/m [J/kg]
        """
        A = self.metric.metric_function_A(r)
        B = self.metric.metric_function_B(r)
        
        E_per_mass = -A * self.c**2 + B * v_r**2 + r**2 * v_tangent**2
        
        return E_per_mass


def demo():
    """Demonstration der minimalen Geodäten."""
    from viz_ssz_metric.unified_metric import UnifiedSSZMetric
    
    M_SUN = 1.98847e30
    metric = UnifiedSSZMetric(mass=M_SUN)
    solver = GeodesicSolverMinimal(metric)
    
    print("\n" + "="*70)
    print("GEODESIC SOLVER MINIMAL - DEMONSTRATION")
    print("="*70)
    
    # Test 1: Radial infall
    print("\n[1] Radial Infall from 100 r_s")
    r0 = 100 * metric.r_s
    v_r0 = -1000  # m/s inward
    
    tau, r_traj = solver.integrate_radial_infall(r0, v_r0, tau_max=5.0)
    
    print(f"  Start: r = {r0/metric.r_s:.1f} r_s, v_r = {v_r0:.0f} m/s")
    print(f"  After 5s: r = {r_traj[-1]/metric.r_s:.1f} r_s")
    print(f"  Distance fallen: {(r0-r_traj[-1])/1000:.1f} km")
    
    # Test 2: Orbit stability
    print("\n[2] Orbit Stability Tests")
    test_radii = [2, 3, 5, 10]
    
    for r_mult in test_radii:
        r_test = r_mult * metric.r_s
        stable = solver.test_orbit_stability(r_test)
        status = "STABLE" if stable else "UNSTABLE"
        print(f"  r = {r_mult} r_s: {status}")
    
    # Test 3: Velocities
    print("\n[3] Velocities at 10 r_s")
    r_test = 10 * metric.r_s
    
    v_esc = solver.escape_velocity(r_test)
    v_circ = solver.circular_orbit_velocity(r_test)
    
    print(f"  Escape velocity:    {v_esc/1000:.1f} km/s")
    print(f"  Circular velocity:  {v_circ/1000:.1f} km/s")
    print(f"  Ratio v_esc/v_circ: {v_esc/v_circ:.3f}")
    
    print("\n" + "="*70)
    print("GEODESIC SOLVER MINIMAL - Demo complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo()
