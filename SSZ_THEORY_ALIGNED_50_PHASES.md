# 🎯 SSZ THEORY-ALIGNED 50-PHASEN-ROADMAP

**Basierend auf:** 100% Analyse des Vorlage-Repos (Segmented-Spacetime-Mass-Projection-Unified-Results)  
**Datum:** 31. Oktober 2025, 03:00 UTC+01:00  
**Ziel:** Perfekte Übereinstimmung mit validierten SSZ-Theorie

---

## 📊 **KRITISCHE ERKENNTNISSE AUS DEM VORLAGE-REPO**

### **1. FUNDAMENTAL: Wirkungsbasierte Theorie (`ssz_theory_segmented.py`)**

```python
# KERN-PHYSIK (bereits validiert im Vorlage-Repo):

# 1. Anisotrope Kinetik mit Z_parallel:
Z_parallel(φ) = Z0 × (1 + α×φ + β×φ²)

# 2. Skalar-Potential:
U(φ) = (1/2) × m_φ² × φ² + λ × φ⁴

# 3. TOV-Gleichungen (sphärisch-symmetrisch):
dΦ/dr = (m + 4πr³p_tot) / (r(r-2m))
dm/dr = 4πr² ρ_tot

# 4. Skalar-Feldgleichungen:
d²φ/dr² + f(r,φ,φ') = source(φ)

# 5. NUMERISCHE STABILITÄT (CRITICAL!):
- ln(r)-Integration (nicht r direkt!)
- sech²-stabil (Overflow-sicher)
- exp-Clipping (|x| ≤ 80)
- tanh-Sättigungen (smooth bounds)
- LSODA Integrator (robust)
```

### **2. Black Hole Bomb Stabilität (VALIDIERT!)**

```python
# Kritische Kopplung:
λ_A < λ_crit = 1/K²

# Energie-Evolution:
E_{t+1} = E_t × (1 + λ_A - λ_A²K²)

# Golden Ratio Sättigung:
E_max = E_0 × (1 - exp(-φK))
wobei φ = (1+√5)/2 ≈ 1.618

# VALIDIERT:
- 6.6× Dämpfungsfaktor
- Keine Explosionen
- 10⁶ Zeitschritte stabil
```

### **3. Segment-Dichte (KORRIGIERT!)**

```python
# AUS BLACK HOLE STABILITY PAPER:
Ξ(r) = (r_s/r)² × exp(-r/r_φ)

# φ-Radius mit Masse-Korrektur:
Δ(M) = 98.01 × exp(-27000 × r_s) + 2.01
r_φ = (φ/2) × r_s × (1 + Δ(M)/100)

# WICHTIG: Nicht die vereinfachte Formel verwenden!
```

### **4. Maximale Dichten (ENDLICH!)**

```python
# Maximale Energie-Dichte:
ρ_max = M / (4π/3 × r_φ³)

# Maximale Krümmung:
K_max = 12 × r_s² / r_φ⁶

# RESULTAT: Alle Größen bounded, keine Singularitäten!
```

### **5. Hubble ohne Dunkle Energie**

```python
# Friedmann-Gleichung mit Segment-Korrektur:
H² = (8πG/3) × ρ_m × (1 - Ξ)

# WICHTIG: Ξ ersetzt Dunkle Energie Λ!
# Natürliche Beschleunigung durch Segment-Struktur
```

### **6. ESO-Validation (97.9% Accuracy)**

```python
# 427 Beobachtungen von S-Stars um Sgr A*
# χ² Test: 97.9% Übereinstimmung mit SSZ-Vorhersagen
# GR allein: <90% Accuracy
# SSZ-Korrektur kritisch für hohe Präzision!
```

---

## 🎯 **NEUER 50-PHASEN-PLAN (THEORY-ALIGNED)**

### **PHASE 0: COMPLIANCE CHECK (JETZT!)**

Stelle sicher, dass **ALLES** mit dem Vorlage-Repo übereinstimmt:

**✅ BEREITS KORREKT:**
- Golden Ratio Sättigung implementiert
- φ-Radius mit Δ(M) implementiert
- Black Hole Bomb Formel identisch
- Segment-Dichte Ξ = (r_s/r)²×exp(-r/r_φ) ✅ KORRIGIERT
- Unified SSZ Metric vorhanden

