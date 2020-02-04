import argparse,json
from tabulate import tabulate
from requests import get
import unicodecsv as csv
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
parser.add_argument('-s', '--sessionid',help="Instagram session ID",required=True)
parser.add_argument('-u', '--usernames',help="List of usernames (filename)",required=True)
parser.add_argument('-o', '--output',help="Name of output csv file",default="output_toutatis.csv")
args = parser.parse_args()
sessionsId=args.sessionid
ListOfInfo = []

def getUserId(username):
    r = get('https://www.instagram.com/{}/?__a=1'.format(username))
    info = json.loads(r.text)
    id = info["logging_page_id"].strip("profilePage_")
    return(id)

def getInfo(userId,sessionId):
    cookies = {'sessionid': sessionId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
    response = get('https://i.instagram.com/api/v1/users/'+userId+'/info/', headers=headers, cookies=cookies)
    info = json.loads(response.text)
    infoUser = info["user"]
    return(infoUser)

def repToDict(info):
    dictInfo=dict(public_phone_country_code=info["public_phone_country_code"],usertags_count=info["usertags_count"],has_anonymous_profile_picture=info["has_anonymous_profile_picture"],full_name=info["full_name"],following_count=info["following_count"],total_ar_effects=info["total_ar_effects"],city_id=info["city_id"],public_phone_number=info["public_phone_number"],auto_expand_chaining=info["auto_expand_chaining"],external_lynx_url=info["external_lynx_url"],can_hide_public_contacts=info["can_hide_public_contacts"],about_your_account_bloks_entrypoint_enabled=info["about_your_account_bloks_entrypoint_enabled"],is_favorite=info["is_favorite"],highlight_reshare_disabled=info["highlight_reshare_disabled"],is_favorite_for_stories=info["is_favorite_for_stories"],address_street=info["address_street"],biography=info["biography"],is_business=info["is_business"],category=info["category"],media_count=info["media_count"],should_show_category=info["should_show_category"],zip=info["zip"],is_potential_business=info["is_potential_business"],account_type=info["account_type"],show_account_transparency_details=info["show_account_transparency_details"],is_bestie=info["is_bestie"],is_favorite_for_highlights=info["is_favorite_for_highlights"],following_tag_count=info["following_tag_count"],follower_count=info["follower_count"],pk=info["pk"],is_verified=info["is_verified"],is_call_to_action_enabled=info["is_call_to_action_enabled"],show_post_insights_entry_point=info["show_post_insights_entry_point"],username=info["username"],show_leave_feedback=info["show_leave_feedback"],public_email=info["public_email"],has_unseen_besties_media=info["has_unseen_besties_media"],contact_phone_number=info["contact_phone_number"],latitude=info["latitude"],include_direct_blacklist_status=info["include_direct_blacklist_status"],profile_pic_id=info["profile_pic_id"],city_name=info["city_name"],should_show_public_contacts=info["should_show_public_contacts"],fb_page_call_to_action_id=info["fb_page_call_to_action_id"],is_private=info["is_private"],can_be_reported_as_fraud=info["can_be_reported_as_fraud"],business_contact_method=info["business_contact_method"],instagram_location_id=info["instagram_location_id"],direct_messaging=info["direct_messaging"],can_hide_category=info["can_hide_category"],longitude=info["longitude"],has_highlight_reels=info["has_highlight_reels"],professional_conversion_suggested_account_type=info["professional_conversion_suggested_account_type"],external_url=info["external_url"],total_igtv_videos=info["total_igtv_videos"])
    return(dictInfo)

with open(args.usernames) as file:
    usernames = [l.strip() for l in file]
print(str(len(usernames))+" users")
print("Export filename : "+args.output)
for username in tqdm(usernames):
    userid = getUserId(username)
    ListOfInfo.append(repToDict(getInfo(userid,sessionsId)))


keys = ListOfInfo[0].keys()
with open(args.output, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(ListOfInfo)
