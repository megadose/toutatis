from toutatis import *

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
