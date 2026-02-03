import argparse
import random
import time
import uuid
import requests
from urllib.parse import quote_plus
from json import dumps, decoder

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)
import pycountry

USER_AGENT = "Instagram 317.0.0.34.109 Android (31/12; 420dpi; 1080x2276; samsung; SM-G991B; o1s; exynos2100)"
IG_APP_ID = "936619743392459"
COMMON_HEADERS = {
    "User-Agent": USER_AGENT,
    "X-IG-App-ID": IG_APP_ID,
    "X-IG-Connection-Type": "WiFi",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
}
MAX_RETRIES = 5
RETRY_BASE_DELAY = 2


def _create_session(sessionId):
    session = requests.Session()
    session.headers.update(COMMON_HEADERS)
    session.cookies.set("sessionid", sessionId, domain=".instagram.com")
    session.headers["X-IG-Device-ID"] = str(uuid.uuid5(uuid.NAMESPACE_URL, sessionId))
    return session


def _request_with_retry(method, url, **kwargs):
    for attempt in range(MAX_RETRIES):
        response = method(url, **kwargs)
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                delay = float(retry_after)
            else:
                delay = RETRY_BASE_DELAY * (2 ** attempt)
            delay = delay + random.uniform(0, delay * 0.25)
            print(f"Rate limited, retrying in {delay:.1f}s... (attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(delay)
            continue
        return response
    return response


def getUserId(username, session):
    response = _request_with_retry(
        session.get,
        f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}',
    )
    if response.status_code == 404:
        return {"id": None, "user": None, "error": "User not found"}
    if response.status_code == 401:
        return {"id": None, "user": None, "error": "Invalid or expired session ID"}
    if response.status_code == 429:
        return {"id": None, "user": None, "error": "Rate limit"}

    try:
        user_data = response.json()["data"]['user']
        user_id = user_data['id']
        return {"id": user_id, "user": user_data, "error": None}
    except decoder.JSONDecodeError:
        return {"id": None, "user": None, "error": f"Unexpected response (status {response.status_code})"}
    except (KeyError, TypeError):
        return {"id": None, "user": None, "error": f"Unexpected API response format (status {response.status_code})"}


def _validate_session(session):
    """Validate session with a lightweight request before making API calls."""
    try:
        response = session.get(
            'https://i.instagram.com/api/v1/accounts/current_user/?edit=true',
            timeout=10,
        )
        if response.status_code in (401, 403):
            return False
        return True
    except requests.exceptions.RequestException:
        return False


def getInfo(search, sessionId, searchType="username"):
    session = _create_session(sessionId)

    if not _validate_session(session):
        return {
            "user": None,
            "error": "Session appears blocked. Try generating the session ID from this machine or use a proxy.",
        }

    if searchType == "username":
        data = getUserId(search, session)
        if data["error"]:
            return data
        userId = data["id"]
        info_user = data["user"]
        info_user["userID"] = userId
        info_user["_session"] = session
        return {"user": info_user, "error": None}
    else:
        try:
            userId = str(int(search))
        except ValueError:
            return {"user": None, "error": "Invalid ID"}

        time.sleep(1.5)

        try:
            response = _request_with_retry(
                session.get,
                f'https://i.instagram.com/api/v1/users/{userId}/info/',
            )
            if response.status_code == 401:
                return {"user": None, "error": "Invalid or expired session ID"}
            if response.status_code == 429:
                return {"user": None, "error": "Rate limit"}

            response.raise_for_status()

            info_user = response.json().get("user")
            if not info_user:
                return {"user": None, "error": "Not found"}

            info_user["userID"] = userId
            info_user["_session"] = session
            return {"user": info_user, "error": None}

        except requests.exceptions.RequestException:
            return {"user": None, "error": "Not found"}


def advanced_lookup(username, session):
    """
        Post to get obfuscated login infos
    """
    data = "signed_body=SIGNATURE." + quote_plus(dumps(
        {"q": username, "skip_recovery": "1"},
        separators=(",", ":")
    ))

    time.sleep(3 + random.uniform(0, 2))

    response = _request_with_retry(
        session.post,
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "i.instagram.com",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )

    if response.status_code in (401, 403):
        return {"user": None, "error": "Invalid or expired session ID"}
    if response.status_code == 429:
        return {"user": None, "error": "rate limit"}

    try:
        return {"user": response.json(), "error": None}
    except decoder.JSONDecodeError:
        return {"user": None, "error": "Unexpected response"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sessionid', help="Instagram session ID", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--username', help="One username")
    group.add_argument('-i', '--id', help="User ID")
    args = parser.parse_args()

    sessionsId = args.sessionid
    search_type = "id" if args.id else "username"
    search = args.id or args.username
    infos = getInfo(search, sessionsId, searchType=search_type)
    if not infos.get("user"):
        exit(infos["error"])

    session = infos["user"].pop("_session", None)
    infos = infos["user"]

    print("Informations about     : " + infos.get("username", "N/A"))
    print("userID                 : " + infos.get("userID", "N/A"))
    print("Full Name              : " + infos.get("full_name", "N/A"))
    print("Verified               : " + str(infos.get('is_verified', 'N/A')) + " | Is buisness Account : " + str(
        infos.get("is_business", "N/A")))
    print("Is private Account     : " + str(infos.get("is_private", "N/A")))
    print(
        "Follower               : " + str(infos.get("follower_count", "N/A")) + " | Following : " + str(infos.get("following_count", "N/A")))
    print("Number of posts        : " + str(infos.get("media_count", "N/A")))
    if infos.get("external_url"):
        print("External url           : " + infos["external_url"])
    if "total_igtv_videos" in infos:
        print("IGTV posts             : " + str(infos["total_igtv_videos"]))
    print("Biography              : " + (f"""\n{" " * 25}""").join(infos.get("biography", "").split("\n")))
    print("Linked WhatsApp        : " + str(infos.get("is_whatsapp_linked", "N/A")))
    print("Memorial Account       : " + str(infos.get("is_memorialized", "N/A")))
    print("New Instagram user     : " + str(infos.get("is_new_to_instagram", "N/A")))

    if "public_email" in infos.keys():
        if infos["public_email"]:
            print("Public Email           : " + infos["public_email"])

    if "public_phone_number" in infos.keys():
        if infos["public_phone_number"]:
            phonenr = "+" + str(infos["public_phone_country_code"]) + " " + str(infos["public_phone_number"])
            try:
                pn = phonenumbers.parse(phonenr)
                countrycode = region_code_for_country_code(pn.country_code)
                country = pycountry.countries.get(alpha_2=countrycode)
                phonenr = phonenr + " ({}) ".format(country.name)
            except (phonenumbers.NumberParseException, AttributeError):
                pass
            print("Public Phone number    : " + phonenr)

    other_infos = advanced_lookup(infos["username"], session)

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
                print("Obfuscated email       : " + other_infos["user"]["obfuscated_email"])
            else:
                print("No obfuscated email found")

        if "obfuscated_phone" in other_infos["user"].keys():
            if other_infos["user"]["obfuscated_phone"]:
                print("Obfuscated phone       : " + str(other_infos["user"]["obfuscated_phone"]))
            else:
                print("No obfuscated phone found")
    print("-" * 24)
    pic_info = infos.get("hd_profile_pic_url_info")
    if pic_info and pic_info.get("url"):
        print("Profile Picture        : " + pic_info["url"])
