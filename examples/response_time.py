from enum import Enum

from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import json

from prometheus_sanic import monitor
from prometheus_sanic.constants import BaseMetrics
from prometheus_sanic.handlers import after_request_uri_handler

app = Sanic()


async def ping(_request):
    return json({'success': 'you are home'})


async def home(_request, home_id):
    return json({'success': 'you are home', 'home': home_id})


async def user(_request):
    return json({'success': 'you are home'})


@app.exception(NotFound)
async def ignore_404s(request, exception):
    return json({'success': False})


class MyBaseMetrics(BaseMetrics, Enum):
    LATENCY = 'my_app_latency_sec'
    COUNT = 'my_app_count'


if __name__ == "__main__":
    monitor(
        app,
        multiprocess_mode='all',
        is_middleware=True,
        after_handler=after_request_uri_handler,
        base_metrics=MyBaseMetrics
    ).expose_endpoint()

    app.add_route(ping, 'ping', methods=['GET'])
    app.add_route(home, 'home/<home_id:int>', methods=['GET'])
    app.add_route(user, 'user', methods=['GET', 'POST'])

    app.run(host="127.0.0.1", port=8000, workers=1)
