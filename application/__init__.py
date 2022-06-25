from flask import Flask, render_template, session, request, \
    copy_current_request_context,jsonify
from flask_mqtt import Mqtt
import pymysql
import random
from application.settings.dev import DevelopmentConfig
from application.settings.prop import  ProductionConfig
from paho.mqtt import client as mqtt_client
from threading import Lock
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_cors import CORS
# 加载配置
config= {
    'dev': DevelopmentConfig,
    'prop': ProductionConfig
}
Config= config['dev']
# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
app = Flask(
    __name__, static_folder="./static", template_folder="./templates")
app.config.from_object(Config)
CORS(app, resources=r'/*')
# 连接数据库
db = pymysql.connect(host=Config.DB_HOST, port=Config.DB_PORT, user=Config.DB_UN, passwd=Config.DB_PW, db=Config.DB_NAME)
# 建立游标
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)  # 返回{}或[{}, {}, ...]
# cursor = db.cursor()  # 返回()或((), (), ...)

async_mode=None
disconnected = None
socketio = SocketIO(app, cors_allowed_origins="*")
thread=None
thread_lock=Lock()
# bootstrap = Bootstrap(app)
broker = '127.0.0.1'
port = 1883
topic = "/picUpload"
client_id = f'python-mqtt-{random.randint(0, 100)}'
topicTest='test'
mqtt_ws = Mqtt(app)
mqtt_ws.subscribe(topic)
mqtt_ws.subscribe(topicTest)


from .apps.picUpload.views import picUploadBlueprint
app.register_blueprint(picUploadBlueprint, url_prefix='/picUpload')
from .apps.index.views import indexBlue
app.register_blueprint(indexBlue,url_prefix='/')
from .apps.api.views import apiBlue
app.register_blueprint(apiBlue,url_prefix='/api')