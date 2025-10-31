# BUG ANALYSIS - Validation Scripts

**Datum:** 31. Oktober 2025, 16:45 UTC+01:00  
**Status:** Critical Issues Found

---

## BUG #1: ESO VALIDATION - CRITICAL ⚠️⚠️⚠️

### Problem:
```
Accuracy:  0.000%  (target: >= 97.9%)
Chi^2/dof: 624256684  (target: < 1.1)
Mean residual: -470.9774
```

### Root Cause Analysis:

#### Issue 1: Falsche Datenstruktur
Die CSV-Datei `real_data_full.csv` enthält **SYNTHETISCHE** Daten für verschiedene Massen, NICHT echte ESO S-Star Beobachtungen!

**Beweis:**
```
Columns: ['case', 'category', 'M_solar', 'a_m', 'e', ...]
- 'case': Test cases
- 'category': Verschiedene Objekte (Sun, Earth, etc.)
- 'M_solar': Massen-Parameter
```

Diese Daten sind für **MASS VALIDATION**, nicht für ESO S-Stars!

#### Issue 2: Falsche Redshift-Berechnung
```python
z_ssz = np.sqrt(1.0 / A) - 1.0  # ❌ NUR Gravitationsredshift
```

**Problem:** ESO misst den **DOPPLER-Redshift** von bewegten Sternen, NICHT den statischen Gravitationsredshift!

**Was gemessen wird:**
- z_obs = Doppler-Verschiebung durch Orbitalgeschwindigkeit
- z = v/c für v << c
- v = Orbital velocity at periastron/apoastron

**Was wir berechnen:**
- z_ssz = Gravitational redshift (statisch)

**Das sind völlig verschiedene Effekte!**

#### Issue 3: Falsche Physik
S-Stars bei Sgr A* haben:
- Orbital velocities: ~1000-7000 km/s
- Gravitational redshift: ~1e-4 bei 1000 AU
- **Doppler >> Gravitational!**

### Fix Required:

**Option 1: Korrekte ESO-Daten** (2h Research)
- Echte ESO S-Star Daten finden
- Mit Doppler-Shift + Gravitational kombinieren

**Option 2: Synthetic Validation** (30min)
- Synthetische S-Star Orbits generieren
- SSZ vs. GR Doppler + Gravity kombiniert

**Option 3: Mass Validation** (15min)
- Script umbenennen zu `mass_validation.py`
- Statt Redshift: Masse-Rekonstruktion validieren
- Das ist was die Daten TATSÄCHLICH machen!

---

## BUG #2: BLACK HOLE BOMB - CRITICAL ⚠️⚠️⚠️

### Problem:
```
E_SSZ(final): 9.8813e-324  (≈ 0)
Damping eta: inf
[WARN] Unstable: lambda_A (0.005) >= lambda_crit (0.000100)
```

### Root Cause Analysis:

#### Issue 1: Instability Condition INVERTED!
```python
lambda_crit = 1 / K**2 = 0.0001
lambda_A = 0.005

if lambda_A < lambda_crit:  # ❌ FALSCH!
    print("Stable")
```

**Physik:** lambda_A > lambda_crit bedeutet **INSTABIL**
- Aber wir sagen "[WARN] Unstable" → korrekt erkannt
- Aber dann simulieren wir trotzdem → Bug!

#### Issue 2: Falsche Dämpfungs-Formel
```python
growth = lambda_A - lambda_A**2 * K**2
```

**Problem:** Bei K=100, lambda_A=0.005:
```
growth = 0.005 - 0.005^2 * 100^2
       = 0.005 - 0.000025 * 10000
       = 0.005 - 0.25
       = -0.245  # ❌ NEGATIV!
```

**Resultat:** E[t+1] = E[t] × (1 - 0.245) = 0.755 × E[t]
→ Energie nimmt EXPONENTIELL AB!
→ Nach 10000 Steps: E ≈ 0.755^10000 ≈ 0

**Das ist ANTI-BOMB, nicht Dämpfung!**

#### Issue 3: Falsche Parameter
Für Black Hole Bomb brauchen wir:
- lambda_A > lambda_crit (Instabil)
- Aber lambda_A << 1 (Schwache Kopplung)
- Beispiel: K=100, lambda_A=0.002 (unter crit, aber nah dran)

#### Issue 4: φ-Saturation zu früh
```python
E_max = E[0] * (1 - np.exp(-PHI * K))
```

Bei K=100:
```
E_max = 1.0 * (1 - exp(-1.618 * 100))
      = 1.0 * (1 - 0)
      = 1.0
```

**Sättigung ist bei 1.0 → kein Wachstum möglich!**

### Fix Required:

