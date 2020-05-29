import argparse,json
from requests import get
from quidam import instagram

def recoveryEmail(username):
    return(instagram(username))

def getUserId(username,sessionsId):
    cookies = {'sessionid': sessionsId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
    r = get('https://www.instagram.com/{}/?__a=1'.format(username),headers=headers, cookies=cookies)
    info = json.loads(r.text)
    id = info["logging_page_id"].strip("profilePage_")
    return(id)

def getInfo(username,sessionId):
    userId = getUserId(username,sessionId)
    cookies = {'sessionid': sessionId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
    response = get('https://i.instagram.com/api/v1/users/'+userId+'/info/', headers=headers, cookies=cookies)
    info = json.loads(response.text)
    infoUser = info["user"]
    return(infoUser)

def getFullName(username,sessionId):
    infos = getInfo(username,sessionId)
    return(infos["full_name"])

def getProfilePicture(username,sessionId):
    infos = getInfo(username,sessionId)
    return(infos["profile_pic_url"])

def getBiographie(username,sessionId):
    infos = getInfo(username,sessionId)
    return(infos["biography"])

def extractEmail(username,sessionId):
    userId = getUserId(username,sessionId)
    dict = getInfo(userId,sessionId)
    try:
        return(dict["public_email"])
    except:
        return("NULL")

def extractPhone(username,sessionId):
    userId = getUserId(username,sessionId)
    dict = getInfo(userId,sessionId)
    try:
        return(dict["public_phone_country_code"]+dict["public_phone_number"])
    except:
        return("NULL")

def getAllInfos(username,sessionId):
    userId=getUserId(username,sessionId)
    recoveryemail=recoveryEmail(username)
    cookies = {'sessionid': sessionId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
    response = get('https://i.instagram.com/api/v1/users/'+userId+'/info/', headers=headers, cookies=cookies)
    info = json.loads(response.text)
    infos = info["user"]
    try:
        publicEmail=infos["public_email"]
    except:
        publicEmail=""
    try:
        publicPhone=str(infos["public_phone_country_code"]+infos["public_phone_number"])
    except:
        publicPhone=""
    return({"username":username,"userID":userId,"FullName":infos["full_name"],"biography":str(infos["biography"]),"publicEmail":publicEmail,"public_phone_number":publicPhone,"recoveryEmail":recoveryemail,"ProfilePicture":infos["profile_pic_url"]})
