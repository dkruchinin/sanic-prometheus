from sanic.response import text
from prometheus_client.exposition import (
    generate_latest, core, CONTENT_TYPE_LATEST
)
from . import metrics, endpoint


def monitor(app,
            metrics_endpoint='/metrics',
            endpoint_type='url:1',
            get_endpoint_fn=None,
            latency_buckets=None,
            mmc_period_sec=30):
    """
    Regiesters a bunch of metrics for Sanic server
    (request latency, count, etc) and exposes an endpoint
    for collecting these metrics.

    :param app: an instance of sanic.app
    :param metrics_endpoint: an endpoint for scraping metrics
                             (/metrics is a default one)
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
    """
    m = metrics.init(latency_buckets=latency_buckets)
    get_endpoint = endpoint.fn_by_type(endpoint_type, get_endpoint_fn)

    @app.middleware('request')
    async def before_request(request):
        metrics.before_request_handler(request)

    @app.middleware('response')
    async def before_response(request, response):
        metrics.after_request_handler(m, request, response, get_endpoint)
        return response

    # can't access the loop directly before Sanic starts
    get_loop_fn = lambda: app.loop
    app.add_task(
        metrics.make_periodic_memcollect_task(m, mmc_period_sec, get_loop_fn)
    )

    @app.route(metrics_endpoint, methods=['GET'])
    async def expose_metrics(request):
        return text(generate_latest(core.REGISTRY),
                    content_type=CONTENT_TYPE_LATEST)
