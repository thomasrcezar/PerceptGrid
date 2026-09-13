# PerceptGrid
<p align="center">
  <img src="docs/assets/perceptgrid-logo.png" alt="PerceptGrid" width="600">
</p>

<p align="center">
  <strong>A modular LiDAR processing foundation for spatial intelligence applications.</strong>
</p>

# PerceptGrid

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

* Python
* NumPy
* Ouster SDK
* Open3D
* Docker
* pytest
* Git / GitHub

More technologies will be added only when they are needed.

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

🚧 PerceptGrid is currently in early development.

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
