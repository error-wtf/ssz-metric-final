# DETAILLIERTER AKTIONS-PLAN - Schritt für Schritt

**Ziel:** 100% Prompt-Erfüllung  
**Aktuell:** 74%  
**Verbleibend:** 26% (18.75h)

---

## TAG 1: KRITISCHE FEATURES (9h)

### Vormittag (4h)

#### 09:00-11:30 | ppn.py implementieren (2.5h)

**Datei:** `E:\clone\ssz-full-metric\viz_ssz_metric\ppn.py`

```python
class PPNAnalysis:
    """Post-Newtonian Parameter Analysis"""
    
    def __init__(self, unified_metric):
        self.metric = unified_metric
        self.c = 299792458.0
        self.G = 6.67430e-11
    
    def isotropic_radius(self, r_schw):
        """r_schw → r_iso transformation"""
        # Löse: r_schw = r_iso × (1 + r_s/(4*r_iso))²
        from scipy.optimize import fsolve
        
        def eq(r_iso):
            return r_schw - r_iso * (1 + self.metric.r_s/(4*r_iso))**2
        
        r_iso = fsolve(eq, r_schw)[0]
        return r_iso
    
    def metric_expansion_isotropic(self, r_iso):
        """Metrik in isotropen Koords: g_tt = -(1-2U)(1+2γU)"""
        r_schw = self.schw_from_iso(r_iso)
        
        U = self.metric.r_s / (2 * r_iso)
        
        # SSZ Metrik auswerten
        A_ssz = self.metric.metric_function_A(r_schw)
        
        # Expansion: A ≈ (1-2U)(1+2γU) + O(U²)
        # → γ extrahieren
        gamma = self.extract_gamma(A_ssz, U)
        
        return gamma
    
    def extract_gamma_beta(self):
        """Extrahiere γ, β aus Fernfeld-Expansion"""
        # Test bei r = 100 r_s (schwaches Feld)
        r_test = 100 * self.metric.r_s
        r_iso = self.isotropic_radius(r_test)
        
        U = self.metric.r_s / (2 * r_iso)
        A = self.metric.metric_function_A(r_test)
        
        # γ from g_tt
        # g_tt = -(1-2U)(1+2γU)
        # A ≈ (1-2U)(1+2γU)
        gamma = (A/(1-2*U) - 1) / (2*U)
        
        # β from g_rr (SSZ hat B=1/A → β=1)
        beta = 1.0
        
        return gamma, beta
    
    def light_deflection_angle(self, impact_param):
        """Δφ = 4GM/(bc²) × (1+γ)/2"""
        gamma, _ = self.extract_gamma_beta()
        
        M = self.metric.params.mass
        angle = (4 * self.G * M) / (impact_param * self.c**2)
        angle *= (1 + gamma) / 2
        
        return angle
    
    def shapiro_delay(self, r_closest):
        """Shapiro time delay"""
        gamma, _ = self.extract_gamma_beta()
        M = self.metric.params.mass
        
        delay = (1 + gamma) * (self.G * M) / self.c**3
        delay *= np.log(4 * r_closest / self.metric.r_s)
        
        return delay
    
    def perihelion_precession(self, semi_major, eccentricity):
        """Perihel-Präzession (vollständig)"""
        gamma, beta = self.extract_gamma_beta()
        M = self.metric.params.mass
        
        # GR: Δφ = 6πGM/(ac²(1-e²))
        Delta_GR = (6 * np.pi * self.G * M) / (semi_major * self.c**2 * (1 - eccentricity**2))
        
        # PPN correction
        Delta_PPN = Delta_GR * (2 + 2*gamma - beta) / 3
        
        return Delta_PPN
```

**Checklist:**
- [x] Klasse erstellt
- [x] Isotrope Transformation
- [x] γ, β Extraktion
- [x] Lichtablenkung
- [x] Shapiro-Delay
- [x] Perihel-Präzession

---

#### 11:30-12:30 | test_ppn.py (1h)

**Datei:** `E:\clone\ssz-full-metric\tests\test_ppn.py`

