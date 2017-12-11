import os
from sanic.response import raw
from prometheus_client import (
    start_http_server,
    multiprocess,
    CollectorRegistry
)
from prometheus_client.exposition import (
    generate_latest, core, CONTENT_TYPE_LATEST
)

from . import metrics, endpoint
from .exceptions import SanicPrometheusError


class MonitorSetup:
    def __init__(self, app, multiprocess_on=False):
        self._app = app
        self._multiprocess_on = multiprocess_on

    def expose_endpoint(self):
        """
        Expose /metrics endpoint on the same Sanic server.

        This may be useful if Sanic is launched from a container
        and you do not want to expose more than one port for some
        reason.
        """
        @self._app.route('/metrics', methods=['GET'])
        async def expose_metrics(request):
            return raw(self._get_metrics_data(),
                       content_type=CONTENT_TYPE_LATEST)

    def start_server(self, addr='', port=8000):
        """
        Expose /metrics endpoint on a new server that will
        be launched on `<addr>:<port>`.

        This may be useful if you want to restrict access to
        metrics data with firewall rules.
        NOTE: can not be used in multiprocessing mode
        """
        if self._multiprocess_on:
            raise SanicPrometheusError(
                "start_server can not be used when multiprocessing " +
                "is turned on")
        start_http_server(addr=addr, port=port)

    def _get_metrics_data(self):
        registry = None
        if not self._multiprocess_on:
            registry = core.REGISTRY
        else:
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)
        return data


def monitor(app, endpoint_type='url:1',
            get_endpoint_fn=None,
            latency_buckets=None,
            mmc_period_sec=30,
            multiprocess_mode='all',
            memcollect_enabled=True):
    """
    Regiesters a bunch of metrics for Sanic server
    (request latency, count, etc) and exposes /metrics endpoint
    to allow Prometheus to scrape them out.

    :param app: an instance of sanic.app
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
    :param memcollect_enabled: a simple flag this enable memcollect task and metrics

    NOTE: memory usage is not collected when when multiprocessing is enabled
    """
    multiprocess_on = 'prometheus_multiproc_dir' in os.environ
    get_endpoint = endpoint.fn_by_type(endpoint_type, get_endpoint_fn)

    @app.listener('before_server_start')
    def before_start(app, loop):
        metrics.init(latency_buckets, multiprocess_mode, memcollect_enabled=memcollect_enabled)

    @app.middleware('request')
    async def before_request(request):
        if request.path != '/metrics':
            metrics.before_request_handler(request)

    @app.middleware('response')
    async def before_response(request, response):
        if request.path != '/metrics':
            metrics.after_request_handler(request, response, get_endpoint)

    if multiprocess_on:
        @app.listener('after_server_stop')
        def after_stop(app, loop):
            multiprocess.mark_process_dead(os.getpid())
    elif memcollect_enabled:
        @app.listener('before_server_start')
        async def start_memcollect_task(app, loop):
            app.memcollect_task = loop.create_task(metrics.periodic_memcollect_task(mmc_period_sec, loop))

        @app.listener('after_server_stop')
        async def stop_memcollect_task(app, loop):
            app.memcollect_task.cancel()

    return MonitorSetup(app, multiprocess_on)


__all__ = ['monitor']
