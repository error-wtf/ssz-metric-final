# -*- coding: utf-8 -*-
"""
Scalar Action Theory - Wirkungsbasierte SSZ-Theorie

Basierend auf: ssz_theory_segmented.py aus dem Vorlage-Repo
Implementiert: Anisotrope Kinetik Z_parallel(φ) und Skalar-Potential U(φ)

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
from __future__ import annotations
import numpy as np
from typing import Tuple
from dataclasses import dataclass


# Golden Ratio
PHI = (1.0 + np.sqrt(5.0)) / 2.0  # ≈ 1.618


@dataclass
class ScalarParams:
    """Parameter für Skalar-Theorie."""
    # Kinetik Z_parallel
    Z0: float = 1.0
    alpha: float = 0.1
    beta: float = 0.01
    Zmin: float = 0.1
    Zmax: float = 10.0
    
    # Potential U(φ)
    m_phi: float = 0.1
    lambda_: float = 0.001
    
    # Sättigungen
    phi_cap: float = 10.0
    phi_prime_cap: float = 1.0


class ScalarActionTheory:
    """
    Wirkungsbasierte SSZ-Theorie.
    
    Lagrangian:
    L = √(-g) × [-Z_parallel(φ) × g^μν ∂_μφ ∂_νφ - U(φ)]
    
    wobei:
    - Z_parallel(φ): Anisotrope kinetische Funktion
    - U(φ): Skalar-Potential
    
    Diese Formulierung führt zu nicht-trivialen Korrekturen
    im Energie-Impuls-Tensor T_μν.
    """
    
    def __init__(self, params: ScalarParams = None):
        """
        Initialize Scalar Action Theory.
        
        Args:
            params: ScalarParams object or None (use defaults)
        """
        self.params = params if params is not None else ScalarParams()
    
    def sat_tanh(self, x: float, cap: float | None) -> float:
        """
        Glatte Sättigung via tanh.
        
        Bounded: |output| ≤ cap
        
        Args:
            x: Input value
            cap: Saturation limit (None = no saturation)
        
        Returns:
            Saturated value
        """
        if cap is None or cap <= 0:
            return x
        return cap * np.tanh(x / cap)
    
    def sech2_stable(self, z: float) -> float:
        """
        sech²(z) = 1/cosh²(z) - Overflow-sicher!
        
        Für |z| > 20: cosh(z) ~ 0.5×exp(|z|)
        => sech²(z) ~ 4×exp(-2|z|)
        
        Args:
            z: Input value
        
        Returns:
            sech²(z) without overflow
        """
        a = abs(z)
        if a < 20.0:
            c = np.cosh(z)
            return 1.0 / (c * c)
        else:
            return 4.0 * np.exp(-2.0 * a)
    
    def Z_parallel_raw(self, phi_eff: float) -> float:
        """
        Ungeklammerte Z_parallel(φ_eff).
        
        Z_parallel = Z0 × (1 + α×φ + β×φ²)
        
        Args:
            phi_eff: Effective field value
        
        Returns:
            Z_parallel value
        """
        p = self.params
        return p.Z0 * (1.0 + p.alpha * phi_eff + p.beta * phi_eff * phi_eff)
    
    def Z_parallel(self, phi: float) -> float:
        """
        Anisotrope Kinetik Z_parallel(φ).
        
        Mit Sättigung und Bounds [Zmin, Zmax].
        
        Args:
            phi: Scalar field value
        
        Returns:
            Z_parallel(φ) bounded
        """
        p = self.params
        
        # Saturiere φ
        phi_sat = self.sat_tanh(phi, p.phi_cap)
        
        # Berechne Z
        Z = self.Z_parallel_raw(phi_sat)
        
        # Bound
        Z = np.clip(Z, p.Zmin, p.Zmax)
        
        return Z
    
    def dZ_dphi(self, phi: float) -> float:
        """
        Ableitung d/dφ Z_parallel(φ) mit gesättigtem φ.
        
        d/dφ sat(φ) = sech²(φ/φ_cap)
        
        Ableitung wird an den Klammern Zmin/Zmax saturiert (≈0 am Rand).
        
        Args:
            phi: Scalar field value
        
        Returns:
            dZ/dφ
        """
        p = self.params
        
        if p.phi_cap is None or p.phi_cap <= 0:
            # Ohne Caps
            Z = self.Z_parallel_raw(phi)
            if Z <= p.Zmin or Z >= p.Zmax:
                return 0.0
            return p.Z0 * (p.alpha + 2.0 * p.beta * phi)
        
        # Mit Caps
        phi_sat = self.sat_tanh(phi, p.phi_cap)
        Z = self.Z_parallel_raw(phi_sat)
        
        if Z <= p.Zmin or Z >= p.Zmax:
            return 0.0
        
        # Kettenregel
        dphi_sat = self.sech2_stable(phi / p.phi_cap)
        return p.Z0 * (p.alpha + 2.0 * p.beta * phi_sat) * dphi_sat
    
    def U_potential(self, phi: float) -> float:
        """
        Skalar-Potential U(φ).
        
        U(φ) = (1/2) × m_φ² × φ² + λ × φ⁴
        
        Mit Sättigung für φ.
        
        Args:
            phi: Scalar field value
        
        Returns:
            U(φ)
        """
        p = self.params
        
        # Saturiere φ
        phi_sat = self.sat_tanh(phi, p.phi_cap)
        
        # Potential
        U = 0.5 * (p.m_phi**2) * (phi_sat**2) + p.lambda_ * (phi_sat**4)
        
        return U
    
    def dU_dphi(self, phi: float) -> float:
        """
        Ableitung dU/dφ mit Kettenregel (sat).
        
        Args:
            phi: Scalar field value
        
        Returns:
            dU/dφ
        """
        p = self.params
        
        if p.phi_cap is None or p.phi_cap <= 0:
            # Ohne Caps
            return (p.m_phi**2) * phi + 4.0 * p.lambda_ * (phi**3)
        
        # Mit Caps
        phi_sat = self.sat_tanh(phi, p.phi_cap)
        dphi_sat = self.sech2_stable(phi / p.phi_cap)
        
        dU = ((p.m_phi**2) * phi_sat + 4.0 * p.lambda_ * (phi_sat**3)) * dphi_sat
        
        return dU
    
    def stress_energy_tensor(self, phi: float, phi_prime: float, 
                           one_minus_2m_r: float) -> Tuple[float, float, float, float]:
        """
        Energie-Impuls-Tensor T_μν aus der Wirkung.
        
        Für sphärisch-symmetrischen Fall:
        
        T_tt = ρ_φ = (1/2) × Z_parallel × X + U(φ)
        T_rr = p_r,φ = (1/2) × Z_parallel × X - U(φ)
        T_θθ = T_φφ = p_t,φ = -(1/2) × Z_parallel × X - U(φ)
        
        wobei X = (1-2m/r) × (φ')²
        
        Anisotropie:
        Δ_φ = p_t - p_r = -Z_parallel × X
        
        Args:
            phi: Scalar field φ
            phi_prime: Radial derivative φ'
            one_minus_2m_r: Metric factor (1 - 2m/r)
        
        Returns:
            (rho_phi, p_r_phi, p_t_phi, Delta_phi)
        """
        # Saturiere φ'
        phi_p_sat = self.sat_tanh(phi_prime, self.params.phi_prime_cap)
        
        # Kinetischer Term
        X = one_minus_2m_r * (phi_p_sat**2)
        
        # Z und U
        Z_par = self.Z_parallel(phi)
        U = self.U_potential(phi)
        
        # Komponenten
        rho_phi = 0.5 * Z_par * X + U
        p_r_phi = 0.5 * Z_par * X - U
        p_t_phi = -0.5 * Z_par * X - U
        Delta_phi = p_t_phi - p_r_phi  # = -Z_par × X
        
        return rho_phi, p_r_phi, p_t_phi, Delta_phi
    
    def scalar_eom_source(self, phi: float, phi_prime: float, 
                         one_minus_2m_r: float) -> float:
        """
        Quellterm für Skalar-Feldgleichung.
        
        Source = dU/dφ + (1/2) × (dZ/dφ) × X
        
        wobei X = (1-2m/r) × (φ')²
        
        Args:
            phi: Scalar field φ
            phi_prime: Radial derivative φ'
            one_minus_2m_r: Metric factor (1 - 2m/r)
        
        Returns:
            Source term
        """
        # Saturiere φ'
        phi_p_sat = self.sat_tanh(phi_prime, self.params.phi_prime_cap)
        
        # Kinetischer Term
        X = one_minus_2m_r * (phi_p_sat**2)
        
        # Ableitungen
        dU = self.dU_dphi(phi)
        dZ = self.dZ_dphi(phi)
        
        # Quellterm
        source = dU + 0.5 * dZ * X
        
        return source


def demo():
    """Demo: Scalar Action Theory für verschiedene φ-Werte."""
    import matplotlib.pyplot as plt
    
    print("\n" + "="*80)
    print("SCALAR ACTION THEORY - Wirkungsbasierte SSZ-Theorie")
    print("="*80)
    
    theory = ScalarActionTheory()
    
    # Test-Werte
    phi_values = np.linspace(-5, 5, 100)
    
    Z_values = [theory.Z_parallel(phi) for phi in phi_values]
    U_values = [theory.U_potential(phi) for phi in phi_values]
    dZ_values = [theory.dZ_dphi(phi) for phi in phi_values]
    dU_values = [theory.dU_dphi(phi) for phi in phi_values]
    
    print(f"\nParameter:")
    print(f"  Z0 = {theory.params.Z0}")
    print(f"  alpha = {theory.params.alpha}")
    print(f"  beta = {theory.params.beta}")
    print(f"  m_phi = {theory.params.m_phi}")
    print(f"  lambda = {theory.params.lambda_}")
    
    print(f"\nValues at phi = 0:")
    print(f"  Z_parallel(0) = {theory.Z_parallel(0):.6f}")
    print(f"  U(0) = {theory.U_potential(0):.6e}")
    
    print(f"\nValues at phi = 1:")
    phi_test = 1.0
    phi_p_test = 0.1
    one_minus_test = 0.9
    
    rho, p_r, p_t, Delta = theory.stress_energy_tensor(
        phi_test, phi_p_test, one_minus_test
    )
    
    print(f"  Z_parallel(1) = {theory.Z_parallel(phi_test):.6f}")
    print(f"  U(1) = {theory.U_potential(phi_test):.6e}")
    print(f"  rho_phi = {rho:.6e}")
    print(f"  p_r,phi = {p_r:.6e}")
    print(f"  p_t,phi = {p_t:.6e}")
    print(f"  Delta_phi = {Delta:.6e}")
    
    print(f"\nProperties:")
    print(f"  Anisotropy: Delta = p_t - p_r = {Delta:.6e}")
    print(f"  Expected: Delta = -Z*X = {-theory.Z_parallel(phi_test) * one_minus_test * phi_p_test**2:.6e}")
    
    print("="*80)
    print("SCALAR ACTION THEORY IMPLEMENTED!")
    print("   - Anisotropic kinetics Z_parallel(phi)")
    print("   - Scalar potential U(phi)")
    print("   - Stress-Energy T_munu from action")
    print("   - Numerically stable (sat_tanh, sech^2)")


if __name__ == "__main__":
    demo()
