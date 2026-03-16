# autoevolve

## Setup

Use setup mode whenever `PROBLEM.md` is still incomplete, stubbed, or unclear.

1. Read the repository and the current `PROBLEM.md`.
2. Work with the user to make `PROBLEM.md` concrete. The goal, metric, constraints, and validation should be specific enough that you can execute against them.
3. If important details are missing, ask focused questions and update `PROBLEM.md` as you learn more.
4. Once the validation is defined, run it to make sure it actually works.
5. If this is a new repo or there is no clear baseline yet, establish a baseline result before starting optimization.
6. Do not begin the forever experiment loop until `PROBLEM.md` is ready and the validation is working.
7. Confirm with the user that everything is set up and ready to start autoevolve.

## The Experiment Loop

Your role is to orchestrate experiments and make progress towards the goal defined in `PROBLEM.md`. You are responsible for managing tradeoffs like exploration vs. exploitation, budget constraints, and resource allocation as you see fit. On each iteration, consider what has been tried so far and choose the next direction or set of directions most likely to make meaningful progress toward the goal, whether through small local moves, large global moves, or broader strategic shifts.

LOOP FOREVER:

1. Inspect the current experiment state. Start from the current commit, then use the autoevolve CLI to inspect prior experiments, compare outcomes, identify promising commits to build on, and reason about the search as a whole. Use commands like `autoevolve status`, `autoevolve log`, `autoevolve best`, `autoevolve pareto`, `autoevolve compare`, and `autoevolve lineage`, and anything else you have at your disposal, to understand what has been tried so far and to reflect on where to go next.
2. Plan the next experiment or batch of experiments based on all the work done so far. Reflect on what prior runs have revealed about the search space, the failure modes, and the most promising openings, then decide whether to exploit promising directions, combine successful ideas, explore new ones, or pursue a materially different approach.
3. Launch the planned experiments. Use `autoevolve start <name> <summary> [--from <ref>]` to create each experiment in its own managed worktree. Carry out each experiment through implementation, execution, and evaluation, and capture the resulting metrics and observations.
4. When an experiment reaches a meaningful checkpoint or conclusion, update `JOURNAL.md` and `EXPERIMENT.json`, then use `autoevolve record`. If a direction needs sustained work, continue it as a sequence of committed experiments rather than one giant uncommitted run. If you need to clear stale worktrees, use `autoevolve clean [<name>]` for housekeeping.

The idea is that you are a completely autonomous orchestrator trying things out. If an approach works, keep it. If it doesn't, still keep it. Continue advancing experiments based on what appears most promising while running parallel work toward the goal in `PROBLEM.md`.

**SUBAGENTS**: This autonomous loop only applies to the top-level orchestrator. Delegated subagents or workers should execute only their assigned experiment, record results, and then stop rather than starting or continuing the forever loop. If you are a subagent, `LOOP FOREVER` and any instructions to continue autonomously apply only to the top-level orchestrator, not to you.

Recommendations:

- One commit = one atomic expriment. Every meaningful experiment should be recorded, including both improvements and regressions. The goal is to preserve the full search history, not just the winners.
- If you try an idea or obtain some intermediate result, however small (within reason), consider committing it as an experiment to document it and preserve traceability.
- Prefer fan-out over a single linear chain. Use `autoevolve start` from the current commit, any promising experiment commit, or another intentionally chosen ref, and continue exploring outward through committed experiments rather than one long-lived uncommitted session.
- Keep the filesystem tidy. Put new files, intermediate results, and other artifacts in the repository itself, or preferably in managed worktrees under `~/.autoevolve/worktrees`, and clean them up before committing the experiment. Do not scatter files across `/tmp`, `/private`, cache directories, your home directory, or other ad hoc paths unless the task explicitly requires it. Managed worktrees should be temporary, and once you are done with them, clean them up with the autoevolve lifecycle commands.
- With `autoevolve start` putting things in worktrees, you can work on multiple indepednent streams of work and research directions concurrently. If the problem and resource allows it, you can parallilize aggressively to evalaute multiple streams of ideas at the same time. You can also keep yourself unblocked as you delegate tasks to subagents to work on exploring different research directions and prepare for what to do next after those experiments are completed.

Parallelization:

- When the problem and available resources allow it, you can scale horizontally by working on multiple independent streams and exploring different research directions concurrently.
- When running experiments concurrently, prefer separate worktrees managed by autoevolve lifecycle commands so each workstream stays isolated and conflicts are minimized.
- If it improves efficiency, you can delegate work to subagents and manage them so they can execute tasks or explore different research directions independently.

## How autoevolve works

### Problem Definition

- `PROBLEM.md` defines the task, metric, constraints, and validation.
- The `## Metric` section begins with a structured, non-empty line that defines the primary metric to optimize, followed by an optional description.
- During experiment loops, treat `PROBLEM.md` as read-only unless a human explicitly changes the task.

### Experiment Record

An experiment is a git commit that contains both root `JOURNAL.md` and `EXPERIMENT.json`.

- `JOURNAL.md` is the narrative record. You can update it as the experiment unfolds. Treat it as notes for your future self: hypotheses, changes made, intermediate observations, failures, reflections, and anything else worth preserving.

- `EXPERIMENT.json` is the structured record for the experiment and should follow this shape:

  ```json
  {
    "summary": "one-sentence result summary",
    "metrics": {
      "primary_metric": 0.0,
      "runtime_sec": 0.0
    },
    "references": [
      {
        "commit": "abc1234",
        "why": "borrowed the premium-guard idea from this experiment"
      }
    ]
  }
  ```

- Faithfully record the metrics produced by this experiment. `metrics` should truthfully reflect what this exact experiment commit achieved when evaluated.
- Every experiment should record at least the primary metric declared in `PROBLEM.md`.
- You are not limited to the primary metric. Store any additional metrics that help you compare experiments, reason about tradeoffs, or plan future search.
- Keep metric names consistent across experiments so tools can compare runs and compute best or Pareto-style frontiers later. But you can always add new metrics to the `metrics` object in later experiments if they help you reason about progress.

### Lineage

- The commit is the durable experiment record.
- Git ancestry captures code lineage. `references` captures idea lineage that git alone does not show.

### Tooling

- The autoevolve CLI gives you structured views over this git-backed history. Under the hood it reads git history plus `JOURNAL.md` and `EXPERIMENT.json` from experiment commits and compiles them into useful views for planning the next experiment.
- Use `autoevolve start <name> <summary> [--from <ref>]` to create a managed experiment worktree.
- Use `autoevolve record` from inside a managed experiment worktree to commit the result and remove that worktree.
- Use `autoevolve clean [<name>] [-f]` to remove stale managed worktrees under `~/.autoevolve/worktrees` for the current repository.
- Use `autoevolve log` to inspect prior experiments.
- Use `autoevolve recent`, `autoevolve best --max <metric>`, or `autoevolve pareto --max <metric> --min <metric>` to find strong candidates to build on.
- Use `autoevolve compare <a> <b>` or `autoevolve lineage <ref>` when you need to understand how experiments differ or connect.
- If you need the full command surface, use `autoevolve --help`.
