from aiohttp import web
import socketio
import json
import os
import time
import sys
import logging as log

# configure logs
log_file = '{}.log'.format(time.strftime("%d-%m-%Y", time.gmtime()))
log.basicConfig(
        format='%(asctime)s | %(name)s | %(levelname)s: %(message)s',
        filename=sys.path[0]+'/logs/{}'.format(log_file),
        level=log.INFO,
        datefmt='%I:%M:%S %p'
    )

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    with open('templates/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('message')
async def scan_user(request):
    try:
        userdata = {'customername': request.query['customername'], 'carnumber': request.query['carnumber']}
        # Process our userdata
        print("Processing userdata: " , userdata)
        response_obj = { 'status' : 'success' }

        await sio.emit('message', userdata)
        log.info('userdata response {}'.format(userdata))

        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = { 'status' : 'failed', 'reason': str(e) }

        return web.Response(text=json.dumps(response_obj), status=500)

app.router.add_static('/static', os.path.join(os.path.dirname(__file__), 'static'))
app.router.add_get('/', index)
app.router.add_post('/userdata', scan_user)

if __name__ == '__main__':
    web.run_app(app, port=8081)
