# Installation Guide - SSZ Metric v1.0.0

Complete installation instructions for all platforms.

---

## 🚀 Quick Install

### Option 1: Automated Install (Recommended)

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

### Option 2: Manual Install

```bash
# Install package
pip install -e .

# Verify
python -c "from viz_ssz_metric import UnifiedSSZMetric; print('✓ OK')"
```

### Option 3: PyPI (when available)

```bash
pip install ssz-metric
```

---

## 📋 Prerequisites

### Required

- **Python:** 3.7, 3.8, 3.9, 3.10, 3.11, or 3.12
- **pip:** Latest version recommended
- **OS:** Linux, macOS, or Windows

### Check Your Python

```bash
python --version  # Should be 3.7+
```

If not installed:
- **Linux:** `sudo apt install python3 python3-pip`
- **macOS:** `brew install python3`
- **Windows:** Download from [python.org](https://python.org)

---

## 🔧 Detailed Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/USERNAME/ssz-full-metric
cd ssz-full-metric
```

### Step 2: Create Virtual Environment (Recommended)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Package

**Basic installation:**
```bash
pip install -e .
```

**With all extras:**
```bash
pip install -e ".[all]"
```

**Individual extras:**
```bash
pip install -e ".[dev]"    # Development tools
pip install -e ".[test]"   # Testing tools
pip install -e ".[plot]"   # Plotting tools
pip install -e ".[notebook]"  # Jupyter notebooks
```

### Step 4: Verify Installation

```bash
python -c "from viz_ssz_metric import UnifiedSSZMetric; m = UnifiedSSZMetric(mass=1e30); print(f'✓ r_s = {m.r_s:.2f} m')"
```

Expected output:
```
✓ r_s = 1485.23 m
```

### Step 5: Run Tests (Optional)

```bash
# Core tests (24 tests, ~0.2s)
python -m pytest tests/test_complete_metric.py -v

# All tests
python -m pytest tests/ -v
```

---

## 📦 Installation Options

### For Users

```bash
pip install -e .
```

Installs:
- `viz_ssz_metric` package
- Core dependencies (numpy, scipy)

### For Developers

```bash
pip install -e ".[dev]"
```

Adds:
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking

### For Testing

```bash
pip install -e ".[test]"
```

Adds:
- `pytest` - Test framework
- `pytest-cov` - Coverage reports

### For Plotting

```bash
pip install -e ".[plot]"
```

Adds:
- `matplotlib` - Plotting
- `scipy` - Scientific computing

### For Notebooks

```bash
pip install -e ".[notebook]"
```

Adds:
- `jupyter` - Jupyter notebooks
- `matplotlib` - Plotting

### Everything

```bash
pip install -e ".[all]"
```

Installs all extras above.

---

## 🐛 Troubleshooting

### Python Version Issues

**Problem:** `Python 3.7+ required`

**Solution:**
```bash
# Check version
python --version

# Use python3 explicitly
python3 -m pip install -e .
```

### Permission Errors

**Problem:** `Permission denied` or `Access denied`

**Solution (Linux/macOS):**
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Solution (Windows):**
```powershell
# Run PowerShell as Administrator
# Or use virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'viz_ssz_metric'`

**Solution:**
```bash
# Reinstall
pip uninstall ssz-metric
pip install -e .

# Check installation
pip list | grep ssz-metric
```

### Dependency Conflicts

**Problem:** `ERROR: pip's dependency resolver...`

**Solution:**
```bash
# Use fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate  # or .\fresh_venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
```

### Test Failures

**Problem:** Tests fail after installation

**Solution:**
```bash
# Install test dependencies
pip install -e ".[test]"

# Run only core tests
python -m pytest tests/test_complete_metric.py tests/test_photon_sphere.py tests/test_perihelion.py -v

# Check 24 core tests pass
```

---

## 🔍 Verification Checklist

After installation, verify:

- [ ] **Import works:** `python -c "from viz_ssz_metric import UnifiedSSZMetric"`
- [ ] **Version correct:** `python -c "import viz_ssz_metric; print(viz_ssz_metric.__version__)"`
- [ ] **Basic test passes:** Run verification script below
- [ ] **Core tests pass:** `python -m pytest tests/test_complete_metric.py`

### Verification Script

```python
from viz_ssz_metric import UnifiedSSZMetric

# Create metric for the Sun
M_SUN = 1.98847e30
metric = UnifiedSSZMetric(mass=M_SUN)

# Test core features
print(f"Schwarzschild radius: {metric.r_s/1000:.2f} km")
print(f"Photon sphere: {metric.photon_sphere_radius()/metric.r_s:.3f} r_s")

# Mercury validation
prec = metric.perihelion_precession_arcsec_per_century(5.791e10, 0.2056, 0.2408)
print(f"Mercury precession: {prec:.2f} arcsec/century")
print(f"Expected: 43.13 arcsec/century")
print(f"Agreement: {prec/43.13*100:.2f}%")

# Check result
if abs(prec - 42.99) < 0.1:
    print("\n✓ Installation verified successfully!")
else:
    print("\n✗ Verification failed")
```

Expected output:
```
Schwarzschild radius: 2.95 km
Photon sphere: 1.338 r_s
Mercury precession: 42.99 arcsec/century
Expected: 43.13 arcsec/century
Agreement: 99.67%

✓ Installation verified successfully!
```

---

## 🌐 Platform-Specific Notes

### Linux

- Recommended Python: System Python 3.7+
- Virtual environment: Always recommended
- Install location: `~/.local/lib/python3.x/site-packages/`

### macOS

- Recommended Python: Homebrew Python 3
- Avoid system Python (use `python3`)
- Virtual environment: Highly recommended

### Windows

- Recommended Python: Official installer from python.org
- Use PowerShell (not CMD)
- Virtual environment: Recommended
- Execution policy: May need to set for scripts

---

## 📚 Next Steps

After successful installation:

1. **Read Quick Start:** `notebooks/01_Quick_Start.md`
2. **Try Mercury example:** `notebooks/02_Mercury_Validation.md`
3. **Explore features:** See README.md
4. **Run examples:** Check notebooks/

---

## 💡 Tips

### Use Virtual Environments

**Why:** Isolates dependencies, prevents conflicts

**How:**
```bash
python -m venv ssz_env
source ssz_env/bin/activate  # Linux/macOS
.\ssz_env\Scripts\Activate.ps1  # Windows
```

### Keep Updated

```bash
# Update package
cd ssz-full-metric
git pull
pip install -e . --upgrade

# Update dependencies
pip install --upgrade numpy scipy
```

### Uninstall

```bash
pip uninstall ssz-metric

# Or with editable install
cd ssz-full-metric
pip uninstall ssz-metric
```

---

## 📞 Getting Help

- **Installation issues:** Open GitHub issue with label `installation`
- **Test failures:** See `tests/README_TESTS.md`
- **Dependencies:** Check `requirements.txt` and `pyproject.toml`
- **General help:** See CONTRIBUTING.md

---

## ✅ Installation Summary

**Minimal:**
```bash
git clone <repo>
cd ssz-full-metric
pip install -e .
python -c "from viz_ssz_metric import UnifiedSSZMetric"
```

**Complete:**
```bash
git clone <repo>
cd ssz-full-metric
python -m venv venv
source venv/bin/activate
pip install -e ".[all]"
python -m pytest tests/test_complete_metric.py -v
```

**Automated:**
```bash
./install.sh  # Linux/macOS
.\install.ps1  # Windows
```

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