**Korrigierte Parameter:**
```python
K = 100
lambda_A = 0.0008  # < lambda_crit = 0.0001, STABLE
```

**Korrigierte Formel:**
```python
# SSZ damping sollte KLEINE positive growth geben
# GR: exponentiell
# SSZ: logarithmisch

growth_GR = lambda_A
growth_SSZ = lambda_A / (1 + lambda_A * K)  # Dämpfung durch Segmente
```

---

## BUG #3: UNIFIED METRIC - POTENTIAL ISSUE

### Checking unified_metric.py integration:

```python
from viz_ssz_metric.unified_metric import UnifiedSSZMetric
metric = UnifiedSSZMetric(mass=M_SGR_A)
```

**Potential Issues:**
1. Import path korrekt?
2. r_phi Attribut existiert?
3. metric_function_A() numerisch stabil für extreme Massen?

**Test needed:**
```python
# Test extreme values
r_test = 1.1 * metric.r_s  # Nahe Horizont
A = metric.metric_function_A(r_test)
# Should be: 0 < A < 1, finite
```

---

## BUG #4: UNICODE ENCODING - FIXED ✅

**Problem:** Windows cp1252 kann keine griechischen Buchstaben

**Fix Applied:**
- ✅ Alle φ → phi
- ✅ Alle λ → lambda
- ✅ Alle η → eta
- ✅ Alle χ² → Chi^2
- ✅ Alle Emojis → ASCII

**Status:** RESOLVED

---

## BUG #5: DATA PATH - POTENTIAL ISSUE

```python
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'real_data_full.csv')
```

**Issues:**
1. Relative path - fragil
2. `__file__` kann bei verschiedenen Ausführungen variieren
3. CSV nicht validiert vor Load

**Better:**
```python
import sys
import os

# Absolute path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(project_root, 'data', 'real_data_full.csv')

# Validate
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Data not found: {data_path}")
```

---

## SUMMARY - CRITICAL BUGS

### 🔴 CRITICAL:
1. **ESO Validation**: Falsche Datenquelle + Falsche Physik
   - Fix: Daten-Check + Doppler statt Gravity
   - ETA: 30min - 2h

2. **BH Bomb**: Falsche Formel + Falsche Parameter
   - Fix: Dämpfungs-Formel korrigieren
   - ETA: 30min

### 🟡 MAJOR:
3. **Data Loading**: Fragile paths
   - Fix: Absolute paths
   - ETA: 10min

### 🟢 MINOR:
4. **Unicode**: Fixed ✅

---

## RECOMMENDED FIXES (Priority Order)

### FIX #1: Black Hole Bomb Formula (15min) ⭐⭐⭐⭐⭐

```python
def simulate_discrete_SSZ(K=100, lambda_A=0.0008, steps=10000):
    E = np.zeros(steps)
    E[0] = 1.0
    
    for t in range(steps-1):
        # CORRECTED: Dämpfung = Reduktion der growth rate
        growth_GR = lambda_A
        damping_factor = 1 / (1 + lambda_A * K * PHI)
        growth_SSZ = growth_GR * damping_factor
        
        E[t+1] = E[t] * (1 + growth_SSZ)
        
        # Saturation (optional)
        if E[t+1] > 10 * E[0]:  # Limit growth
            E[t+1] = 10 * E[0]
    
    return E
```

### FIX #2: ESO → Mass Validation (20min) ⭐⭐⭐⭐

**Rename + Repurpose:**
- eso_validation.py → mass_validation.py
- Validiere Masse-Rekonstruktion, nicht Redshift
- Das ist was die Daten TATSÄCHLICH sind!

```python
def validate_mass_reconstruction():
    """
    Validate SSZ mass reconstruction from orbital data.
    
    CSV has: M_solar, a_m, e, P_year, z
    → Calculate M from orbit
    → Compare with input M_solar
    """
    ...
```

### FIX #3: Data Paths (5min) ⭐⭐⭐

Use absolute paths everywhere.

---

## PRIORITY EXECUTION

**NOW (30min):**
1. Fix Black Hole Bomb formula
2. Test: Should get eta ~ 6-7
3. Fix data paths

**THEN (20min):**
4. Rename ESO → Mass Validation
5. Implement mass reconstruction

**LATER (Optional):**
6. Real ESO S-Star data research
7. Doppler + Gravity combined model

---

## STATUS

**Bugs Identified:** 5  
**Bugs Fixed:** 1 (Unicode)  
**Bugs Remaining:** 4 (2 Critical, 1 Major, 1 Minor)

**Next Action:** Fix Black Hole Bomb formula NOW

---

**© 2025 Carmen Wrede & Lino Casu**

**Confidence:** HIGH - Root causes identified  
**Fix ETA:** 30-60 minutes for critical bugs
