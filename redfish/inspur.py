import requests
import copy
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import time

requests.packages.urllib3.disable_warnings()
headers = {'Content-Type': 'application/json'}
device_ip = '149.1.22.12'
# url = 'https://{device_ip}/api/session'.format(device_ip=device_ip)
# data = {"username":"admin","password":"admin","encrypt_flag":0}
# headers = {"X-Requested-With":"XMLHttpRequest"}
# result = requests.post(url, data=data, headers=headers, verify=False)
# print(result.content,result.headers)
user = 'admin'
pasd = 'admin'
bios_version = None
bmc_version = None

url = 'https://{device_ip}/api/session'.format(device_ip=device_ip)
data = dict(username=user, password=pasd, log_type=0)
headers = {'X-Requested-With': "XMLHttpRequest"}
result = requests.post(url, data=data, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    headers['Cookie'] = result.headers.get('Set-Cookie')
    headers['X-CSRFTOKEN'] = result.json().get('CSRFToken')
    sessionId = headers['Cookie']
    print('-----------------111----------------------------\n')
    print(result.json())
    print('--------------------222-------------------------\n')
    print(headers)

else:
    print('11111')
    print(result.content)
print(headers)

MAINTENANCE_LIST = dict(
    id=1, sdr=1, fru=1,
    sel=1, ipmi=1, network=1,
    ntp=1, snmp=1, ssh=1,
    kvm=1, authentication=1, syslog=1,
    pef=1, sol=1, smtp=1,
    user=1, dcmi=1, hostname=1
)
url = 'https://{device_ip}/api/maintenance/preserve'.format(device_ip=device_ip)

result = requests.put(url=url, data=MAINTENANCE_LIST, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    pass
    # not value
else:
    print(result.content)

url = 'https://{device_ip}/api/maintenance/bios_flash'.format(device_ip=device_ip)
data = dict(force_update_bios='no', preserve_setup_options=1)
result = requests.put(url=url, headers=headers, data=data, verify=False)
if 200 <= result.status_code <= 299:
    pass  # no value
else:
    print(result.content)

url = 'https://{device_ip}/api/maintenance/firmware'.format(device_ip=device_ip)
headers = copy.deepcopy(headers)

# filepath = '/home/cmp/20191209104530353/NF5280M5_BIOS_4.1.11_Standard_20190904.bin'
# filename = 'NF5280M5_BIOS_4.1.11_Standard_20190904.bin'
filepath = '/home/cmp/20191126161544045/NF5180M4_BIOS_4.1.25_standard_20190606.bin'
filename = 'NF5180M4_BIOS_4.1.25_standard_20190606.bin'

multipart_encoder = MultipartEncoder(
    fields={
        'fwimage': (filename, open(filepath, 'rb'))
    },
)
headers['Content-Type'] = multipart_encoder.content_type
result = requests.post(url, data=multipart_encoder, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    print(result.json())
else:
    print(result.content)

url = 'https://{device_ip}/api/maintenance/firmware/bios_verification'.format(device_ip=device_ip)
result = requests.get(url=url, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    pass  # not value
else:
    print(result.json())

url = 'https://{device_ip}/api/maintenance/firmware/biosupgrade'.format(device_ip=device_ip)
data = dict(
    preserve_me=0,
    preserve_setup_options=1,
    preserve_phy_image=1,
    preserve_phy_mac=1,
)
result = requests.put(url=url, headers=headers, data=data, verify=False)
if 200 <= result.status_code <= 299:
    print(result.text)
else:
    print(result.content)

'''
{ "id": 1, "action": "Flashing...", "progress": "9% done         ", "state": 0 }
{
    "id": 1,
    "action": "Flashing...",
    "progress": "Complete...",
    "state": 2
}
'''
url = 'https://{device_ip}/api/maintenance/firmware/flash-progress'.format(device_ip=device_ip)
result = requests.get(url=url, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    print(result.text)
else:
    print(result.content)
