# PerceptGrid Roadmap

Last reviewed: 2026-10-03.

This is the tracked source of truth for project status and task order. Update
it when a task is completed or the scope changes. Work on one task at a time;
do not automatically start the next phase.

## Project Purpose

Build a reusable Python foundation that reads LiDAR data, preserves its meaning,
and progressively supports processing, geometric detection, tracking, and
spatial analytics. Recorded and live sources must feed the same internal model.

## What Exists Today

| Area | Current state |
| --- | --- |
| Application | Importable `src/perceptgrid` package; `python -m perceptgrid` prints a bootstrap status |
| Python | Requires Python 3.12 |
| Dependencies | uv, `pyproject.toml`, committed `uv.lock`; no runtime dependencies yet |
| Quality | pytest, Ruff lint and formatting, strict mypy for source and tests |
| Tests | One passing test for the entry point |
| Container | Dockerfile using Python 3.12, locked application dependencies, and a non-root runtime user |
| CI | `.github/workflows/ci.yml`: Python quality and Docker smoke-test jobs; local workflow validation passed, first remote run pending |
| LiDAR | Not implemented; Ouster SDK, NumPy, and Open3D are not project dependencies yet |
| Engineering notes | Local `Agents/` files describe phases; this directory is intentionally ignored by Git |

Local verification on the review date: locked offline dependency sync, module
entry point, pytest (1 test), Ruff lint, Ruff format check, and mypy all passed.
Docker build/run, container import, and the non-root runtime (UID 10001) also
passed. The workflow passed actionlint 1.7.12. Remote CI has not run for these
local changes yet.

## Completed Task: B00-01 — Close the Bootstrap Gaps

**Status:** complete locally on 2026-10-03. First remote CI run pending.

Deliverables:

- [x] Add a GitHub Actions workflow that installs Python 3.12 and uv, syncs with
  the lockfile, and runs tests, lint, formatting, and type checks.
- [x] Build the existing Docker image and run its entry point when a Docker
  daemon is available; record any environment blocker instead of claiming success.
- [x] Confirm the package imports and the documented development commands work.
- [x] Update this roadmap with validation results and remaining limitations.

Done when local quality checks and Docker build/run pass, and the CI workflow
is present. Record a successful remote CI run separately when one is available.
No LiDAR features or new runtime dependencies were added.

### Validation Record

Commands were run from the repository root. Local uv checks used
`UV_CACHE_DIR=/tmp/perceptgrid-uv-cache` and `--offline` to reuse the installed
environment; CI installs dependencies normally using the lockfile.

| Check | Result |
| --- | --- |
| `uv sync --locked --offline` | Passed |
| Package import and entry point | Passed |
| `uv run --locked --offline pytest` | Passed: 1 test |
| `uv run --locked --offline ruff check .` | Passed |
| `uv run --locked --offline ruff format --check .` | Passed |
| `uv run --locked --offline mypy` | Passed |
| `actionlint .github/workflows/ci.yml` | Passed using verified official actionlint 1.7.12, temporarily installed under `/tmp` |
| `docker build --tag perceptgrid:bootstrap-check .` | Passed |
| `docker run --rm perceptgrid:bootstrap-check` | Passed; printed bootstrap status and exited successfully |
| Container package import and `os.getuid() == 10001` | Passed |
| Remote GitHub Actions run | Pending a push of these changes |

Docker access required sandbox escalation, which was approved. CI has two
independent jobs with read-only repository permissions, commit-pinned actions,
Python 3.12, and uv 0.12.13. Docker validation runs automatically in CI.

## Next Task: L01-01 — Verify SDK Compatibility and Select a Recording

**Status:** ready, not started. **Prerequisite:** B00-01 complete locally.

- [ ] Verify current official Ouster SDK documentation and Python 3.12 support.
- [ ] Select an SDK version and identify recorded-data and metadata APIs.
- [ ] Select a recording outside Git and document its required companion files,
  access path, and coordinate/timestamp assumptions.
- [ ] Document compatibility findings and the data needed for adapter validation.

This investigation comes before adding models or adapter code. Confirm the
first remote bootstrap CI result when the changes are pushed to GitHub.

## Ordered Roadmap

