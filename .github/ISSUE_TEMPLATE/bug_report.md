---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Environment

- **OS:** [e.g., Windows 10, Ubuntu 22.04, macOS 13]
- **Python version:** [e.g., 3.11.2]
- **SSZ Metric version:** [e.g., 1.0.0]
- **Installation method:** [pip, source, other]

## Code to Reproduce

```python
from viz_ssz_metric import UnifiedSSZMetric

# Minimal code that reproduces the bug
metric = UnifiedSSZMetric(mass=1e30)
result = metric.some_method()
```

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Error Message

If applicable, paste the full error traceback:

```
Traceback (most recent call last):
  File "...", line X, in <module>
    ...
Error: ...
```

## Additional Context

Add any other context about the problem here (screenshots, related issues, etc.)

## Possible Solution

(Optional) If you have ideas on how to fix this.
