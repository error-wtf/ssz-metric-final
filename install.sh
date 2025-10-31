#!/bin/bash
# SSZ Metric Installation Script (Linux/macOS)
# © 2025 Carmen Wrede & Lino Casu

set -e

echo "=========================================="
echo "  SSZ Metric v1.0.0 Installation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo -e "${RED}Error: Python 3.7+ required, found $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

# Create virtual environment (optional)
read -p "Create virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install package
echo ""
echo "Installing SSZ Metric package..."
python3 -m pip install -e .

# Install optional extras
echo ""
read -p "Install development tools? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing dev extras..."
    python3 -m pip install -e ".[dev]"
fi

read -p "Install test tools? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing test extras..."
    python3 -m pip install -e ".[test]"
fi

# Verify installation
echo ""
echo "Verifying installation..."
if python3 -c "from viz_ssz_metric import UnifiedSSZMetric; print('✓ Import OK')" 2>/dev/null; then
    echo -e "${GREEN}✓ Package installed successfully${NC}"
else
    echo -e "${RED}✗ Installation verification failed${NC}"
    exit 1
fi

# Run basic test
echo ""
read -p "Run basic functionality test? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Testing basic functionality..."
    python3 << EOF
from viz_ssz_metric import UnifiedSSZMetric
import numpy as np

# Create metric for the Sun
M_SUN = 1.98847e30
metric = UnifiedSSZMetric(mass=M_SUN)

# Test core features
r_s = metric.r_s
r_ph = metric.photon_sphere_radius()
prec = metric.perihelion_precession_arcsec_per_century(5.791e10, 0.2056, 0.2408)

print(f"Schwarzschild radius: {r_s/1000:.2f} km")
print(f"Photon sphere: {r_ph/r_s:.3f} r_s")
print(f"Mercury precession: {prec:.2f} arcsec/century")
print(f"Expected: 43.13 arcsec/century")
print(f"Agreement: {prec/43.13*100:.2f}%")

if abs(prec - 42.99) < 0.1:
    print("\n✓ All tests passed!")
else:
    print("\n✗ Test failed")
    exit(1)
EOF
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Functionality test passed${NC}"
    else
        echo -e "${RED}✗ Functionality test failed${NC}"
        exit 1
    fi
fi

# Run full test suite
echo ""
read -p "Run full test suite? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running test suite..."
    python3 -m pytest tests/test_complete_metric.py tests/test_photon_sphere.py tests/test_perihelion.py tests/test_qnm.py tests/test_isco.py -v
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=========================================="
echo ""
echo "Quick Start:"
echo "  python3"
echo "  >>> from viz_ssz_metric import UnifiedSSZMetric"
echo "  >>> metric = UnifiedSSZMetric(mass=1.98847e30)"
echo "  >>> print(metric.photon_sphere_radius())"
echo ""
echo "Documentation: README.md"
echo "Tutorials: notebooks/"
echo "Examples: See notebooks/01_Quick_Start.md"
echo ""
echo "Happy Computing! 🚀"
echo ""
