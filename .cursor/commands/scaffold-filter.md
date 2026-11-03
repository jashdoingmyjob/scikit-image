# scaffold-filter

Scaffold a new image processing filter in `src/skimage/filters/` based on the provided ticket or description:

1. Read the target ticket in `acme_platform/sample_issues/` (e.g., `ACME-142.md`).
2. Follow all conventions in `.cursor/rules/01-scaffolding-conventions.mdc` and `02-architecture-boundaries.mdc`:
   - Implement the filter inside `src/skimage/filters/` using `@_supported_float_type` and `channel_axis` from `skimage._shared.utils`.
   - Export the new function cleanly in `src/skimage/filters/__init__.py`.
   - Include a complete NumPy-style docstring `Parameters`, `Returns`, `Examples`).
3. Create the matching unit test suite in `tests/skimage/filters/` following `.cursor/rules/03-testing-guardrails.mdc` (testing 2D, 3D multi-channel, float32 dtype preservation, and invalid parameter `ValueError` checks).
4. Run `pytest` on the new test file and `python acme_platform/ci_guardrails/check_boundaries.py` on the new files to verify zero boundary or convention violations.
