# Quick Start Tutorial - SSZ Metric

**Duration:** 5 minutes  
**Level:** Beginner

---

## Installation

```bash
# From PyPI (when available)
pip install ssz-metric

# Or from source
git clone https://github.com/USERNAME/ssz-full-metric
cd ssz-full-metric
pip install -e .
```

---

## Import

```python
from viz_ssz_metric import UnifiedSSZMetric
import numpy as np
```

---

## Create Your First Metric

### Example 1: The Sun

```python
# Solar mass in kg
M_sun = 1.98847e30

# Create metric
sun = UnifiedSSZMetric(mass=M_sun)

# Check basic properties
print(f"Mass: {sun.params.mass:.3e} kg")
print(f"Schwarzschild radius: {sun.r_s:.2f} m ({sun.r_s/1000:.2f} km)")
print(f"Golden ratio φ-radius: {sun.r_phi:.2e} m")
```

**Output:**
```
Mass: 1.988e+30 kg
Schwarzschild radius: 2953.34 m (2.95 km)
Golden ratio φ-radius: 1.85e+12 m
```

---

### Example 2: Sgr A* (Supermassive Black Hole)

```python
# Sgr A* mass
M_sgr_a = 4.15e6 * M_sun

# Create metric
sgr_a = UnifiedSSZMetric(mass=M_sgr_a)

print(f"Schwarzschild radius: {sgr_a.r_s/1e9:.2f} million km")
print(f"That's {sgr_a.r_s/1.496e11:.2f} AU (Earth-Sun distances)")
```

**Output:**
```
Schwarzschild radius: 12.26 million km
That's 0.08 AU (Earth-Sun distances)
```

---

## Calculate Basic Observables

### Photon Sphere

The unstable orbit where light can circle the black hole:

```python
r_ph = sun.photon_sphere_radius()

print(f"Photon sphere radius: {r_ph:.2f} m")
print(f"In units of r_s: {r_ph/sun.r_s:.3f} r_s")
print(f"GR prediction: 1.5 r_s")
print(f"SSZ value: ~1.338 r_s (due to metric modifications)")
```

---

### Shadow Radius

The apparent size of the black hole shadow:

```python
# For Sgr A*
distance_kpc = 8.277  # distance to Sgr A* in kiloparsecs

shadow = sgr_a.shadow_angular_size_microarcsec(distance_kpc)

print(f"Shadow angular size: {shadow:.1f} microarcsec")
print(f"EHT observation: ~52 microarcsec")
print(f"With accretion disk: {sgr_a.shadow_with_accretion_disk(distance_kpc):.1f} microarcsec")
```

---

### ISCO (Innermost Stable Circular Orbit)

```python
r_isco = sun.ISCO_radius()

print(f"ISCO radius: {r_isco/sun.r_s:.3f} r_s")
print(f"GR prediction: 3.0 r_s")
print(f"SSZ includes small correction: +2.2%")
```

---

## Next Steps

- **Tutorial 02:** Mercury perihelion validation (99.7% agreement!)
- **Tutorial 03:** All black hole observables
- **Tutorial 04:** Advanced Kerr features

---

## Summary

You've learned:
- ✅ How to create a metric
- ✅ Basic properties (r_s, r_φ)
- ✅ Photon sphere calculation
- ✅ Shadow radius
- ✅ ISCO

**Time:** ~5 minutes  
**Next:** `02_Mercury_Validation.md`

---

© 2025 Carmen Wrede & Lino Casu
