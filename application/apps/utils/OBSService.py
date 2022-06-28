from obs import ObsClient
import datetime
# 创建ObsClient实例
obsClient = ObsClient(
    access_key_id='WOFJ0CGNYNU0EEWP0GMZ',
    secret_access_key='WCWS0DyTo1H3KZnlnFyBUf9anq1SP5B5DVfZFaKC',
    server='obs.cn-north-4.myhuaweicloud.com'
)
bucketName="iot-data-zwq"

# 使用访问OBS


'''
subject:
    user-data
    mask-data
        tag:
            mask
            incorrect-mask
            no-mask
    gender-data:
        tag:
            male
            female
            others
    model:
        tag:
            model-info
    fusion:

'''
def uploadFile(filePathPrefix,fileName,subject, tag):
    resp=0
    if subject=='user-data':
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resp = obsClient.putFile(bucketName, subject+"/"+create_time+".jpg", filePathPrefix+fileName)
    else:
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resp = obsClient.putFile(bucketName, subject+"/"+tag+"/"+create_time+fileName, filePathPrefix + fileName)

    if resp.status < 300:
        # 输出请求Id
        print('requestId:', resp.requestId)
        obsClient.close()
        return resp.body['objectUrl']
    else:
        # 输出错误码
        print('errorCode:', resp.errorCode)
        # 输出错误信息
        print('errorMessage:', resp.errorMessage)
        return resp.errorMessage
        obsClient.close()

def uploadUserPicture(filePath,create_time):
    resp=0
    fileName="temp.jpg"
    resp = obsClient.putFile(bucketName, "mask-data/mask/"+create_time+fileName, filePath)
    if resp.status < 300:
        # 输出请求Id
        print('requestId:', resp.requestId)
        obsClient.close()
        return resp.body['objectUrl']
    else:
        # 输出错误码
        print('errorCode:', resp.errorCode)
        # 输出错误信息
        print('errorMessage:', resp.errorMessage)
        return resp.errorMessage
        obsClient.close()

def readDir(dirPrefix):
    try:
        resp = obsClient.listObjects(bucketName, prefix=dirPrefix, max_keys=100)
        resultList=[]
        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('name:', resp.body.name)
            print('prefix:', resp.body.prefix)
            print('max_keys:', resp.body.max_keys)
            print('is_truncated:', resp.body.is_truncated)
            index = 1
            for content in resp.body.contents:
                resultList.append(content.key)
                print('object [' + str(index) + ']')
                print('key:', content.key[content.key.rindex('/')+1:])
                downloadFile(content.key, "application/resources/")
                print('lastModified:', content.lastModified)
                print('etag:', content.etag)
                print('size:', content.size)
                print('storageClass:', content.storageClass)
                print('owner_id:', content.owner.owner_id)
                print('owner_name:', content.owner.owner_name)
                index += 1
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        import traceback
        print(traceback.format_exc())
    return resultList


def downloadFile(objectName,downloadPath):
    try:
        fullDownloadPath=""
        if objectName.count('/')!=0:
            fullDownloadPath=downloadPath+objectName[objectName.rindex('/')+1:]
        else:
            fullDownloadPath = downloadPath + objectName
        resp = obsClient.getObject(bucketName, objectName, downloadPath=fullDownloadPath)

        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('url:', resp.body.url)
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        import traceback
        print(traceback.format_exc())

def readBinaryFile(objectName):
    try:
        resp = obsClient.getObject(bucketName, objectName, loadStreamInMemory=True)

        if resp.status < 300:
            print('requestId:', resp.requestId)
            # 获取对象内容
            print('buffer:', resp.body.buffer)
            print('size:', resp.body.size)
            return resp.body.buffer
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return resp.errorCode
    except:
        import traceback
        print(traceback.format_exc())

def calculatePictureObsPath(subject,tag,fileName):
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    obsPath= subject + "/" + tag + "/" + create_time+".png"
    return obsPath