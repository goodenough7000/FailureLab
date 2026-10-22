"""Local replay workbench. Run with python -m failurelab.server."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from failurelab.evaluate import evaluate, number, point

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY = 2_000_000


def inspect_run(run):
    """Validate the trace and the geometry needed for safe rendering."""
    if not isinstance(run, dict):
        raise ValueError("Run must be a JSON object")
    metrics = evaluate(run)
    for key in ("run_id", "controller_id"):
        if not isinstance(run[key], str) or not run[key]:
            raise ValueError(f"{key} must be a nonempty string")
    scenario = run["scenario"]
    size = point(scenario["world_size_m"], "world_size_m")
    if any(v <= 0 or v > 10000 for v in size):
        raise ValueError("World dimensions must be positive and at most 10000")
    if number(scenario["robot_radius_m"], "robot_radius_m", 0) <= 0:
        raise ValueError("Robot radius must be positive")
    if not isinstance(scenario["obstacles"], list):
        raise ValueError("obstacles must be a list")
    for obstacle in scenario["obstacles"]:
        for key in ("x_m", "y_m", "width_m", "height_m"):
            number(obstacle[key], key, 0)
        if obstacle["width_m"] <= 0 or obstacle["height_m"] <= 0:
            raise ValueError("Obstacle dimensions must be positive")
    return {"run": run, "metrics": metrics}


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, body, kind="application/json"):
        if kind == "application/json":
            body = json.dumps(body, allow_nan=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            return self.respond(200, {"status": "ok", "mode": "replay"})
        if self.path == "/api/example":
            run = json.loads((ROOT / "examples/delivery.json").read_text())
            return self.respond(200, inspect_run(run))
        assets = {"/": ("index.html", "text/html; charset=utf-8"),
                  "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                  "/style.css": ("style.css", "text/css; charset=utf-8")}
        if self.path in assets:
            name, kind = assets[self.path]
            return self.respond(200, (ROOT / "web" / name).read_bytes(), kind)
        self.respond(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/api/inspect":
            return self.respond(404, {"error": "Not found"})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_BODY:
                return self.respond(413, {"error": "Upload a JSON file smaller than 2 MB"})
            run = json.loads(self.rfile.read(size))
            result = inspect_run(run)
        except (ValueError, KeyError, TypeError, AttributeError, OverflowError) as exc:
            return self.respond(400, {"error": f"Invalid run: {exc}"})
        self.respond(200, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"FailureLab: http://127.0.0.1:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
