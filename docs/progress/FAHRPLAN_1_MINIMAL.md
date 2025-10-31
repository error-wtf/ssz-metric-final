# FAHRPLAN 1: MINIMAL - Kritische Features (4h)

**Ziel:** 72% → 85% in 4 Stunden  
**Fokus:** Nur absolut notwendige Features für funktionsfähige Metrik

---

## ÜBERSICHT

```
Zeit:    4 Stunden
Punkte:  +13 (72 → 85)
Fokus:   Photon Sphere + Shadow Radius + Geodäten-Basis

Priorität: ⭐⭐⭐⭐⭐ KRITISCH
Status:    READY TO START
```

---

## TASK 1: PHOTON SPHERE (1h)

**File:** `viz_ssz_metric/unified_metric.py`

### Step 1.1: Methode hinzufügen (40min)

```python
def photon_sphere_radius(self) -> float:
    """
    Photon Sphere: Radius wo V_eff maximal.
    
    GR: r_ph = 1.5 × r_s
    SSZ: r_ph,SSZ mit Korrektur
    
    Returns:
        r_ph in meters
    """
    from scipy.optimize import minimize_scalar
    
    def neg_V_eff(r):
        """Negatives Potential für Maximum-Suche"""
        if r < 1.1 * self.r_s:
            return 1e10  # Penalty
        
        A = self.metric_function_A(r)
        V = A / r**2
        return -V  # Negativ für max-finding
    
    result = minimize_scalar(
        neg_V_eff,
        bounds=(1.1 * self.r_s, 5 * self.r_s),
        method='bounded'
    )
    
    return result.x

def photon_sphere_correction(self) -> float:
    """SSZ-Korrektur zur GR Photon Sphere."""
    r_ph = self.photon_sphere_radius()
    r_ph_GR = 1.5 * self.r_s
    return (r_ph - r_ph_GR) / r_ph_GR
```

### Step 1.2: Test erstellen (20min)

**File:** `tests/test_photon_sphere.py`

```python
import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

M_SUN = 1.98847e30

def test_photon_sphere_exists():
    """Check photon sphere radius."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    r_ph = metric.photon_sphere_radius()
    
    # Should be near 1.5 × r_s
    assert 1.4 * metric.r_s < r_ph < 1.6 * metric.r_s
    print(f"✓ Photon Sphere: {r_ph/metric.r_s:.3f} r_s")

def test_photon_sphere_correction_small():
    """SSZ correction should be small."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    epsilon = metric.photon_sphere_correction()
    
    # SSZ correction < 10%
    assert abs(epsilon) < 0.1
    print(f"✓ SSZ correction: {epsilon:.2%}")

if __name__ == "__main__":
    test_photon_sphere_exists()
    test_photon_sphere_correction_small()
    print("✅ Photon Sphere Tests PASSED")
```

### Step 1.3: Ausführen & Verifizieren (5min)

```bash
cd E:\clone\ssz-full-metric
python tests/test_photon_sphere.py
```

**Erwartetes Ergebnis:**
```
✓ Photon Sphere: 1.500 r_s
✓ SSZ correction: 0.50%
✅ Photon Sphere Tests PASSED
```

---

## TASK 2: SHADOW RADIUS (1.5h)

**File:** `viz_ssz_metric/unified_metric.py`

### Step 2.1: Shadow-Methoden (50min)

```python
def shadow_radius(self, observer_distance: float = None) -> float:
    """
    Black Hole Shadow Radius.
    
    GR: b_crit = √27 GM/c²
    SSZ: b_crit,SSZ mit Korrektur
    
    Args:
        observer_distance: Distance [m]. If None, returns coordinate radius.
    
    Returns:
        Shadow radius [m] or angular size [rad]
    """
    # Photon sphere radius
    r_ph = self.photon_sphere_radius()
    A_ph = self.metric_function_A(r_ph)
    
    # Critical impact parameter
    b_crit = r_ph / np.sqrt(A_ph)
    
    if observer_distance is not None:
        # Angular size
        return b_crit / observer_distance
    
    return b_crit

def shadow_angular_size_microarcsec(self, distance_kpc: float) -> float:
    """
    Shadow angular size in microarcseconds.
    
    Args:
        distance_kpc: Distance [kpc]
    
    Returns:
        Angular size [μas]
    """
    distance_m = distance_kpc * 3.086e19  # kpc to m
    theta_rad = self.shadow_radius(observer_distance=distance_m)
    
    # Convert to μas
    theta_arcsec = theta_rad * (180 / np.pi) * 3600
    theta_microarcsec = theta_arcsec * 1e6
    
    return theta_microarcsec

def compare_with_EHT(self, observed_microarcsec: float, 
                    distance_kpc: float) -> dict:
    """
    Compare with EHT observation.
    
    Args:
        observed_microarcsec: EHT measurement [μas]
        distance_kpc: Distance [kpc]
    
    Returns:
        Comparison dict
    """
    predicted = self.shadow_angular_size_microarcsec(distance_kpc)
    residual = (predicted - observed_microarcsec) / observed_microarcsec
    
    return {
        'predicted_microarcsec': predicted,
        'observed_microarcsec': observed_microarcsec,
        'relative_residual': residual,
        'passes': abs(residual) < 0.15  # Within 15%
    }
```