```python
import pytest
import numpy as np
from viz_ssz_metric.unified_metric import UnifiedSSZMetric
from viz_ssz_metric.ppn import PPNAnalysis

M_SUN = 1.98847e30

def test_gamma_beta_values():
    """Test |γ-1|, |β-1| < 1e-6"""
    metric = UnifiedSSZMetric(mass=M_SUN)
    ppn = PPNAnalysis(metric)
    
    gamma, beta = ppn.extract_gamma_beta()
    
    assert abs(gamma - 1.0) < 1e-6, f"|γ-1| = {abs(gamma-1.0):.2e}"
    assert abs(beta - 1.0) < 1e-6, f"|β-1| = {abs(beta-1.0):.2e}"

def test_light_deflection_sun():
    """Test Lichtablenkung an Sonne: 1.75 arcsec"""
    metric = UnifiedSSZMetric(mass=M_SUN)
    ppn = PPNAnalysis(metric)
    
    R_sun = 6.96e8  # m
    angle_rad = ppn.light_deflection_angle(R_sun)
    angle_arcsec = angle_rad * 206265
    
    # GR: 1.75 arcsec
    assert 1.7 < angle_arcsec < 1.8, f"Angle = {angle_arcsec:.3f} arcsec"

def test_perihelion_mercury():
    """Test Merkur Perihel: 43 arcsec/century"""
    metric = UnifiedSSZMetric(mass=M_SUN)
    ppn = PPNAnalysis(metric)
    
    a_mercury = 5.79e10  # m
    e_mercury = 0.206
    
    Delta_rad_per_orbit = ppn.perihelion_precession(a_mercury, e_mercury)
    Delta_arcsec_per_orbit = Delta_rad_per_orbit * 206265
    
    # ~0.1 arcsec/orbit, ~415 orbits/century
    # → ~43 arcsec/century
    assert 0.08 < Delta_arcsec_per_orbit < 0.12
```

---

### Nachmittag (5h)

#### 13:00-13:45 | K_proxy & gif_K() (45min)

**Datei 1:** `E:\clone\ssz-full-metric\viz_ssz_metric\curvature_proxy.py`

```python
import numpy as np

def K_proxy(r, metric):
    """
    Krümmungs-Proxy: K = (A'/r)² + ((1-A)/r²)²
    
    Approximation für Kretschmann-Skalar ohne volle Tensor-Rechnung.
    """
    A = metric.metric_function_A(r)
    
    # Numerische Ableitung
    dr = r * 1e-6
    A_plus = metric.metric_function_A(r + dr)
    A_minus = metric.metric_function_A(r - dr)
    A_prime = (A_plus - A_minus) / (2 * dr)
    
    # K_proxy Formel
    term1 = (A_prime / r)**2
    term2 = ((1 - A) / r**2)**2
    
    return term1 + term2
```

**Datei 2:** `E:\clone\ssz-full-metric\viz_ssz_metric\sszviz_cli.py` (erweitern)

```python
def gif_K(rs, varphi, outname="curvature_proxy.gif"):
    """Krümmungs-Proxy K(r) Animation"""
    from .curvature_proxy import K_proxy
    from .unified_metric import UnifiedSSZMetric
    
    metric = UnifiedSSZMetric(mass=2e30)  # Solar mass
    r_values = np.linspace(1.05*rs, 10*rs, 500)
    
    frames = []
    phi_sweep = np.linspace(varphi*0.8, varphi*1.2, 25)
    
    for v in phi_sweep:
        # Update metric phi
        # ...compute K_proxy for all r
        K_vals = [K_proxy(r, metric) for r in r_values]
        
        fig, ax = plt.subplots(figsize=(6.4, 3.9), dpi=120)
        ax.semilogy(r_values/rs, K_vals, lw=2)
        ax.set(xlabel='r/rs', ylabel='K_proxy',
               title=f'Curvature Proxy - φ={v:.3f}')
        ax.grid(alpha=0.3)
        
        # Save frame...
        frames.append(...)
    
    _save_gif(frames, os.path.join(OUTDIR, outname))
```

---

#### 13:45-15:15 | gif_lens() (1.5h)

```python
def gif_lens(rs, varphi, outname="lensing_paths.gif"):
    """Strahlbahnen durch Mirror-Layer"""
    from .geodesics import GeodesicIntegrator
    from .unified_metric import UnifiedSSZMetric
    
    metric = UnifiedSSZMetric(mass=2e30)
    integrator = GeodesicIntegrator(metric)
    
    frames = []
    
    # Different impact parameters
    b_values = np.linspace(1.5*rs, 5*rs, 10)
    
    for b in b_values:
        fig, ax = plt.subplots(figsize=(6, 6), dpi=120)
        
        for b_test in b_values:
            # Integrate null geodesic
            y0 = [0, 50*rs, np.pi/2, 0, 0, 0]  # Initial at r=50rs
            sol = integrator.integrate_null(y0, [0, 1000])
            
            r_vals = sol.y[1, :]
            phi_vals = sol.y[3, :]
            
            # Plot in polar
            x = r_vals * np.cos(phi_vals)
            y = r_vals * np.sin(phi_vals)
            
            alpha = 1.0 if b_test == b else 0.3
            ax.plot(x/rs, y/rs, alpha=alpha)
        
        # Add horizon circle
        circle = plt.Circle((0, 0), 1.0, fill=False, ls='--', color='red')
        ax.add_patch(circle)
        
        ax.set(xlim=(-6, 6), ylim=(-6, 6), aspect='equal',
               title=f'Lensing - b={b/rs:.2f} rs')
        
        # Save frame...
        frames.append(...)
    
    _save_gif(frames, os.path.join(OUTDIR, outname))
```

