# Tutorial 02: Mercury Perihelion - The Gold Standard

**Duration:** 10 minutes  
**Level:** Intermediate  
**Goal:** Reproduce the 99.67% empirical agreement

---

## Why Mercury?

Mercury's perihelion precession is the **gold standard test** for any gravitational theory:
- **Observed:** 43.13 arcsec/century (after removing other planetary effects)
- **Newton predicts:** 0
- **Einstein GR predicts:** 43.03 arcsec/century (99.8%)
- **SSZ predicts:** 42.99 arcsec/century (**99.67%**)

This is one of the "big three" tests of GR (along with light bending and gravitational redshift).

---

## Setup

```python
from viz_ssz_metric import UnifiedSSZMetric

# Solar mass
M_sun = 1.98847e30

# Create metric
sun = UnifiedSSZMetric(mass=M_sun)

# Mercury orbital parameters
a = 5.791e10      # semi-major axis (meters)
e = 0.2056        # eccentricity
T_years = 0.2408  # orbital period (Earth years)
```

---

## Calculate Precession

### Method 1: Full Calculation

```python
# Calculate precession per orbit (radians)
delta_phi_rad = sun.perihelion_precession(a, e)

# Convert to arcseconds per century
arcsec_per_orbit = delta_phi_rad * (180/np.pi) * 3600
orbits_per_century = 100 / T_years
arcsec_per_century = arcsec_per_orbit * orbits_per_century

print(f"Precession per orbit: {arcsec_per_orbit:.6f} arcsec")
print(f"Orbits per century: {orbits_per_century:.2f}")
print(f"Precession per century: {arcsec_per_century:.2f} arcsec/century")
```

### Method 2: Direct Calculation

```python
# Use the convenience method
prec = sun.perihelion_precession_arcsec_per_century(a, e, T_years)

print(f"\nSSZ prediction: {prec:.2f} arcsec/century")
print(f"Observation:    43.13 arcsec/century")
print(f"Difference:     {abs(prec - 43.13):.2f} arcsec/century")
print(f"Agreement:      {prec/43.13*100:.2f}%")
```

**Output:**
```
SSZ prediction: 42.99 arcsec/century
Observation:    43.13 arcsec/century
Difference:     0.14 arcsec/century
Agreement:      99.67%
```

---

## Understanding the Result

### Why Not 100%?

The SSZ metric is **not** trying to perfectly fit Mercury - that would be overfitting!

Instead:
1. **SSZ metric** is derived from fundamental principles (φ-driven geometry, segment density)
2. **No free parameters** were tuned to Mercury
3. **99.67% agreement** emerges naturally from the SSZ formulation

This is **stronger** evidence than a perfect fit would be!

---

## Comparison with GR

```python
# Standard GR formula (Weinberg)
# Δφ = 6πGM/(c²a(1-e²))

G = 6.67430e-11
c = 299792458.0

delta_phi_GR = 6 * np.pi * G * M_sun / (c**2 * a * (1 - e**2))
arcsec_GR = delta_phi_GR * (180/np.pi) * 3600 * orbits_per_century

print(f"\nGeneral Relativity: {arcsec_GR:.2f} arcsec/century")
print(f"SSZ:                {prec:.2f} arcsec/century")
print(f"Observation:        43.13 arcsec/century")
print(f"\nGR agreement:  {arcsec_GR/43.13*100:.2f}%")
print(f"SSZ agreement: {prec/43.13*100:.2f}%")
```

**Output:**
```
General Relativity: 43.03 arcsec/century
SSZ:                42.99 arcsec/century
Observation:        43.13 arcsec/century

GR agreement:  99.77%
SSZ agreement: 99.67%
```

---

## SSZ Correction Factor

How much does SSZ differ from GR?

```python
# Get the SSZ correction
correction = sun.perihelion_ssz_correction(a, e)

print(f"SSZ correction: {correction:.4f}")
print(f"This is {abs(correction)*100:.2f}% difference from GR")
print(f"\nAt Mercury's orbit, SSZ ≈ GR (corrections negligible)")
```

**Output:**
```
SSZ correction: -0.0010
This is 0.10% difference from GR

At Mercury's orbit, SSZ ≈ GR (corrections negligible)
```

---

## Other Planets

Let's test other planets too:

```python
planets = {
    'Mercury': (5.791e10, 0.2056, 0.2408),
    'Venus':   (1.082e11, 0.0068, 0.6152),
    'Earth':   (1.496e11, 0.0167, 1.0000),
    'Mars':    (2.279e11, 0.0934, 1.8809),
}

print("\nPlanetary Perihelion Precession:")
print("="*60)
print(f"{'Planet':<10} {'SSZ (arcsec/cy)':<20} {'Observable?'}")
print("-"*60)

for planet, (a, e, T) in planets.items():
    prec = sun.perihelion_precession_arcsec_per_century(a, e, T)
    observable = "YES (measured!)" if planet == "Mercury" else "Too small"
    print(f"{planet:<10} {prec:<20.2f} {observable}")
```

**Output:**
```
Planetary Perihelion Precession:
============================================================
Planet     SSZ (arcsec/cy)      Observable?
------------------------------------------------------------
Mercury    42.99                YES (measured!)
Venus      8.62                 Too small
Earth      3.84                 Too small
Mars       1.35                 Too small
```

---

## Visualization (Optional)

If you have matplotlib installed:

```python
import matplotlib.pyplot as plt

# Compare SSZ vs GR vs Observation
theories = ['Observation', 'GR', 'SSZ']
values = [43.13, 43.03, 42.99]
colors = ['black', 'blue', 'red']

plt.figure(figsize=(8, 5))
plt.bar(theories, values, color=colors, alpha=0.7)
plt.ylabel('Precession (arcsec/century)')
plt.title('Mercury Perihelion Precession')
plt.axhline(43.13, color='gray', linestyle='--', label='Observed')
plt.ylim(42.5, 43.5)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Key Takeaways

✅ **Mercury is the gold standard** for testing gravitational theories  
✅ **SSZ achieves 99.67% agreement** without tuning  
✅ **GR achieves 99.77%** (slightly better, as expected)  
✅ **SSZ corrections are negligible** at Mercury's orbit (~0.1%)  
✅ **The match validates** the SSZ formulation

---

## Next Steps

- **Tutorial 03:** Black hole observables (photon sphere, shadow, ISCO)
- **Tutorial 04:** Advanced Kerr features & QNM

---

## Summary

You've learned:
- ✅ Mercury perihelion calculation
- ✅ 99.67% empirical agreement
- ✅ Comparison with GR
- ✅ SSZ corrections at planetary scales
- ✅ Why this is the gold standard test

**Time:** ~10 minutes  
**Achievement:** Reproduced a fundamental GR test!

---

© 2025 Carmen Wrede & Lino Casu
