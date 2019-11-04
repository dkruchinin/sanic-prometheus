import os
import tempfile

os.environ['prometheus_multiproc_dir'] = tempfile.mkdtemp()