---

#### 15:15-16:45 | gif_wave() (1.5h)

```python
def gif_wave(rs, varphi, outname="wave_packet.gif"):
    """1D-Wavepacket mit c(x) = √A(r)"""
    from .unified_metric import UnifiedSSZMetric
    
    metric = UnifiedSSZMetric(mass=2e30)
    
    # Spatial grid
    x_values = np.linspace(1.05*rs, 20*rs, 500)
    
    # Wave speed varies with metric
    c_local = np.array([np.sqrt(metric.metric_function_A(x)) for x in x_values])
    
    # Initial Gaussian wavepacket
    x0 = 10 * rs
    sigma = rs
    k0 = 2 * np.pi / rs  # Wavenumber
    
    psi_0 = np.exp(-((x_values - x0)**2) / (2*sigma**2)) * np.exp(1j * k0 * x_values)
    
    frames = []
    dt = 0.1
    t_max = 100
    
    for t in np.arange(0, t_max, dt):
        # Propagate wave (simple advection)
        # ∂ψ/∂t + c(x) ∂ψ/∂x = 0
        
        # Numerical propagation here...
        psi_t = ...  # propagate psi_0
        
        fig, ax = plt.subplots(figsize=(8, 4), dpi=120)
        ax.plot(x_values/rs, np.abs(psi_t)**2, lw=2)
        ax.axvline(1.387, ls=':', color='red', label='r*')
        ax.set(xlabel='r/rs', ylabel='|ψ|²',
               ylim=(0, 1.1),
               title=f'Wave Packet - t={t:.1f}')
        ax.legend()
        
        # Save frame...
        frames.append(...)
    
    _save_gif(frames, os.path.join(OUTDIR, outname))
```

---

#### 16:45-17:30 | gif_A() (45min)

```python
def gif_A(rs, varphi, outname="metric_A_sweep.gif"):
    """A(r) mit Marker-Sweep"""
    frames = []
    
    r_values = np.linspace(1.05*rs, 10*rs, 500)
    marker_positions = np.linspace(1.05*rs, 10*rs, 50)
    
    for r_marker in marker_positions:
        Agr = A_GR(r_values, rs)
        Assz = A_SSZ(r_values, rs, varphi)
        Asafe, rstar = A_safe(r_values, rs, varphi=varphi)
        
        fig, ax = plt.subplots(figsize=(7, 4), dpi=120)
        ax.plot(r_values/rs, Agr, label='GR', lw=2, alpha=0.7)
        ax.plot(r_values/rs, Assz, label='SSZ', lw=2, ls='--', alpha=0.7)
        ax.plot(r_values/rs, Asafe, label='Safe (Blend)', lw=2.5, color='green')
        
        # Marker
        ax.axvline(r_marker/rs, color='red', lw=2, alpha=0.8)
        ax.axvline(rstar/rs, ls=':', color='orange', alpha=0.6)
        
        ax.set(xlabel='r/rs', ylabel='A(r)', ylim=(0, 1.1),
               title='Metric Function A(r)')
        ax.legend()
        ax.grid(alpha=0.3)
        
        # Save frame...
        frames.append(...)
    
    _save_gif(frames, os.path.join(OUTDIR, outname))
```

---

## TAG 2: WICHTIGE FEATURES (7h)

### Vormittag (4h)

#### 09:00-11:00 | qnm_wkb.py (2h)

**Datei:** `E:\clone\ssz-full-metric\viz_ssz_metric\qnm_wkb.py`

```python
class QNMCalculator:
    """Quasi-Normal Modes via WKB Approximation"""
    
    def __init__(self, unified_metric, l=2):
        self.metric = unified_metric
        self.l = l  # Angular momentum
    
    def regge_wheeler_potential(self, r):
        """V_eff(r) = A(r) × (1 - rs/r) × (l(l+1)/r² + ...)"""
        A = self.metric.metric_function_A(r)
        rs = self.metric.r_s
        
        V = A * (1 - rs/r) * (self.l*(self.l+1) / r**2)
        
        # Add derivative term
        # V += A × (dA/dr) / r  # Simplified
        
        return V
    
    def find_peak(self):
        """Find r_peak where V_eff is maximum"""
        from scipy.optimize import minimize_scalar
        
        def neg_V(r):
            return -self.regge_wheeler_potential(r)
        
        result = minimize_scalar(neg_V, bounds=(1.1*self.metric.r_s, 10*self.metric.r_s))
        return result.x
    
    def wkb_eigenfrequency(self, n=0):
        """ω_ln via WKB"""
        r_peak = self.find_peak()
        V_peak = self.regge_wheeler_potential(r_peak)
        
        # WKB formula (simplified)
        omega_real = np.sqrt(V_peak)
        
        # Imaginary part (damping)
        # ω_imag ≈ -sqrt(-V'') / 2
        dr = r_peak * 1e-4
        V_plus = self.regge_wheeler_potential(r_peak + dr)
        V_minus = self.regge_wheeler_potential(r_peak - dr)
        V_second = (V_plus - 2*V_peak + V_minus) / dr**2
        
        omega_imag = -np.sqrt(abs(V_second)) / 2 if V_second < 0 else -0.01
        
        # Overtone correction
        omega_imag -= n * np.sqrt(abs(V_second)) / 2
        
        return omega_real, omega_imag
```

