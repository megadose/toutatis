# Toutatis
![PyPI](https://img.shields.io/pypi/v/toutatis) ![PyPI - Week](https://img.shields.io/pypi/dw/toutatis) ![PyPI - Downloads](https://static.pepy.tech/badge/toutatis) ![PyPI - License](https://img.shields.io/pypi/l/toutatis)
#### For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ
## Educational purposes only
Toutatis is a tool that allows you to extract information from instagrams accounts such as e-mails, phone numbers and more

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## 💡 Prerequisite
 [Python](https://www.python.org/downloads/release/python-370/)

## 🛠️ Installation
### With PyPI
 ```pip3 install holehe
 ```
### With Github
```bash
git clone https://github.com/megadose/toutatis.git
cd toutatis/
python3 setup.py install
```
### ⚠️ Warning with the forgotten password function the user is warned.
## 📈 Usage
toutatis [-h] -u USERNAME -s SESSIONID
```
## 📚 To retrieve the sessionID
![alt text](https://github.com/megadose/toutatis/blob/master/sessionsId.png?raw=true)
## 📈 Usage with python
```python3
from toutatis import *
print(getUserId("username",sessionsId))#To get the UserID
print(getInfo("username",sessionId))#To get the informations not parsed
print(getFullName("username",sessionId))#To get the Full Name
print(getProfilePicture("username",sessionId))#To get the Profile Picture
print(getBiographie("username",sessionId))#To get the Biography
print(extractEmail("username",sessionId))#To get the public email
print(extractPhone("username",sessionId))#To get the public phone number
print(getAllInfos("username",sessionId))#To get parsed informations
```
## 📝 License
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)
