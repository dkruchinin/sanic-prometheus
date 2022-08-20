IS_MULTIPROCESS = True

if IS_MULTIPROCESS:
    import os

    os.environ['prometheus_multiproc_dir'] = 'prometheus_tmp'


import asyncio
from time import time
from enum import Enum

from prometheus_client import Counter, Histogram
from sanic import Sanic
from sanic.response import json

from prometheus_sanic import monitor

app = Sanic()


class MetricsType(Enum):
    COUNT = 'sanic_count'
    TIME_LATENCY = 'sanic_latency_sec'


async def ping(request):
    start_time = time()

    await asyncio.sleep(1)
    request.app.ctx.metrics[MetricsType.COUNT.name].labels(
        label_1='ping',
        label_2='GET',
    ).inc()

    request.app.ctx.metrics[MetricsType.TIME_LATENCY.name].labels(
        label_1='ping',
        label_2='GET',
    ).observe(round(float(time() - start_time), 3))

    return json({'success': 'you are home'})


if __name__ == "__main__":
    monitor(
        app,
        multiprocess_mode='all',
        metrics_path='/metrics',
        is_middleware=False,
        metrics_list=[(
            MetricsType.COUNT.name, Counter(
                name=MetricsType.COUNT.value,
                documentation='Total count',
                labelnames=['label_1', 'label_2']
            )), (
            MetricsType.TIME_LATENCY.name, Histogram(
                name=MetricsType.TIME_LATENCY.value,
                documentation='Gauge',
                labelnames=['label_1', 'label_2'],
            )
        )]
    ).expose_endpoint()

    app.add_route(ping, 'ping', methods=['GET'])
    app.run(host="127.0.0.1", port=8000, workers=2)
