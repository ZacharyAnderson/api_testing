import requests, json, pprint

#This will create Virtual volume sets on the 3Par
def create_vvset(base_url, headers, name):
    req = requests.post(url = base_url + 'volumesets', headers = headers, json = {'name': name}, verify=False )
    return (req.ok)

def create_vv(base_url, headers, name, vol_type, vol_size, cpg):
    #vol_type will be broken out to fill the requirments
    #for Thin Provisioning and Dedup Enabled Devices
    if vol_type == '1':
        tpvv = False
        tdvv = True
    else:
        tpvv = True
        tdvv = False
    #Convert all our imported information to json format
    json_list = {'name':name, 'tpvv':bool(tpvv), 'tdvv':bool(tdvv), 'sizeMiB':int(vol_size), 'cpg':cpg, 'snapCPG':cpg}
    #This is the API call to create the Volume
    req = requests.post(url = base_url+'volumes', headers = headers, json = json_list, verify=False)
    query_vv(base_url, headers, name)
    return (req.ok)

def create_vlun(base_url, headers, name, hostname):
    json_list = {'volumeName':name, 'hostname':hostname, 'autoLun':bool(True), 'maxAutoLun':int(4000), 'lun':int(1)}
    req = requests.post(url = base_url + 'vluns', headers = headers, json = json_list, verify=False)
    return (req.ok)

def add_vv2vvset(base_url, headers, vv_set, vv):
    vv_arr=[str(vv)]
    req = requests.put(url = base_url + 'volumesets/'+vv_set, headers = headers, json = {'action':int('1') ,'setmembers':vv_arr}, verify=False )
    return (req.ok)

def delete_session(base_url, headers, key):
    req = requests.delete(url = base_url + 'credentials/'+key, headers=headers, verify=False)
    return (req.ok)

#query_vv will query the name you give and output all volumes that the name is a sub-string of
def query_vv(base_url, headers, name):
    req = requests.get(url = base_url + 'volumes/', headers = headers, verify=False )
    vv_info = (req.json())
    is_basevol = False
    for volume_info in vv_info['members']:
        if volume_info['name'].find(name) != -1:
            is_basevol = True
            print ("{0:32} {1:32}".format(volume_info['name'], volume_info['wwn']))
    if is_basevol == False:
        print ("The base volume does not exist.\n")
    return 

#query_vvset will show you all vvsets with the substring inputted
def query_vvset(base_url, headers, name):
    req = requests.get(url = base_url + 'volumesets', headers=headers, verify=False)
    vvset_info = req.json()
    is_vvset = False
    for set_info in vvset_info['members']:
        if set_info['name'].find(name) != -1:
            is_vvset = True
            print ("{0:32}".format(set_info['name']))
    if is_vvset == False:
        print ("The VVset does not exist.\n")
    return

def query_cpgs(base_url, headers):
    req = requests.get(url = base_url + 'cpgs', headers=headers, verify=False)
    cpg_info = req.json()
    for cpgs in cpg_info['members']:
        print ("{0:32}\n".format(cpgs['name']))
    return