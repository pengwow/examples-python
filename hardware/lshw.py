import subprocess
import json
import os
import time


def get_lshw():
    cmd = "sshpass -p password ssh {user}@{ip} lshw -json".format(user='root', ip='172.16.1.102')
    try:
        completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed_process.returncode == 0:
            data = completed_process.stdout
            filename = './test-{time}.json'.format(time=time.time())
            print(data)
            with open(filename, 'wb') as json_file:
                json_file.write(data)
            with open(filename, 'r') as _file:
                new_data = json.load(_file)
                print(new_data)
            # if os.path.exists(filename):
            #     os.remove(filename)
            return new_data
        else:
            print("Returncode is not 0")
    except Exception as err:
        print(err)


# data = get_lshw()
# print(hash(json.dumps(data)))

with open('test1.json', 'r') as A:
    AA = json.load(A)
with open('test2.json', 'r') as B:
    BB = json.load(B)
import hashlib


# 3373611294997101355
def get_token(md5str):
    # 生成一个md5对象
    m1 = hashlib.md5()
    # 使用md5对象里的update方法md5转换
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token


import operator

ddd = operator.eq(AA, BB)
print(ddd)
print(get_token(str(AA)))
print(get_token(str(BB)))


class DiffDict(object):
    """获取两个dict的差异"""

    def __init__(self, current, last):
        self.current = current
        self.last = last
        self.set_current = set(current)
        self.set_last = set(last)
        self.intersect_keys = self.set_current & self.set_last

    def get_added(self):
        """current - 交集 = 新增的key"""
        added_keys = self.set_current - self.intersect_keys
        return [{'key': key, 'value': self.current.get(key)} for key in added_keys]

    def get_removed(self):
        """last - 交集 = 减去的key"""
        removed_keys = self.set_last - self.intersect_keys
        return [{'key': key, 'value': self.current.get(key)} for key in removed_keys]

    def get_changed(self):
        """用交集中的key去两个dict中找出值不相等的"""
        changed_keys = set(o for o in self.intersect_keys if self.current.get(o) != self.last.get(o))
        return [{
            'key': key,
            'value': '%s -> %s' % (self.last.get(key), self.current.get(key))
        } for key in changed_keys]


from deepdiff import DeepDiff
from pprint import pprint

diff_dict = DeepDiff(AA, BB)
print(diff_dict)
if diff_dict:
    for item in diff_dict.get('values_changed').keys():
        if 'size' in item[-8:]:
            continue
        else:
            print('OK')
