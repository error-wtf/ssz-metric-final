# QUICKSTART - Metrik Vervollständigung

**3-Tage-Plan: Von 72% → 100%**

---

## SOFORT LOSLEGEN

### Option 1: ALLES AUF EINMAL (12h)

```bash
# Tag 1: Geodäten (6h)
# Erstelle Datei:
touch viz_ssz_metric/geodesics_unified.py

# Kopiere Template aus CODE_TEMPLATES_FOR_COMPLETION.md
# → TEMPLATE 1: GEODÄTEN-SOLVER

# Füge zu unified_metric.py hinzu:
# → TEMPLATE 2: PHOTON SPHERE
# → TEMPLATE 4: PERIHELION PRECESSION

# Tests:
pytest tests/test_geodesics_unified.py

# Tag 2: Observables (4h)
# Füge zu unified_metric.py hinzu:
# → TEMPLATE 3: SHADOW RADIUS
# → TEMPLATE 5: QNM

# Tests:
pytest tests/test_observables.py

# Tag 3: Polish (2h)
# Füge zu unified_metric.py hinzu:
# → TEMPLATE 6: HAWKING TEMPERATURE

# Final Tests:
pytest tests/test_unified_metric_complete.py
```

---

### Option 2: NUR KRITISCHES (6h)

**Fokus auf Must-Have Features:**

```bash
# Schritt 1: Photon Sphere (1h)
# In unified_metric.py einfügen:
def photon_sphere_radius(self):
    from scipy.optimize import minimize_scalar
    def neg_potential(r):
        A = self.metric_function_A(r)
        return -A / r**2
    result = minimize_scalar(neg_potential, bounds=(1.1*self.r_s, 5*self.r_s), method='bounded')
    return result.x

# Schritt 2: Shadow Radius (1h)
def shadow_radius(self, observer_distance=None):
    r_ph = self.photon_sphere_radius()
    A_ph = self.metric_function_A(r_ph)
    b_crit = r_ph / np.sqrt(A_ph)
    if observer_distance:
        return b_crit / observer_distance
    return b_crit

# Schritt 3: Geodäten-Basis (4h)
# Kopiere geodesics_unified.py Template
# Integriere in unified_metric.py

# FERTIG: 72% → 85% in 6 Stunden!
```

---

### Option 3: SCHRITTWEISE (1 Feature/Tag)

**Tag 1:** Photon Sphere (1-2h)  
**Tag 2:** Shadow Radius (1-2h)  
**Tag 3:** Geodäten (4-6h)  
**Tag 4:** QNM (2h)  
**Tag 5:** Perihelion (1.5h)  
**Tag 6:** Hawking (1h)  
**Tag 7:** Tests & Polish (2h)

---

## FEATURE-CHECKLISTE

```
□ Geodäten-Gleichungen
  □ GeodesicSolver Klasse
  □ integrate_timelike()
  □ integrate_null()
  □ Tests

□ Photon Sphere
  □ photon_sphere_radius()
  □ Test mit GR Vergleich

□ ISCO
  □ ISCO_radius()
  □ Test mit GR

□ Perihelion Precession
  □ perihelion_precession()
  □ Test mit Merkur

□ Shadow Radius
  □ shadow_radius()
  □ shadow_microarcsec()
  □ compare_with_EHT()
  □ Test mit Sgr A*

□ QNM
  □ quasi_normal_modes_wkb()
  □ ringdown_time()
  □ Tests

□ Hawking
  □ hawking_temperature()
  □ hawking_luminosity()
  □ evaporation_time()

□ Documentation
  □ Docstrings
  □ README.md Update
  □ Examples/

□ Tests
  □ test_geodesics_unified.py
  □ test_observables.py
  □ test_unified_metric_complete.py
```

---

## COPY-PASTE REIHENFOLGE

### 1. Erstelle geodesics_unified.py

```python
# viz_ssz_metric/geodesics_unified.py
# → Kopiere TEMPLATE 1 aus CODE_TEMPLATES_FOR_COMPLETION.md
```

### 2. Erweitere unified_metric.py

