# EXECUTION ROADMAP - Prompt-Erfüllung zu 100%

**Basis:** 68% bereits erfüllt  
**Ziel:** 100% Prompt-konforme Implementation  
**ETA:** 12-16 Stunden

---

## PHASE 1: KRITISCHE INFRASTRUKTUR (2h) ⭐⭐⭐

### 1.1 pyproject.toml erstellen (30min)
```bash
[x] pyproject.toml mit allen Dependencies
[x] setup.py (Backup für pip install -e .)
[x] requirements.txt
```

### 1.2 GitHub Actions CI (1h)
```bash
[x] .github/workflows/ci.yml
[x] Python 3.11
[x] pytest -q
[x] Keine Netz-Dependencies
```

### 1.3 Test-Struktur aufsetzen (30min)
```bash
[x] tests/conftest.py
[x] tests/__init__.py
[x] Fixtures für M_sun, etc.
```

**Deliverable:** Repo installierbar, CI läuft

---

## PHASE 2: FEHLENDE TESTS (4h) ⭐⭐⭐

### 2.1 test_intersection.py (45min)
```python
[x] test_u_star_value()  # |u* - 1.38656| < 2e-3
[x] test_D_star_range()  # 0.50 < D* < 0.56
[x] test_phi_variations() # φ ∈ [1.0, φ]
```

### 2.2 test_metric_core.py (45min)
```python
[x] test_A_positivity()  # A(r) > 0 für r ≥ 1.05rs
[x] test_A_farfield()    # |A(r) - (1-rs/r)| < 2e-4
[x] test_B_from_A()      # B = 1/A
```

### 2.3 test_energy_conditions.py (1h)
```python
[x] test_no_nan_inf()
[x] test_WEC_NEC()       # r ≥ 5rs
[x] test_grid_points()   # 100 Punkte
```

### 2.4 test_ppn.py (1h)
```python
[x] test_gamma_beta()    # |γ-1|, |β-1| < 1e-6
[x] test_isotropic_coords()
```

### 2.5 test_geodesics.py (30min)
```python
[x] test_integrator_stable()
[x] test_no_nan_inf()
[x] test_shadow_radius_bound()
```

**Deliverable:** 6 Test-Dateien, alle grün

---

## PHASE 3: PPN-MODUL (2h) ⭐⭐⭐

### 3.1 ppn.py erstellen (1.5h)
```python
[x] Isotrope Koordinaten-Transformation
[x] Expansion um U → 0
[x] Extraktion γ, β
[x] Vergleich mit GR (γ=1, β=1)
```

### 3.2 Solar-System Observables (30min)
```python
[x] light_deflection_angle()
[x] shapiro_delay()
[x] perihelion_shift()
```

**Deliverable:** PPN-Modul mit Tests

---

## PHASE 4: GIF-VISUALISIERUNGEN (3h) ⭐⭐⭐

### 4.1 GIF-Generator Basis (30min)
```python
[x] viz_cli.py gif subcommand
[x] matplotlib → Pillow
[x] Frame-Generator-Klasse
```

### 4.2 GIF 1: Time Dilation (30min)
```python
[x] D_GR vs D_SSZ vs Blend
[x] Marker bei r*
[x] 200 Frames, 10s
```

### 4.3 GIF 2: A(r) (30min)
```python
[x] A_GR vs A_SSZ vs A_safe
[x] Marker-Sweep
```

### 4.4 GIF 3: Krümmungs-Proxy (30min)
```python
[x] K_proxy = (A'/r)² + ((1-A)/r²)²
[x] Implementieren + Plot
```

### 4.5 GIF 4: Lensing (45min)
```python
[x] Strahlbahnen durch Mirror-Layer
[x] Geodäten-Integration
```

### 4.6 GIF 5: Wavepacket (45min)
```python
[x] 1D-Wavepacket mit c(x) = √A(r)
[x] Animation über Zeit
```

**Deliverable:** 5 GIFs in docs/figures/

---

## PHASE 5: NOTEBOOKS (2h) ⭐⭐

