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

if len(infos["biography"]) >1:
    infos["biography"]="Not found"

print("Biography : "+infos["biography"])

if len(infos["publicEmail"])==0:
    infos["publicEmail"]="Not found"

print("Public Email : "+infos["publicEmail"])

if infos["recoveryEmail"]=="NULL":
    infos["recoveryEmail"]=="Not found"

print("Recovery Email : "+infos["recoveryEmail"])

if len(infos["public_phone_number"])<1:
    infos["public_phone_number"]="Not found"

print("Public Phone number : "+infos["public_phone_number"])
print("Profile Picture : "+infos["ProfilePicture"])
