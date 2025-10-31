"""Run all validation tests and generate scientific output."""

import subprocess
import sys
from pathlib import Path

# Test files
tests = [
    'tests/test_photon_sphere.py',
    'tests/test_shadow_radius.py',
    'tests/test_geodesics_minimal.py',
    'tests/test_qnm.py',
    'tests/test_perihelion.py',
    'tests/test_isco.py',
    'tests/test_observables_complete.py',
    'tests/test_complete_metric.py'
]

print('=' * 70)
print('RUNNING ALL TEST SUITES')
print('=' * 70)
print()

results = []
for test in tests:
    name = Path(test).name
    print(f'Running {name}...')
    
    result = subprocess.run(
        ['python', test],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    status = 'PASS' if result.returncode == 0 else 'FAIL'
    results.append((name, status, result.returncode))
    
    print(f'  {status}')
    if status == 'FAIL':
        print(f'  Error code: {result.returncode}')
        if result.stderr:
            print(f'  Stderr: {result.stderr[:200]}')
    print()

print('=' * 70)
print('TEST SUMMARY')
print('=' * 70)

for name, status, code in results:
    symbol = '✓' if status == 'PASS' else '✗'
    print(f'{symbol} {name:40s} {status}')

passed = sum(1 for _, s, _ in results if s == 'PASS')
print()
print(f'Total: {passed}/{len(results)} PASSED ({passed/len(results)*100:.1f}%)')
print('=' * 70)