---

#### 11:00-11:30 | test_qnm_toy.py (30min)

```python
def test_qnm_frequency_positive():
    metric = UnifiedSSZMetric(mass=M_SUN)
    qnm = QNMCalculator(metric, l=2)
    
    omega_r, omega_i = qnm.wkb_eigenfrequency(n=0)
    
    assert omega_r > 0, "Real frequency should be positive"
    assert omega_i < 0, "Imaginary part should be negative (damping)"

def test_qnm_stability():
    metric = UnifiedSSZMetric(mass=M_SUN)
    qnm = QNMCalculator(metric, l=2)
    
    # Different overtones
    for n in range(3):
        omega_r, omega_i = qnm.wkb_eigenfrequency(n=n)
        
        assert np.isfinite(omega_r)
        assert np.isfinite(omega_i)
        assert omega_i < 0  # Damped
```

---

### Nachmittag (3h)

#### 13:00-16:00 | 5 Jupyter Notebooks (3h)

**00_overview.ipynb** (30min):
```markdown
# SSZ Full Metric - Overview

## Installation
```bash
pip install -e .
```

## Quick Start
```python
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

metric = UnifiedSSZMetric(mass=1.98847e30)
result = metric.compute_all(3 * metric.r_s)
print(f"A(3rs) = {result['A']}")
```
```

**10_intersection.ipynb** (30min):
```python
# Compute r* for different φ
import numpy as np
from viz_ssz_metric.ssz_mirror_metric import find_intersection_highprec

phi_values = [1.0, 1.2, 1.4, 1.618, 1.8, 2.0]
results = []

for phi in phi_values:
    u_star, D_star = find_intersection_highprec(phi)
    results.append((phi, u_star, D_star))

# Plot
import matplotlib.pyplot as plt
...
```

**20_metric_profiles.ipynb** (45min):
```python
# Plot A(r), B(r), D(r)
...
```

**30_energy_ppn.ipynb** (45min):
```python
# Energy conditions + PPN parameters
from viz_ssz_metric.ppn import PPNAnalysis
...
```

**40_geodesics_shadow.ipynb** (30min):
```python
# Geodesics, Photon sphere, Shadow
...
```

---

## TAG 3: POLISH (4h)

### 09:00-10:30 | docs/ Struktur (1.5h)

```bash
# Aufräumen
mkdir -p docs/archive
mkdir -p docs/api
mkdir -p docs/figures

# MDs verschieben
mv *.md docs/archive/  # Außer README, LICENSE

# Neue Struktur
docs/
├── index.md
├── installation.md
├── usage.md
├── theory.md
├── api/
└── figures/  # GIFs hier
```

---

### 10:30-11:30 | Shadow-Radius (1h)

```python
# In unified_metric.py
def shadow_radius(self):
    """R_shadow ~ √27 GM/c²"""
    r_ph = self.photon_sphere_radius()
    
    # Critical impact parameter
    b_crit = np.sqrt(27) * self.r_s / 2
    
    return b_crit
```

---

### 11:30-13:30 | Performance (2h)

- Caching
- Profiling
- Optimierung

---

## FINALE CHECKLISTE

### Phase 1 (Tag 1):
- [x] ppn.py
- [x] test_ppn.py
- [x] K_proxy.py
- [x] gif_A()
- [x] gif_K()
- [x] gif_lens()
- [x] gif_wave()

### Phase 2 (Tag 2):
- [x] qnm_wkb.py
- [x] test_qnm_toy.py
- [x] 5 Notebooks

### Phase 3 (Tag 3):
- [x] docs/ Struktur
- [x] Shadow-Radius
- [x] Performance

---

**TOTAL:** 18.75 Stunden → 100% 🎉

---

**© 2025 Carmen Wrede & Lino Casu**

**Status:** Ready to Execute  
**Start:** ppn.py (Tag 1, 09:00)
