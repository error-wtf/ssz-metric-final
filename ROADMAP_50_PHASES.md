# 50-Phasen-Fahrplan: Vollständige SSZ-Metrik für die Astrophysik

**Ziel:** Komplette, wissenschaftlich rigorose SSZ-Metrik die ALLE astrophysikalischen Szenarien abdeckt

**Status:** 🚧 In Arbeit  
**Autoren:** Carmen Wrede & Lino Casu  
**Start:** 31. Oktober 2025

---

## 📋 **Übersicht der 50 Phasen**

### **Block A: Fundamentale Metrik (Phasen 1-10)**
- [x] Phase 1: Post-Newtonsche Serie A(r) = 1-2U+2U²+ε₃U³ ✅
- [x] Phase 2: Vollständiger Tensor g_μν (diagonal, statisch) ✅
- [x] Phase 3: Mirror-Blend für starke Felder (A_safe) ✅
- [x] Phase 4: Schnittpunkt r* (high-precision) ✅
- [ ] Phase 5: Höhere Ordnungen U⁴, U⁵, ... (erweiterte Serie)
- [ ] Phase 6: φ-Abhängigkeit in Metrik (variable Golden Ratio)
- [ ] Phase 7: Masse-abhängige Korrekturen Δ(M)
- [ ] Phase 8: Natürliche Grenze r_φ = φ·GM/c²
- [ ] Phase 9: Segment-Dichte Ξ(r) exakte Integration
- [ ] Phase 10: Zeitdilatation D(r) vs. Koordinatenzeit

### **Block B: Geometrie & Krümmung (Phasen 11-20)**
- [ ] Phase 11: Christoffel-Symbole Γ^μ_νρ (symbolisch)
- [ ] Phase 12: Riemann-Tensor R^μ_νρσ
- [ ] Phase 13: Ricci-Tensor R_μν
- [ ] Phase 14: Ricci-Skalar R
- [ ] Phase 15: Kretschmann-Skalar K = R_μνρσ R^μνρσ
- [ ] Phase 16: Weyl-Tensor C^μ_νρσ (Gezeitenfeld)
- [ ] Phase 17: Einstein-Tensor G_μν
- [ ] Phase 18: Energie-Impuls-Tensor T_μν (effektiv)
- [ ] Phase 19: Energie-Bedingungen (WEC/DEC/SEC)
- [ ] Phase 20: Raychaudhuri-Gleichung

### **Block C: Rotation & Kerr-SSZ (Phasen 21-30)**
- [ ] Phase 21: Kerr-Metrik Basis (Boyer-Lindquist)
- [ ] Phase 22: SSZ-Kerr: Rotation + Segment-Dichte
- [ ] Phase 23: Spin-Parameter a = J/(Mc)
- [ ] Phase 24: Ergo-Sphäre in SSZ
- [ ] Phase 25: Frame-Dragging (Lense-Thirring)
- [ ] Phase 26: ISCO (Innermost Stable Circular Orbit) für a≠0
- [ ] Phase 27: Photonensphäre bei Rotation
- [ ] Phase 28: Schwarzschild-Shadow vs. Kerr-Shadow
- [ ] Phase 29: Akkretionsscheiben-Geometrie
- [ ] Phase 30: Gravitomagnetischer Effekt

### **Block D: Geodäten & Bewegung (Phasen 31-40)**
- [ ] Phase 31: Geodätengleichungen d²x^μ/dλ² + Γ dx dx = 0
- [ ] Phase 32: Numerischer Integrator (RK45)
- [ ] Phase 33: Zeitartige Geodäten (massive Teilchen)
- [ ] Phase 34: Nullgeodäten (Photonen)
- [ ] Phase 35: Perihel-Präzession Δφ
- [ ] Phase 36: Lichtablenkung α(b)
- [ ] Phase 37: Shapiro-Delay Δt
- [ ] Phase 38: Orbit-Stabilität (Lyapunov-Exponenten)
- [ ] Phase 39: Chaotische Bahnen nahe r_φ
- [ ] Phase 40: Escape-Velocity vs. Dual-Velocity