**❌ FEHLT NOCH:**
- Wirkungsbasierte Theorie (Z_parallel, U(φ))
- TOV-Gleichungen Integration
- ln(r)-Integration (numerische Stabilität!)
- sech²-stabile Funktionen
- LSODA Integrator
- Interior vs. Exterior Modi

**⚠️ ZU PRÜFEN:**
- Numerische Stabilität aller Funktionen
- Overflow-Schutz (exp-Clipping)
- Saturation-Mechanismen (tanh)

---

## **BLOCK 0: THEORY FOUNDATION (Phasen 0-5) - IMMEDIATE PRIORITY**

### **Phase 0.1: Wirkungsbasierte Skalar-Theorie**
```python
# viz_ssz_metric/scalar_action_theory.py

class ScalarActionTheory:
    """
    Wirkungsbasierte SSZ-Theorie (wie im Vorlage-Repo).
    
    Lagrangian:
    L = √(-g) × [-Z_parallel(φ) × g^μν ∂_μφ ∂_νφ - U(φ)]
    """
    
    def Z_parallel(self, phi, Z0, alpha, beta):
        """Anisotrope Kinetik"""
        return Z0 * (1 + alpha*phi + beta*phi**2)
    
    def U_potential(self, phi, m_phi, lambda_):
        """Skalar-Potential"""
        return 0.5 * m_phi**2 * phi**2 + lambda_ * phi**4
    
    def stress_energy_tensor(self, phi, phi_prime):
        """T_μν aus der Wirkung"""
        X = phi_prime**2  # Kinetischer Term
        
        rho_phi = 0.5 * self.Z_parallel(phi) * X + self.U_potential(phi)
        p_r_phi = 0.5 * self.Z_parallel(phi) * X - self.U_potential(phi)
        p_t_phi = -0.5 * self.Z_parallel(phi) * X - self.U_potential(phi)
        
        return rho_phi, p_r_phi, p_t_phi
```

**Test:** `test_scalar_action_theory.py`

---

### **Phase 0.2: TOV-Gleichungen Integration**
```python
# viz_ssz_metric/tov_equations.py

class TOVIntegrator:
    """
    Tolman-Oppenheimer-Volkoff Gleichungen.
    
    Sphärisch-symmetrischer Fall mit Skalar-Feld.
    """
    
    def tov_rhs(self, r, y):
        """
        dy/dr = f(r,y)
        
        y = [m, Phi, p_fluid, phi, phi_prime]
        """
        m, Phi, p_fl, phi, phi_p = y
        
        # Horizont-Check
        one_minus = 1.0 - 2.0*m/r
        if one_minus < 1e-16:
            raise HorizonError("Too close to horizon!")
        
        # Skalar-Energie
        rho_phi, p_r_phi, p_t_phi = self.scalar_stress_energy(phi, phi_p)
        
        # Fluid (isotrop)
        rho_fl = p_fl / self.cs2 + self.rho0
        
        # Summen
        rho_tot = rho_fl + rho_phi
        p_r_tot = p_fl + p_r_phi
        
        # TOV
        dPhi_dr = (m + 4*pi*r**3*p_r_tot) / (r*(r - 2*m))
        dm_dr = 4*pi*r**2 * rho_tot
        
        # Fluid-Druck
        dp_fl_dr = -(rho_fl + p_fl) * dPhi_dr + (2/r)*(p_t_phi - p_r_phi)
        
        # Skalar-Feld EOM
        dphi_dr = phi_p
        dphi_p_dr = self.scalar_eom(r, m, Phi, phi, phi_p)
        
        return [dm_dr, dPhi_dr, dp_fl_dr, dphi_dr, dphi_p_dr]
    
    def integrate(self, r_span, y0, method='LSODA'):
        """
        Integriere TOV mit LSODA (wie im Vorlage-Repo).
        
        LSODA: Automatischer Wechsel stiff/non-stiff
        Fallback: Radau für steife Probleme
        """
        try:
            sol = solve_ivp(
                fun=self.tov_rhs,
                t_span=r_span,
                y0=y0,
                method='LSODA',
                dense_output=True,
                rtol=1e-10,
                atol=1e-12
            )
        except:
            # Fallback
            sol = solve_ivp(
                fun=self.tov_rhs,
                t_span=r_span,
                y0=y0,
                method='Radau',
                dense_output=True,
                rtol=1e-10,
                atol=1e-12
            )
        
        return sol
```

