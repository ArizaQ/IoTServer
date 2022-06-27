from flask import Flask, render_template, session, request, \
    copy_current_request_context,jsonify,Blueprint
# import aiohttp
# import random
# from aiohttp import web
# from aiohttp.client_ws import ClientWebSocketResponse
# import asyncio
indexBlue=Blueprint('index', __name__, template_folder='../../templates', static_folder='../../static')
from application.apps.index.model import getPictureTest,getAllUserInfo
from websocket import create_connection
import asyncio
import websockets


async def ws_client_main():
    async with websockets.connect("ws://localhost:5000") as websocket:
        # websocket: <class 'websockets.legacy.client.WebSocketClientProtocol'>
        await websocket.send("Hello World")
        msg = await websocket.recv()
        print(msg)


# asyncio.run(ws_client_main())


def send_query_webSocket():
    ws = create_connection("ws://localhost:5000")
    result_1 = ws.recv()  # 接收服务端发送的连接成功消息
    print(result_1)

# send_query_webSocket()
@indexBlue.route('/',methods=['get'])
def index0():
    return render_template("index.html");

@indexBlue.route('/test',methods=['get'])
def indexTest():
    return "test";

@indexBlue.route('/<name>',methods=['get'])
def index(name):
    getPictureTest(1)
    return "hello "+name;

@indexBlue.route('/login',methods=['get'])
def loginPage():
    return render_template("login.html");


@indexBlue.route('/login/login',methods=['post'])
def login():
    email=request.get_json()['email']
    password=request.get_json()['password']
    if email=="admin@qq.com" and password=="12345678":
        return jsonify("success")
    return jsonify("password error")

@indexBlue.route('/admin',methods=['get'])
def adminPage():
    return render_template("admin.html");


@indexBlue.route('/info',methods=['get'])
def info():
    return render_template("info.html")

