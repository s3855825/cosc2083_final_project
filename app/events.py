from flask import session
from flask_socketio import leave_room, join_room, emit
from flask_login import current_user
from . import socket

ROOM = "PUBLIC CHAT ROOM"


@socket.on('joined', namespace='/chat')
def join(message):
    join_room(ROOM)
    emit('status', {'msg': current_user.student_name + ' has entered the chat.'}, room=ROOM)


@socket.on('left', namespace='/chat')
def left(message):
    leave_room(ROOM)
    emit('status', {'msg': current_user.student_name + ' has left the chat.'}, room=ROOM)


@socket.on('text', namespace='/chat')
def message(message):
    emit('message', {'msg': current_user.student_name + ':' + message['msg']}, room=ROOM)