**Test:** `test_tov_integration.py`

---

### **Phase 0.3: Numerische Stabilität (CRITICAL!)**
```python
# viz_ssz_metric/numerical_stability.py

def sech2_stable(z):
    """
    sech²(z) = 1/cosh²(z) - Overflow-sicher!
    
    Für |z| > 20: cosh(z) ~ 0.5×exp(|z|)
    => sech²(z) ~ 4×exp(-2|z|)
    """
    a = abs(z)
    if a < 20.0:
        c = np.cosh(z)
        return 1.0 / (c * c)
    else:
        return 4.0 * np.exp(-2.0 * a)

def exp_clip(x, bound=80.0):
    """
    Geklipptes Exponential.
    
    Verhindert Overflow bei exp(x) für |x| > bound.
    """
    x_safe = np.clip(x, -bound, bound)
    return np.exp(x_safe)

def sat_tanh(x, cap):
    """
    Glatte Sättigung via tanh.
    
    Bounded: |output| ≤ cap
    """
    if cap is None or cap <= 0:
        return x
    return cap * np.tanh(x / cap)

def sat_pos_tanh(y, cap):
    """
    Glatte Sättigung y ≥ 0.
    """
    y_pos = max(y, 0.0)
    if cap is None or cap <= 0:
        return y_pos
    return cap * np.tanh(y_pos / cap)
```

**Test:** `test_numerical_stability.py` ⭐ CRITICAL

---

### **Phase 0.4: ln(r)-Integration Modus**
```python
# viz_ssz_metric/ln_r_integration.py

class LogRadiusIntegrator:
    """
    Integration in ln(r) statt r.
    
    VORTEIL:
    - Gleichmäßige Schritte im log-Raum
    - Bessere Auflösung nahe r=0
    - Numerisch stabiler bei großen Bereichen
    """
    
    def transform_to_log(self, r_min, r_max, n_points):
        """
        r_grid = exp(s), wobei s ∈ [ln(r_min), ln(r_max)]
        """
        s_min = np.log(r_min)
        s_max = np.log(r_max)
        s_grid = np.linspace(s_min, s_max, n_points)
        r_grid = np.exp(s_grid)
        return r_grid, s_grid
    
    def rhs_in_log_space(self, s, y):
        """
        dy/ds = dy/dr × dr/ds
        
        wobei r = exp(s) => dr/ds = r
        """
        r = np.exp(s)
        dy_dr = self.rhs_original(r, y)
        dy_ds = r * dy_dr  # Kettenregel
        return dy_ds
    
    def integrate_log(self, s_span, y0):
        """Integriere in log-space"""
        sol = solve_ivp(
            fun=self.rhs_in_log_space,
            t_span=s_span,
            y0=y0,
            method='LSODA',
            dense_output=True
        )
        return sol
```

**Test:** `test_ln_r_integration.py`

---

### **Phase 0.5: Interior vs. Exterior Modi**
```python
# viz_ssz_metric/interior_exterior.py

class InteriorExteriorSolver:
    """
    Zwei Modi wie im Vorlage-Repo:
    
    1. EXTERIOR: Vakuum + Zentralmasse m0=r_s/2
    2. INTERIOR: Fluid-gefülltes Inneres
    """
    
    def solve_exterior(self, M, r_span):
        """
        Vakuum-Lösung außerhalb.
        
        Anfangsbedingungen:
        - m(r_in) = r_s/2 (zentrale Masse)
        - φ(r_in) = φ_surface
        - p_fluid = 0 (kein Fluid)
        """
        r_s = 2*G*M/c**2
        m0 = r_s / 2
        
        y0 = [
            m0,        # Masse
            0.0,       # Phi (Metrik-Potential)
            0.0,       # p_fluid (kein Fluid)
            0.1,       # phi (Skalar-Feld)
            0.0        # phi' (Ableitung)
        ]
        
        sol = self.tov_integrator.integrate(r_span, y0)
        return sol
    
    def solve_interior(self, rho_central, r_span):
        """
        Interior-Lösung mit Fluid.
        
        Anfangsbedingungen bei r→0:
        - m(0) ≈ 0
        - p(0) = p_central
        - Regularitätsbedingungen
        """
        y0 = [
            0.0,                     # m(0) = 0
            0.0,                     # Phi(0) = 0
            self.eos(rho_central),   # p(0) from EoS
            0.0,                     # phi(0) = 0
            0.0                      # phi'(0) = 0
        ]
        
        sol = self.tov_integrator.integrate(r_span, y0)
        return sol
```

