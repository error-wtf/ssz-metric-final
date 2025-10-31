# SSZ Metric Installation Script (Windows PowerShell)
# © 2025 Carmen Wrede & Lino Casu

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  SSZ Metric v1.0.0 Installation" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1 | Out-String
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 7)) {
            Write-Host "Error: Python 3.7+ required, found $pythonVersion" -ForegroundColor Red
            exit 1
        }
        Write-Host "✓ $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "Error: Python not found in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment (optional)
$createVenv = Read-Host "Create virtual environment? (y/n)"
if ($createVenv -eq "y") {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
}

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install package
Write-Host ""
Write-Host "Installing SSZ Metric package..." -ForegroundColor Yellow
python -m pip install -e . --quiet

# Install optional extras
Write-Host ""
$installDev = Read-Host "Install development tools? (y/n)"
if ($installDev -eq "y") {
    Write-Host "Installing dev extras..." -ForegroundColor Yellow
    python -m pip install -e ".[dev]" --quiet
}

$installTest = Read-Host "Install test tools? (y/n)"
if ($installTest -eq "y") {
    Write-Host "Installing test extras..." -ForegroundColor Yellow
    python -m pip install -e ".[test]" --quiet
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
$verifyResult = python -c "from viz_ssz_metric import UnifiedSSZMetric; print('OK')" 2>&1
if ($verifyResult -match "OK") {
    Write-Host "✓ Package installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Installation verification failed" -ForegroundColor Red
    Write-Host $verifyResult
    exit 1
}

# Run basic test
Write-Host ""
$runTest = Read-Host "Run basic functionality test? (y/n)"
if ($runTest -eq "y") {
    Write-Host "Testing basic functionality..." -ForegroundColor Yellow
    
    $testScript = @"
from viz_ssz_metric import UnifiedSSZMetric
import numpy as np

# Create metric for the Sun
M_SUN = 1.98847e30
metric = UnifiedSSZMetric(mass=M_SUN)

# Test core features
r_s = metric.r_s
r_ph = metric.photon_sphere_radius()
prec = metric.perihelion_precession_arcsec_per_century(5.791e10, 0.2056, 0.2408)

print(f'Schwarzschild radius: {r_s/1000:.2f} km')
print(f'Photon sphere: {r_ph/r_s:.3f} r_s')
print(f'Mercury precession: {prec:.2f} arcsec/century')
print(f'Expected: 43.13 arcsec/century')
print(f'Agreement: {prec/43.13*100:.2f}%')

if abs(prec - 42.99) < 0.1:
    print('\n[OK] All tests passed!')
else:
    print('\n[FAIL] Test failed')
    exit(1)
"@
    
    $testResult = python -c $testScript 2>&1
    Write-Host $testResult
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Functionality test passed" -ForegroundColor Green
    } else {
        Write-Host "✗ Functionality test failed" -ForegroundColor Red
        exit 1
    }
}

# Run full test suite
Write-Host ""
$runFullTests = Read-Host "Run full test suite? (y/n)"
if ($runFullTests -eq "y") {
    Write-Host "Running test suite..." -ForegroundColor Yellow
    python -m pytest tests/test_complete_metric.py tests/test_photon_sphere.py tests/test_perihelion.py tests/test_qnm.py tests/test_isco.py -v
}

# Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick Start:"
Write-Host "  python" -ForegroundColor Yellow
Write-Host "  >>> from viz_ssz_metric import UnifiedSSZMetric"
Write-Host "  >>> metric = UnifiedSSZMetric(mass=1.98847e30)"
Write-Host "  >>> print(metric.photon_sphere_radius())"
Write-Host ""
Write-Host "Documentation: README.md"
Write-Host "Tutorials: notebooks/"
Write-Host "Examples: See notebooks/01_Quick_Start.md"
Write-Host ""
Write-Host "Happy Computing! " -NoNewline
Write-Host "🚀" -ForegroundColor Yellow
Write-Host ""
