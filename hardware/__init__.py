"""
(python3_all) pengwow@DESKTOP-KEIOB4P:/mnt/d/workspace/OwnProject/examples-python$ pip install python-hwinfo
Collecting python-hwinfo
  Downloading https://files.pythonhosted.org/packages/8a/be/f391353de3993c6ebe94a4e265449b233f4430a470829443488b9431f797/python-hwinfo-0.1.6.tar.gz
Collecting paramiko (from python-hwinfo)
  Using cached https://files.pythonhosted.org/packages/4b/80/74dace9e48b0ef923633dfb5e48798f58a168e4734bca8ecfaf839ba051a/paramiko-2.6.0-py2.py3-none-any.whl
Collecting prettytable (from python-hwinfo)
  Downloading https://files.pythonhosted.org/packages/ef/30/4b0746848746ed5941f052479e7c23d2b56d174b82f4fd34a25e389831f5/prettytable-0.7.2.tar.bz2
Collecting argparse (from python-hwinfo)
  Downloading https://files.pythonhosted.org/packages/f2/94/3af39d34be01a24a6e65433d19e107099374224905f1e0cc6bbe1fd22a2f/argparse-1.4.0-py2.py3-none-any.whl
Collecting bcrypt>=3.1.3 (from paramiko->python-hwinfo)
  Using cached https://files.pythonhosted.org/packages/8b/1d/82826443777dd4a624e38a08957b975e75df859b381ae302cfd7a30783ed/bcrypt-3.1.7-cp34-abi3-manylinux1_x86_64.whl
Collecting pynacl>=1.0.1 (from paramiko->python-hwinfo)
  Using cached https://files.pythonhosted.org/packages/27/15/2cd0a203f318c2240b42cd9dd13c931ddd61067809fee3479f44f086103e/PyNaCl-1.3.0-cp34-abi3-manylinux1_x86_64.whl
Collecting cryptography>=2.5 (from paramiko->python-hwinfo)
  Using cached https://files.pythonhosted.org/packages/97/18/c6557f63a6abde34707196fb2cad1c6dc0dbff25a200d5044922496668a4/cryptography-2.7-cp34-abi3-manylinux1_x86_64.whl
Requirement already satisfied: six>=1.4.1 in /mnt/d/virtualenv/python3_all/lib/python3.6/site-packages (from bcrypt>=3.1.3->paramiko->python-hwinfo) (1.11.0)
Collecting cffi>=1.1 (from bcrypt>=3.1.3->paramiko->python-hwinfo)
  Using cached https://files.pythonhosted.org/packages/5f/bf/6aa1925384c23ffeb579e97a5569eb9abce41b6310b329352b8252cee1c3/cffi-1.12.3-cp36-cp36m-manylinux1_x86_64.whl
Collecting asn1crypto>=0.21.0 (from cryptography>=2.5->paramiko->python-hwinfo)
  Using cached https://files.pythonhosted.org/packages/ea/cd/35485615f45f30a510576f1a56d1e0a7ad7bd8ab5ed7cdc600ef7cd06222/asn1crypto-0.24.0-py2.py3-none-any.whl
Collecting pycparser (from cffi>=1.1->bcrypt>=3.1.3->paramiko->python-hwinfo)
Installing collected packages: pycparser, cffi, bcrypt, pynacl, asn1crypto, cryptography, paramiko, prettytable, argparse, python-hwinfo
  Running setup.py install for prettytable ... done
  Running setup.py install for python-hwinfo ... done
Successfully installed argparse-1.4.0 asn1crypto-0.24.0 bcrypt-3.1.7 cffi-1.12.3 cryptography-2.7 paramiko-2.6.0 prettytable-0.7.2 pycparser-2.19 pynacl-1.3.0 python-hwinfo-0.1.6
You are using pip version 10.0.1, however version 19.2.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
"""



