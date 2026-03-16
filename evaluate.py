import argparse
import importlib.util
import json
import math
from pathlib import Path
import time
import traceback

import numpy as np

NUM_CIRCLES = 26
TARGET_VALUE = 2.6359830849


def _load_program(program_path: Path):
    module_name = f"_packing_program_{abs(hash(program_path.resolve()))}"
    spec = importlib.util.spec_from_file_location(module_name, program_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {program_path}.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_program(program_path: Path) -> tuple[np.ndarray, np.ndarray]:
    module = _load_program(program_path)
    run_packing = getattr(module, "run_packing", None)
    if run_packing is None:
        raise AttributeError("Function 'run_packing' not found.")

    centers, radii, _ = run_packing(num_circles=NUM_CIRCLES)
    return np.asarray(centers, dtype=float), np.asarray(radii, dtype=float)


def validate(centers: np.ndarray, radii: np.ndarray) -> dict:
    """Strict geometric validation with no slack."""
    centers = np.asarray(centers, dtype=float)
    radii = np.asarray(radii, dtype=float)

    if centers.shape != (NUM_CIRCLES, 2):
        return {"ok": False, "reason": f"Expected centers shape {(NUM_CIRCLES, 2)}, got {centers.shape}."}

    if radii.shape != (NUM_CIRCLES,):
        return {"ok": False, "reason": f"Expected radii shape {(NUM_CIRCLES,)}, got {radii.shape}."}

    if not np.isfinite(centers).all() or not np.isfinite(radii).all():
        return {"ok": False, "reason": "Centers and radii must be finite."}

    if np.any(radii < 0.0):
        return {"ok": False, "reason": "Radii must be non-negative."}

    boundary_slacks = np.column_stack(
        [
            centers[:, 0] - radii,
            centers[:, 1] - radii,
            1.0 - centers[:, 0] - radii,
            1.0 - centers[:, 1] - radii,
        ]
    )
    if float(np.min(boundary_slacks)) < 0.0:
        return {"ok": False, "reason": "At least one circle leaves the unit square."}

    for i in range(NUM_CIRCLES):
        for j in range(i + 1, NUM_CIRCLES):
            dx = float(centers[i, 0] - centers[j, 0])
            dy = float(centers[i, 1] - centers[j, 1])
            center_distance = math.hypot(dx, dy)
            pair_slack = center_distance - float(radii[i] + radii[j])
            if pair_slack < 0.0:
                return {"ok": False, "reason": f"Circles {i} and {j} overlap."}

    sum_radii = float(np.sum(radii, dtype=np.float64))
    return {"ok": True, "sum_radii": sum_radii}


def evaluate(program_path: str | Path) -> dict:
    """Evaluate a candidate program."""
    program_path = Path(program_path).resolve()
    started_at = time.perf_counter()

    try:
        centers, radii = run_program(program_path)
    except Exception as exc:
        return {
            "status": "execution_failed",
            "summary": str(exc),
            "metrics": {
                "sum_radii": 0.0,
                "target_ratio": 0.0,
                "validity": 0.0,
                "eval_time": float(time.perf_counter() - started_at),
            },
            "artifacts": {"traceback": traceback.format_exc()},
        }

    validation = validate(centers, radii)
    sum_radii = float(validation.get("sum_radii", 0.0))
    target_ratio = sum_radii / TARGET_VALUE if validation["ok"] else 0.0

    metrics = {
        "sum_radii": sum_radii,
        "target_ratio": float(target_ratio),
        "validity": 1.0 if validation["ok"] else 0.0,
        "eval_time": float(time.perf_counter() - started_at),
    }

    if not validation["ok"]:
        return {
            "status": "validation_failed",
            "summary": validation["reason"],
            "metrics": metrics,
        }

    return {"status": "success", "metrics": metrics}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program_path", help="Path to the candidate program.")
    args = parser.parse_args(argv)

    result = evaluate(args.program_path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
