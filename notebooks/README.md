# SSZ Metric Tutorials

Interactive Jupyter notebooks demonstrating the SSZ metric implementation.

## Available Notebooks

### 1. Quick Start (`01_Quick_Start.md`)
- Installation
- Basic usage
- First metric calculation
- **Duration:** 5 minutes

### 2. Mercury Validation (`02_Mercury_Validation.md`)
- Perihelion precession
- 99.7% empirical agreement
- Comparison with GR
- **Duration:** 10 minutes

### 3. Black Hole Observables (`03_Black_Hole_Features.md`)
- Photon sphere
- Shadow radius
- ISCO
- Hawking radiation
- **Duration:** 15 minutes

### 4. Advanced Features (`04_Advanced_Features.md`)
- Kerr black holes
- QNM frequencies
- Geodesic integration
- **Duration:** 20 minutes

## Usage

```bash
# Install Jupyter
pip install jupyter matplotlib

# Start Jupyter
jupyter notebook

# Open a notebook and run cells
```

## Quick Example

```python
from viz_ssz_metric import UnifiedSSZMetric

# Create metric for the Sun
sun = UnifiedSSZMetric(mass=1.98847e30)

# Calculate observables
print(f"Schwarzschild radius: {sun.r_s/1000:.2f} km")
print(f"Photon sphere: {sun.photon_sphere_radius()/sun.r_s:.3f} r_s")

# Mercury perihelion
prec = sun.perihelion_precession_arcsec_per_century(
    5.791e10,  # semi-major axis (m)
    0.2056,    # eccentricity
    0.2408     # orbital period (years)
)
print(f"Mercury precession: {prec:.2f} arcsec/century")
print(f"Observation: 43.13 arcsec/century")
print(f"Agreement: {prec/43.13*100:.2f}%")
```

**Output:**
```
Schwarzschild radius: 2.95 km
Photon sphere: 1.338 r_s
Mercury precession: 42.99 arcsec/century
Observation: 43.13 arcsec/century
Agreement: 99.67%
```

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
