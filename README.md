# FailureLab

FailureLab is a robotics testing project: propose experiments, run a simulator, replay failures, and compare controller revisions.

The first milestone is a Python trace contract and evaluator. The simulator and NVIDIA/Nebius experiment planner are the next milestones.

## Run today's starter

Python 3.11 or newer; no external packages required.

```powershell
python -m unittest discover -s tests -v
python -m failurelab.evaluate examples/delivery.json
```

The example is a hand-authored integration fixture, not an AI-discovered result. The evaluator validates trace structure and reports delivery completion, distance, elapsed simulation time, and recorded collisions. Collision detection itself belongs to the simulator.

See `outputs/BUILD_PLAN.md`, `outputs/JOHNSON_MESSAGE.md`, and `outputs/SIMULATOR_CONTRACT.md` for the schedule, ownership, and shared interface.
