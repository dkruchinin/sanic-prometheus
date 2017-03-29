# Sanic prometheus metrics

After a little bit of googling I didn't find a library that would enabled some [prometheus](https://prometheus.io/) metrics for [Sanic](https://github.com/channelcat/sanic)-based apps, so I had to write one. 

## Exposed metrics

At the moment the `sanic-prometheus` provides four metrics:
  * **sanic_request_count** - total number of requests (labels: *method*, *endpoint*, *status*) [[counter](https://prometheus.io/docs/concepts/metric_types/#counter)]
  * **sanic_request_latency_sec** - request latency in seconds (labels: *method*, *endpoint*) [[histogram](https://prometheus.io/docs/concepts/metric_types/#histogram)]
  * **sanic_mem_rss_bytes** - resident memory used by the process (int bytes) [[gague](https://prometheus.io/docs/concepts/metric_types/#gauge)]
  * **sanic_mem_rss_perc** - a percent of total physical memory used by the process running Sanic [[gague](https://prometheus.io/docs/concepts/metric_types/#gauge)]
  
### Labels

* **method**: a HTTP method (i.e. GET/POST/DELETE/etc)
* **endpoint**: just a string, a name identifying a point handling a bunch of requests. By default it's just a first element of the relative path in URL (i.e. for http://myhost/a/b/c you'll end up having `/a` as your endpoint). It is quite configurable, in fact it's up you what's gonna get to the `endpoint` label (see `help(sanic_prometheus.monitor)` for more details)
* **status**: a HTTP status code

## Enabling monitoring

Easy-peasy:

```python
from sanic import Sanic
from sanic_prometheus import monitor

app = Sanic()
...

def main():
  ...
  monitor(app)
  app.run(...)
```

## Options

```
In [1]: from sanic_prometheus import monitor

In [2]: help(monitor)
Help on function monitor in module sanic_prometheus:

monitor(app, port=8000, addr='', endpoint_type='url:1', get_endpoint_fn=None, latency_buckets=None, mmc_period_sec=30)
    Regiesters a bunch of metrics for Sanic server
    (request latency, count, etc) and runs a HTTP
    server for prometheus with /metrics endpoint exposed.

    :param app: an instance of sanic.app
    :param port: a port to run prometheus server on
    :param addr: an address to run the server on
    :param endpoint_type: All request related metrics have a label called
                         'endpoint'. It can be fetched from Sanic `request`
                          object using different strategies specified by
                          `endpoint_type`:
                            url - full relative path of a request URL
                                (i.e. for http://something/a/b/c?f=x you end up
                                having `/a/b/c` as the endpoint)
                            url:n - like URL but with at most `n` path elements
                                in the endpoint (i.e. with `url:1`
                                http://something/a/b/c becomes `/a`).
                            custom - custom endpoint fetching funciton that
                                should be specified by `get_endpoint_fn`
    :param get_endpoint_fn: a custom endpoint fetching function that is ignored
                            until `endpoint_type='custom'`.
                              get_endpoint_fn = lambda r: ...
                            where `r` is Sanic request object
    :param latency_buckets: an optional list of bucket sizes for latency
                            histogram (see prometheus `Histogram` metric)
    :param mmc_period_sec: set a period (in seconds) of how frequently memory
                           usage related metrics are collected
```
