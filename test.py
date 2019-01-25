#!/usr/bin/env python3

from sanic_prometheus import monitor
from sanic import Sanic, response, Blueprint
from sanic_limiter import Limiter, get_remote_address


app = Sanic()
test_bp = Blueprint('test')

limiter = Limiter(
    app,
    global_limits=['10 per second', '500 per day'],
    key_func=get_remote_address)


@test_bp.route('/home', methods=['GET'])
async def home(request):
    return response.json({'success': 'you are home'})


if __name__ == '__main__':
    monitor(app).expose_endpoint()
    app.blueprint(test_bp)
    app.run(host='127.0.0.1', port=8000, access_log=True, debug=True)
