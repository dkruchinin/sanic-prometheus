import asyncio
import time
import psutil
from prometheus_client import Counter, Histogram, Gauge


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
    metrics['RQS_LATENCY'] = Histogram(
        'sanic_request_latency_sec',
        'Sanic Request Latency Histogram',
        ['method', 'endpoint'],
        **hist_kwargs
    )

    metrics['PROC_RSS_MEM_BYTES'] = Gauge(
        'sanic_mem_rss_bytes',
        'Resident memory used by process running Sanic'
    )
    metrics['PROC_RSS_MEM_PERC'] = Gauge(
        'sanic_mem_rss_perc',
        'A per cent of total physical memory used by the process running Sanic'
    )

    return metrics


def make_periodic_memcollect_task(metrics, period_sec, get_loop_fn):
    p = psutil.Process()

    async def collector():
        while True:
            await asyncio.sleep(period_sec, loop=get_loop_fn())
            metrics['PROC_RSS_MEM_BYTES'].set(p.memory_info().rss)
            metrics['PROC_RSS_MEM_PERC'].set(p.memory_percent())
    return collector


def before_request_handler(request):
    request['__START_TIME__'] = time.time()


def after_request_handler(metrics, request, response, get_endpoint_fn):
    lat = time.time() - request['__START_TIME__']
    endpoint = get_endpoint_fn(request)
    metrics['RQS_LATENCY'].labels(request.method, endpoint).observe(lat)
    metrics['RQS_COUNT'].labels(request.method, endpoint,
                                response.status).inc()
