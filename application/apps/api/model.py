from application import db
import pymysql
def getAllUserInfo():
    sql = "select * from userinfo order by timenow  desc limit 10"
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    users = cursor.fetchall()
    # db.close()
    return users
twin_pictures_online=["https://s2.loli.net/2022/06/20/ukxDvzf3jiYHKrA.jpg","https://s2.loli.net/2022/06/20/cKE89ivS5duHnwj.jpg","https://s2.loli.net/2022/06/20/FHZyMa7c6oemXDz.jpg","https://s2.loli.net/2022/06/20/brs7kxmeQBTR2l5.jpg","https://s2.loli.net/2022/06/20/JSlFcN4jwqYgsRC.jpg","https://s2.loli.net/2022/06/20/FnjExzZmASITOlk.jpg ","https://s2.loli.net/2022/06/20/ukxDvzf3jiYHKrA.jpg","https://s2.loli.net/2022/06/20/cKE89ivS5duHnwj.jpg","https://s2.loli.net/2022/06/20/FHZyMa7c6oemXDz.jpg"]

def getAllFullUserInfo():
    users = getAllUserInfo()
    finalData = []
    for user in users:
        twin_pic = twin_pictures_online[getTwinType(user)]
        user['twin_pic'] = twin_pic
        finalData.append(user)
    return finalData


def getTwinType(user):
    male_twin_table=[0,1,2]
    female_twin_table=[3,4,5]
    other_twin_table = [6,7,8]
    gender_mask_table=[male_twin_table,female_twin_table,other_twin_table]
    return gender_mask_table[user['gender']][user['ismasked']]