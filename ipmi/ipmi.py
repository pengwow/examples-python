# coding=utf-8


ddd = {'netfn': 7, 'command': 1, 'code': 0, 'data': bytearray(b'\x01\x81\x03X\x02\xad\xdb\x07\x00\x01\x00\x18\x00\x10\x00')}

print(ddd['data'])
print(len(ddd['data']))
# for item in ddd['data']:
#     print(item)
class Health:
    Ok = 0
    Warning, Critical, Failed = [2**x for x in range(0, 3)]
for x in range(0, 3):
    print(x)