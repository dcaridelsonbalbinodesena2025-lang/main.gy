import os
from flask import Flask
from flask_socketio import SocketIO
from pocketoptionapi.stable_api import PocketOption
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# AQUI VOCÊ VAI COLAR O SEU SSID DEPOIS
SSID = "COLE_SEU_SSID_AQUI" 

api = PocketOption(SSID)
api.connect()

def enviar_precos():
    while True:
        # Pega preços de todos os ativos ativos (incluindo OTC)
        precos = api.get_all_realtime_candles()
        for ativo, dados in precos.items():
            socketio.emit('v19_update', {'ativo': ativo, 'valor': dados['close']})
        eventlet.sleep(0.5)

if __name__ == '__main__':
    eventlet.spawn(enviar_precos)
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
