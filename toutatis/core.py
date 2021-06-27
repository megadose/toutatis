import sys
import colorama
import argparse,json
import httpx,hmac,hashlib,urllib
import requests
import os
from httpx import get
from colorama import Fore, Back, Style, init

colorama.init(autoreset=True)


def getUserId(username,sessionsId):
    cookies = {'sessionid': sessionsId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
    r = get('https://www.instagram.com/{}/?__a=1'.format(username),headers=headers, cookies=cookies)
    try:
        info = json.loads(r.text)
        id = info["logging_page_id"].strip("profilePage_")
        return({"id":id,"error":None})
    except :
        return({"id":None,"error":"User not found or rate limit"})

def getInfo(username,sessionId):
    userId=getUserId(username,sessionId)
    if userId["error"]!=None:
        return({"user":None,"error":"User not found or rate limit"})
    else:
        cookies = {'sessionid': sessionId}
        headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
        response = get('https://i.instagram.com/api/v1/users/'+userId["id"]+'/info/', headers=headers, cookies=cookies)
        info = json.loads(response.text)
        infoUser = info["user"]
        infoUser["userID"]=userId["id"]
        return({"user":infoUser,"error":None})


def advanced_lookup(username):
    USERS_LOOKUP_URL = 'https://i.instagram.com/api/v1/users/lookup/'
    SIG_KEY_VERSION = '4'
    IG_SIG_KEY = 'e6358aeede676184b9fe702b30f4fd35e71744605e39d2181a34cede076b3c33'

    def generate_signature(data):
        return 'ig_sig_key_version=' + SIG_KEY_VERSION + '&signed_body=' + hmac.new(IG_SIG_KEY.encode('utf-8'),data.encode('utf-8'),hashlib.sha256).hexdigest() + '.'+ urllib.parse.quote_plus(data)

    def generate_data( phone_number_raw):
        data = {'login_attempt_count': '0',
                'directly_sign_in': 'true',
                'source': 'default',
                'q': phone_number_raw,
                'ig_sig_key_version': SIG_KEY_VERSION
                }
        return data

    data=generate_signature(json.dumps(generate_data(username)))
    headers={
    "Accept-Language": "en-US",
    "User-Agent": "Instagram 101.0.0.15.120",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "X-FB-HTTP-Engine": "Liger",
    "Connection": "close"}
    try:
        r = httpx.post(USERS_LOOKUP_URL,headers=headers,data=data)
        rep=r.json()
        return({"user":rep,"error":None})
    except :
        return({"user":None,"error":"rate limit"})


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    parser.add_argument('-s', '--sessionid',help="Instagram session ID",required=True)
    parser.add_argument('-u','--username',help="One username",required=True)
    args = parser.parse_args()
    sessionsId=args.sessionid


    infos = getInfo(args.username,sessionsId)
    if infos["user"]==None:
        print(infos["error"])
    else:
        infos=infos["user"]

        print("Informations about     : "+infos["username"])
        print("Full Name              : "+infos["full_name"]+" | userID : "+infos["userID"])
        print("Verified               : "+str(infos['is_verified'])+" | Is buisness Account : "+str(infos["is_business"]))
        print("Is private Account     : "+str(infos["is_private"]))
        print("Follower               : "+str(infos["follower_count"]) + " | Following : "+str(infos["following_count"]))
        print("Number of posts        : "+str(infos["media_count"]))
        print("Number of tag in posts : "+str(infos["following_tag_count"]))
        print("External url           : "+infos["external_url"])
        print("IGTV posts             : "+str(infos["total_igtv_videos"]))
        print("Biography              : "+infos["biography"])
        if "public_email" in infos.keys():
            if infos["public_email"]!='':
                print("Public Email           : "+infos["public_email"])
            else:
                print("No public email found  : ")
        if "public_phone_number"in infos.keys():
            if str(infos["public_phone_number"])!='':
                print("Public Phone number    : +"+str(infos["public_phone_country_code"])+" "+str(infos["public_phone_number"]))

        other_infos=advanced_lookup(args.username)
        if other_infos["error"]=="rate limit":
            print("Rate limit please wait a few minutes before you try again")
        elif "message" in other_infos["user"].keys():
            if other_infos["user"]["message"]=="No users found":
                print("The lookup did not work on this account")
            else:
                print("Rate limit please wait a few minutes before you try again.")
        else:
            if "obfuscated_email" in other_infos["user"].keys():
                if other_infos["user"]["obfuscated_email"]!='':
                    print("Obfuscated email       : "+other_infos["user"]["obfuscated_email"])
                else:
                    print("No obfuscated email found")

            if "obfuscated_phone"in other_infos["user"].keys():
                if str(other_infos["user"]["obfuscated_phone"])!='':
                    print("Obfuscated phone       : "+str(other_infos["user"]["obfuscated_phone"]))
                else:
                    print("No obfuscated phone found")
        print("-"*24)
        print("Profile Picture        : "+infos["hd_profile_pic_url_info"]["url"])
