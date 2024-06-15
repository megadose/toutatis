import argparse
import requests
from urllib.parse import quote_plus
from json import dumps, decoder

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)
import pycountry

def getUserId(username,sessionsId):
    headers = {"User-Agent": "iphone_ua", "x-ig-app-id": "936619743392459"}
    api = requests.get(
        f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}',
        headers=headers,
    )
    try:
        if api.status_code == 404:
            return {"id": None, "error": "User not found"}
        
        id = api.json()["data"]['user']['id']
        return {"id":id, "error": None}

    except decoder.JSONDecodeError:
        return {"id":None, "error":"Rate limit"}

def getInfo(username,sessionId):
    userId = getUserId(username, sessionId)
    if userId["error"]:
        return userId

    response = requests.get(
        f'https://i.instagram.com/api/v1/users/{userId["id"]}/info/',
        headers={'User-Agent': 'Instagram 64.0.0.14.96'},
        cookies={'sessionid': sessionId}
    ).json()["user"]
    
    infoUser = response
    infoUser["userID"] = userId["id"]
    
    return {"user":infoUser, "error":None}

def advanced_lookup(username):
    """
        Post to get obfuscated login infos
    """
    data = "signed_body=SIGNATURE."+quote_plus(dumps(
        {"q":username, "skip_recovery":"1"},
        separators=(",",":")
    ))
    api = requests.post(
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-App-ID": "124024574287414",
            "Accept-Encoding": "gzip, deflate",
            "Host": "i.instagram.com",
            #"X-FB-HTTP-Engine": "Liger",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )

    try:
        return({"user": api.json(),"error": None})
    except decoder.JSONDecodeError:
        return({"user": None, "error": "rate limit"})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sessionid',help="Instagram session ID",required=True)
    parser.add_argument('-u','--username',help="One username",required=True)
    args = parser.parse_args()

    sessionsId=args.sessionid

    infos = getInfo(args.username, sessionsId)
    if not infos["user"]:
        exit(infos["error"])

    infos=infos["user"]

    print("Informations about     : "+infos["username"])
    print("userID                 : "+infos["userID"])
    print("Full Name              : "+infos["full_name"])
    print("Verified               : "+str(infos['is_verified'])+" | Is buisness Account : "+str(infos["is_business"]))
    print("Is private Account     : "+str(infos["is_private"]))
    print("Follower               : "+str(infos["follower_count"]) + " | Following : "+str(infos["following_count"]))
    print("Number of posts        : "+str(infos["media_count"]))
    # print("Number of tag in posts : "+str(infos["following_tag_count"]))
    if infos["external_url"]:
        print("External url           : "+infos["external_url"])
    print("IGTV posts             : "+str(infos["total_igtv_videos"]))
    print("Biography              : "+(f"""\n{" "*25}""").join(infos["biography"].split("\n")))
    
    if "public_email" in infos.keys():
        if infos["public_email"]:
            print("Public Email           : "+infos["public_email"])

    if "public_phone_number" in infos.keys():
        if str(infos["public_phone_number"]):
            phonenr = "+"+str(infos["public_phone_country_code"])+" "+str(infos["public_phone_number"])
            try:
                pn = phonenumbers.parse(phonenr)
                countrycode = region_code_for_country_code(pn.country_code)
                country = pycountry.countries.get(alpha_2=countrycode)
                phonenr = phonenr + " ({}) ".format(country.name)
            except: # except what ??
                pass # pass what ??
            print("Public Phone number    : " + phonenr)

    other_infos=advanced_lookup(args.username)
    
    if other_infos["error"] == "rate limit":
        print("Rate limit please wait a few minutes before you try again")
    
    elif "message" in other_infos["user"].keys():
        if other_infos["user"]["message"] == "No users found":
            print("The lookup did not work on this account")
        else:
            print(other_infos["user"]["message"])
    
    else:
        if "obfuscated_email" in other_infos["user"].keys():
            if other_infos["user"]["obfuscated_email"]:
                print("Obfuscated email       : "+other_infos["user"]["obfuscated_email"])
            else:
                print("No obfuscated email found")

        if "obfuscated_phone"in other_infos["user"].keys():
            if str(other_infos["user"]["obfuscated_phone"]):
                print("Obfuscated phone       : "+str(other_infos["user"]["obfuscated_phone"]))
            else:
                print("No obfuscated phone found")
    print("-"*24)
    print("Profile Picture        : "+infos["hd_profile_pic_url_info"]["url"])
    