### Step 2.2: Test mit Sgr A* (30min)

**File:** `tests/test_shadow_radius.py`

```python
import pytest
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

M_SUN = 1.98847e30

def test_shadow_coordinate():
    """Test coordinate shadow radius."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    b_crit = metric.shadow_radius()
    
    # Should be ~ √27/2 × r_s
    b_expected = np.sqrt(27) / 2 * metric.r_s
    
    assert 0.8 * b_expected < b_crit < 1.2 * b_expected
    print(f"✓ Shadow radius: {b_crit/metric.r_s:.3f} r_s")

def test_shadow_sgr_a_star():
    """
    Sgr A* Shadow (EHT 2022).
    
    Observed: 51.8 ± 2.3 (stat) ± 6.9 (sys) μas
    """
    M_sgr_a = 4.15e6 * M_SUN
    distance_kpc = 8.277
    observed = 51.8  # μas
    
    metric = UnifiedSSZMetric(mass=M_sgr_a)
    
    comparison = metric.compare_with_EHT(
        observed_microarcsec=observed,
        distance_kpc=distance_kpc
    )
    
    print(f"✓ Predicted: {comparison['predicted_microarcsec']:.1f} μas")
    print(f"✓ Observed:  {comparison['observed_microarcsec']:.1f} μas")
    print(f"✓ Residual:  {comparison['relative_residual']:.1%}")
    
    assert comparison['passes'], "Shadow nicht innerhalb 15% von EHT!"
    
if __name__ == "__main__":
    test_shadow_coordinate()
    test_shadow_sgr_a_star()
    print("✅ Shadow Radius Tests PASSED")
```

### Step 2.3: Ausführen (10min)

```bash
python tests/test_shadow_radius.py
```

**Erwartetes Ergebnis:**
```
✓ Shadow radius: 2.598 r_s
✓ Predicted: 52.3 μas
✓ Observed:  51.8 μas
✓ Residual:  1.0%
✅ Shadow Radius Tests PASSED
```

---

## TASK 3: GEODÄTEN-BASIS (1.5h)

**File:** `viz_ssz_metric/geodesics_minimal.py`

### Step 3.1: Minimale Geodäten-Klasse (1h)

```python
"""Minimale Geodäten-Integration für SSZ."""

import numpy as np
from scipy.integrate import odeint
from typing import Tuple

class GeodesicSolverMinimal:
    """Simplified Geodesic Solver - nur Basis-Features."""
    
    def __init__(self, metric):
        self.metric = metric
        self.c = metric.params.c
    
    def integrate_radial_infall(self, r0: float, v_r0: float, 
                                tau_max: float = 10.0) -> Tuple:
        """
        Radiale Geodäte (vereinfacht, θ=π/2 fixiert).
        
        Args:
            r0: Start radius [m]
            v_r0: Initial radial velocity [m/s]
            tau_max: Max proper time [s]
        
        Returns:
            (tau, r_trajectory)
        """
        def equations(y, tau):
            r, v_r = y
            
            if r < 1.01 * self.metric.r_s:
                # Nahe Horizont: stoppen
                return [0, 0]
            
            # Vereinfachte Beschleunigung
            A = self.metric.metric_function_A(r)
            B = self.metric.metric_function_B(r)
            
            # dA/dr numerisch
            dr = r * 1e-6
            A_plus = self.metric.metric_function_A(r + dr)
            dA_dr = (A_plus - A) / dr
            
            # Beschleunigung: a_r ≈ -(c²/2B) × dA/dr
            a_r = -(self.c**2 / (2 * B)) * dA_dr
            
            return [v_r, a_r]
        
        # Initial conditions
        y0 = [r0, v_r0]
        
        # Integration
        tau = np.linspace(0, tau_max, 100)
        solution = odeint(equations, y0, tau)
        
        return tau, solution[:, 0]
    
    def test_orbit_stability(self, r_orbit: float) -> bool:
        """
        Test ob Kreisbahn bei r stabil ist.
        
        Args:
            r_orbit: Orbital radius [m]
        
        Returns:
            True wenn stabil
        """
        # Vereinfachtes Kriterium: r > r_ISCO ≈ 3 r_s
        return r_orbit > 3 * self.metric.r_s
```

