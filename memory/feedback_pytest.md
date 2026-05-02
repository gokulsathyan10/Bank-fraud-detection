---
name: User prefers pytest over unittest
description: For Python tests in this project, use pytest (fixtures, plain functions/classes, assert statements) — not unittest
type: feedback
---

User prefers pytest for writing tests in this project.

**Why:** User explicitly said "I need it using pytest. Later I need to implement github actions" after I drafted a unittest version. They are setting up CI with GitHub Actions and pytest is the standard there.

**How to apply:**
- Default to pytest style: plain `def test_*` functions or simple classes (no `unittest.TestCase`), `assert` statements, `@pytest.fixture` for setup, `pytest.raises` for exception tests
- Add `pytest` to `requirements.txt` so CI can `pip install -r requirements.txt && pytest`
- Keep tests deterministic (CI-friendly): use fixtures with synthetic data for the assertions that matter; only touch real CSVs in smoke tests