"""

(python3_all) pengwow@DESKTOP-KEIOB4P:/mnt/d/workspace/OwnProject/examples-python$ pip install hardware
Collecting hardware
  Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x7fce81235a90>, 'Connection to files.pythonhosted.org timed out. (connect timeout=15)')': /packages/52/04/ec4206c998143fae58671e5883e26dad327c924afcc840ca52818c2478f8/hardware-0.21.1.tar.gz
  Downloading https://files.pythonhosted.org/packages/52/04/ec4206c998143fae58671e5883e26dad327c924afcc840ca52818c2478f8/hardware-0.21.1.tar.gz (3.1MB)
    100% |████████████████████████████████| 3.1MB 63kB/s 
Collecting pbr>=1.0 (from hardware)
  Downloading https://files.pythonhosted.org/packages/f9/d8/bd657bfa0e89eb71ad5e977ed99a9bb2b44e5db68d9190970637c26501bb/pbr-5.4.2-py2.py3-none-any.whl (110kB)
    100% |████████████████████████████████| 112kB 103kB/s 
Requirement already satisfied: six in /mnt/d/virtualenv/python3_all/lib/python3.6/site-packages (from hardware) (1.11.0)
Collecting Babel>=1.3 (from hardware)
  Downloading https://files.pythonhosted.org/packages/2c/60/f2af68eb046c5de5b1fe6dd4743bf42c074f7141fe7b2737d3061533b093/Babel-2.7.0-py2.py3-none-any.whl (8.4MB)
    100% |████████████████████████████████| 8.4MB 120kB/s 
Collecting ipaddress (from hardware)
  Using cached https://files.pythonhosted.org/packages/fc/d0/7fc3a811e011d4b388be48a0e381db8d990042df54aa4ef4599a31d39853/ipaddress-1.0.22-py2.py3-none-any.whl
Collecting netaddr (from hardware)
  Downloading https://files.pythonhosted.org/packages/ba/97/ce14451a9fd7bdb5a397abf99b24a1a6bb7a1a440b019bebd2e9a0dbec74/netaddr-0.7.19-py2.py3-none-any.whl (1.6MB)
    100% |████████████████████████████████| 1.6MB 130kB/s 
Collecting pexpect (from hardware)
  Downloading https://files.pythonhosted.org/packages/0e/3e/377007e3f36ec42f1b84ec322ee12141a9e10d808312e5738f52f80a232c/pexpect-4.7.0-py2.py3-none-any.whl (58kB)
    100% |████████████████████████████████| 61kB 116kB/s 
Collecting numpy (from hardware)
  Downloading https://files.pythonhosted.org/packages/19/b9/bda9781f0a74b90ebd2e046fde1196182900bd4a8e1ea503d3ffebc50e7c/numpy-1.17.0-cp36-cp36m-manylinux1_x86_64.whl (20.4MB)
    100% |████████████████████████████████| 20.4MB 222kB/s 
Collecting pandas (from hardware)
  Downloading https://files.pythonhosted.org/packages/1d/9a/7eb9952f4b4d73fbd75ad1d5d6112f407e695957444cb695cbb3cdab918a/pandas-0.25.0-cp36-cp36m-manylinux1_x86_64.whl (10.5MB)
    100% |████████████████████████████████| 10.5MB 3.3MB/s 
Requirement already satisfied: pytz>=2015.7 in /mnt/d/virtualenv/python3_all/lib/python3.6/site-packages (from Babel>=1.3->hardware) (2017.2)
Collecting ptyprocess>=0.5 (from pexpect->hardware)
  Downloading https://files.pythonhosted.org/packages/d1/29/605c2cc68a9992d18dada28206eeada56ea4bd07a239669da41674648b6f/ptyprocess-0.6.0-py2.py3-none-any.whl
Collecting python-dateutil>=2.6.1 (from pandas->hardware)
  Downloading https://files.pythonhosted.org/packages/41/17/c62faccbfbd163c7f57f3844689e3a78bae1f403648a6afb1d0866d87fbb/python_dateutil-2.8.0-py2.py3-none-any.whl (226kB)
    100% |████████████████████████████████| 235kB 323kB/s 
Installing collected packages: pbr, Babel, ipaddress, netaddr, ptyprocess, pexpect, numpy, python-dateutil, pandas, hardware
  Running setup.py install for hardware ... done
Successfully installed Babel-2.7.0 hardware-0.21.1 ipaddress-1.0.22 netaddr-0.7.19 numpy-1.17.0 pandas-0.25.0 pbr-5.4.2 pexpect-4.7.0 ptyprocess-0.6.0 python-dateutil-2.8.0
You are using pip version 10.0.1, however version 19.2.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

"""