# FAHRPLÄNE ÜBERSICHT - 3 Stufen zur Perfektion

**Von 72% → 100% in 3 Schritten**

---

## STRUKTUR

```
FAHRPLAN 1: MINIMAL (4h)      →  72% → 85%  [KRITISCH]
FAHRPLAN 2: ERWEITERT (5h)    →  85% → 95%  [WICHTIG]
FAHRPLAN 3: PERFEKT (2h)      →  95% → 100% [POLISH]

TOTAL: 11 Stunden → 100% Perfekte Metrik
```

---

## FAHRPLAN 1: MINIMAL (4h) ⭐⭐⭐⭐⭐

**Datei:** `FAHRPLAN_1_MINIMAL.md`

### Was wird implementiert:
- ✅ **Photon Sphere** (1h)
  - photon_sphere_radius()
  - Test mit GR Vergleich
  
- ✅ **Shadow Radius** (1.5h)
  - shadow_radius()
  - shadow_microarcsec()
  - compare_with_EHT()
  - Test mit Sgr A* (51.8 μas)
  
- ✅ **Geodäten-Basis** (1.5h)
  - geodesics_minimal.py
  - integrate_radial_infall()
  - test_orbit_stability()

### Ergebnis:
```
Vorher:  72/100
Nachher: 85/100
+13 Punkte

Kritische Features vorhanden ✅
Basis-Funktionsfähigkeit erreicht ✅
```

---

## FAHRPLAN 2: ERWEITERT (5h) ⭐⭐⭐⭐

**Datei:** `FAHRPLAN_2_ERWEITERT.md`

### Was wird implementiert:
- ✅ **QNM** (2h)
  - quasi_normal_modes_wkb()
  - ringdown_time()
  - qnm_frequency_hz()
  - Tests mit Masse-Skalierung
  
- ✅ **Perihelion Precession** (1.5h)
  - perihelion_precession_arcsec_per_century()
  - Test mit Merkur (43 arcsec/century)
  - SSZ-Korrektur
  
- ✅ **ISCO** (1h)
  - ISCO_radius()
  - ISCO_correction()
  - Test prograde/retrograde
  
- ✅ **Validation Suite** (30min)
  - Alle Tests zusammen
  - Sgr A* Observables

### Ergebnis:
```
Vorher:  85/100
Nachher: 95/100
+10 Punkte

Wissenschaftliche Observables komplett ✅
EHT + LIGO validierbar ✅
```

---

## FAHRPLAN 3: PERFEKT (2h) ⭐⭐⭐

**Datei:** `FAHRPLAN_3_PERFEKT.md`

### Was wird implementiert:
- ✅ **Hawking Radiation** (1h)
  - hawking_temperature()
  - hawking_luminosity()
  - evaporation_time()
  
- ✅ **Kretschmann Integration** (30min)
  - kretschmann_scalar()
  - Integration mit curvature_proxy
  
- ✅ **Documentation** (30min)
  - README.md Update
  - examples/complete_demo.py
  - Usage guide

### Ergebnis:
```
Vorher:  95/100
Nachher: 100/100
+5 Punkte

PERFEKTE METRIK! ✅
Alle Features vorhanden ✅
Vollständig dokumentiert ✅
```

---

## ZEITPLAN

### Option A: Marathon (11h an 1-2 Tagen)
```
Tag 1 (6h):  Fahrplan 1 + Fahrplan 2 Start
Tag 2 (5h):  Fahrplan 2 Ende + Fahrplan 3
```

### Option B: Wochenplan (3 Tage)
```
Tag 1 (4h):  Fahrplan 1 - Minimal
Tag 2 (5h):  Fahrplan 2 - Erweitert
Tag 3 (2h):  Fahrplan 3 - Perfekt
```

### Option C: Entspannt (5 Tage à 2-3h)
```
Tag 1:  Photon Sphere + Shadow Start
Tag 2:  Shadow Ende + Geodäten
Tag 3:  QNM
Tag 4:  Perihelion + ISCO
Tag 5:  Hawking + Docs
```

---

## FEATURE-MATRIX

| Feature | Fahrplan | Zeit | Punkte | Priorität |
|---------|----------|------|--------|-----------|
| **Photon Sphere** | 1 | 1h | +5 | ⭐⭐⭐⭐⭐ |
| **Shadow Radius** | 1 | 1.5h | +5 | ⭐⭐⭐⭐⭐ |
| **Geodäten-Basis** | 1 | 1.5h | +3 | ⭐⭐⭐⭐⭐ |
| **QNM** | 2 | 2h | +3 | ⭐⭐⭐⭐ |
| **Perihelion** | 2 | 1.5h | +4 | ⭐⭐⭐⭐ |
| **ISCO** | 2 | 1h | +3 | ⭐⭐⭐⭐ |
| **Hawking** | 3 | 1h | +2 | ⭐⭐⭐ |
| **Kretschmann** | 3 | 30min | +1 | ⭐⭐ |
| **Documentation** | 3 | 30min | +2 | ⭐⭐⭐ |

