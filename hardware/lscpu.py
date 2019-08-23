import subprocess
import json
import os
import time


def get_lscpu():
    cmd = "sshpass -p password ssh {user}@{ip} lscpu ".format(user='root', ip='172.16.1.102')
    result = dict()
    try:
        completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed_process.returncode == 0:
            data = completed_process.stdout
            filename = './test-{time}.json'.format(time=time.time())
            print(data)
            with open(filename, 'wb') as _file:
                _file.write(data)
            with open(filename, 'r') as _file:
                new_data = _file.readlines()
            for item in new_data:
                cpu_line = item.split(':')
                if len(cpu_line) >= 2:
                    result[cpu_line[0].strip()] = cpu_line[1].strip()
            if os.path.exists(filename):
                os.remove(filename)
            return result
        else:
            print("Returncode is not 0")
    except Exception as err:
        print(err)


result = get_lscpu()
print(result)
