# Stats Library Training

A from-scratch training example based on a real internal pattern: an
internal Python **library** (not a service) that ships to a private package
registry (e.g. Artifactory) via CI whenever its version bumps, with API
documentation generated straight from docstrings via Sphinx and deployed to
its own static docs site.

The actual math in `src/statlib` is deliberately trivial -- mean/variance,
Pearson correlation, z-scores/min-max scaling. This is **not** a copy of any
production system; the real project this is modeled on performs proprietary
psychometric calculations that are not reproduced here. What's reproduced is
the *packaging, testing, and documentation pipeline* around a library like
that.

## The problem this solves

Several other internal apps need the same well-tested statistical
functions. Instead of copy-pasting them (and their bugs) into every
consumer, they live in one versioned library that's:

- **Installable** like any other PyPI package (`pip install training-stats-library`),
  just from a private registry instead of public PyPI.
- **Documented from its own docstrings** -- nobody has to remember to
  separately update a wiki page when a function's behavior changes.
- **Tested against a matrix of dependency versions** (here: two pinned
  pandas versions), so a consumer isn't surprised by a subtle behavior
  change when they upgrade pandas independently of this library.

## Repository layout

```
src/statlib/           # the library itself (see below)
tests/                 # pytest suite, one file per module
docs/source/           # Sphinx source: conf.py + hand-written index/module pages
infra/cdk/             # CDK stack that deploys the built docs to S3 + CloudFront
.github/workflows/ci.yml
```

## The library (`src/statlib/`)

- `descriptive.py` -- `summary_stats()` (n/mean/variance/std_dev/std_error), `standard_error_of_mean()`
- `correlation.py` -- `pearson_correlation()`, `correlation_matrix()`
- `scaling.py` -- `z_scores()`, `min_max_scale()`

```python
import pandas as pd
from statlib import summary_stats

scores = pd.Series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
print(summary_stats(scores))
# {'n': 8, 'mean': 5.0, 'variance': 4.571..., 'std_dev': 2.138..., 'std_error': 0.756...}
```

## Three patterns worth studying

### 1. Docstrings *are* the documentation (`docs/`)

Every public function has a Google-style docstring (`Args:`/`Returns:`/
`Raises:`/`Examples:`). `docs/source/conf.py` wires up
`sphinx.ext.autodoc` + `sphinx.ext.napoleon` (which parses Google/NumPy
style docstrings into proper Sphinx field lists) and the RTD theme. Each
page under `docs/source/modules/*.rst` is just a two-line `automodule::`
directive -- the actual content comes from the code:

```rst
.. automodule:: statlib.descriptive
   :members:
   :undoc-members:
   :show-inheritance:
```

Build it locally:

```bash
pip install -r requirements-dev.txt -r docs/requirements.txt
cd docs
make html      # or `.\make.bat html` on Windows
```

Open `docs/build/html/index.html`. The `Examples:` blocks are also live
doctests (`sphinx.ext.doctest`), so a docstring example that goes stale
fails a build instead of silently lying to readers.

### 2. Testing against a dependency-version matrix (`tox.ini`)

`tox.ini` runs the test suite twice -- once against `pandas==2.2.0`, once
against `pandas==2.2.3` -- so a pandas upgrade that changes, say, how
`Series.corr()` handles NaNs is caught by CI instead of by a confused
downstream consumer months later. The version list is easy to extend
whenever a new pandas release needs covering.

### 3. Publish-on-merge packaging (`.github/workflows/ci.yml`, `pyproject.toml`)

The real pipeline this mirrors: bump `version` in `pyproject.toml`, merge to
the main branch, and CI builds a wheel/sdist and `twine upload`s it to an
internal Artifactory PyPI repository -- so every other project can just
`pip install` the new version. This training's `build-package` CI job does
the build step for real (`python -m build`) and uploads the result as a
GitHub Actions artifact; the actual `twine upload` to a private registry is
left commented out since there's no registry for this repo to publish to.
The `build-docs` job does the same for the Sphinx site: it builds real HTML
and uploads it as an artifact, standing in for the real pipeline's
`cdk deploy` of that HTML to `infra/cdk`'s S3 + CloudFront stack.

## Running everything locally

```bash
pip install -e . -r requirements-dev.txt
pytest                                   # 15 tests
flake8 src tests
mypy
tox                                      # dependency-version matrix
```

## Exercises

1. **Add a new statistic** (e.g. a median absolute deviation function) with
   a Google-style docstring, a test file, and a new `docs/source/modules/*.rst`
   page -- confirm it shows up in the built docs without touching `conf.py`.
2. **Add a `CHANGELOG.md`** and wire a CI check that fails a PR if
   `pyproject.toml`'s version wasn't bumped versus `main`.
3. **Uncomment and adapt the `twine upload` step** in `ci.yml` to point at a
   real registry (e.g. TestPyPI) using repository secrets, and watch a
   version bump actually publish.
4. **Deploy `infra/cdk`** against a real (or sandbox) AWS account and hosted
   zone -- see `infra/cdk/README.md`.
5. **Add a `doctest` that intentionally goes stale** (change a function's
   behavior without updating its docstring's `Examples:` block) and watch
   `make html` fail the build -- then fix it properly.
