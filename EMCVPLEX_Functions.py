import requests, json, configparser, time

#opens config document to load username and password of the VPLEX
config = configparser.ConfigParser()
config.read('config.ini')
VPLEX_USERNAME = config['EMC_VPLEX']['VPLEX_USERNAME']
VPLEX_PASSWORD = config['EMC_VPLEX']['VPLEX_PASSWORD']

#Dictionary for VPLEX Names to IP mappings
vplexip_map = {
    'VPX0222':'192.168.18.70',
    'VPX0112':'192.168.18.70',
    'VPX0184':'192.168.142.163',
    'VPX0248':'192.168.18.36',
    'VPX0032':'192.168.142.163'
}

vplexcluster_map = {
    'VPX0222':'cluster-1',
    'VPX0112':'cluster-2',
    'VPX0184':'cluster-1',
    'VPX0248':'cluster-1',
    'VPX0032':'cluster-2'
}

def is_device_ready(vplex_device_id, vplex_name, sleep_counter):
    '''
        is_device_ready checks if the newly exported volume from the array is ready
        to be claimed on the VPLEX end. We do this by trying to find the WWN of the device
        in the available storage-volumes.
    '''
    headers = {"Username": VPLEX_USERNAME, "Password": VPLEX_PASSWORD, "Content-Type": "application/json"}
    url = "https://"+vplexip_map[vplex_name]+":443/vplex/clusters/"+ vplexcluster_map[vplex_name]+"/storage-elements/storage-volumes/" + vplex_device_id
    query_device = requests.get(url = url, headers=headers, verify=False)
    if query_device.status_code != 200:
        time.sleep(sleep_counter)
        sleep_counter = sleep_counter * sleep_counter
        is_device_ready(vplex_device_id, vplex_name, sleep_counter)
    return       
    

def claim_storage(name, device_id, vplex_name):
    '''
        In claim_storage we will take the name of the device and device_id
        given by the volume create function of the chosen array and 
        claim the storage on the chose VPLEX array.
    '''
    url = "https://"+vplexip_map[vplex_name]+":443/vplex/storage-volume+claim"
    vplex_device_id = "VPD83T3:"+ device_id.lower()
    json_list = {"args":"--thin-rebuild -n "+ name + " -d " + vplex_device_id + " -f"} 
    headers = {"Username": VPLEX_USERNAME, "Password": VPLEX_PASSWORD, "Content-Type": "application/json"}
    is_device_ready(vplex_device_id, vplex_name, 2)
    req = requests.post(url = url, headers = headers, json=json_list, verify=False)
    return (req.ok)

def create_extent(name, vplex_name):
    '''
        In create_extent we will take a newly claimed storage volume
        and create an extent on top of it. All that is needed is the
        name of the storage volume and the Vplex Name.
    '''
    url = "https://"+vplexip_map[vplex_name]+":443/vplex/extent+create"
    json_list = {"args": "-d " + name}
    headers = {"Username": VPLEX_USERNAME, "Password": VPLEX_PASSWORD, "Content-Type": "application/json"}
    req = requests.post(url = url, headers = headers, json = json_list, verify=False)
    return req.ok

def create_device(name, vplex_name):
    '''
        In create_device we will take a newly created extent
        and create a device on top of it. All that we need for this
        is the name of the storage volume an the Vplex Name.
    '''
    url = "https://"+vplexip_map[vplex_name]+":443/vplex/local-device+create"
    device_name = "device_" + name + "_1"
    extent_name = "extent_" + name + "_1"
    json_list = {"args": "--geometry raid-0 -n " + device_name + " -e " + extent_name + " -f"}
    headers = {"Username": VPLEX_USERNAME, "Password": VPLEX_PASSWORD, "Content-Type": "application/json"}
    req = requests.post(url = url, headers = headers, json = json_list, verify = False)
    return req.ok

def create_virtualvolume(name, vplex_name):
    '''
        In create_virtualvolume we will finish the last task of building
        a complete volume on the VPLEX. We will take the newly created
        device and build a Virtual Volume on top of that.
    '''
    url = "https://"+vplexip_map[vplex_name]+":443/vplex/virtual-volume+create"
    device_name = "device_" + name + "_1"
    json_list = {"args": "-r " + device_name}
    headers = {"Username": VPLEX_USERNAME, "Password": VPLEX_PASSWORD, "Content-Type": "application/json"}
    req = requests.post(url = url, headers = headers, json = json_list, verify = False)
    return req.ok

def export_virtualvolume(name, vplex_name, storageview_name):
    '''
        In export_virtualvolume we will take the created virtual volume
        and export it to the storage view specified in the cal.
    '''
    url = "https://"+vplexip_map[vplex_name]+":443/vplex/export+storage-view+addvirtualvolume"
    device_name = "device_" + name + "_1_vol"
    json_list = {"args": "--view " + storageview_name + " --virtual-volumes " + device_name + " -f"}
    headers = {"Username": VPLEX_USERNAME, "Password": VPLEX_PASSWORD, "Content-Type": "application/json"}
    req = requests.post(url = url, headers = headers, json = json_list, verify = False)
    return req.ok