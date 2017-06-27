import os
import unittest
from tempfile import mkdtemp
from shutil import rmtree

from sanic import Sanic
from sanic_prometheus import monitor, SanicPrometheusError


TEST_PORT = 54424


class TestMultiprocessing(unittest.TestCase):
    def setUp(self):
        os.environ['prometheus_multiproc_dir'] = mkdtemp()

    def tearDown(self):
        pm_dir = os.environ['prometheus_multiproc_dir']
        if os.path.exists(pm_dir):
            rmtree(pm_dir)

    def test_start_server_should_not_work_with_mp(self):
        app = Sanic('test_mp')
        self.assertRaises(SanicPrometheusError, monitor(app).start_server)
