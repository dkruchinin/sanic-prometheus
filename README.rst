Sanic prometheus metrics
=========================
|Build Status| |PyPI| |PyPI version|

After googling for a while I didn't find a library that would enable some `prometheus <https://prometheus.io/>`_ metrics for `Sanic <https://github.com/channelcat/sanic>`_-based apps, so I had to write one. It makes adding monitoring to your Sanic app super easy, just add one line to your code (ok, two if you count import :) and point Prometheus to a newly appeared `/metrics` endpoint.

Versions compatibility
----------------------

* ☑︎ use **>= 0.1.0** for Sanic <= 0.4.1
* ☑︎ use **0.1.3** for Sanic >= 0.5.0
* ☑︎ use >= **0.1.4** if you need multiprocessing support
* ☑︎ use **0.1.6** if you have to use `promtheus-client` <= 0.4.2
* ☑︎ use **0.1.8** with `prometheus-client` >= 0.5.0
* ☑︎ use **0.2.0** with `prometheus-client` >= 0.7.1 and Sanic >= 18.12

Exposed metrics
-----------------

At the moment ``sanic-prometheus`` provides four metrics:

* **sanic_request_count** - total number of requests (labels: *method*, *endpoint*, *status*) [`counter <https://prometheus.io/docs/concepts/metric_types/#counter>`_]
* **sanic_request_latency_sec** - request latency in seconds (labels: *method*, *endpoint*) [`histogram <https://prometheus.io/docs/concepts/metric_types/#histogram>`_]
* **sanic_mem_rss_bytes** - resident memory used by the process (in bytes) [`gauge <https://prometheus.io/docs/concepts/metric_types/#gauge>`_]
* **sanic_mem_rss_perc** - a percent of total physical memory used by the process running Sanic [`gauge <https://prometheus.io/docs/concepts/metric_types/#gauge>`_]

Labels
-----------------

* **method**: a HTTP method (i.e. GET/POST/DELETE/etc)
* **endpoint**: just a string, a name identifying a point handling a group of requests. By default it's just the first element of the relative path of the URL being called (i.e. for http://myhost/a/b/c you'll end up having ``/a`` as your endpoint). It is quite configurable, in fact it's up you what's gonna get to the ``endpoint`` label (see ``help(sanic_prometheus.monitor)`` for more details)
* **http_status**: a HTTP status code

Enabling monitoring
-----------------

Easy-peasy:

.. code:: python

  from sanic import Sanic
  from sanic_prometheus import monitor

  app = Sanic()
  ...

  if __name__ == "__main__":
    monitor(app).expose_endpoint() # adds /metrics endpoint to your Sanic server
    app.run(host="0.0.0.0", port=8000)


Actually, there're two ways to run monitoring:


1. The one you've seen above, ``monitor(app).expose_endpoint()``.
   It just adds a new ``route`` to your Sanic app, exposing ``/metrics`` endpoint
   on the same host and port your Sanic server runs. It might be useful if you run your
   app in a container and you do not want to expose different ports for metrics and everything else.
   You can customize the ``/metrics`` endpoint by passing the ``metrics_path`` keyword argument:
   ``monitor(app, metrics_path='/my_metrics_path').expose_endpoint()``.
2. ``monitor(app).start_server(addr=..., port=...)``.
   Runs a HTTP server on given address and port and exposes ``/metrics`` endpoint on it.
   This might be useful if you want to restrict access to your ``/metrics`` endpoint using some
   firewall rules


Multiprocess mode
-----------------

Sanic allows to launch multiple worker processes to utilise parallelisation, which is great but makes metrics collection much trickier (`read more <https://github.com/prometheus/client_python/blob/master/README.md#multiprocess-mode-gunicorn>`_) and introduces some limitations.

In order to collect metrics from multiple workers, create a directory and point a ``prometheus_multiproc_dir`` environment variable to it. Make sure the directory is empty before you launch your service::


     % rm -rf /path/to/your/directory/*
     % env prometheus_multiproc_dir=/path/to/your/directory python your_sanic_app.py


Unfortunately you can not use ``monitor(app).start_server(addr=..., port=...)`` in multiprocess mode as it exposes a prometheus endpoint from a newly created process.

Configuration
-----------------

Best you can do is::

     % ipython
     In [1]: from sanic_prometheus import monitor
     In [2]: help(monitor)


Prometheus quering examples:
-----------------------------

* *Average latency over last 30 minutes*::

    rate(sanic_request_latency_sec_sum{endpoint='/your-endpoint'}[30m]) /
    rate(sanic_request_latency_sec_count{endpoint='/your-endpoint'}[30m])

* *95th percentile of request latency*::

    histogram_quantile(0.95, sum(rate(sanic_request_latency_sec_bucket[5m])) by (le))

* *Physical memory usage percent over last 10 minutes*::

    rate(sanic_mem_rss_perc[10m])

.. |Build Status| image:: https://travis-ci.org/dkruchinin/sanic-prometheus.svg?branch=master
   :target: https://travis-ci.org/dkruchinin/sanic-prometheus
.. |PyPI| image:: https://img.shields.io/pypi/v/sanic-prometheus.svg
   :target: https://pypi.python.org/pypi/sanic-prometheus/
.. |PyPI version| image:: https://img.shields.io/pypi/pyversions/sanic-prometheus.svg
   :target: https://pypi.python.org/pypi/sanic-prometheus/
