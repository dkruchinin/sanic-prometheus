import time

from sanic.exceptions import NotFound, InvalidUsage

from prometheus_sanic.constants import RequestMetaData, BaseMetrics


def before_request_handler(request):
    setattr(request.ctx, RequestMetaData.TIME, time.time())


def after_request_endpoint_handler(request, response, get_endpoint_fn,
                                   *args, **kwargs):
    lat = time.time() - getattr(request.ctx, RequestMetaData.TIME)
    endpoint = get_endpoint_fn(request)

    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    request.app.ctx.metrics[BaseMetrics.LATENCY.name].labels(
        request.method, endpoint, response_status
    ).observe(lat)
    request.app.ctx.metrics[BaseMetrics.COUNT.name].labels(
        request.method, endpoint, response_status
    ).inc()


def after_request_uri_handler(request, response, *args, **kwargs):
    lat = time.time() - getattr(request.ctx, RequestMetaData.TIME)
    uri = request.path

    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    request.app.ctx.metrics[BaseMetrics.LATENCY.name].labels(
        request.method, uri, response_status
    ).observe(lat)
    request.app.ctx.metrics[BaseMetrics.COUNT.name].labels(
        request.method, uri, response_status
    ).inc()
