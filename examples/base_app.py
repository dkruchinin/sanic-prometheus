from sanic import Sanic
from sanic.response import json

from prometheus_sanic import monitor

app = Sanic()


async def ping(_request):
    return json({'success': 'you are home'})


async def hone(_request):
    return json({'success': 'you are home'})


async def user(_request):
    return json({'success': 'you are home'})


if __name__ == "__main__":
    monitor(
        app,
        multiprocess_mode='all',
        is_middleware=True,
    ).expose_endpoint()

    app.add_route(ping, 'ping', methods=['GET'])
    app.add_route(hone, 'hone', methods=['GET'])
    app.add_route(user, 'user', methods=['GET', 'POST'])

    app.run(host="127.0.0.1", port=8000, workers=1)
