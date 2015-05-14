from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, send, join_room, leave_room
import json

app = Flask(__name__)
socketio = SocketIO(app)

values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template("testhtml.html", **values)

@socketio.on('send_message')
def handle_source(json_data):
    text = json_data['message'].encode('ascii', 'ignore')
    socketio.emit('echo', {'echo': 'Server Says: '+text})

@socketio.on('value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    print(message)

if __name__ == "__main__":
    socketio.run(app)