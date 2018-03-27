import os, sys, urllib3
import requests, json, urllib3
import HPE3Par_Functions
import pprint, configparser
import EMCVPLEX_Functions

hpe3parwwn_map = {
    '192.168.142.50':'246B',
    '192.168.18.40':'246C',
    '192.168.18.26':'9525',
    '140.163.142.66':'9106',
    '140.163.146.193':'27B4',
    '192.168.18.23':'9287',
    '10.254.200.29':'AF8A'
}

# This Function will be used to authenticate into the ESGMID3PAR7400C1 API
# and be interactive for specific types of programming tasks
def HPE3Par(ipaddr,arrayname):
    os.system('clear')
    print ('You made it into: ' + arrayname +'!\n')
    print ('We have the ability to complete basic storage administration tasks through the HPE 3PAR WSAPI.\n')
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    base_url = 'https://' + ipaddr +':8080/api/v1/'
    config = configparser.ConfigParser()
    config.read('config.ini')
    HPE_PASSWORD = config['HPE_3PAR']['HPE_PASSWORD']
    HPE_USERNAME = config['HPE_3PAR']['HPE_USERNAME']

    r = requests.post(url = base_url + 'credentials', json = {'user':HPE_USERNAME,'password':HPE_PASSWORD},
    headers={'Content-Type':'application/json'}, verify=False)
    # Take the generated session key and set it up on the header dictionary
    session_key = json.loads(r.text)
    print ('You have now successfully logged into the 3PAR.\n')
    exec_menu(base_url, session_key, ipaddr)

def exec_menu(base_url,session_key, ipaddr):
    headers = {'X-HP3PAR-WSAPI-SessionKey':session_key['key']}
    print ('Select the task you would like to complete:\n')
    print ('1. Create Virtual Volume Set\n')
    print ('2. Create Virtual Volumes\n')
    print ('3. Query VV/Vlun information\n')
    print ('4. Query VVset names\n')
    print ('5. Query CPG names\n')
    print ('9. Exit\n')
    choice = input(' >> ')
    ch = choice.lower()
    
    #This will start the menus process
    #'1' being to create a new volume set
    if ch == '1':
        print ('Please Enter the name of the new Volume Set to be created:\n')
        vv_set_name = input(' >> ')
        print (HPE3Par_Functions.create_vvset(base_url,headers,vv_set_name))
        exec_menu(base_url, session_key, ipaddr)
    #'2' Will create 1 or more volumes of the same size
    elif ch == '2':
        print ('Please enter the name of the Base Volume to be created:\n')
        name = input(' >> ')
        print("Please enter the amount of volumes of the same size you would like to create\n")
        vol_amount = int(input(' >> '))
        print ("Please enter the volume number you would like to start at:\n")
        print ("If a new Host, put 1 as this is default\n")
        count = int(input(' >> '))
        print ('\nPlease enter the size of the volume in GBs\n')
        vol_size = input(' >> ')
        print ('\nPlease enter a 0 for tpvv, or a 1 tdvv \n')
        vol_type = input (' >> ')
        print ('\nEnter the VV set')
        vv_set_name = input(' >> ')
        print ('\nEnter the CPG')
        cpg = input(' >> ')
       
        print ('\nEnter # of the Host to export to')
        print ('\n1 - VPX0222 - Metro 2 LDC')
        print('\n2 - VPX0122 - Metro 2 MDC')
        print('\n3 - VPX0184 - Metro 1 LDC')
        print('\n4 - VPX0248 - Local LDC')
        print('\n5 - VPX0032 - Metro 1 MDC')
        export2 = input(' >> ')
        
        if export2 == '1':
            export2 = 'VPX0222'
        elif export2 == '2':
            export2 = 'VPX0112'
        elif export2 == '3':
            export2 = 'VPX0184'
        elif export2 == '4':
            export2 = 'VPX0248'
        elif export2 == '5':
            export2 = 'VPX0032'
        else:
            print ("\nNot a valid response.")
            exec_menu(base_url, session_key, ipaddr)

        print ('\nEnter the Storage View you would like to export to on the vplex')
        storageview_name = input(' >> ')

        while vol_amount > 0:
            if not (HPE3Par_Functions.create_vv(base_url, headers, name + "_" + str(count), vol_type,(int(vol_size) * 1024), cpg)):
                print ("There was an error creating the Virtual Volume\n")
                exec_menu(base_url, session_key, ipaddr)
            if not (HPE3Par_Functions.add_vv2vvset(base_url,headers, vv_set_name, name + "_" + str(count))):
                print ("There was a problem adding the virtual volume to the VVset\n")
                print ("The VVset may not exist\n")
                exec_menu(base_url, session_key, ipaddr)
            if not (HPE3Par_Functions.create_vlun(base_url, headers, name + "_" + str(count), export2)):
                print ("There was a problem exporting the VV -> Vlun.\n")
                exec_menu(base_url, session_key, ipaddr)
            #Get specific WWN of the new volume so you can build the device on the VPLEX
            req = requests.get(url = base_url + 'volumes/'+ name + "_" + str(count), headers = headers, verify=False )
            vv_info = (req.json())
            if not (EMCVPLEX_Functions.claim_storage(name + "_" + str(count) + "_" + hpe3parwwn_map[ipaddr],vv_info['wwn'], export2)):
                print ("There was a problem claiming device: " + name + "_" + str(count) + " on "+ export2 +"\n")
            if not (EMCVPLEX_Functions.create_extent(name + "_" + str(count) + "_" + hpe3parwwn_map[ipaddr],export2)):
                print ("There was a problem creating the extent for: " + name + "_" + str(count))
            if not (EMCVPLEX_Functions.create_device(name + "_" + str(count) + "_" + hpe3parwwn_map[ipaddr],export2)):
                print ("There was a problem creating the device for: " + name + "_" + str(count))
            if not (EMCVPLEX_Functions.create_virtualvolume(name + "_" + str(count) + "_" + hpe3parwwn_map[ipaddr],export2)):
                print ("There was a problem creating the virtual volume for: " + name + "_" + str(count))
            if not storageview_name == '':
                if not (EMCVPLEX_Functions.export_virtualvolume(name + "_" + str(count) + "_" + hpe3parwwn_map[ipaddr],export2, storageview_name)):
                    print ("There was a problem exporting the virtual volume: " + (name + "_" + str(count)) + " to the view: " + storageview_name)   
            count += 1
            vol_amount -= 1
        exec_menu(base_url, session_key, ipaddr)
    #'3' Will query the base volume name for all volumes listed
    elif ch == '3':
        print ('\nPlease enter the base volume you want to query:')
        base_vol = input(' >> ')
        HPE3Par_Functions.query_vv(base_url, headers, base_vol)
        exec_menu(base_url, session_key, ipaddr)

    elif ch == '4':
        print ('Please enter the VVset you would like to query.\n')
        vvset = input(' >> ')
        HPE3Par_Functions.query_vvset(base_url, headers, vvset)
        exec_menu(base_url, session_key, ipaddr)

    elif ch == '5':
        HPE3Par_Functions.query_cpgs(base_url, headers)
        exec_menu(base_url, session_key, ipaddr)
        
    # will exit the Array menu you are in
    elif ch == '9':
        HPE3Par_Functions.delete_session(base_url,headers, session_key['key'])
        return
    #Any choice not written will bring you back to the top of the menu
    else:
        print ('invalid input')
        exec_menu(base_url, session_key, ipaddr)

            
    return

