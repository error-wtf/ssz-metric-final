# Contributing to SSZ Metric

Thank you for your interest in contributing to the SSZ Metric project!

---

## 🌟 How to Contribute

### Areas Where We Welcome Contributions

1. **Bug Reports** - Found an issue? Let us know!
2. **Feature Requests** - Have an idea? Share it!
3. **Code Contributions** - Improvements, optimizations, new features
4. **Documentation** - Tutorials, examples, clarifications
5. **Scientific Validation** - New tests, comparisons, benchmarks
6. **Performance** - Optimization suggestions

---

## 🚀 Getting Started

### 1. Development Setup

```bash
# Clone the repository
git clone https://github.com/USERNAME/ssz-full-metric
cd ssz-full-metric

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all extras
pip install -e ".[dev,test,all]"

# Run tests to verify setup
python -m pytest tests/ -v
```

---

### 2. Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Run tests
python -m pytest tests/ -v

# Check code style
black viz_ssz_metric/ --line-length=100 --check
flake8 viz_ssz_metric/ --max-line-length=100

# Commit changes
git add .
git commit -m "FEAT: Description of your feature"

# Push to your fork
git push origin feature/your-feature-name
```

---

## 📝 Code Style Guidelines

### Python Style

- **PEP 8 compliant** with 100 character line limit
- **Black** for formatting: `black viz_ssz_metric/ --line-length=100`
- **Type hints** encouraged (but not required)
- **Docstrings** required for all public methods

### Docstring Format

```python
def new_method(self, param1: float, param2: str = "default") -> float:
    """
    Brief one-line description.
    
    Longer description if needed. Explain the physics or math
    behind the method. Reference papers when applicable.
    
    Args:
        param1: Description of param1 (units if applicable)
        param2: Description of param2
    
    Returns:
        Description of return value (units if applicable)
    
    Raises:
        ValueError: When param1 is negative
    
    References:
        Author et al. (Year), Journal, Volume, Page
    
    Example:
        >>> metric = UnifiedSSZMetric(mass=1e30)
        >>> result = metric.new_method(10.0)
        >>> print(result)
        42.0
    """
    if param1 < 0:
        raise ValueError(f"param1 must be positive, got {param1}")
    
    # Implementation
    return param1 * 42.0
```

---

## ✅ Testing Requirements

### All Contributions Must Include Tests

```python
# tests/test_new_feature.py

def test_new_method():
    """Test the new method with standard input."""
    metric = UnifiedSSZMetric(mass=1.98847e30)
    result = metric.new_method(10.0)
    
    assert result > 0
    assert abs(result - 420.0) < 1e-10

def test_new_method_validation():
    """Test input validation."""
    metric = UnifiedSSZMetric(mass=1.98847e30)
    
    with pytest.raises(ValueError):
        metric.new_method(-1.0)
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_new_feature.py -v

# Run with coverage
python -m pytest tests/ --cov=viz_ssz_metric --cov-report=term
```

---

## 🔬 Scientific Contributions

### Adding New Observables

If you're adding a new physical observable:

1. **Implement the method** with clear physics documentation
2. **Add validation** - compare with known results (GR, literature)
3. **Write tests** - including edge cases
4. **Update documentation** - add to README feature list
5. **Reference papers** - cite the formulas you're using

Example:

```python
def new_observable(self, r: float) -> float:
    """
    Calculate [physical quantity].
    
    APPROACH:
    - Base: Standard GR formula (Reference 1)
    - SSZ correction: Via metric modification (Reference 2)
    
    Args:
        r: Radius (meters, must be > r_s)
    
    Returns:
        [Quantity] in [units]
    
    References:
        1. Einstein (1916), Annalen der Physik
        2. SSZ formulation (this work)
    """
    if r <= self.r_s:
        raise ValueError(f"Radius must be > r_s = {self.r_s} m")
    
    # Standard GR formula
    gr_value = ...
    
    # SSZ correction via metric
    A_ssz = self.metric_function_A(r)
    A_gr = 1 - self.r_s / r
    correction = A_ssz / A_gr
    
    return gr_value * correction
```

---

## 🐛 Bug Reports

### Good Bug Reports Include:

1. **Python version** and OS
2. **SSZ Metric version** (`import viz_ssz_metric; print(viz_ssz_metric.__version__)`)
3. **Minimal reproducible example**
4. **Expected behavior**
5. **Actual behavior**
6. **Error messages** (full traceback)

### Template:

```markdown
**Environment:**
- OS: Windows 10
- Python: 3.11.2
- SSZ Metric: 1.0.0

**Code:**
```python
from viz_ssz_metric import UnifiedSSZMetric
metric = UnifiedSSZMetric(mass=1e30)
result = metric.some_method()
```

**Expected:** Should return 42.0

**Actual:** Returns NaN

**Error:**
```
Traceback (most recent call last):
  ...
```
```

---

## 💡 Feature Requests

### Good Feature Requests Include:

1. **Scientific justification** - Why is this feature important?
2. **Use case** - How would you use it?
3. **References** - Papers or formulas if applicable
4. **Implementation ideas** (optional)

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Code formatted (`black --check`)
- [ ] Docstrings complete
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts with main

### PR Description Should Include

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes
- Added feature X
- Fixed bug Y
- Updated documentation Z

## Testing
How did you test this?

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

---

## 📚 Documentation Contributions

### Types of Documentation We Need

1. **Tutorials** - Step-by-step guides
2. **Examples** - Practical use cases
3. **API docs** - Method descriptions
4. **Scientific explanations** - Physics background

### Writing Documentation

- **Clear and concise** - avoid jargon when possible
- **Include examples** - show, don't just tell
- **Reference equations** - use LaTeX when needed
- **Test your code** - ensure examples actually run

---

## 🎯 Scientific Honesty

This project values **scientific transparency**. Please:

✅ **DO:**
- Clearly state which formulas are standard GR
- Document SSZ-specific modifications
- Compare with literature values
- Cite your sources
- Report limitations honestly

❌ **DON'T:**
- Cherry-pick results
- Overstate accuracy
- Claim originality for standard formulas
- Hide discrepancies

See `SCIENTIFIC_HONESTY.md` for full guidelines.

---

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in release notes
- Credited in papers (for significant scientific contributions)

---

## 📞 Getting Help

- **Questions?** Open a GitHub issue with label `question`
- **Discussion?** Use GitHub Discussions
- **Email?** See README for contact info

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4.

See `LICENSE` for details.

---

## 🙏 Thank You!

Every contribution makes this project better. Whether it's:
- A typo fix
- A new feature
- A bug report
- A question

**We appreciate it!**

---

© 2025 Carmen Wrede & Lino Casu  
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
