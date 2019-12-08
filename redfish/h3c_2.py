import requests
import copy
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import time

requests.packages.urllib3.disable_warnings()
headers = {'Content-Type': 'application/json'}
device_ip = '149.1.22.17'
# url = 'https://{device_ip}/api/session'.format(device_ip=device_ip)
# data = {"username":"admin","password":"admin","encrypt_flag":0}
# headers = {"X-Requested-With":"XMLHttpRequest"}
# result = requests.post(url, data=data, headers=headers, verify=False)
# print(result.content,result.headers)
user = 'admin'
pasd = 'Password@_'
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
# url = 'https://{device_ip}/api/version_summary'.format(device_ip=device_ip)
# result = requests.get(url, headers=headers, verify=False)
# if 200 <= result.status_code <= 299:
#     print('----------------333-----------------------------\n')
#     for item in result.json():
#         if 'BMC' == item.get('dev_name'):
#             bmc_version = item.get('dev_version')
#         if 'BIOS' == item.get('dev_name'):
#             bios_version = item.get('dev_version')
# else:
#     print(result.content)
#     print('11111')
#
# print(bios_version, bmc_version)

# set type
url = 'https://{device_ip}/api/maintenance/firmware/type'.format(device_ip=device_ip)
# 更新后手动重置 reboot_type = 2
# 覆盖所有配置 : preserve_config = 0
data = {"preserve_config": 0, "fw_type_name": "BIOS", "reboot_type": 2, "reboot_time": 0}
result = requests.post(url, json=data, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    print(result.json())
else:
    print(result.content)

# in flash
url = 'https://{device_ip}/api/maintenance/flash'.format(device_ip=device_ip)
result = requests.put(url, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    print(result.text)
else:
    print(result.content)

# upload
url = 'https://{device_ip}/api/maintenance/firmware'.format(device_ip=device_ip)
headers = copy.deepcopy(headers)
filepath = '/home/cmp/20191126160546823/C35-BIOS-1.00.35_Signed.bin'
filename = 'C35-BIOS-1.00.35_Signed.bin'

# filepath = '/home/cmp/20191126160634042/C35-BIOS-2.00.32P05-signed.bin'
# filename = 'C35-BIOS-2.00.32P05-signed.bin'

multipart_encoder = MultipartEncoder(
    fields={
        'fwimage': (filename, open(filepath, 'rb'))
    },
)
content_type = multipart_encoder.content_type
print(content_type)
headers['Content-Type'] = content_type
result = requests.post(url, data=multipart_encoder, headers=headers, verify=False)
print(result.content)

url = 'https://{device_ip}/api/maintenance/firmware/verification'.format(device_ip=device_ip)
result = requests.get(url, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    print(result.json())
else:
    print(result.content)

url = 'https://{device_ip}/api/maintenance/firmware/upgrade'.format(device_ip=device_ip)
data = {"flash_status": 1}
headers['Content-Type'] = 'application/json'
result = requests.put(url, data=data, headers=headers, verify=False)
if 200 <= result.status_code <= 299:
    print(result.json())
else:
    print(result.content)

while True:
    url = 'https://{device_ip}/api/maintenance/firmware/flash_progress'.format(device_ip=device_ip)
    result = requests.get(url, headers=headers, verify=False)
    if 200 <= result.status_code <= 299:
        result = result.json()
        print(result)
        if 'Complete' in result.get('progress'):
            os.system('ipmitool -I lanplus -U admin -P Password@_ -H {device_ip} chassis power reset'.format(
                device_ip=device_ip))
            break
        else:
            print(result.get('progress'))
    else:
        print(result.content)
        break
    time.sleep(1)

'''
{'action': 'BIOS Writing...', 'progress': '2% done         ', 'cc': 0}

{
    "action": "Writing...",
    "progress": "Complete...",
    "cc": 255
}
'''
