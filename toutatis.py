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
    try:
        r = get('https://www.instagram.com/{}/?__a=1'.format(username))
        info = json.loads(r.text)
        id = info["logging_page_id"].strip("profilePage_")
        return(id)
    except ValueError:
        print(ValueError)
        exit()

def getInfo(userId,sessionId):
    cookies = {'sessionid': sessionId}
    headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
    response = get('https://i.instagram.com/api/v1/users/'+userId+'/info/', headers=headers, cookies=cookies)
    info = json.loads(response.text)
    infoUser = info["user"]
    return(infoUser)

with open(args.usernames) as file:
    usernames = [l.strip() for l in file]
print(str(len(usernames))+" users")
print("Export filename : "+args.output)
for username in tqdm(usernames):
    userid = getUserId(username)
    ListOfInfo.append(getInfo(userid,sessionsId))


keys = ListOfInfo[0].keys()
with open(args.output, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(ListOfInfo)
