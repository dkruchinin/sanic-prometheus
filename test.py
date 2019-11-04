#!/usr/bin/env python3

from prometheus_sanic import monitor
from sanic import Sanic, response, Blueprint

app = Sanic()
test_bp = Blueprint('test')


@test_bp.route('/home', methods=['GET'])
async def home(request):
    return response.json({'success': 'you are home'})


if __name__ == '__main__':
    monitor(app).expose_endpoint()
    app.blueprint(test_bp)
    app.run(host='127.0.0.1', port=8000, auto_reload=False, access_log=True, debug=True)
