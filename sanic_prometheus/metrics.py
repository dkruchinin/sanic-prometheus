import asyncio
import time
import psutil
from prometheus_client import Counter, Histogram, Gauge

# I hate global variables but I didn't find a better way
# to make things compatible with how prometheus_client works
# in multiprocessing mode
METRICS = None


def init(
        latency_buckets=None, multiprocess_mode='all',
        memcollect_enabled=True):
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
        ['method', 'endpoint', 'http_status'],
        **hist_kwargs
    )

    if memcollect_enabled:
        metrics['PROC_RSS_MEM_BYTES'] = Gauge(
            'sanic_mem_rss_bytes',
            'Resident memory used by process running Sanic',
            multiprocess_mode=multiprocess_mode
        )
        metrics['PROC_RSS_MEM_PERC'] = Gauge(
            'sanic_mem_rss_perc',
            'A per cent of total physical memory used by ' +
            'the process running Sanic',
            multiprocess_mode=multiprocess_mode
        )

    global METRICS
    METRICS = metrics


async def periodic_memcollect_task(period_sec, loop):
    p = psutil.Process()
    while True:
        await asyncio.sleep(period_sec, loop=loop)
        METRICS['PROC_RSS_MEM_BYTES'].set(p.memory_info().rss)
        METRICS['PROC_RSS_MEM_PERC'].set(p.memory_percent())


def before_request_handler(request):
    request['__START_TIME__'] = time.time()


def after_request_handler(request, response, get_endpoint_fn):
    lat = time.time() - request['__START_TIME__']
    endpoint = get_endpoint_fn(request)

    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    METRICS['RQS_LATENCY'].labels(request.method, endpoint,
                                  response_status).observe(lat)
    METRICS['RQS_COUNT'].labels(request.method, endpoint,
                                response_status).inc()
