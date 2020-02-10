# Toutatis
### Educational purposes only
Toutatis est un outils qui permet d'extraire des informations de comptes instagrams mails, numéro de téléphone ect...

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## 💡 Prérequis
   [Python](https://www.python.org/downloads/release/python-370/)
## 🛠️ Installation
```bash
git clone https://github.com/megadose/toutatis.git
cd toutatis/
pip install -r requirements.txt
```
## Exemple
![](toutatis.gif)
## 📈 Usage
### arguments avec -i ou  --informations :
- mail pour extraires les mails
- phone pour extraires les numéros de telephones
- mp pour les 2
- all pour tous
```bash
python toutatis.py [-h] -u USERNAMES -s SESSIONID [-o OUTPUT]
python toutatis.py -u usernames.txt -s sessionsid
```
## 📚 Pour recuperer le sessionsID
![alt text](https://github.com/megadose/toutatis/blob/master/sessionsId.png?raw=true)

## 📝 License
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)
