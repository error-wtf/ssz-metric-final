# VOLLSTÄNDIGE LÜCKEN-ANALYSE & FAHRPLAN

**Datum:** 31. Oktober 2025, 16:00 UTC+01:00  
**Status:** 74% erfüllt, 26% fehlt

---

## EXECUTIVE SUMMARY

```
VORHANDEN:  74% ██████████████░░░░
FEHLEND:    26% █████░░░░░░░░░░░░░

Kritisch:    12% (MUSS)
Wichtig:     10% (SOLLTE)
Optional:     4% (KANN)
```

**Gesamt-Aufwand:** ~18-24 Stunden

---

## WAS FEHLT - KRITISCH

### 1. ppn.py - PPN-Modul (2.5h) ⭐⭐⭐⭐⭐

**Was:** Isotrope Koordinaten, γ/β Extraktion, Solar-System Observables

**Akzeptanz:** |γ-1|, |β-1| < 1e-6

---

### 2. GIF-Visualisierungen (4h) ⭐⭐⭐⭐⭐

**Fehlend:**
- gif_A() - A(r) Sweep (45min)
- gif_K() - Krümmungs-Proxy (1h + K_proxy implementieren)
- gif_lens() - Lensing (1.5h)
- gif_wave() - Wavepacket (1.5h)

**Akzeptanz:** 5 GIFs in docs/figures/

---

### 3. test_ppn.py (1h) ⭐⭐⭐⭐

**Was:** Tests für γ, β, isotrope Koords

---

## WAS FEHLT - WICHTIG

### 4. Jupyter Notebooks (3h) ⭐⭐⭐

**Fehlend:** 5 Notebooks (00-40)

---

### 5. qnm_wkb.py (2h) ⭐⭐⭐

**Was:** WKB-Approximation, Regge-Wheeler Potential

---

### 6. docs/ Struktur (1.5h) ⭐⭐⭐

**Was:** 30+ MDs organisieren, docs/ Struktur

---

## WAS FEHLT - OPTIONAL

### 7. Shadow-Radius (1h) ⭐⭐
### 8. K_proxy (30min) ⭐
### 9. Performance (2h) ⭐

---

## FAHRPLAN

### PHASE 1: KRITISCHES (8.75h)
```
1. ppn.py                  2.5h
2. test_ppn.py             1h
3. gif_A()                 0.75h
4. gif_K() + K_proxy       1.5h
5. gif_lens()              1.5h
6. gif_wave()              1.5h
```

**Ergebnis:** 88% (Prompt erfüllt)

---

### PHASE 2: WICHTIGES (7h)
```
7. qnm_wkb.py              2h
8. test_qnm_toy.py         0.5h
9. 5 Notebooks             3h
10. docs/ Struktur         1.5h
```

**Ergebnis:** 98% (Voll nutzbar)

---

### PHASE 3: POLISH (3h)
```
11. Shadow-Radius          1h
12. Performance            2h
```

**Ergebnis:** 100% (Perfekt)

---

## TIMELINE

```
Minimum (Phase 1):     ~9h  → 88%
Empfohlen (Phase 1+2): ~16h → 98%
Perfektion (Alle):     ~19h → 100%
```

---

## NÄCHSTER SCHRITT

**START:** ppn.py implementieren (2.5h)

**ETA:** 9h bis Prompt-erfüllt, 16h bis voll nutzbar

---

**© 2025 Carmen Wrede & Lino Casu**
