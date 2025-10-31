# -*- coding: utf-8 -*-
"""
ESO S-Stars Validation - 97.9% Accuracy Target

Validates SSZ metric against 427 S-star observations around Sgr A*.
Target: accuracy >= 97.9%, χ²/dof < 1.1

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import chi2

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from viz_ssz_metric.unified_metric import UnifiedSSZMetric

# Constants
M_SUN = 1.98847e30  # kg
M_SGR_A = 4.15e6 * M_SUN  # Sgr A* mass


def load_eso_data():
    """Load ESO S-star observations"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'real_data_full.csv')
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"ESO data not found at {data_path}")
    
    df = pd.read_csv(data_path)
    
    print(f"Loaded {len(df)} observations")
    print(f"Columns: {list(df.columns)}")
    
    return df


def compute_ssz_redshift(metric, r):
    """
    SSZ gravitational redshift prediction.
    
    z = sqrt(1/A(r)) - 1
    """
    A = metric.metric_function_A(r)
    z_ssz = np.sqrt(1.0 / A) - 1.0
    return z_ssz


def validate():
    """
    Main validation function.
    
    Returns:
        accuracy: Fraction of observations matching within 5%
        chi_squared_reduced: χ²/dof
    """
    print("\n" + "="*80)
    print("ESO S-STARS VALIDATION - SSZ vs. Observations")
    print("="*80)
    
    # Load data
    df = load_eso_data()
    
    # Check and map column names
    if 'z' in df.columns:
        df['z_observed'] = df['z']
    elif 'redshift' in df.columns:
        df['z_observed'] = df['redshift']
    
    if 'r_emit_m' in df.columns:
        df['radius_m'] = df['r_emit_m']
    elif 'r_m' in df.columns:
        df['radius_m'] = df['r_m']
    elif 'distance_m' in df.columns:
        df['radius_m'] = df['distance_m']
    
    # Filter valid data
    df = df.dropna(subset=['z_observed', 'radius_m'])
    df = df[df['radius_m'] > 0]
    df = df[df['z_observed'] > 0]
    
    print(f"\nValid observations after filtering: {len(df)}")
    
    if len(df) < 100:
        print("[WARN] Less than 100 valid observations!")
    
    # Create SSZ metric for Sgr A*
    print(f"\nSgr A* Parameters:")
    print(f"  Mass: {M_SGR_A/M_SUN:.2e} Msun")
    
    metric = UnifiedSSZMetric(mass=M_SGR_A)
    print(f"  r_s: {metric.r_s/1e9:.3f} Gm")
    print(f"  r_phi: {metric.r_phi/1e9:.3f} Gm")
    
    # Compute SSZ predictions
    print("\nComputing SSZ predictions...")
    z_obs = df['z_observed'].values
    r_vals = df['radius_m'].values
    
    z_ssz = np.array([compute_ssz_redshift(metric, r) for r in r_vals])
    
    # Statistics
    print("\nStatistical Analysis:")
    
    # Residuals
    residuals = z_obs - z_ssz
    relative_residuals = residuals / z_obs
    
    # Chi-squared
    # Assuming uncertainty ~5% of observed value
    sigma = 0.05 * z_obs
    chi_squared = np.sum((residuals / sigma)**2)
    dof = len(z_obs) - 1
    chi_squared_reduced = chi_squared / dof
    
    print(f"  Chi^2 = {chi_squared:.2f}")
    print(f"  dof = {dof}")
    print(f"  Chi^2/dof = {chi_squared_reduced:.3f}")
    
    # p-value
    p_value = 1 - chi2.cdf(chi_squared, dof)
    print(f"  p-value = {p_value:.4f}")
    
    # Accuracy (within 5% tolerance)
    tolerance = 0.05
    matches = np.abs(relative_residuals) < tolerance
    accuracy = np.sum(matches) / len(z_obs)
    
    print(f"\nAccuracy Metrics:")
    print(f"  Tolerance: {tolerance*100}%")
    print(f"  Matches: {np.sum(matches)}/{len(z_obs)}")
    print(f"  Accuracy: {accuracy:.3%}")
    
    # Residual statistics
    print(f"\nResidual Statistics:")
    print(f"  Mean: {np.mean(relative_residuals):.4f}")
    print(f"  Median: {np.median(relative_residuals):.4f}")
    print(f"  Std: {np.std(relative_residuals):.4f}")
    print(f"  RMS: {np.sqrt(np.mean(relative_residuals**2)):.4f}")
    
    # Results
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)
    print(f"Accuracy:     {accuracy:.3%}  (target: >= 97.9%)")
    print(f"Chi^2/dof:    {chi_squared_reduced:.3f}  (target: < 1.1)")
    
    # Check acceptance criteria
    passed = True
    
    if accuracy >= 0.979:
        print("[OK] Accuracy criterion MET")
    else:
        print("[FAIL] Accuracy criterion FAILED")
        passed = False
    
    if chi_squared_reduced < 1.1:
        print("[OK] Chi-squared/dof criterion MET")
    else:
        print("[FAIL] Chi-squared/dof criterion FAILED")
        passed = False
    
    print("="*80)
    
    if passed:
        print("[OK] ESO VALIDATION PASSED - SSZ metric validated!")
    else:
        print("[!!] ESO VALIDATION NOT FULLY PASSED - Check criteria")
    
    print("="*80 + "\n")
    
    return accuracy, chi_squared_reduced


if __name__ == "__main__":
    try:
        accuracy, chi_sq = validate()
        
        # Exit code for automation
        if accuracy >= 0.979 and chi_sq < 1.1:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n[ERROR] Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
