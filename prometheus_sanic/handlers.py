import time

from sanic.exceptions import NotFound, InvalidUsage

from prometheus_sanic.constants import RequestMetaData, BaseMetrics


def before_request_handler(request):
    # Note, since sanic>=20.3.0 arbitrary setting request keys
    # (e.g. request[...] = ...) are no longer supported. We need
    # to use the ctx object which by default is SimpleNamespace
    # instance. That's why we use setattr/getattr.
    setattr(request.ctx, RequestMetaData.TIME, time.time())

    # Fetch handler from router
    try:
        # Note, number of elements in tuple returned from the
        # request.app.router.get(request) is another backwards
        # incompatible change that happened in sanic 20.3.0.
        # To be more future-proof let's use *_ "rest unpacking"
        _handler, _args, _kwargs, uri, *_ = request.app.router.get(request)
        setattr(request.ctx, RequestMetaData.ROUTER, uri)
    except NotFound:
        setattr(request.ctx, RequestMetaData.ROUTER, None)
    except InvalidUsage:
        setattr(request.ctx, RequestMetaData.ROUTER, None)


def after_request_endpoint_handler(request, response, get_endpoint_fn,
                                   *args, **kwargs):
    lat = time.time() - getattr(request.ctx, RequestMetaData.TIME)
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
    lat = time.time() - getattr(request.ctx, RequestMetaData.TIME)
    uri = getattr(request.ctx, RequestMetaData.ROUTER)

    # Note, that some handlers can ignore response logic,
    # for example, websocket handler
    response_status = response.status if response else 200
    request.app.metrics[BaseMetrics.LATENCY.name].labels(
        request.method, uri, response_status
    ).observe(lat)
    request.app.metrics[BaseMetrics.COUNT.name].labels(
        request.method, uri, response_status
    ).inc()
