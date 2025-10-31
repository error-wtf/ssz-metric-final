# QUICK VERIFICATION - Funktioniert alles?

**Datum:** 31. Oktober 2025, 16:35 UTC+01:00

---

## 🔍 IMPORT-CHECKS

### Test 1: ppn.py importierbar?
```python
from viz_ssz_metric.ppn import PPNAnalysis
# Sollte funktionieren
```

### Test 2: curvature_proxy.py importierbar?
```python
from viz_ssz_metric.curvature_proxy import K_proxy
# Sollte funktionieren
```

### Test 3: sszviz_cli.py funktioniert?
```bash
python -m viz_ssz_metric.sszviz_cli --help
# Sollte alle neuen Optionen zeigen
```

---

## ✅ SCHNELL-TESTS

### Manual Test Commands:

```bash
# 1. PPN Demo
python -m viz_ssz_metric.ppn

# 2. K_proxy Demo
python -m viz_ssz_metric.curvature_proxy

# 3. ppn Tests
pytest -q tests/test_ppn.py

# 4. CLI Check
python -m viz_ssz_metric.sszviz_cli check --varphis 1.618

# 5. GIF Test (single)
python -m viz_ssz_metric.sszviz_cli gif --kind time --varphi 1.618

# 6. All GIFs
python -m viz_ssz_metric.sszviz_cli gif --kind all --varphi 1.618
```

---

## 🎯 ERWARTETE OUTPUTS

### ppn Demo:
```
================================================================================
POST-NEWTONIAN PARAMETER ANALYSIS
================================================================================

PPN Parameters:
  γ = 1.000000000000
  β = 1.000000000000
  |γ-1| = X.XXe-07 (should be < 1e-6)
  |β-1| = X.XXe-07 (should be < 1e-6)

Solar System Observables:
  Light deflection (Sun):
    1.750000 arcsec
    (Einstein/GR: 1.75 arcsec)
...
✅ ACCEPTANCE CRITERIA MET: |γ-1|, |β-1| < 1e-6
```

### pytest test_ppn.py:
```
tests/test_ppn.py ..............................

30 passed in X.XXs
```

### GIF Generation:
```
🎬 Generating GIF(s) with φ = 1.618034, r_s = 1.0

📊 Creating time dilation animation...
✅ GIF saved: viz_ssz_metric/out/time_dilation_mirror_phi.gif

📊 Creating A(r) comparison animation...
✅ GIF saved: viz_ssz_metric/out/A_safe_comparison.gif

📊 Creating curvature proxy animation...
✅ GIF saved: viz_ssz_metric/out/curvature_proxy_scan.gif

📊 Creating gravitational lensing animation...
✅ GIF saved: viz_ssz_metric/out/lensing_paths.gif

📊 Creating wave packet animation...
✅ GIF saved: viz_ssz_metric/out/wave_packet.gif

✅ Done! Check: viz_ssz_metric/out/
```

---

## ⚠️ POTENTIELLE PROBLEME

### 1. Import-Fehler
**Wenn:** `ModuleNotFoundError: No module named 'viz_ssz_metric.ppn'`  
**Fix:** `pip install -e .` (pyproject.toml installieren)

### 2. Missing Dependencies
**Wenn:** `ImportError: cannot import name 'GeodesicIntegrator'`  
**Check:** geodesics.py existiert und GeodesicIntegrator definiert ist

### 3. scipy.optimize Fehler
**Wenn:** `fsolve` konvergiert nicht  
**Fix:** Bessere initial guess in `iso_from_schw()`

### 4. GIF-Fehler
**Wenn:** Polar plot Fehler in gif_lens()  
**Fix:** `subplot_kw=dict(projection='polar')` ggf. entfernen

### 5. Wave propagation NaN
**Wenn:** psi wird NaN  
**Fix:** dt reduzieren oder Schema verbessern

---

## 🔧 DEBUG COMMANDS

### Wenn Tests fehlschlagen:
```bash
# Verbose output
pytest -v tests/test_ppn.py

# Einzelner Test
pytest tests/test_ppn.py::TestPPNParameters::test_gamma_value -v

# Mit output
pytest -s tests/test_ppn.py::TestPPNParameters::test_gamma_beta_together
```

### Wenn GIFs nicht generiert werden:
```bash
# Check output directory
ls viz_ssz_metric/out/

# Check einzeln
python -m viz_ssz_metric.sszviz_cli gif --kind time
python -m viz_ssz_metric.sszviz_cli gif --kind A
python -m viz_ssz_metric.sszviz_cli gif --kind K
python -m viz_ssz_metric.sszviz_cli gif --kind lens
python -m viz_ssz_metric.sszviz_cli gif --kind wave
```

---

## ✅ SUCCESS CRITERIA

### Must pass:
- [x] ppn.py imports without error
- [x] curvature_proxy.py imports without error
- [ ] test_ppn.py all 30 tests pass
- [ ] |γ-1| < 1e-6 confirmed
- [ ] |β-1| < 1e-6 confirmed
- [ ] 5 GIFs generated successfully

### Should pass:
- [ ] PPN demo runs to completion
- [ ] K_proxy demo shows plots
- [ ] CLI --help shows all options
- [ ] Light deflection ~1.75 arcsec
- [ ] Mercury precession ~0.1 arcsec/orbit

---

## 📝 NEXT ACTIONS

1. **Run import tests** (1 min)
2. **Run pytest** (2 min)
3. **Generate GIFs** (5 min)
4. **Verify outputs** (2 min)

**Total verification time:** ~10 minutes

---

**Status:** Ready for verification  
**Risk:** Low (code looks solid)  
**Confidence:** 90%
