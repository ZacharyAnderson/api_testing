import os, sys, urllib3
import requests, json, urllib3
import HPE3Par_Functions
import configparser
from pprint import pprint

ipaddr = '192.168.142.50'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://' + ipaddr +':8080/api/v1/'
config = configparser.ConfigParser()
config.read('config.ini')
HPE_PASSWORD = config['HPE_3PAR']['HPE_PASSWORD']
HPE_USERNAME = config['HPE_3PAR']['HPE_USERNAME']

r = requests.post(url = base_url + 'credentials', json = {'user':HPE_USERNAME,'password':HPE_PASSWORD},
headers={'Content-Type':'application/json'}, verify=False)
#Take the generated session key and set it up on the header dictionary
session_key = json.loads(r.text)
print ('You have now successfully logged into the 3PAR.\n')
headers = {'X-HP3PAR-WSAPI-SessionKey':session_key['key']}

#Get all information of Vluns to compare with sourcefile 
req = requests.get(url = base_url + 'vluns/', headers = headers, verify=False )
vlun_query = req.json()

with open("3ParWWNlist.txt", "r") as sourcefile:
    tempfile = [s.strip() for s in sourcefile.readlines()]
    for wwn_id in tempfile:
        for vlun_info in vlun_query['members']:
            if vlun_info.get('volumeWWN', "") == wwn_id.upper():
                if not HPE3Par_Functions.remove_vlun(base_url, headers, vlun_info.get('volumeName', ""), vlun_info.get('lun',""),vlun_info.get('hostname', "") ) == True:
                    print ("There was a problem removing vlun: " + vlun_info.get('volumeName', ""))
                if not HPE3Par_Functions.remove_vol_from_vvset(base_url, headers, vlun_info.get('volumeName', "")) == True:
                    print ("There was a problem removing" + vlun_info.get('volumeName', "") + "from the volume set.")
                if not HPE3Par_Functions.remove_storage_vol(base_url, headers, vlun_info.get('volumeName', "")) == True:
                    print ("There was a problem remove the storage volume: ", vlun_info.get('volumeName', ""))
                break
                
#Terminates the session
delete_session = requests.delete(url = base_url + 'credentials/'+session_key['key'], headers=headers, verify=False)
print (delete_session.ok)