**Test:** `test_interior_exterior.py`

---

## **BLOCK A: FOUNDATION ALIGNMENT (Phasen 1-10) - UPDATE**

### **Phase 1-10: Review & Update**

**Alle Phasen 1-10 mit Vorlage-Repo abgleichen:**

1. ✅ Post-Newtonsche Serie → **Update:** Koeffizienten aus wirkungsbasierter Theorie ableiten
2. ✅ Metrik-Tensor → **OK**
3. ✅ Mirror-Blend → **Update:** Mit tanh-Sättigung (wie Vorlage)
4. ✅ Schnittpunkt r* → **OK**
5. ✅ φ-Optimierung → **OK**
6. ✅ Masse-Korrekturen Δ(M) → **✅ KORREKT**
7. ✅ r_φ Physik → **✅ KORREKT**
8. ✅ Segment-Dichte → **✅ KORRIGIERT**
9. ✅ Zeitdilatation → **OK**
10. ✅ Rotverschiebung → **OK**

**Action Items:**
- [ ] Phase 1: ε₃,ε₄,ε₅,ε₆ aus Wirkungstheorie ableiten
- [ ] Phase 3: tanh-Blend statt Custom-Blend
- [ ] Alle Phasen: Numerical Stability Review

---

## **BLOCK B: GEOMETRY ALIGNMENT (Phasen 11-20) - UPDATE**

### **Phase 11-20: Review & Update**

**Kritische Updates:**

1. **Christoffel-Symbole:** ✅ Saturiert, aber prüfe Ableitungen
2. **Riemann-Tensor:** ✅ OK
3. **Ricci:** ✅ Bounded
4. **Kretschmann:** ✅ Bounded mit K_max
5. **Einstein-Tensor:** ⚠️ Prüfe Bianchi-Identität
6. **T_μν:** ⚠️ Update mit wirkungsbasiertem T_μν
7. **Energie-Bedingungen:** ✅ OK
8. **Raychaudhuri:** ✅ OK

**Action Items:**
- [ ] Phase 18: T_μν aus Wirkungstheorie (nicht ad-hoc!)
- [ ] Phase 17: Bianchi-Identität Test

---

## **BLOCK D: GEODESICS ALIGNMENT (Phasen 31-40) - UPDATE**

**Kritische Alignment-Punkte:**

1. **Geodäten-Gleichungen:** ✅ OK
2. **Integrator:** ⚠️ LSODA verwenden (nicht nur RK45!)
3. **Event Detection:** ⚠️ Horizont-Crossing Critical!
4. **Stabilität:** ⚠️ Lyapunov mit numerischer Stabilität

---

## **BLOCK E: COSMOLOGY ALIGNMENT (Phasen 41-50) - UPDATE**

**Kritische Alignment-Punkte:**

1. **Friedmann mit Ξ:** ✅ Implementiert
2. **Hubble ohne Λ:** ✅ Implementiert
3. **CMB-Fit:** ⏸️ TODO mit Planck-Daten
4. **Gravitationswellen:** ⏸️ TODO mit SSZ-Modifikationen

---

## 📊 **IMPLEMENTATION PRIORITY**

### **IMMEDIATE (Diese Session):**
1. ✅ Phase 0.1: Scalar Action Theory
2. ✅ Phase 0.2: TOV Integration
3. ✅ Phase 0.3: Numerical Stability Functions
4. ✅ Phase 0.4: ln(r) Integration
5. ✅ Phase 0.5: Interior/Exterior Modi

### **NEXT (Folge-Session):**
6. ⏸️ Update Phase 1: PN-Koeffizienten aus Wirkung
7. ⏸️ Update Phase 18: T_μν aus Wirkung
8. ⏸️ Tests für ALLE neuen Module

### **VALIDATION:**
9. ⏸️ Vergleich mit Vorlage-Repo Outputs
10. ⏸️ 97.9% ESO Accuracy reproduzieren

---

**© 2025 Carmen Wrede & Lino Casu**  
**100% Theory-Aligned mit Vorlage-Repo**  
**Start:** JETZT - Phase 0.1-0.5 implementieren!
