# FailureLab

FailureLab is a robotics testing project: propose experiments, run a simulator, replay failures, and compare controller revisions.

The first milestone includes a Python trace evaluator and a browser replay workbench with JSON import, playback, a time slider, and event navigation. The simulator and NVIDIA/Nebius experiment planner are the next milestones.

## Run today's starter

Python 3.11 or newer; no external packages required.

```powershell
python -m unittest discover -s tests -v
python -m failurelab.evaluate examples/delivery.json
python -m failurelab.server
```

Open http://127.0.0.1:8000 to use the replay workbench. Use `--port 8001` if port 8000 is occupied. Import a simulator run matching the v1.0 contract, or load the included example. The local server binds only to your computer; it is not a production hosting server. Uploads are evaluated in memory and are not saved.

The example is a hand-authored integration fixture, not an AI-discovered result. The evaluator validates trace structure and reports delivery completion, distance, elapsed simulation time, and recorded collisions. Collision detection itself belongs to the simulator. Playback interpolates recorded positions for display.

The app exposes `GET /api/health`, `GET /api/example`, and `POST /api/inspect` (a complete run JSON, maximum 2 MB). Simulation execution and AI search are not implemented yet. Johnson owns the simulator; the workbench consumes its output without modifying his engine.

See `outputs/BUILD_PLAN.md`, `outputs/JOHNSON_MESSAGE.md`, and `outputs/SIMULATOR_CONTRACT.md` for the schedule, ownership, and shared interface.
