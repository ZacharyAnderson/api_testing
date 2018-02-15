import os, sys
import requests, json
import HPE3Par_Functions

# This Function will be used to authenticate into the ESGMID3PAR7400C1 API
# and be interactive for specific types of programming tasks
def ESGMID3PAR7400C1():
    print ('You made it into ESGMID3PAR7400C1\n')
    print ('Here we have the ability to complete basic storage administration tasks through the HPE 3PAR WSAPI.\n')
    base_url = 'https://192.168.142.50:8080/api/v1/'

    r = requests.post(url = base_url + 'credentials', json = {'user':'3paradm','password':'bare4115.'},
    headers={'Content-Type':'application/json'}, verify=False)
    os.system('clear')
    # Take the generated session key and set it up on the header dictionary
    session_key = json.loads(r.text)
    '''headers = {'X-HP3PAR-WSAPI-SessionKey':session_key['key']}
    print ('You have now successfully logged into the 3PAR.\n')
    print ('Select the task you would like to complete:\n')
    print ('1. Create Virtual Volume Set\n')
    print ('2. Create Virtual Volumes\n')
    choice = input(' >> ')'''
    exec_menu(base_url, session_key)

def exec_menu(base_url,session_key):
    headers = {'X-HP3PAR-WSAPI-SessionKey':session_key['key']}
    print ('You have now successfully logged into the 3PAR.\n')
    print ('Select the task you would like to complete:\n')
    print ('1. Create Virtual Volume Set\n')
    print ('2. Create Virtual Volumes\n')
    print ('9. Exit\n')
    choice = input(' >> ')
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        print ('Invalid Choice')
        exec_menu(base_url, session_key)
    elif ch == '1':
        print ('Please Enter the name of the new Volume Set to be created:\n')
        vv_set_name = input(' >> ')
        print (HPE3Par_Functions.create_vvset(base_url,headers,vv_set_name))
        exec_menu(base_url, session_key)
            
    elif ch == '2':
        print ('Please enter the name of the Volume to be created:\n')
        name = input(' >> ')
        print ('\nPlease enter the size of the volume in GBs\n')
        vol_size = input(' >> ')
        print ('\nPlease enter a 0 for tpvv, or a 1 tdvv \n')
        vol_type = input (' >> ')
        print ('\nEnter the VV set')
        vv_set_name = input(' >> ')
        print ('\nEnter the CPG')
        cpg = input(' >> ')
        #print ('\nEnter the Host to export to')
        #export2 = input(' >> ')
        print (HPE3Par_Functions.create_vv(base_url, headers, name, vol_type, vol_size, cpg, vv_set_name))
        print (HPE3Par_Functions.add_vv2vvset(base_url,headers, name, 'VPX0032'))
        exec_menu(base_url, session_key)

    elif ch == '9':
        HPE3Par_Functions.delete_session(base_url,headers, session_key['key'])
        return

    else:
        print ('invalid input')
        exec_menu(base_url, session_key)

            


    #print (HPE3Par_Functions.create_vvset(base_url, headers, 'Api_test'))
    #d = requests.delete(url = base_url+'credentials/'+session_key['key'], headers = headers,verify=False)
    return

