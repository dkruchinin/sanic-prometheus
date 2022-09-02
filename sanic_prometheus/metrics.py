import asyncio
import time
import typing as tp

import psutil
from prometheus_client import Counter, Histogram, Gauge


def init(app, latency_buckets=None, multiprocess_mode='all',
         memcollect_enabled=True, metrics_list=None):
    app.metrics['RQS_COUNT'] = Counter(
        'sanic_request_count',
        'Sanic Request Count',
        ['method', 'endpoint', 'http_status']
    )

    hist_kwargs = {}
    if latency_buckets is not None:
        hist_kwargs = {'buckets': latency_buckets}
    app.metrics['RQS_LATENCY'] = Histogram(
        'sanic_request_latency_sec',
        'Sanic Request Latency Histogram',
        ['method', 'endpoint', 'http_status'],
        **hist_kwargs
    )

    if memcollect_enabled:
        app.metrics['PROC_RSS_MEM_BYTES'] = Gauge(
            'sanic_mem_rss_bytes',
            'Resident memory used by process running Sanic',
            multiprocess_mode=multiprocess_mode
        )
        app.metrics['PROC_RSS_MEM_PERC'] = Gauge(
            'sanic_mem_rss_perc',
            'A per cent of total physical memory used by ' +
            'the process running Sanic',
            multiprocess_mode=multiprocess_mode
        )

    if metrics_list:
        for name, pm_metric in metrics_list:
            app.metrics[name] = pm_metric


async def periodic_memcollect_task(app, period_sec, loop):
    p = psutil.Process()
    while True:
        await asyncio.sleep(period_sec, loop=loop)
        app.metrics['PROC_RSS_MEM_BYTES'].set(p.memory_info().rss)
        app.metrics['PROC_RSS_MEM_PERC'].set(p.memory_percent())


def before_request_handler(request):
    _set_start_time_compat(request, time.perf_counter())


def after_request_handler(request, response, get_endpoint_fn):
    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    if not isinstance(response_status, int):
        response_status = int(response_status)  # HTTPStatus -> int

    endpoint = get_endpoint_fn(request)

    req_start_time = _get_start_time_compat(request)
    if req_start_time:
        latency = time.perf_counter() - req_start_time

        request.app.metrics['RQS_LATENCY'].labels(
            request.method, endpoint, response_status
        ).observe(latency)

    request.app.metrics['RQS_COUNT'].labels(
        request.method, endpoint, response_status
    ).inc()


def _set_start_time_compat(request, value: float):
    if hasattr(request, 'ctx'):
        request.ctx.__START_TIME__ = value
    else:
        request['__START_TIME__'] = value


def _get_start_time_compat(request) -> tp.Optional[float]:
    if hasattr(request, 'ctx') and hasattr(request.ctx, '__START_TIME__'):
        return request.ctx.__START_TIME__
    elif hasattr(request, "__getitem__") and '__START_TIME__' in request:
        return request['__START_TIME__']
    return None
