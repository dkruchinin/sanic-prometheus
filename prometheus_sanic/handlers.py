import time

from sanic.exceptions import NotFound, InvalidUsage

from prometheus_sanic.constants import RequestMetaData, BaseMetrics


def before_request_handler(request):
    request[RequestMetaData.TIME] = time.time()

    # Fetch handler from router
    try:
        _handler, _args, _kwargs, uri = request.app.router.get(request)
        request[RequestMetaData.ROUTER] = uri
    except NotFound:
        request[RequestMetaData.ROUTER] = None
    except InvalidUsage:
        request[RequestMetaData.ROUTER] = None


def after_request_endpoint_handler(request, response, get_endpoint_fn,
                                   *args, **kwargs):
    lat = time.time() - request[RequestMetaData.TIME]
    endpoint = get_endpoint_fn(request)

    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    request.app.metrics[BaseMetrics.LATENCY.name].labels(
        request.method, endpoint, response_status
    ).observe(lat)
    request.app.metrics[BaseMetrics.COUNT.name].labels(
        request.method, endpoint, response_status
    ).inc()


def after_request_uri_handler(request, response, *args, **kwargs):
    lat = time.time() - request[RequestMetaData.TIME]

    uri = request[RequestMetaData.ROUTER]

    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    request.app.metrics[BaseMetrics.LATENCY.name].labels(
        request.method, uri, response_status
    ).observe(lat)
    request.app.metrics[BaseMetrics.COUNT.name].labels(
        request.method, uri, response_status
    ).inc()
