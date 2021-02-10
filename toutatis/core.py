import argparse,json
import httpx,sys
from httpx import get

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
    return({"username":username,"userID":userId,"FullName":infos["full_name"],"biography":str(infos["biography"]),"publicEmail":publicEmail,"public_phone_number":publicPhone,"ProfilePicture":infos["profile_pic_url"]})

def searchInProfil(query,sessionid,targetID):
    def scrapeNumber(number):
        cookies = {
            'sessionid': sessionid,
        }

        headers = {
            'User-Agent': 'Instagram 153.0.0.34.96 Android',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en,en-US;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-GPC': '1',
            'TE': 'Trailers',
        }

        params = {
            'search_surface': 'follow_list_page',
            'max_id': number,
            'order': 'default',
            'query': query,
            'enable_groups': 'true'
        }
        try:
            response = httpx.get('https://i.instagram.com/api/v1/friendships/'+targetID+'/followers/', headers=headers, params=params, cookies=cookies)
            return(response.json())
        except :
            exit()
    def appendUsers(users,reponse):
        for user in users:
            reponse.append(user)
        return(reponse)


    terminate=0
    number=0
    responses=[]
    while terminate != 1:
        print(number)
        req=scrapeNumber(number)
        responses=appendUsers(req["users"],responses)
        if req["next_max_id"] != None and req["next_max_id"] != number:
            number=req["next_max_id"]
        else:
            responses=appendUsers(req["users"],responses)
            terminate=1
    return(responses)

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    parser.add_argument('-s', '--sessionid',help="Instagram session ID",required=True)
    parser.add_argument('-u','--username',help="One username",required=True)
    args = parser.parse_args()
    sessionsId=args.sessionid

    infos = getAllInfos(args.username,sessionsId)

    print("Informations about : "+infos["username"])
    print("Full Name : "+infos["FullName"]+" userID : "+infos["userID"])

    info = getInfo(args.username,sessionsId)
    print("Verified : "+str(info['is_verified'])+" Is buisness Acount : "+str(info["is_business"]))
    print("Is private Account : "+str(info["is_private"]))
    print("Follower : "+str(info["follower_count"]) + " Following : "+str(info["following_count"]))
    print("Number of posts : "+str(info["media_count"]))
    print("Number of tag in posts : "+str(info["following_tag_count"]))
    print("External url : "+info["external_url"])
    print("IGTV posts : "+str(info["total_igtv_videos"]))
    if len(infos["biography"]) <1:
        infos["biography"]="Not found"

    print("Biography : "+infos["biography"])

    if len(infos["publicEmail"])==0:
        infos["publicEmail"]="Not found"

    print("Public Email : "+infos["publicEmail"])

    if len(infos["public_phone_number"])<1:
        infos["public_phone_number"]="Not found"

    print("Public Phone number : "+infos["public_phone_number"])
    print("Profile Picture : "+infos["ProfilePicture"])
