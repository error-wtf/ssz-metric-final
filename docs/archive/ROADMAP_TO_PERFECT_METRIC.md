# ROADMAP TO PERFECT METRIC - 100% Vollständigkeit

**Von 72% → 100% in 3 Phasen**  
**Datum:** 31. Oktober 2025, 18:00 UTC+01:00

---

## EXECUTIVE SUMMARY

```
Aktuell:  72/100  ██████████████░░░░░░░░░░
Ziel:    100/100  ████████████████████████

Fehlend: 28 Punkte = 12 Stunden Arbeit

PHASE A: Geodäten (6h)      →  +15 Punkte  →  87%
PHASE B: Observables (4h)   →  +10 Punkte  →  97%
PHASE C: Polish (2h)        →   +3 Punkte  → 100%
```

---

## PHASE A: GEODÄTEN & ORBITS (6h)

**Ziel:** Von 72% → 87%

### Task A1: Geodäten-Gleichungen (2.5h)

**File:** `viz_ssz_metric/geodesics_unified.py`

**Implementation:**
1. GeodesicSolver Klasse (1h)
2. Integration timelike/null (1h)
3. Tests (30min)

**Deliverable:** Geodäten-Integration funktioniert ✅

---

### Task A2: Photon Sphere & ISCO (2h)

**File:** `viz_ssz_metric/unified_metric.py`

**Add Methods:**
```python
def photon_sphere_radius(self) -> float
def ISCO_radius(self, prograde=True) -> float
```

**Deliverable:** Kritische Radien berechnet ✅

---

### Task A3: Perihelion Precession (1.5h)

**Add Method:**
```python
def perihelion_precession(self, a, e) -> float
def perihelion_precession_arcsec_per_century(self, a, e, P) -> float
```

**Test:** Merkur Perihel = 43 arcsec/century

**Deliverable:** Perihel-Präzession ✅

---

## PHASE B: OBSERVABLES (4h)

**Ziel:** Von 87% → 97%

### Task B1: Shadow Radius (1.5h)

**Add Methods:**
```python
def shadow_radius(self, observer_distance=None) -> float
def shadow_angular_size_microarcsec(self, distance_pc) -> float
def compare_with_EHT(self, observed, distance) -> Dict
```

**Test:** Sgr A* Shadow = 51.8 μas

**Deliverable:** EHT-Vergleich möglich ✅

---

### Task B2: Quasi-Normal Modes (2h)

**Add Methods:**
```python
def quasi_normal_modes(self, l=2, n=0) -> Tuple[float, float]
def ringdown_time(self, l=2, n=0) -> float
```

**Integration:** Use qnm_wkb.py module

**Deliverable:** QNM frequencies ✅

---

### Task B3: Kretschmann Scalar (30min)

**Add Method:**
```python
def kretschmann_scalar(self, r, theta) -> float
```

**Integration:** Use curvature_proxy.py

**Deliverable:** Krümmungs-Invariante ✅

---

## PHASE C: POLISH & INTEGRATION (2h)

**Ziel:** Von 97% → 100%

### Task C1: Hawking Temperature (1h)

**Add Methods:**
```python
def hawking_temperature(self) -> float
def hawking_luminosity(self) -> float
def evaporation_time(self) -> float
```

**Deliverable:** Hawking Radiation ✅

---

### Task C2: Documentation (30min)

- Docstrings für alle neuen Methoden
- Update README.md
- Add examples/

**Deliverable:** Dokumentation komplett ✅

---

### Task C3: Integration Tests (30min)

**File:** `tests/test_unified_metric_complete.py`

**Test:**
- Alle Features zusammen
- Konsistenz-Checks
- Performance-Tests

**Deliverable:** 100% Test-Coverage ✅

---

## ZEITPLAN

```
TAG 1 (6h): Phase A - Geodäten
  09:00-11:00  A1: Geodäten-Gleichungen
  11:00-13:00  A2: Photon Sphere & ISCO
  14:00-15:30  A3: Perihelion Precession
  15:30-16:00  Tests & Review

TAG 2 (4h): Phase B - Observables
  09:00-10:30  B1: Shadow Radius
  10:30-12:30  B2: QNM
  13:00-13:30  B3: Kretschmann
  13:30-14:00  Tests & Review

TAG 3 (2h): Phase C - Polish
  09:00-10:00  C1: Hawking Temperature
  10:00-10:30  C2: Documentation
  10:30-11:00  C3: Integration Tests
  11:00-12:00  Final Review & Polish
```

**TOTAL:** 12 Stunden = 3 Tage (4h/Tag)

---

## PRIORITY ORDER

```
⭐⭐⭐⭐⭐ CRITICAL (must-have):
1. A1 Geodäten-Gleichungen
2. A2 Photon Sphere
3. B1 Shadow Radius

⭐⭐⭐⭐ HIGH (should-have):
4. A3 Perihelion Precession
5. B2 QNM
6. A2 ISCO

⭐⭐⭐ MEDIUM (nice-to-have):
7. B3 Kretschmann
8. C1 Hawking Temperature

⭐⭐ LOW (optional):
9. C2 Documentation
10. C3 Tests
```

---

## DELIVERABLES

### After Phase A (+15 points → 87%):
- ✅ Geodäten-Integration
- ✅ Photon Sphere berechnet
- ✅ ISCO berechnet
- ✅ Perihel-Präzession
- ✅ Orbital mechanics

### After Phase B (+10 points → 97%):
- ✅ Shadow Radius für EHT
- ✅ QNM frequencies
- ✅ Ringdown time
- ✅ Kretschmann scalar

### After Phase C (+3 points → 100%):
- ✅ Hawking Temperature
- ✅ Complete Documentation
- ✅ 100% Test Coverage
- ✅ **PERFECT METRIC!**

---

## DEPENDENCIES

```
Phase A:
  A1 → A2 (Geodäten needed for Photon Sphere)
  A2 → A3 (Photon Sphere needed for Precession)

Phase B:
  A2 → B1 (Photon Sphere needed for Shadow)
  A1 → B2 (Geodäten needed for QNM)

Phase C:
  A + B → C (All features needed for polish)
```

---

## FILES TO CREATE/MODIFY

**New Files:**
```
viz_ssz_metric/geodesics_unified.py       # Geodäten-Integration
tests/test_geodesics_unified.py           # Geodäten-Tests
tests/test_observables.py                 # Shadow, QNM Tests
examples/example_complete_metric.py       # Demo
```

**Modified Files:**
```
viz_ssz_metric/unified_metric.py          # Add all methods
viz_ssz_metric/__init__.py                # Export new classes
tests/test_unified_metric.py              # Update tests
README.md                                  # Update documentation
```

---

## SUCCESS CRITERIA

```
✅ Geodäten: radial, circular, null alle funktionieren
✅ Photon Sphere: < 5% Abweichung von GR
✅ ISCO: < 10% Abweichung von GR
✅ Perihel: Merkur = 43±2 arcsec/century
✅ Shadow: Sgr A* = 51.8±7 μas
✅ QNM: Ringdown-Zeit plausibel
✅ Tests: 100% pass
✅ Dokumentation: vollständig
```

---

## ROADMAP EXECUTION

**START:** Tag 1, 09:00
**END:** Tag 3, 12:00
**RESULT:** 100% Perfect Metric!

---

**© 2025 Carmen Wrede & Lino Casu**

**Status:** ✅ Roadmap Ready  
**ETA:** 3 Tage (4h/Tag)  
**Ziel:** 100% Vollständige SSZ-Metrik
