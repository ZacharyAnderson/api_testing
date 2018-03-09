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
    'VPX0032':'cluster-1'
}

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
    ## Implement better checking system to make sure Device is available on vplex
    req = requests.post(url = url, headers = headers, json=json_list, verify=False)
    if not req.ok:
        time.sleep(1)
        claim_storage(name, device_id, vplex_name)
    return (req.ok)