```python
# Am Ende der Klasse UnifiedSSZMetric einfügen:

# TEMPLATE 2: Photon Sphere
def photon_sphere_radius(self): ...

# TEMPLATE 3: Shadow Radius
def shadow_radius(self, observer_distance=None): ...
def shadow_microarcsec(self, distance_kpc): ...

# TEMPLATE 4: Perihelion
def perihelion_precession_arcsec_per_century(self, a, e, P): ...

# TEMPLATE 5: QNM
def quasi_normal_modes_wkb(self, l=2, n=0): ...
def ringdown_time(self, l=2, n=0): ...

# TEMPLATE 6: Hawking
def hawking_temperature(self): ...
def hawking_luminosity(self): ...
def evaporation_time(self): ...
```

### 3. Update __init__ in UnifiedSSZMetric

```python
def __init__(self, ...):
    # ... existing code ...
    
    # Add at end:
    from .geodesics_unified import GeodesicSolver
    self.geodesic_solver = GeodesicSolver(self)
```

### 4. Erstelle Tests

```python
# tests/test_unified_metric_complete.py
# → Kopiere TESTING TEMPLATE aus CODE_TEMPLATES_FOR_COMPLETION.md
```

### 5. Run Tests

```bash
pytest tests/test_unified_metric_complete.py -v
```

---

## VERIFICATION

Nach jedem Feature:

```python
from viz_ssz_metric.unified_metric import UnifiedSSZMetric

metric = UnifiedSSZMetric(mass=1.98847e30)

# Check feature exists
assert hasattr(metric, 'photon_sphere_radius')
assert hasattr(metric, 'shadow_radius')
assert hasattr(metric, 'quasi_normal_modes_wkb')
assert hasattr(metric, 'hawking_temperature')

# Check feature works
r_ph = metric.photon_sphere_radius()
print(f"✅ Photon Sphere: {r_ph/metric.r_s:.3f} r_s")

shadow = metric.shadow_microarcsec(8.277)
print(f"✅ Shadow: {shadow:.1f} μas")

omega_r, omega_i = metric.quasi_normal_modes_wkb()
print(f"✅ QNM: {omega_r:.3f} - i×{abs(omega_i):.3f}")

T_H = metric.hawking_temperature()
print(f"✅ Hawking: {T_H:.2e} K")
```

---

## HÄUFIGE PROBLEME

### Problem 1: Import Errors

```python
# Fix: Update __init__.py
# viz_ssz_metric/__init__.py

from .unified_metric import UnifiedSSZMetric
from .geodesics_unified import GeodesicSolver

__all__ = ['UnifiedSSZMetric', 'GeodesicSolver']
```

### Problem 2: Christoffel Symbols fehlen

```python
# Prüfe ob christoffel_symbols() die richtigen Keys zurückgibt
Gamma = metric.christoffel_symbols(r, theta)
print(Gamma.keys())

# Sollte enthalten:
# 'Gamma_t_tt', 'Gamma_t_tr', 'Gamma_r_tt', 'Gamma_r_rr', etc.
```

### Problem 3: Numerische Instabilität

```python
# Nutze Safe-Guards:
r_safe = max(r, 1.1 * metric.r_s)  # Nicht zu nahe am Horizont
A = metric.metric_function_A(r_safe)  # Softplus garantiert A > 0
```

---

## PROGRESS TRACKING

```
Phase A: Geodäten        [ ] [ ] [ ] [ ] [ ] [ ]  0/6h
Phase B: Observables     [ ] [ ] [ ] [ ]          0/4h
Phase C: Polish          [ ] [ ]                  0/2h

Total: 0/12h → 72/100 points
```

Nach jedem Feature: `[✓]` markieren

**Ziel:** Alle `[✓]` → 100/100 points!

---

## FINAL CHECK

```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=viz_ssz_metric --cov-report=term

# Should be 100%:
# - All tests pass
# - All features present
# - Documentation complete
```

---

## HELP & SUPPORT

**Stuck? Check:**
1. CODE_TEMPLATES_FOR_COMPLETION.md (alle Templates)
2. ROADMAP_TO_PERFECT_METRIC.md (detaillierter Plan)
3. METRIC_COMPLETENESS_CHECK.md (was fehlt genau)

**Debug:**
```python
# Test einzelne Funktion:
metric = UnifiedSSZMetric(mass=M_SUN)
print(dir(metric))  # Liste alle Methoden

# Test Christoffel:
Gamma = metric.christoffel_symbols(10*metric.r_s, np.pi/2)
print(Gamma)
```

---

**© 2025 Carmen Wrede & Lino Casu**

**Ready to Start!**  
**Pick an option and begin!**
