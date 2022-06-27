from flask import Flask, render_template, session, request, \
    copy_current_request_context,jsonify,Blueprint
from application import socketio,thread_lock,thread
from flask_socketio import  emit, join_room, leave_room, \
    close_room, rooms, disconnect
from application.apps.api.model import getAllFullUserInfo
apiBlue=Blueprint('api', __name__, template_folder='../../templates', static_folder='../../static')

twin_pictures_online=["https://s2.loli.net/2022/06/20/ukxDvzf3jiYHKrA.jpg","https://s2.loli.net/2022/06/20/cKE89ivS5duHnwj.jpg","https://s2.loli.net/2022/06/20/FHZyMa7c6oemXDz.jpg","https://s2.loli.net/2022/06/20/brs7kxmeQBTR2l5.jpg","https://s2.loli.net/2022/06/20/JSlFcN4jwqYgsRC.jpg","https://s2.loli.net/2022/06/20/FnjExzZmASITOlk.jpg ","https://s2.loli.net/2022/06/20/ukxDvzf3jiYHKrA.jpg","https://s2.loli.net/2022/06/20/cKE89ivS5duHnwj.jpg","https://s2.loli.net/2022/06/20/FHZyMa7c6oemXDz.jpg"]
ws_session=None
ws_emit=None
@apiBlue.route('/getPictures',methods=['GET'])
def getPictures():
    return jsonify( {'data':getAllFullUserInfo(),
          'count': 1})


@apiBlue.route('/reTrainMask',methods=['GET'])
def retrainMask():
    #TODO
    return jsonify("success")

@apiBlue.route('/reTrainGender',methods=['GET'])
def reTrainGender():
    # TODO
    return jsonify("success")

@apiBlue.route('/ws',methods=['GET'])
def testWS():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('picture_upload',
         {'data':getAllFullUserInfo(),
          'count': session['receive_count']},namespace='',broadcast=True)
    return 'done!'






def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})

@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.event
def my_broadcast_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.event
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.event
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room')
def on_close_room(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         to=message['room'])
    close_room(message['room'])


@socketio.event
def my_room_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         to=message['room'])


@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.event
def my_ping():
    emit('my_pong')


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    ws_session=session
    ws_emit=emit
    emit('my_response', {'data': 'Connected1111111111111111111111', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


def getTwinType(user):
    male_twin_table=[0,1,2]
    female_twin_table=[3,4,5]
    other_twin_table = [6,7,8]
    gender_mask_table=[male_twin_table,female_twin_table,other_twin_table]
    return gender_mask_table[user['gender']][user['ismasked']]