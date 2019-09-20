import json

test_str = {
    'serial_number': '817204284',
    'cpu_model_name': 'Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz',
    'mfg': 'Inspur',
    'product': 'NF5180M4 (Default string)',
    'cpu_s': '40',
    'memory': '16384 MB * 12',
    'network_card': 'I350 Gigabit Network Connection * 2,Ethernet Controller 10-Gigabit X540-AT2 * 4',
    'total_disk': 'SCSI Disk/837GiB (899GB) * 1'
  }

ddd = json.dumps(test_str)
print(ddd)

