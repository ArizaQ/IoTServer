from shutil import copyfile

from flask import request, jsonify, Blueprint
from application import topic
from application import mqtt_ws, socketio
from application.apps.picUpload.model import transmitModel, insertUserInfo, getAllUserInfo, runMaskModel, getUserData, \
    takePhotoCommand
from application.apps.utils import constVal
from application.apps.utils.OBSService import uploadFile, downloadFile,uploadUserPicture
import datetime
import requests
import urllib
import json
picUploadBlueprint = Blueprint('picUpload', __name__, template_folder='../../templates', static_folder='../../static')
current_user = None
current_stay_local = False


@mqtt_ws.on_message()
def handle_mqtt_message(client, userdata, message):
    global current_stay_local
    if message.topic == topic:  # picUpload, 图片拍摄完成
        filePathPrefix = "application/static/"
        tempFileName = "temp.jpg"
        fullFileName = filePathPrefix + tempFileName
        with open(fullFileName, mode='wb') as file_obj:
            file_obj.write(message.payload)
        print("picture received")
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_time_file_name=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        # isComplain, isMasked, picUrl=resolveUploadedPicture(tempFileName)
        isMasked = runMaskModel(filePathPrefix + tempFileName)

        pictureUrl=""
        if current_stay_local:
            local_store_file_path="application/static/images/"+create_time_file_name+".jpg"
            copyfile(fullFileName,local_store_file_path)
            pictureUrl="../static/images/"+create_time_file_name+".jpg"
        else:
            pictureUrl = uploadUserPicture(fullFileName,create_time)

        user = insertUserInfo(pictureUrl, isMasked, create_time)
        global current_user
        current_user = user
        current_user["argue"] = -1
        # current_stay_local = False

        socketio.emit('picture_upload',
                      {'data': user,
                       'count': 3}, namespace='', broadcast=True)

    else:
        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        print('Received message on topic: {topic} with payload: {payload}'.format(**data))
@picUploadBlueprint.route('/takePhoto', methods=['GET'])
def takePhoto():
    global current_user
    global current_stay_local
    if current_user is not None:
        sendUserInfoToCloud(current_user)

    ifStayLocal = request.args.get("ifStayLocal")
    if (ifStayLocal == "true"):
        current_stay_local = True
    else:
        current_stay_local = False

    if takePhotoCommand(constVal.topicTakePhoto) == 0:
        return "拍摄成功！"
    else:
        return "抱歉，摄像头有点问题，请重试"


def sendUserInfoToCloud(user):
    if current_stay_local:
        return
    url = constVal.cloudBack + "/uploadPicture"
    payload = json.dumps(user)
    result = requests.post(url, json=payload)
    print(result.status_code)
    print(result.content)


@picUploadBlueprint.route('/feedback', methods=['POST'])
def feedback():
    global current_user
    feedbackContent = request.get_json()['feedback']
    if current_user is None:
        return "请先拍照！"
    else:
        current_user["argue"] = feedbackContent
        return "success"

# 模型下发
@socketio.event
def model_transmit(message):
    pictureUrl = message['data']
    # downloadFile(pictureUrl,constVal.modelPath)
    urllib.request.urlretrieve(pictureUrl, constVal.modelPath)
    print(message)
    print("模型获取成功")

@picUploadBlueprint.route('/modelTransmit', methods=['POST'])
def model_transmit2():
    model_url=request.get_json()
    urllib.request.urlretrieve(model_url, constVal.modelPath)
    print(request.get_json())
    print("模型获取成功")
    return "success"
@picUploadBlueprint.route('/publishToPicUpload', methods=['POST'])
def publish_message():
    # pass
    request_data = request.get_json()
    publish_result = mqtt_ws.publish(request_data['topic'], request_data['msg'])
    status = publish_result[0]
    if status == 0:
        print(f"publish `{request_data['msg']}` to `{request_data['topic']}` successfully.")
    else:
        print(f"publish `{request_data['msg']}` to `{request_data['topic']}` failed.")

    return jsonify({'code': publish_result[0]})


@picUploadBlueprint.route('/', methods=['GET'])
def transmitModelTest():
    # transmitModel()
    return "transfer success"


@picUploadBlueprint.route('/uploadToObs', methods=['GET'])
def uploadToObs():
    # uploadFile('application/resources/','p34.jpg',"user-data","my girlfriend")'
    # readDir("user-data/杨超越/")
    # downloadFile("user-data/p34.jpg","application/resources/")
    insertUserInfo("application/resources/p34.jpg", 0)
    getAllUserInfo()
    return "upload success"