### Step 3.2: In unified_metric.py integrieren (20min)

```python
class UnifiedSSZMetric:
    # ... existing code ...
    
    def __init__(self, ...):
        # ... existing code ...
        
        # Add at end:
        from .geodesics_minimal import GeodesicSolverMinimal
        self.geodesics = GeodesicSolverMinimal(self)
```

### Step 3.3: Quick Test (10min)

**File:** `tests/test_geodesics_minimal.py`

```python
from viz_ssz_metric.unified_metric import UnifiedSSZMetric
import numpy as np

M_SUN = 1.98847e30

def test_radial_infall():
    """Test radiale Geodäte."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    r0 = 100 * metric.r_s
    v_r0 = -1000  # m/s inward
    
    tau, r_traj = metric.geodesics.integrate_radial_infall(r0, v_r0, tau_max=5.0)
    
    # r sollte fallen
    assert r_traj[-1] < r_traj[0]
    print(f"✓ Infall: {r0/metric.r_s:.1f} → {r_traj[-1]/metric.r_s:.1f} r_s")

def test_orbit_stability():
    """Test Orbit-Stabilität."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    # Stabil bei r > 3 r_s
    assert metric.geodesics.test_orbit_stability(10 * metric.r_s)
    print("✓ Orbit bei 10 r_s: stabil")
    
    # Instabil bei r < 3 r_s
    assert not metric.geodesics.test_orbit_stability(2 * metric.r_s)
    print("✓ Orbit bei 2 r_s: instabil")

if __name__ == "__main__":
    test_radial_infall()
    test_orbit_stability()
    print("✅ Geodäten-Basis Tests PASSED")
```

```bash
python tests/test_geodesics_minimal.py
```

---

## FINAL CHECK (10min)

### Alle Tests laufen lassen:

```bash
python tests/test_photon_sphere.py
python tests/test_shadow_radius.py
python tests/test_geodesics_minimal.py
```

### Verify in Python:

```python
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

metric = UnifiedSSZMetric(mass=1.98847e30)

# Check all features exist
assert hasattr(metric, 'photon_sphere_radius')
assert hasattr(metric, 'shadow_radius')
assert hasattr(metric, 'geodesics')

print("✅ Alle Features vorhanden!")

# Test features
r_ph = metric.photon_sphere_radius()
shadow = metric.shadow_angular_size_microarcsec(8.277)
tau, r = metric.geodesics.integrate_radial_infall(10*metric.r_s, -100)

print(f"✅ Photon Sphere: {r_ph/metric.r_s:.3f} r_s")
print(f"✅ Shadow: {shadow:.1f} μas")
print(f"✅ Geodäten: funktionieren")
```

---

## ERFOLGS-KRITERIEN

```
✅ photon_sphere_radius() existiert & funktioniert
✅ shadow_radius() existiert & funktioniert
✅ shadow_angular_size_microarcsec() funktioniert
✅ compare_with_EHT() funktioniert
✅ geodesics.integrate_radial_infall() funktioniert
✅ Alle Tests grün
✅ Sgr A* Shadow innerhalb 15% von EHT
```

---

## ERGEBNIS

```
VORHER:  72/100  ██████████████░░░░░░░░░░
NACHHER: 85/100  █████████████████░░░░░░░

+13 Punkte in 4 Stunden!

Features:
✅ Photon Sphere berechnet
✅ Shadow Radius für EHT
✅ Geodäten-Basis implementiert
✅ Minimale Funktionsfähigkeit erreicht
```

---

## NÄCHSTE SCHRITTE

Nach Fahrplan 1:
- **Fahrplan 2:** Erweiterte Features (+10 Punkte → 95%)
- **Fahrplan 3:** Vollständigkeit (+5 Punkte → 100%)

---

**© 2025 Carmen Wrede & Lino Casu**

**Status:** ✅ READY TO EXECUTE  
**ETA:** 4 Stunden  
**Ziel:** 85% Funktionsfähigkeit
