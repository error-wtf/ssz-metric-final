"""Test Perihelion Precession implementation."""

import sys
sys.path.insert(0, 'E:/clone/ssz-full-metric')

from viz_ssz_metric.unified_metric import UnifiedSSZMetric
import numpy as np

M_SUN = 1.98847e30

# Mercury orbital parameters
MERCURY = {
    'a': 5.791e10,  # m
    'e': 0.2056,
    'P': 0.2408     # years
}


def test_mercury_precession():
    """
    Mercury perihelion precession.
    
    Observed: 43.13 arcsec/century (total relativistic)
    GR prediction: 42.98 arcsec/century
    """
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    precession = metric.perihelion_precession_arcsec_per_century(
        semi_major_axis=MERCURY['a'],
        eccentricity=MERCURY['e'],
        period_years=MERCURY['P']
    )
    
    print(f"[OK] Mercury precession: {precession:.2f} arcsec/century")
    print(f"     (Observed: 43.13 arcsec/century)")
    
    # Should be within 5% of observed
    assert 40 < precession < 45, f"Precession {precession:.2f} outside [40, 45]"


def test_ssz_correction_small():
    """SSZ correction should be small for Mercury."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    eta = metric.ssz_precession_correction(
        semi_major_axis=MERCURY['a'],
        eccentricity=MERCURY['e']
    )
    
    print(f"[OK] SSZ correction: {eta:.4f} ({eta*100:.2f}%)")
    
    # Should be < 1%
    assert abs(eta) < 0.01, f"SSZ correction {eta:.2%} too large!"


def test_precession_scaling():
    """Precession should scale as 1/a and inversely with period."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    # Mercury
    prec_mercury = metric.perihelion_precession_arcsec_per_century(
        MERCURY['a'], MERCURY['e'], MERCURY['P']
    )
    
    # Hypothetical orbit at 2x distance (P ~ sqrt(a^3) ~ 2.83 × P_mercury)
    # But we use 2*P for simplicity
    prec_far = metric.perihelion_precession_arcsec_per_century(
        2*MERCURY['a'], MERCURY['e'], 2*MERCURY['P']
    )
    
    ratio = prec_mercury / prec_far
    
    # delta_phi per orbit ~ 1/a → factor 2
    # orbits per century ~ 1/P → factor 2  
    # Total: ~4
    assert 3 < ratio < 5, f"Scaling {ratio:.2f} not ~4"
    
    print(f"[OK] Scaling: prec(a) / prec(2a) = {ratio:.2f} (expect ~4)")


def test_precession_per_orbit():
    """Test precession per orbit calculation."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    delta_phi_rad = metric.perihelion_precession(
        MERCURY['a'], MERCURY['e']
    )
    
    # Should be tiny (radians per orbit)
    assert 0 < delta_phi_rad < 1e-6, "Precession per orbit should be microradians"
    
    # Convert to arcsec
    delta_phi_arcsec = delta_phi_rad * (180/np.pi) * 3600
    
    print(f"[OK] Precession per orbit: {delta_phi_arcsec:.4f} arcsec")


def test_precession_eccentricity_dependence():
    """Precession should depend on eccentricity."""
    metric = UnifiedSSZMetric(mass=M_SUN)
    
    # Circular orbit (e=0)
    prec_circular = metric.perihelion_precession_arcsec_per_century(
        MERCURY['a'], eccentricity=0.0, period_years=MERCURY['P']
    )
    
    # Eccentric orbit (Mercury e=0.2056)
    prec_eccentric = metric.perihelion_precession_arcsec_per_century(
        MERCURY['a'], MERCURY['e'], MERCURY['P']
    )
    
    # Eccentric should precess MORE (smaller denominator 1-e²)
    assert prec_eccentric > prec_circular, "Eccentric orbit should precess more"
    
    ratio = prec_eccentric / prec_circular
    print(f"[OK] prec(e=0.21) / prec(e=0) = {ratio:.2f}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("PERIHELION PRECESSION TESTS")
    print("="*70 + "\n")
    
    test_mercury_precession()
    test_ssz_correction_small()
    test_precession_scaling()
    test_precession_per_orbit()
    test_precession_eccentricity_dependence()
    
    print("\n[PASS] ALL PERIHELION TESTS PASSED!\n")
