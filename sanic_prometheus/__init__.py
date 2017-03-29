from prometheus_client import start_http_server
from . import metrics, endpoint


def monitor(app, port=8000, addr='',
            endpoint_type='url:1',
            get_endpoint_fn=None,
            latency_buckets=None):
    """
    Regiesters a bunch of metrics for Sanic server
    (latency summary, latency histogram, request count, etc) and runs a HTTP
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

    start_http_server(port, addr)
