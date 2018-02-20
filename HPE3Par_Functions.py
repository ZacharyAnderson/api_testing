import requests, json

#This will create Virtual volume sets on the 3Par
def create_vvset(base_url, headers, name):
    req = requests.post(url = base_url + 'volumesets', headers = headers, json = {'name': name}, verify=False )
    return (req.ok)

def create_vv(base_url, headers, name, vol_type, vol_size, cpg):
    #vol_type will be broken out to fill the requirments
    #for Thin Provisioning and Dedup Enabled Devices
    if vol_type == '1':
        tpvv = True
        tdvv = True
    else:
        tpvv = True
        tdvv = False
    #Convert all our imported information to json format
    json_list = {'name':name, 'tpvv':bool(tpvv), 'tdvv':bool(tdvv), 'sizeMiB':int(vol_size), 'cpg':cpg, 'snapCPG':cpg}
    print (json.dumps(json_list))
    #This is the API call to create the Volume
    req = requests.post(url = base_url+'volumes', headers = headers, json = json_list, verify=False)
    print (req.text)
    return (req.ok)

def create_vlun(base_url, headers, name, hostname):
    json_list = {'volumeName':name, 'hostname':hostname, 'autoLun':bool(True), 'maxAutoLun':int(4000), 'lun':int(1)}
    req = requests.post(url = base_url + 'vluns', headers = headers, json = json_list, verify=False)
    print (req.headers)
    return (req.ok)

def add_vv2vvset(base_url, headers, vv_set, vv):
    vv_arr=[str(vv)]
    req = requests.put(url = base_url + 'volumesets/'+vv_set, headers = headers, json = {'action':int('1') ,'setmembers':vv_arr}, verify=False )
    print (req.text)
    return (req.ok)

def delete_session(base_url, headers, key):
    req = requests.delete(url = base_url + 'credentials/'+key, headers=headers, verify=False)
    return (req.ok)

def query_vv(base_url, headers, name):
    req = requests.get(url = base_url + 'volumes/', headers = headers, verify=False )
    return req.json()