---

## DEPENDENCIES

```
Fahrplan 1:
  Task 1 (Photon Sphere)
    ↓
  Task 2 (Shadow Radius) ← benötigt Photon Sphere
    ↓
  Task 3 (Geodäten-Basis) ← unabhängig

Fahrplan 2:
  Task 4 (QNM) ← benötigt metric_function_A
    ↓
  Task 5 (Perihelion) ← benötigt metric_function_A
    ↓
  Task 6 (ISCO) ← benötigt metric_function_A
    ↓
  Task 7 (Validation) ← benötigt alle obigen

Fahrplan 3:
  Task 8 (Hawking) ← benötigt r_s
    ↓
  Task 9 (Kretschmann) ← benötigt ricci_scalar
    ↓
  Task 10 (Docs) ← benötigt alle Features
```

---

## AUSFÜHRUNGS-STRATEGIE

### Start mit Fahrplan 1:
```bash
cd E:\clone\ssz-full-metric

# Öffne Fahrplan 1
code FAHRPLAN_1_MINIMAL.md

# Folge Schritt für Schritt
# Nach jedem Task: Test ausführen
# Am Ende: Alle 3 Tests grün
```

### Dann Fahrplan 2:
```bash
# Nach erfolgreicher Completion von Fahrplan 1
code FAHRPLAN_2_ERWEITERT.md

# Implementiere Task 4-7
# Tests nach jedem Task
```

### Abschluss mit Fahrplan 3:
```bash
# Nach Fahrplan 1 + 2
code FAHRPLAN_3_PERFEKT.md

# Task 8-10
# Final validation
# FERTIG! 100%
```

---

## ERFOLGS-KRITERIEN

### Nach Fahrplan 1: ✅
```
□ photon_sphere_radius() funktioniert
□ shadow_microarcsec() funktioniert
□ Sgr A* Shadow innerhalb 15% von EHT
□ Geodäten-Basis funktioniert
□ Alle Tests grün
```

### Nach Fahrplan 2: ✅
```
□ QNM gibt plausible Werte
□ Merkur Precession = 43±2 arcsec/century
□ ISCO bei ~3 r_s
□ Alle neuen Tests grün
```

### Nach Fahrplan 3: ✅
```
□ Hawking Temperature berechnet
□ Kretschmann implementiert
□ Dokumentation vollständig
□ examples/complete_demo.py läuft
□ 100% aller Tests grün
□ PERFEKT!
```

---

## HILFE & SUPPORT

### Bei Problemen:
1. Check `CODE_TEMPLATES_FOR_COMPLETION.md`
2. Check `QUICKSTART_COMPLETION.md`
3. Check `METRIC_COMPLETENESS_CHECK.md`

### Debug Commands:
```python
# Check was existiert:
from viz_ssz_metric.unified_metric import UnifiedSSZMetric
metric = UnifiedSSZMetric(mass=1.98847e30)
print(dir(metric))

# Test einzelne Feature:
r_ph = metric.photon_sphere_radius()
print(f"Works: {r_ph/metric.r_s:.3f} r_s")
```

---

## NÄCHSTER SCHRITT

**JETZT STARTEN MIT:**

```bash
# Fahrplan 1 öffnen
code E:\clone\ssz-full-metric\FAHRPLAN_1_MINIMAL.md

# Task 1 beginnen: Photon Sphere
# ETA: 4 Stunden → 85%
```

**DANN IN DEN NÄCHSTEN 5 PROMPTS:**

```
Prompt 1: Fahrplan 1 - Task 1-2 (Photon Sphere + Shadow)
Prompt 2: Fahrplan 1 - Task 3 + Check (Geodäten + Validation)
Prompt 3: Fahrplan 2 - Task 4-5 (QNM + Perihelion)
Prompt 4: Fahrplan 2 - Task 6-7 + Fahrplan 3 Start (ISCO + Hawking)
Prompt 5: Fahrplan 3 - Task 9-10 + Final Check (Docs + Validation)
```

---

**© 2025 Carmen Wrede & Lino Casu**

**Status:** ✅ 3 FAHRPLÄNE READY  
**Total ETA:** 11 Stunden  
**Ziel:** 100% Perfekte SSZ-Metrik  
**Los geht's!** 🚀