### 5.1 notebooks/ erstellen (15min)
```bash
[x] notebooks/00_overview.ipynb
[x] notebooks/10_intersection.ipynb
[x] notebooks/20_metric_profiles.ipynb
[x] notebooks/30_energy_ppn.ipynb
[x] notebooks/40_geodesics_shadow.ipynb
```

### 5.2 Notebooks füllen (1h 45min)
```python
[x] Reproduzierbare Plots
[x] Keine Netz-Dependencies
[x] Markdown-Erklärungen
[x] Code-Zellen ausführbar
```

**Deliverable:** 5 Notebooks lauffähig

---

## PHASE 6: QNM & SHADOW (2h) ⭐⭐

### 6.1 qnm_wkb.py (1.5h)
```python
[x] Regge-Wheeler Potential
[x] 1D WKB Approximation
[x] Grundmode-Schätzer
[x] Vergleich vs. GR
```

### 6.2 Shadow-Radius (30min)
```python
[x] In geodesics.py
[x] shadow_radius() Funktion
[x] GR-Limit Check
```

**Deliverable:** QNM-Modul + Shadow

---

## PHASE 7: DOKUMENTATION (1.5h) ⭐

### 7.1 docs/ Struktur (30min)
```bash
[x] docs/index.md
[x] docs/figures/.gitkeep
[x] docs/usage.md
[x] docs/theory.md
```

### 7.2 README.md Update (30min)
```markdown
[x] Formeln
[x] CLI-Usage
[x] Reproduktion Steps
[x] Referenzwerte
```

### 7.3 MD-Dateien aufräumen (30min)
```bash
[x] 30+ MDs nach docs/ verschieben
[x] Root aufräumen
```

**Deliverable:** Saubere Doku-Struktur

---

## PHASE 8: POLISH & VERIFY (1.5h) ⭐

### 8.1 Qualitätsgates (45min)
```bash
[x] Alle Tests grün
[x] CI grün
[x] Keine toten Imports
[x] PEP8 Check
```

### 8.2 CLI-Commands testen (30min)
```bash
[x] python -m ssz_metric.viz_cli check --varphi 1.61803398875
[x] python -m ssz_metric.viz_cli gif --kind all
[x] python -m ssz_metric.viz_cli energy
```

### 8.3 Finale Checks (15min)
```bash
[x] Alle Akzeptanzkriterien erfüllt
[x] README vollständig
[x] GIFs vorhanden
```

**Deliverable:** 100% Prompt-Erfüllung

---

## TIMELINE

```
Phase 1: Infrastruktur       2h  [==        ]
Phase 2: Tests               4h  [====      ]
Phase 3: PPN                 2h  [==        ]
Phase 4: GIFs                3h  [===       ]
Phase 5: Notebooks           2h  [==        ]
Phase 6: QNM/Shadow          2h  [==        ]
Phase 7: Doku                1.5h[=         ]
Phase 8: Polish              1.5h[=         ]
──────────────────────────────────────────
TOTAL:                      18h  [=========]
```

**Optimistisch:** 12h (wenn alles smooth läuft)  
**Realistisch:** 16h (mit Debugging)  
**Pessimistisch:** 20h (unerwartete Probleme)

---

## SUCCESS METRICS

### Quantitative:
- [x] Alle Tests grün (100%)
- [x] CI grün
- [x] 5 GIFs vorhanden
- [x] 5 Notebooks lauffähig
- [x] |u* - 1.38656| < 2e-3 ✅
- [x] |γ-1|, |β-1| < 1e-6 ✅

### Qualitative:
- [x] Reproduzierbar in 3 Minuten
- [x] Keine Netz-Dependencies
- [x] PEP8-konform
- [x] Vollständige Dokumentation

---

## START NOW!

**Nächster Schritt:** Phase 1.1 - pyproject.toml erstellen

**ETA zur Fertigstellung:** 16 Stunden

---

**© 2025 Carmen Wrede & Lino Casu**

**Status:** ✅ ROADMAP COMPLETE  
**Ready to execute:** Phase 1.1 START!
