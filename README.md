# PerceptGrid
<p align="center">
  <img src="docs/assets/perceptgrid-logo.png" alt="PerceptGrid" width="600">
</p>

<p align="center">
  <strong>A modular LiDAR processing foundation for spatial intelligence applications.</strong>
</p>

PerceptGrid is a Python-based project for learning, processing, and building solutions with LiDAR data.

The project starts with recorded Ouster datasets and will later support live Ouster sensors and other LiDAR sources.

The main goal is to build a reusable foundation for future LiDAR and spatial intelligence applications.

## Initial Pipeline

```text
LiDAR Source
     ↓
Sensor Adapter
     ↓
LiDAR Frame
     ↓
Point Cloud
     ↓
Processing
     ↓
Analysis / Visualization
```

## Version 1 Goals

* Read recorded Ouster LiDAR data
* Inspect LiDAR frames and metadata
* Generate point clouds
* Filter and process point-cloud data
* Visualize and analyze the results
* Create a reusable sensor-independent pipeline
* Run the project using Docker
* Prepare the architecture for future live sensors

## Technology

Implemented foundation:

* Python 3.12 with a `src/` package layout
* uv and a committed dependency lockfile
* pytest, Ruff, and strict mypy checks
* Dockerfile for a non-root Linux runtime
* GitHub Actions for Python quality checks and Docker validation
* Git

Planned for LiDAR work: Ouster SDK and NumPy. Open3D will be evaluated when
visualization is useful. These libraries are not installed in the project yet.

Development continues in Python. Rust is deferred until profiling identifies
a concrete bottleneck and benchmarks justify adding it.

## Future Direction

PerceptGrid will progressively evolve toward:

```text
LiDAR Data
    ↓
Processing
    ↓
Detection
    ↓
Tracking
    ↓
Spatial Analytics
    ↓
Real-world Applications
```

## Status

Phase 00 is complete locally: the Python bootstrap exists and the application
prints a status message. Recorded data loading, point-cloud processing,
detection, tracking, and live sensors are not implemented yet.

The local test, lint, formatting, and type checks pass. Docker build/run and
the non-root runtime have been verified. The CI workflow is validated locally;
its first remote run is pending a push to GitHub.

## Tasks and Roadmap

[The project roadmap](docs/ROADMAP.md) is the main task list. It records the
current state, the active task, ordered next steps, and completion criteria.

The next task is **L01-01: verify Ouster SDK compatibility and select a recording**.
Phase 01 will add recorded Ouster data inspection through a sensor-independent
frame model.
Later phases remain queued until their prerequisites are complete.

## Development

Install Python 3.12 and uv, then run these commands from the repository root:

```bash
uv sync --locked
uv run python -m perceptgrid
```

Check behavior, code style, formatting, and types:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Mypy checks both source code and tests in strict mode. Development tools are
recorded in `pyproject.toml` and `uv.lock`.

## Continuous Integration

`.github/workflows/ci.yml` runs on pushes, pull requests, and manual dispatch.
It has two independent jobs:

* Python 3.12 quality checks: locked dependency sync, package import, entry point,
  pytest, Ruff lint, formatting, and strict mypy.
* Docker validation: image build, entry point smoke test, package import, and
  verification of the non-root runtime user.

Actions are pinned to commit hashes. CI uses uv 0.12.13, matching the Dockerfile,
with read-only repository permissions and no retained checkout credentials.
No image is published by this workflow.

## Docker

With Docker running (in Linux container mode on Docker Desktop), build and run:

```bash
docker build -t perceptgrid:dev .
docker run --rm perceptgrid:dev
```

The image installs the application from the lockfile without development tools
and runs as a non-root user. The build context excludes local environments and
datasets. The current application prints its bootstrap status and exits.

The Python base image follows the 3.12 slim-trixie tag, so rebuilding can pick up
base-image updates. The lockfile fixes application dependencies; it does not pin
the base image or isolated build dependencies.
