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
* **endpoint**: just a string, a name identifying a point handling a group of requests. By default it's just the first element of the relative path in the URL being called (i.e. for http://myhost/a/b/c you'll end up having `/a` as your endpoint). It is quite configurable, in fact it's up you what's gonna get to the `endpoint` label (see `help(sanic_prometheus.monitor)` for more details)
* **status**: a HTTP status code

## Enabling monitoring

Easy-peasy:

```python
from sanic import Sanic
from sanic_prometheus import monitor

app = Sanic()
...

if __name__ == "__main__":
    monitor(app)
    app.run(host="0.0.0.0", port=8000)
```

## Options

Best you can do is

```
% ipython
In [1]: from sanic_prometheus import monitor
In [2]: help(monitor)
```
