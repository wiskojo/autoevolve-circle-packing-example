# Circle Packing Example

A small example repository for trying out [autoevolve](https://github.com/wiskojo/autoevolve) on an optimization problem.

The goal is to pack 26 circles inside the unit square and maximize the sum of their radii. AlphaEvolve reported a 26-circle construction with sum of radii of `2.63586275`. This example sets a current reference target of `2.6359830849`.

- `program.py` contains the current packing implementation
- `evaluate.py` validates the result and reports the metrics
- `PROBLEM.md` defines the optimization target and constraints
- `PROGRAM.md` tells an agent how to use `autoevolve` in this repo

## Quickstart

Install the `autoevolve` CLI:

```bash
pip install autoevolve-cli
```

Clone the repo:

```bash
git clone https://github.com/wiskojo/autoevolve-circle-packing-example.git
```

Within the repo, tell your coding agent:

```text
Read PROGRAM.md, then start working.
```

Start the dashboard TUI to monitor progress:

```bash
autoevolve dashboard
```
