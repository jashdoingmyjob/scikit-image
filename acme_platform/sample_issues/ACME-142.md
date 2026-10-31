# Ticket ACME-142: Add `high_boost_filter` to `src/skimage/filters`
**Assignee:** New Platform Engineer (Week 1)
**Context:** Ops customers need an edge-sharpening high-boost filter (`output = image + boost_factor * (image - smoothed)`), where `smoothed` is computed via `gaussian` filter.
**Acceptance Criteria:**
1. Follow all `skimage` conventions (`_supported_float_type`, `channel_axis`, NumPy docstring with Parameters, Returns, and Examples).
2. Do not import from `acme_platform/legacy_deprecated/`.
3. Export `high_boost_filter` in `src/skimage/filters/__init__.py`.
4. Include unit tests in `tests/skimage/filters/test_high_boost.py` covering 2D, 3D `channel_axis`, `float32` dtype preservation, and `ValueError` for invalid `boost_factor < 0`.
