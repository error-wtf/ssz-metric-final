# MASTER ROADMAP TO PERFECTION

**Von 74% → 100% in 3 Phasen**  
**Datum:** 31. Oktober 2025

---

## ÜBERSICHT

```
PHASE 1: CRITICAL    20h (7d)  →  95%  ⭐⭐⭐⭐⭐
PHASE 2: EXCELLENCE  15h (5d)  →  98%  ⭐⭐⭐
PHASE 3: BEYOND      50h (15d) → 100%+ ⭐⭐
```

---

## PHASE 1: CRITICAL (20h)

### TAG 1-2: VALIDIERUNG (5h) ⭐⭐⭐⭐⭐

#### Tag 1 Vormittag (3h): ESO S-Stars
1. Daten kopieren (30min)
2. eso_validation.py erstellen (1.5h)
3. Test: 97.9% Accuracy (1h)

#### Tag 1 Nachmittag (2h): Black Hole Bomb
1. black_hole_bomb.py erstellen (1.5h)
2. Test: η = 6.6× Dämpfung (30min)

**Deliverable:** ESO + BH Bomb validiert ✅

---

### TAG 2: QNM & NOTEBOOKS (4.5h) ⭐⭐⭐⭐

#### Vormittag (2.5h): QNM
1. qnm_wkb.py (2h)
2. test_qnm_toy.py (30min)

#### Nachmittag (2h): Notebooks
1. 00_overview.ipynb (20min)
2. 10_intersection.ipynb (20min)
3. 20_metric_profiles.ipynb (30min)
4. 30_energy_ppn.ipynb (30min)
5. 40_geodesics_shadow.ipynb (30min)

**Deliverable:** QNM + 5 Notebooks ✅

---

### TAG 3-7: LATEX PAPER (8h) ⭐⭐⭐⭐⭐

**2h/Tag, an 4 Tagen verteilt:**

- Tag 3: Structure + Abstract (2h)
- Tag 4: Mathematical Framework (2h)
- Tag 5: Implementation + Validation (2h)
- Tag 6: Results (1h)
- Tag 7: Discussion + Conclusion (1h)

**Deliverable:** 20-Seiten Paper ✅

---

### TAG 7: FINALIZE (30min)

```bash
pytest -q tests/
python validation/eso_validation.py
python validation/black_hole_bomb.py
python -m viz_ssz_metric.sszviz_cli gif --kind all
```

**Checklist:**
- [ ] Tests grün
- [ ] ESO 97.9% ✅
- [ ] BH Bomb 6.6× ✅
- [ ] 5 GIFs
- [ ] 5 Notebooks
- [ ] Paper 20 Seiten

**→ 95% Publication-Ready!**

---

## PHASE 2: EXCELLENCE (15h)

### TAG 8: FIGURES (2h)
- 7 High-Res Figures (EPS, 300 DPI)
- Fig 1-7: Metric, Ξ, ESO, BH Bomb, Energy, 3D

### TAG 9: SUPPLEMENTARY (2h)
- supplementary.pdf
- Code repo links
- Reproduction instructions

### TAG 10: VISUALISIERUNG (5h)
- Dashboard mit Dash/Plotly (3h)
- 3D Plots WebGL (2h)

### TAG 11: SHADOW-RADIUS (1h)
- shadow_radius() in unified_metric.py
- Test mit Sgr A* (51.8 μas)

### TAG 12: DOKUMENTATION (5h)
- Sphinx API Docs (2h)
- MD Organisation (1.5h)
- Usage Guide (1.5h)

**→ 98% Excellence!**

---

## PHASE 3: BEYOND (50h - Optional)

### Woche 3: Performance (13h)
- Caching (2h)
- Numba JIT (3h)
- Bisector Frame (4h)
- TOV vollständig (4h)

### Woche 4: Advanced Features (20h)
- Kerr-SSZ Rotation (10h)
- Charged BH (8h)
- Review (2h)

### Woche 5: Educational (14h)
- Interactive Web App (6h)
- Video Tutorials (8h)

**→ 100%+ Perfektion!**

---

## TIMELINE

```
Woche 1: Phase 1 → 95%
Woche 2: Phase 2 → 98%
Wochen 3-5: Phase 3 → 100%+ (optional)
```

---

## MEILENSTEINE

**M1 (Tag 1):** ESO + BH Bomb validiert  
**M2 (Tag 2):** QNM + Notebooks fertig  
**M3 (Tag 7):** Paper Draft komplett  
**M4 (Tag 12):** Excellence erreicht  
**M5 (Woche 3):** Paper auf arXiv

---

## DECISION POINTS

**Nach Tag 7:** Paper genügt? → STOP bei 95%  
**Nach Tag 12:** Excellence genügt? → STOP bei 98%  
**Nach Woche 5:** 100%+ erreicht!

---

## DAILY SCHEDULE

```
3h/Tag: 2 Wochen für Phase 1+2
6h/Tag: 1 Woche für Phase 1+2

Empfohlen: 3h/Tag, flexibel
```

---

**© 2025 Carmen Wrede & Lino Casu**

**Status:** Roadmap Ready  
**Start:** Phase 1, Tag 1  
**ETA:** 2 Wochen zu 98%
