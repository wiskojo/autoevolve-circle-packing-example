import math

import numpy as np

NUM_CIRCLES = 26


def construct_packing(num_circles: int = NUM_CIRCLES) -> tuple[np.ndarray, np.ndarray, float]:
    """Build a simple seed arrangement for the 26-circle instance."""
    if num_circles != NUM_CIRCLES:
        raise ValueError(f"This seed constructor only supports n={NUM_CIRCLES}.")

    centers = np.zeros((num_circles, 2), dtype=float)
    centers[0] = [0.5, 0.5]

    for index in range(8):
        angle = 2.0 * math.pi * index / 8.0
        centers[index + 1] = [0.5 + 0.3 * math.cos(angle), 0.5 + 0.3 * math.sin(angle)]

    for index in range(16):
        angle = 2.0 * math.pi * index / 16.0
        centers[index + 9] = [0.5 + 0.7 * math.cos(angle), 0.5 + 0.7 * math.sin(angle)]

    centers = np.clip(centers, 0.01, 0.99)
    radii = compute_max_radii(centers)
    sum_radii = float(np.sum(radii, dtype=np.float64))
    return centers, radii, sum_radii


def compute_max_radii(centers: np.ndarray) -> np.ndarray:
    """Assign conservative radii that are always feasible for the chosen centers."""
    centers = np.asarray(centers, dtype=float)
    boundary_limits = np.min(
        np.column_stack(
            [
                centers[:, 0],
                centers[:, 1],
                1.0 - centers[:, 0],
                1.0 - centers[:, 1],
            ]
        ),
        axis=1,
    )
    pair_limits = np.full(len(centers), np.inf, dtype=float)

    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            distance = float(np.linalg.norm(centers[i] - centers[j]))
            half_distance = 0.5 * distance
            pair_limits[i] = min(pair_limits[i], half_distance)
            pair_limits[j] = min(pair_limits[j], half_distance)

    radii = np.minimum(boundary_limits, pair_limits)
    return radii


def run_packing(num_circles: int = NUM_CIRCLES) -> tuple[np.ndarray, np.ndarray, float]:
    """Return circle centers, radii, and their sum."""
    return construct_packing(num_circles=num_circles)


if __name__ == "__main__":
    _, _, sum_radii = run_packing()
    print(f"sum_radii={sum_radii:.12f}")
