from typing import List, Tuple

from prometheus_client import Counter, Histogram
from prometheus_client.metrics import MetricWrapperBase


def init(app, latency_buckets=None, multiprocess_mode='all',
         metrics_list: List[Tuple[str, MetricWrapperBase]] = None,
         metrics=None):
    app.metrics[metrics.COUNT.name] = Counter(
        metrics.COUNT.value,
        'Sanic Request Count',
        ['method', 'endpoint', 'http_status']
    )

    hist_kwargs = {}
    if latency_buckets is not None:
        hist_kwargs = {'buckets': latency_buckets}
    app.metrics[metrics.LATENCY.name] = Histogram(
        metrics.LATENCY.value,
        'Sanic Request Latency Histogram',
        ['method', 'endpoint', 'http_status'],
        **hist_kwargs
    )

    if metrics_list:
        for name, pm_metric in metrics_list:
            # todo set multiprocess_mode is Gauge
            # app.metrics[name'] = Gauge(
            #             ...
            #             multiprocess_mode=multiprocess_mode
            #         )
            app.metrics[name] = pm_metric