### **Block E: Kosmologie & Große Skalen (Phasen 41-50)**
- [ ] Phase 41: Friedmann-Metrik SSZ (FLRW-ähnlich)
- [ ] Phase 42: Hubble-Parameter H(t) mit Segment-Dichte
- [ ] Phase 43: Beschleunigung ä(t) (Dunkle Energie Proxy)
- [ ] Phase 44: CMB-Spektrum (Planck-Daten)
- [ ] Phase 45: BAO (Baryon Acoustic Oscillations)
- [ ] Phase 46: Strukturbildung (Jeans-Länge in SSZ)
- [ ] Phase 47: Gravitationswellen h_μν (Linearisierung)
- [ ] Phase 48: Multi-Body Gravitation (N-Körper)
- [ ] Phase 49: Hawking-Radiation Proxy T_H
- [ ] Phase 50: Vereinheitlichung GR↔SSZ↔Quantum

---

## 🔧 **Detaillierte Phasen-Beschreibung**

### **PHASE 1: Post-Newtonsche Serie** ✅ COMPLETED

**Ziel:** A(r) = 1 - 2U + 2U² + ε₃U³

**Implementiert in:**
- `viz_ssz_metric/ssz_mirror_metric.py:209-252`
- Funktion: `metric_functions_pn(mass, r)`

**Test:** `test_post_newtonian_series()` ✅

**Status:** ✅ **Abgeschlossen**

---

### **PHASE 2: Vollständiger Tensor g_μν** ✅ COMPLETED

**Ziel:** 4×4 metrischer Tensor (diagonal, statisch)

**Implementiert in:**
- `viz_ssz_metric/ssz_mirror_metric.py:255-294`
- Funktion: `metric_tensor(mass, r, theta)`

**Komponenten:**
```
g_tt = -A(r)
g_rr = B(r) = 1/A(r)
g_θθ = r²
g_φφ = r²sin²θ
```

**Test:** `test_metric_tensor_components()` ✅

**Status:** ✅ **Abgeschlossen**

---

### **PHASE 3: Mirror-Blend (starke Felder)** ✅ COMPLETED

**Ziel:** Singularitätsfreie Metrik A_safe > 0

**Implementiert in:**
- `viz_ssz_metric/ssz_mirror_metric.py:118-157`
- Funktion: `A_safe(r, rs, varphi)`

**Methode:**
- tanh-Übergang am Schnittpunkt r*
- Softplus-Floor: A_safe = ε + (1/β)·ln(1+exp(β·(A_mix-ε)))

**Test:** `test_A_safe_positive_and_farfield()` ✅

**Status:** ✅ **Abgeschlossen**

---

### **PHASE 4: Schnittpunkt r*** ✅ COMPLETED

**Ziel:** High-precision Lösung von sqrt(1-1/u) = 1/(2-exp(-φu))

**Implementiert in:**
- `viz_ssz_metric/ssz_mirror_metric.py:326-393`
- Funktion: `intersection_time_dilation(varphi)`

**Methode:** mpmath.findroot() mit ≥12 Dezimalstellen

**Referenzwerte:**
- φ=1.0: u*=1.4689714056, D*=0.5650235
- φ=φ: u*=1.3865616196, D*=0.5280071

**Test:** `test_intersection_high_precision()` ✅

**Status:** ✅ **Abgeschlossen**

---

### **PHASE 5: Höhere Ordnungen U⁴, U⁵**

**Ziel:** Erweiterte Post-Newtonsche Serie für bessere Genauigkeit

**Aufgaben:**
1. Berechne ε₄, ε₅ aus SSZ-Theorie
2. Erweitere `metric_functions_pn()`:
   ```python
   A(r) = 1 - 2U + 2U²+ ε₃U³ + ε₄U⁴ + ε₅U⁵ + ...
   ```
