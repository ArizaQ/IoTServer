from application import db, mqtt_ws, topic,jsonify
from application.apps.utils.OBSService import uploadFile
from application.apps.picUpload import modelRun
from application.apps.utils import constVal
import tarfile
# import json
import pymysql
import os


def resolveUploadedPicture(zipFileName):
    filePathPrefix = ""
    extractedFilePath = filePathPrefix + "extracted"

    tf = tarfile.open(filePathPrefix + zipFileName)
    tf.extractall(extractedFilePath)
    data = None
    with open(extractedFilePath + "/result.txt") as f:
        data = f.readlines()
    isComplain = int(data[0])
    isMasked = int(data[1])
    picUrl = uploadFile(extractedFilePath, "1.jpg", "user-data", "hahaha")
    return isComplain, isMasked, picUrl

def runMaskModel(pictureFullPath):
    return int(modelRun.predict(pictureFullPath,constVal.modelPath)[0])
def getUserData(pictureFullPath, isMask):
    return insertUserInfo(pictureFullPath, isMask)

def takePhotoCommand(topicTakePhoto):
    result = mqtt_ws.publish(topicTakePhoto, "takePhoto")
    status = result[0]
    return status

# it's wasted
def transmitModel():
    modelMaskPath = "application/resources/models/modelMask.pth"
    topicTransmit = "/model"
    data = None
    with open(modelMaskPath, 'rb') as f:
        data = f.read(os.path.getsize(modelMaskPath))
    result = mqtt_ws.publish(topicTransmit, data)
    status = result[0]
    return status


def insertUserInfo(picturePath, isMasked,create_time):
    gender = 0
    sql = f"insert into userinfo(pictureurl, \
        ismasked, gender, timeNow)\
         values ('{picturePath}','{isMasked}','{gender}','{create_time}') "
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        db.begin()
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    # db.close()
    return {
        'id': 0,
        'pictureurl': picturePath,
        "ismasked": isMasked,
        "gender": gender,
        "timeNow": create_time
    }


def getAllUserInfo():
    sql = "select * from userinfo "
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    users = cursor.fetchall()
    db.close()
    return users


def getGender(picUrl):
    return 0


class UserInfo():
    def __init__(self, ismasked, gender, timeNow):
        self.id = -1
        self.ismasked = ismasked;
        self.gender = gender
        self.timeNow = timeNow

    def __init__(self, id, ismasked, gender, timeNow):
        self.id = id
        self.ismasked = ismasked;
        self.gender = gender
        self.timeNow = timeNow
