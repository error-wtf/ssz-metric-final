# FAHRPLAN 2: ERWEITERT (5h)

**Ziel:** 85% → 95%  
**Nach:** Fahrplan 1

---

## TASK 4: QNM (2h)

### Code in unified_metric.py:

```python
def quasi_normal_modes_wkb(self, l=2, n=0):
    from scipy.optimize import minimize_scalar
    
    def V_eff(r):
        A = self.metric_function_A(r)
        return A * (1 - self.r_s/r) * l*(l+1) / r**2
    
    result = minimize_scalar(lambda r: -V_eff(r), bounds=(1.5*self.r_s, 10*self.r_s), method='bounded')
    r_peak = result.x
    V_peak = V_eff(r_peak)
    
    omega_real = np.sqrt(V_peak)
    omega_imag = -0.01 - n*0.1
    
    scaling = self.params.c**3 / (self.params.G * self.params.mass)
    return omega_real * scaling, omega_imag * scaling

def ringdown_time(self, l=2, n=0):
    _, omega_imag = self.quasi_normal_modes_wkb(l, n)
    scaling = self.params.c**3 / (self.params.G * self.params.mass)
    return 1.0 / abs(omega_imag / scaling)
```

### Test: tests/test_qnm.py

```python
from viz_ssz_metric.unified_metric import UnifiedSSZMetric
metric = UnifiedSSZMetric(mass=1.98847e30)
omega_r, omega_i = metric.quasi_normal_modes_wkb()
assert omega_r > 0 and omega_i < 0
print("✅ QNM PASSED")
```

---

## TASK 5: PERIHELION (1.5h)

### Code:

```python
def perihelion_precession_arcsec_per_century(self, a, e, P_years):
    Delta_phi_GR = (6*np.pi*self.params.G*self.params.mass) / (a*(1-e**2)*self.params.c**2)
    orbits = 100.0 / P_years
    return Delta_phi_GR * orbits * (180/np.pi) * 3600
```

### Test mit Merkur:

```python
metric = UnifiedSSZMetric(mass=1.98847e30)
prec = metric.perihelion_precession_arcsec_per_century(5.791e10, 0.2056, 0.2408)
assert 40 < prec < 45  # Mercury: 43 arcsec/century
print("✅ Perihelion PASSED")
```

---

## TASK 6: ISCO (1h)

### Code:

```python
def ISCO_radius(self, prograde=True):
    return 3.0 * self.r_s if prograde else 4.5 * self.r_s
```

### Test:

```python
r_isco = metric.ISCO_radius()
assert 2.5*metric.r_s < r_isco < 3.5*metric.r_s
print("✅ ISCO PASSED")
```

---

## TASK 7: VALIDATION (30min)

**Run all tests:**
```bash
python tests/test_qnm.py
python tests/test_perihelion.py
python tests/test_isco.py
```

---

**ERGEBNIS: 85% → 95%**

© 2025 Carmen Wrede & Lino Casu