3. Validiere Konvergenz für r > 2r_s
4. Vergleiche mit numerischer Integration

**Benötigte Inputs:**
- Segment-Dichte Ξ(r) höhere Ableitungen
- φ-Struktur in Korrekturen

**Datei:** `viz_ssz_metric/higher_order_pn.py` (neu)

**Status:** 🚧 **Pending**

---

### **PHASE 6: φ-Abhängigkeit in Metrik**

**Ziel:** Variable Golden Ratio als Parameter

**Aufgaben:**
1. Koeffizienten als Funktionen von φ:
   ```python
   ε₃(φ) = -24/5 · f(φ)  # f(φ) zu bestimmen
   ```
2. Sensitivitätsanalyse: dA/dφ
3. Optimaler φ-Wert für verschiedene Massen

**Datei:** `viz_ssz_metric/phi_variation.py` (neu)

**Status:** 🚧 **Pending**

---

### **PHASE 7: Masse-abhängige Korrekturen Δ(M)**

**Ziel:** Implementiere Δ(M) = A·exp(-α·r_s) + B aus archiviertem Repo

**Formel (aus Theorie):**
```python
delta_M = 98.01 * exp(-27000 * r_s(M)) + 2.01
r_phi = PHI * (G*M/c²) * (1 + delta_M/100)
```

**Aufgaben:**
1. Berechne r_φ(M) für verschiedene Massen
2. Integriere in Metrik-Funktionen
3. Grenzfälle: M→0 (Δ→100%), M→∞ (Δ→2%)

**Datei:** `viz_ssz_metric/mass_corrections.py` (neu)

**Status:** 🚧 **Pending**

---

### **PHASE 8: Natürliche Grenze r_φ**

**Ziel:** Physikalische Bedeutung der φ-Radius-Grenze

**Aufgaben:**
1. Berechne r_φ vs. r_s Verhältnis
2. Maximale Dichte N_max bei r_φ
3. Vergleich mit Schwarzschild-Horizon
4. Segment-Sättigung

**Physikalische Interpretation:**
- r_φ ≈ 0.809·r_s (für Δ=2%)
- SSZ-Horizont INNERHALB GR-Horizont

**Datei:** `viz_ssz_metric/natural_boundary.py` (neu)

**Status:** 🚧 **Pending**

---

### **PHASE 9: Segment-Dichte Ξ(r) exakte Integration**

**Ziel:** Präzise Berechnung der Segment-Dichte

**Formel:**
```python
Xi(r) = Xi_max * (1 - exp(-phi * r / r_s))
N(r) = N_0 * Xi(r)  # Absolute Dichte
```

**Aufgaben:**
1. Integration ∫ Ξ(r) dr für Masse
2. Ableitungen dΞ/dr, d²Ξ/dr²
3. Lokale vs. globale Segment-Zahl
4. Vergleich mit Kerndichte ρ_nuc

**Datei:** `viz_ssz_metric/segment_density.py` (neu)

**Status:** 🚧 **Pending**

---

### **PHASE 10: Zeitdilatation D(r) Koordinatenzeit**

**Ziel:** Vollständige Analyse der Zeitdilatation

**Zwei Formulierungen:**
1. **Aus Metrik:** D_PN = √A(r)
2. **Aus Segmenten:** D_SSZ = 1/(1+Ξ)

**Aufgaben:**
1. Vergleich D_PN ↔ D_SSZ
2. Differenz Δ(r) = D_PN - D_SSZ
3. Physikalische Interpretation
4. Uhren-Experiment Vorhersage

**Datei:** `viz_ssz_metric/time_dilation_analysis.py` (neu)

**Status:** 🚧 **Pending**

---

## 📊 **Fortschritt**

**Abgeschlossen:** 4/50 (8%)  
**In Arbeit:** 0/50  
**Pending:** 46/50 (92%)

---

**Nächste Schritte:** Ich beginne jetzt mit Phase 5...