| Phase | Status | Deliverable | Completion gate |
| --- | --- | --- | --- |
| 00 — Bootstrap | Complete locally; remote CI confirmation pending | Reproducible Python development foundation | Local checks, container validation, CI workflow |
| 01 — LiDAR foundation | L01-01 ready; implementation not started | Stream recorded Ouster scans into PerceptGrid-owned frames and inspect them | Real recording smoke test, preserved metadata, deterministic adapter/model tests |
| 02 — Processing | Queued after Phase 01 | Compose basic sensor-independent point-cloud operations | Tested filtering behavior, metadata alignment, bounded memory |
| 03 — Detection | Queued after Phase 02 | Produce geometric object candidates from processed clouds | Synthetic scene tests and validation against available recordings |
| 04 — Tracking | Queued after Phase 03 | Associate detections over time with persistent IDs | Motion, missed observations, crossings, and variable time interval tests |
| 05 — Live Ouster | Queued after Phase 04 | Feed live scans through the same model and pipeline | Lifecycle and failure tests plus a separate hardware smoke test |
| 06 — Spatial intelligence | Queued after Phase 05 | Derive generic zone and movement events from tracks | Boundary, time gap, entry/exit, and dwell tests |
| 07 — Production | Queued after Phase 06 | Deployment capabilities justified by application requirements | Explicit requirements, documented decisions, operational validation |

## Phase 01 Task Breakdown

L01-01 is the next task; all tasks below are unstarted. Complete them in order.

| ID | Task | Required result |
| --- | --- | --- |
| L01-01 | Verify SDK compatibility and select a recording | Confirm an Ouster SDK version compatible with Python 3.12, check official APIs, identify required data/metadata and an external dataset path |
| L01-02 | Define and test the core frame model | Explicit timestamps and units, source/frame identity, XYZ shape, coordinate frame, validity, and aligned optional fields |
| L01-03 | Implement the recorded Ouster adapter | Iterate scans, convert to the core model, handle errors and cleanup, avoid loading the entire recording |
| L01-04 | Add developer inspection | Report source, frame/scan shape, fields, timestamp meaning, valid measurement counts, and coordinate information |
| L01-05 | Validate the complete recorded-data path | Deterministic adapter/model tests, a real recording smoke test, quality checks, Docker validation, and updated usage documentation |

Before choosing SDK APIs or adding dependencies, consult current official
documentation and record compatibility assumptions. A real recording has not
been selected yet; keep datasets outside Git and mount them into containers.
CI tests should use small synthetic fixtures or mocked SDK boundaries and
must not require sensor hardware or a large recording.

## Phase 02 Task Breakdown

Finalize scope after inspecting the Phase 01 data.

1. **P02-01 — Processing contract:** define stage input/output behavior and
   metadata preservation using the existing frame model.
2. **P02-02 — Basic filters:** implement valid/finite-point filtering, ROI
   cropping, and distance filtering where the data demonstrates a need.
3. **P02-03 — Pipeline composition:** compose stages deterministically and
   test empty clouds, boundaries, and field alignment.
4. **P02-04 — Verification:** add useful inspection/export or visualization,
   document usage, and profile representative recordings. Evaluate voxel
   downsampling only if reduced point density is needed.

Detection and tracking are separate later phases. A cluster is an object
candidate, not a semantic label such as person or vehicle.

## Architecture and Technology Decisions

```text
Recorded source (later: live source)
                ↓
         Sensor adapter
                ↓
     PerceptGrid frame model
                ↓
 Processing → Detection → Tracking → Spatial events
```

- Continue in Python; prefer NumPy vectorization for array operations once
  point-cloud processing exists.
- Keep Ouster-specific objects and calibration conversion inside the adapter.
- Preserve timestamps, validity, units, coordinate frames, and field alignment.
- Stream frames with bounded memory and explicit resource ownership.
- Add dependencies and infrastructure only for the current task.
- Defer Rust. Revisit it only after profiling shows a concrete bottleneck;
  compare a small prototype against the Python/NumPy baseline before adoption.
- APIs, databases, dashboards, GPU work, and orchestration remain outside the
  current scope.

## Task Completion Checklist

- [ ] Deliverables and relevant behavior tests are complete.
- [ ] pytest, Ruff lint, Ruff format check, and strict mypy pass.
- [ ] Docker remains buildable when the task affects packaging or runtime.
- [ ] README usage and this roadmap reflect meaningful changes.
- [ ] External data, hardware dependencies, and unverified checks are explicit.
- [ ] Report exactly one next task; do not start the next phase automatically.

## Working with Local Agent Notes

`Agents/AGENT.md` contains engineering guidance and `Agents/phases/` contains
the detailed phase briefs. `Agents/TASK.MD` should mirror the active task here.
Use the actual directory casing on Linux. These local notes are not tracked,
so all project status and task decisions needed by collaborators belong in
this roadmap.
