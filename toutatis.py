import argparse,json
from tabulate import tabulate
from requests import get
import unicodecsv as csv
from tqdm import tqdm

parser = argparse.ArgumentParser()
required = parser.add_argument_group('required arguments')
parser.add_argument('-s', '--sessionid',help="Instagram session ID",required=True)
parser.add_argument('-i','--informations',help="The informations you want. mail : just extract the mail, phone : just extract the phone number ,ep extract email and phone , all : extract all informations")
parser.add_argument('-f', '--file',help="List of usernames (filename)")
parser.add_argument('-u','--username',help="One username")
parser.add_argument('-o', '--output',help="Name of output csv file")
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

def exportDictUnicode(dictToExport,exportFilename):
    keys = []
    for listinfo in dictToExport:
    	for i in listinfo.keys():
    		keys.append(i) if i not in keys else keys

    with open(exportFilename, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dictToExport)

def extractEmail(dict):
    try:
        return(dict["public_email"])
    except:
        return("NULL")
def extractPhone(dict):
    try:
        return(dict["public_phone_country_code"]+dict["public_phone_number"])
    except:
        return("NULL")

if(args.username !=  None):
    print("The informations about : "+args.username)
    userid = getUserId(str(args.username))
    print("User id : "+userid)
    info = getInfo(userid,sessionsId)
    if(args.informations == "mail"):
        email = extractEmail(info)
        print("Mail of {} : {}".format(args.username,email))
        dict = {'username':username,'mail':email}
        ListOfInfo.append(dict)
    elif(args.informations == "phone"):
        phone = extractPhone(info)
        print("Phone of {} : {}".format(args.username))
        dict = {'username':username,'phone':phone}
        ListOfInfo.append(dict)

    elif(args.informations == "all"):
        ListOfInfo.append(info)
    else:
        print("check --help")
        exit()
    if (args.output != None):
        print(ListOfInfo)
        exportDictUnicode(ListOfInfo,args.output)
        print("Export in "+args.output)
elif(args.file != None):
    if (args.output != None):
        try:
            with open(args.file) as f:
                usernames = [l.strip() for l in f]
                # Do something with the file
        except IOError:
            print("File not accessible")
        print(str(len(usernames))+" users")

        if(args.informations == "mail"):
            for username in tqdm(usernames):
                userid = getUserId(str(username))
                info = getInfo(userid,sessionsId)
                email = extractEmail(info)
                dict = {'username':username,'mail':email}
                ListOfInfo.append(dict)

        elif(args.informations == "phone"):
            for username in tqdm(usernames):
                userid = getUserId(str(username))
                info = getInfo(userid,sessionsId)
                phone = extractPhone(info)
                dict = {'username':username,'phone':phone}
                ListOfInfo.append(dict)
        elif(args.informations == "all"):
            for username in tqdm(usernames):
                userid = getUserId(str(username))
                info = getInfo(userid,sessionsId)
                ListOfInfo.append(info)
        else:
            print("check --help")
            exit()

        #print(ListOfInfo)
        exportDictUnicode(ListOfInfo,args.output)
        print("Export in "+args.output)

    else:
        print("Export a required if you want get informations of multiple usernames")

else:
    print("check --help")
    exit()
