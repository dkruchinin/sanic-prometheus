import time
from prometheus_client import Counter, Histogram, Summary


def init(latency_buckets=None):
    metrics = {}
    metrics['RQS_COUNT'] = Counter(
        'sanic_request_count',
        'Sanic Request Count',
        ['method', 'endpoint', 'http_status']
    )

    hist_kwargs = {}
    if latency_buckets is not None:
        hist_kwargs = {'buckets': latency_buckets}
    metrics['RQS_LATENCY_HST'] = Histogram(
        'sanic_request_latency_hist',
        'Sanic Request Latency Histogram',
        ['method', 'endpoint'],
        **hist_kwargs
    )

    metrics['RQS_LATENCY'] = Summary(
        'sanic_request_latency',
        'Sanic Requst Latency',
        ['method', 'endpoint']
    )

    return metrics


def before_request_handler(request):
    request['__START_TIME__'] = time.time()


def after_request_handler(metrics, request, response, get_endpoint_fn):
    lat = time.time() - request['__START_TIME__']
    endpoint = get_endpoint_fn(request)
    metrics['RQS_LATENCY_HST'].labels(request.method, endpoint).observe(lat)
    metrics['RQS_LATENCY'].labels(request.method, endpoint).observe(lat)
    metrics['RQS_COUNT'].labels(request.method, endpoint,
                                response.status).inc()
