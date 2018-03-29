import os
import re
import unittest
from tempfile import mkdtemp
from shutil import rmtree
from time import sleep
from multiprocessing import Process
from urllib import request
from importlib import reload

from sanic import Sanic
from sanic.response import json
import prometheus_client
from sanic_prometheus import monitor, SanicPrometheusError


TEST_PORT = 54424


def launch_server():
    app = Sanic('test_mp')

    @app.route('/test')
    async def test(request):
        return json({'a': 'b'})

    monitor(app).expose_endpoint()
    app.run(port=TEST_PORT, workers=2)


class TestMultiprocessing(unittest.TestCase):
    def setUp(self):
        self._procs = []

    def tearDown(self):
        for p in self._procs:
            p.terminate()

    def test_start_server_should_not_work_with_mp(self):
        app = Sanic('test_mp')
        self.assertRaises(SanicPrometheusError, monitor(app).start_server)

    def test_metrics_are_aggregated_between_workers(self):
        p = Process(target=launch_server)
        self._procs.append(p)
        p.start()
        sleep(1)

        for _ in range(100):
            r = request.urlopen("http://localhost:{}/test".format(TEST_PORT))
            _ = r.read()

        r = request.urlopen("http://localhost:{}/metrics".format(TEST_PORT))
        nreqs = None
        for l in r.readlines():
            l = l.decode('ascii')
            m = re.match(r"^service_request_count\{.+\}\s+(\d+)\s*", l)
            if m:
                nreqs = int(m.group(1))
                break
        self.assertIsNotNone(nreqs)
        self.assertEqual(nreqs, 100)
