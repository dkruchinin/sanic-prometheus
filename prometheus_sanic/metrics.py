import time
from typing import List, Tuple

from prometheus_client import Counter, Histogram
from prometheus_client.metrics import MetricWrapperBase


class MetricsName:
    LATENCY = 'RQS_LATENCY'
    COUNT = 'RQS_COUNT'


def init(app, latency_buckets=None, multiprocess_mode='all',
         metrics_list: List[Tuple[str, MetricWrapperBase]] = None):
    app.metrics[MetricsName.COUNT] = Counter(
        'sanic_request_count',
        'Sanic Request Count',
        ['method', 'endpoint', 'http_status']
    )

    hist_kwargs = {}
    if latency_buckets is not None:
        hist_kwargs = {'buckets': latency_buckets}
    app.metrics[MetricsName.LATENCY] = Histogram(
        'sanic_request_latency_sec',
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


def before_request_handler(request):
    request['__START_TIME__'] = time.time()


def after_request_handler(request, response, get_endpoint_fn):
    lat = time.time() - request['__START_TIME__']
    endpoint = get_endpoint_fn(request)

    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    request.app.metrics[MetricsName.LATENCY].labels(
        request.method, endpoint, response_status
    ).observe(lat)
    request.app.metrics[MetricsName.COUNT].labels(
        request.method, endpoint, response_status
    ).inc()
