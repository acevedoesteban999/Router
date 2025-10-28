import asyncio, aiohttp, time
from threading import Thread
from flask import Blueprint, jsonify

async def _ping(host, timeout=2):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as s:
            async with s.get(host):
                return True
    except:
        return False

status_info = {'status': 'no-network'}   

def bg_ping_loop():                     
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        internet = loop.run_until_complete(_ping('https://8.8.8.8'))
        if internet:
            status_info['status'] = 'network'
        else:
            portal = loop.run_until_complete(_ping('https://secure.etecsa.net:8443'))
            status_info['status'] = 'router' if portal else 'no-network'
        #print(status_info)
        time.sleep(5)


Thread(target=bg_ping_loop, daemon=True).start()

api_bp = Blueprint('api', __name__, url_prefix='/api')
@api_bp.route('/status')
def api_status():
    return jsonify(status_info)