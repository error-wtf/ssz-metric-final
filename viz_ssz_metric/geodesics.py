# -*- coding: utf-8 -*-
"""
PHASE 31: Geodätengleichungen d²x^μ/dλ² + Γ^μ_νρ (dx^ν/dλ)(dx^ρ/dλ) = 0

Implementiert die fundamentalen Bewegungsgleichungen für:
- Zeitartige Geodäten (massive Teilchen)
- Nullgeodäten (Photonen)
- Numerische Integration (RK45)

Dies ist die Basis für alle Orbit-Simulationen!

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Callable, Tuple, List
from scipy.integrate import odeint, solve_ivp
from .christoffel_symbols import christoffel_nonzero
from .ssz_mirror_metric import schwarzschild_radius, metric_functions_pn


def geodesic_equations_rhs(state: np.ndarray, lambda_param: float, 
                           mass: float, particle_mass: float = 1.0) -> np.ndarray:
    """Rechte Seite der Geodätengleichungen für numerische Integration.
    
    State-Vektor: [t, r, theta, phi, dt/dλ, dr/dλ, dθ/dλ, dφ/dλ]
    
    Geodätengleichung:
    d²x^μ/dλ² = -Γ^μ_νρ (dx^ν/dλ)(dx^ρ/dλ)
    
    Args:
        state: Zustandsvektor [x, v] (Koordinaten + Geschwindigkeiten)
        lambda_param: Affiner Parameter λ
        mass: Zentral-Masse (kg)
        particle_mass: Teilchen-Masse (0 für Photonen)
    
    Returns:
        dstate/dλ (Ableitungen)
    """
    # Entpacke State
    t, r, theta, phi = state[0:4]
    v_t, v_r, v_theta, v_phi = state[4:8]
    
    # Christoffel-Symbole bei aktueller Position
    gamma = christoffel_nonzero(mass, r, theta)
    
    # Beschleunigungen aus Geodätengleichung
    # d²t/dλ² = -Γ^t_νρ v^ν v^ρ
    a_t = -(
        2 * gamma['Gamma^t_tr'] * v_t * v_r
    )
    
    # d²r/dλ² = -Γ^r_νρ v^ν v^ρ
    a_r = -(
        gamma['Gamma^r_tt'] * v_t * v_t +
        gamma['Gamma^r_rr'] * v_r * v_r +
        gamma['Gamma^r_thth'] * v_theta * v_theta +
        gamma['Gamma^r_phph'] * v_phi * v_phi
    )
    
    # d²θ/dλ² = -Γ^θ_νρ v^ν v^ρ
    a_theta = -(
        2 * gamma['Gamma^th_rth'] * v_r * v_theta +
        gamma['Gamma^th_phph'] * v_phi * v_phi
    )
    
    # d²φ/dλ² = -Γ^φ_νρ v^ν v^ρ
    a_phi = -(
        2 * gamma['Gamma^ph_rph'] * v_r * v_phi +
        2 * gamma['Gamma^ph_thph'] * v_theta * v_phi
    )
    
    # Rückgabe: [dx/dλ, dv/dλ]
    return np.array([
        v_t, v_r, v_theta, v_phi,  # Geschwindigkeiten
        a_t, a_r, a_theta, a_phi   # Beschleunigungen
    ])


def integrate_geodesic(mass: float, 
                      initial_state: np.ndarray,
                      lambda_span: Tuple[float, float],
                      num_points: int = 1000,
                      particle_mass: float = 1.0) -> dict:
    """Integriere Geodäte numerisch (Runge-Kutta 4/5).
    
    Args:
        mass: Zentral-Masse (kg)
        initial_state: [t0, r0, θ0, φ0, v_t0, v_r0, v_θ0, v_φ0]
        lambda_span: (λ_start, λ_end)
        num_points: Anzahl Output-Punkte
        particle_mass: Teilchen-Masse (0 für Licht)
    
    Returns:
        dict mit Keys: 'lambda', 't', 'r', 'theta', 'phi', 
                      'v_t', 'v_r', 'v_theta', 'v_phi'
    """
    # RHS-Funktion mit mass als Parameter
    def rhs(lambda_val, state):
        return geodesic_equations_rhs(state, lambda_val, mass, particle_mass)
    
    # Integration mit solve_ivp (adaptive RK45)
    solution = solve_ivp(
        rhs,
        lambda_span,
        initial_state,
        method='RK45',
        t_eval=np.linspace(lambda_span[0], lambda_span[1], num_points),
        rtol=1e-8,
        atol=1e-10
    )
    
    # Extrahiere Ergebnisse
    result = {
        'lambda': solution.t,
        't': solution.y[0],
        'r': solution.y[1],
        'theta': solution.y[2],
        'phi': solution.y[3],
        'v_t': solution.y[4],
        'v_r': solution.y[5],
        'v_theta': solution.y[6],
        'v_phi': solution.y[7],
        'success': solution.success,
        'message': solution.message
    }
    
    return result


def initial_conditions_circular_orbit(mass: float, r_orbit: float, 
                                      direction: int = 1) -> np.ndarray:
    """Anfangsbedingungen für kreisförmige Äquator-Bahn.
    
    Für kreisförmige Geodäte in SSZ-Metrik.
    
    Args:
        mass: Zentral-Masse (kg)
        r_orbit: Bahnradius (m)
        direction: +1 (prograd) oder -1 (retrograd)
    
    Returns:
        Initial state [t, r, θ, φ, v_t, v_r, v_θ, v_φ]
    """
    from .ssz_mirror_metric import G_DEFAULT
    
    # Kreisbahn-Geschwindigkeit (Newtonsch approximiert)
    v_circ = np.sqrt(G_DEFAULT * mass / r_orbit)
    
    # Winkelgeschwindigkeit
    omega = v_circ / r_orbit
    
    # Anfangsbedingungen (Äquator: θ = π/2)
    t0 = 0.0
    r0 = r_orbit
    theta0 = np.pi / 2
    phi0 = 0.0
    
    # 4-Geschwindigkeiten (zeitartig normalisiert)
    A, B = metric_functions_pn(mass, r0)
    v_t = 1.0 / np.sqrt(A)
    v_r = 0.0  # Kreisbahn
    v_theta = 0.0  # Äquator
    v_phi = direction * omega
    
    return np.array([t0, r0, theta0, phi0, v_t, v_r, v_theta, v_phi])


def check_geodesic_constraint(mass: float, state: np.ndarray, 
                              particle_mass: float = 1.0) -> float:
    """Prüfe Geodäten-Constraint g_μν (dx^μ/dλ)(dx^ν/dλ) = -ε².
    
    Für zeitartige Geodäten: ε² = 1 (massive Teilchen)
    Für nullartige Geodäten: ε² = 0 (Photonen)
    
    Args:
        mass: Zentral-Masse
        state: [t, r, θ, φ, v_t, v_r, v_θ, v_φ]
        particle_mass: Teilchen-Masse
    
    Returns:
        Constraint-Wert (sollte -1 für massive, 0 für masselose Teilchen sein)
    """
    import math
    
    r, theta = state[1], state[2]
    v_t, v_r, v_theta, v_phi = state[4:8]
    
    # Metrik
    A, B = metric_functions_pn(mass, r)
    g_tt = -A
    g_rr = B
    g_thth = r**2
    g_phph = (r**2) * (math.sin(theta)**2)
    
    # Constraint
    constraint = (g_tt * v_t**2 + 
                 g_rr * v_r**2 + 
                 g_thth * v_theta**2 + 
                 g_phph * v_phi**2)
    
    return constraint


def demo():
    """Demo: Geodäten-Integration für kreisförmige Bahn."""
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    M_sun = 1.98847e30
    rs = schwarzschild_radius(M_sun)
    
    # Kreisbahn bei r = 5 r_s
    r_orbit = 5 * rs
    
    # Anfangsbedingungen
    initial_state = initial_conditions_circular_orbit(M_sun, r_orbit, direction=1)
    
    # Integration für ~2 Umläufe
    from .ssz_mirror_metric import G_DEFAULT
    T_orbit = 2 * np.pi * np.sqrt(r_orbit**3 / (G_DEFAULT * M_sun))
    lambda_span = (0, 2.5 * T_orbit)
    
    print("\nIntegriere Geodäte...")
    result = integrate_geodesic(M_sun, initial_state, lambda_span, num_points=2000)
    
    if not result['success']:
        print(f"⚠️  Integration fehlgeschlagen: {result['message']}")
        return
    
    print(f"✅ Integration erfolgreich: {len(result['lambda'])} Punkte")
    
    # Konvertiere zu kartesischen Koordinaten
    r = result['r']
    theta = result['theta']
    phi = result['phi']
    
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    
    # Plot 3D-Bahn
    fig = plt.figure(figsize=(14, 6))
    
    # Left: 3D Trajectory
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(x/rs, y/rs, z/rs, lw=1.5, color='#1f77b4')
    ax1.scatter([0], [0], [0], color='orange', s=100, label='Zentral-Masse')
    ax1.set_xlabel('x/r_s')
    ax1.set_ylabel('y/r_s')
    ax1.set_zlabel('z/r_s')
    ax1.set_title('3D Geodäte (Kreisbahn @ 5r_s)')
    ax1.legend()
    ax1.set_box_aspect([1,1,1])
    
    # Right: r(λ) und Constraint-Check
    ax2 = fig.add_subplot(222)
    ax2.plot(result['lambda'] / T_orbit, result['r'] / rs, lw=2, color='#ff7f0e')
    ax2.set_xlabel('λ/T_orbit')
    ax2.set_ylabel('r/r_s')
    ax2.set_title('Radialkoordinate r(λ)')
    ax2.grid(alpha=0.3)
    
    ax3 = fig.add_subplot(224)
    # Constraint-Check
    constraints = [check_geodesic_constraint(M_sun, 
                                            np.array([result['t'][i], result['r'][i], 
                                                     result['theta'][i], result['phi'][i],
                                                     result['v_t'][i], result['v_r'][i],
                                                     result['v_theta'][i], result['v_phi'][i]]))
                  for i in range(0, len(result['lambda']), 10)]
    
    ax3.plot(np.arange(len(constraints)), constraints, lw=2, color='#2ca02c')
    ax3.axhline(-1, ls='--', color='red', label='Soll: -1 (zeitartig)')
    ax3.set_xlabel('Schritt')
    ax3.set_ylabel('g_μν v^μ v^ν')
    ax3.set_title('Geodäten-Constraint-Check')
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('viz_ssz_metric/out/geodesic_orbit.png', dpi=150)
    print("✅ Saved: viz_ssz_metric/out/geodesic_orbit.png")
    
    # Statistik
    print("\n" + "="*70)
    print("GEODÄTEN-INTEGRATION: ERGEBNISSE")
    print("="*70)
    print(f"Bahnradius:       {r_orbit/rs:.3f} r_s")
    print(f"Orbitperiode:     {T_orbit:.3f} s")
    print(f"Integration Zeit: {lambda_span[1]:.3f} s ({lambda_span[1]/T_orbit:.2f} Orbits)")
    print(f"Anzahl Punkte:    {len(result['lambda'])}")
    print(f"Durchschn. r:     {np.mean(result['r'])/rs:.6f} r_s (Soll: {r_orbit/rs:.6f})")
    print(f"Std.dev. r:       {np.std(result['r'])/rs:.6e} r_s")
    print(f"Constraint-Mean:  {np.mean(constraints):.6f} (Soll: -1.0)")
    print(f"Constraint-Std:   {np.std(constraints):.6e}")
    print("="*70)


if __name__ == "__main__":
    demo()
