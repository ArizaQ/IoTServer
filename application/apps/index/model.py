from application import db
import pymysql
def getPictureTest(used):
    # sql="select * from pictures where used="+str(used)
    # cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute(sql)
    # pictures=cursor.fetchall()
    # db.close()
    # return pictures
    pass
def getAllUserInfo():
    sql = "select * from userinfo order by timenow  desc limit 50"
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    users = cursor.fetchall()
    # db.close()
    return users