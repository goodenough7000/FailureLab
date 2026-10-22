import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from failurelab.server import Handler


class ReplayApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, method, path, body=None):
        connection = HTTPConnection(*self.server.server_address)
        connection.request(method, path, body)
        response = connection.getresponse()
        status, content = response.status, response.read()
        connection.close()
        return status, content

    def test_example_can_be_imported_without_changes(self):
        status, body = self.request("GET", "/api/example")
        self.assertEqual(status, 200)
        data = json.loads(body)
        status, imported = self.request("POST", "/api/inspect", json.dumps(data["run"]))
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(imported), data)

    def test_malformed_uploads_return_actionable_errors(self):
        for body in ("not json", "[]", "null", '{"schema_version":"1.0"}'):
            with self.subTest(body=body):
                status, result = self.request("POST", "/api/inspect", body)
                self.assertEqual(status, 400)
                self.assertIn("Invalid run", json.loads(result)["error"])

    def test_invalid_geometry_rejected(self):
        _, body = self.request("GET", "/api/example")
        run = json.loads(body)["run"]
        run["scenario"]["world_size_m"] = [0, 10]
        status, _ = self.request("POST", "/api/inspect", json.dumps(run))
        self.assertEqual(status, 400)

    def test_only_app_assets_are_served(self):
        for path in ("/.env", "/../README.md", "/failurelab/server.py"):
            self.assertEqual(self.request("GET", path)[0], 404)
        self.assertEqual(self.request("GET", "/")[0], 200)

    def test_body_limit(self):
        self.assertEqual(self.request("POST", "/api/inspect", " " * 2_000_001)[0], 413)
