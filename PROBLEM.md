# Problem

## Goal

Pack 26 circles inside the unit square to maximize the sum of their radii.

## Metric

max sum_radii

Maximize the total sum of all 26 circle radii. The current reference target is `2.6359830849`, which you should aim to surpass.

## Constraints

- Keep the same interface: `run_packing(num_circles=26)` must return `(centers, radii, sum_radii)`.
- Try to keep `run_packing(...)` under 300 seconds.
- Do not look up solutions or ideas online.
- Do not edit `evaluate.py`.

## Validation

Run `uv run evaluate.py program.py`.

- validates strict exact geometry, with no overlap slack and no boundary slack
- reports recomputed `sum_radii`, `target_ratio`, `validity`, and `eval_time`
