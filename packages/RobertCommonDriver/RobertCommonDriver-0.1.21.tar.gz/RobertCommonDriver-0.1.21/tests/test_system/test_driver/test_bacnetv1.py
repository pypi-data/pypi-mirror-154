import random
import time
from robertcommondriver.system.driver.bacnet_v1 import BacnetClient, SimulateObject


def test_read():
    dict_config = {
        'address': '192.168.1.36/24:47808',  # bacnet server ip(绑定网卡)
        'identifier': 555,  # bacnet server identifier
        'name': 'BacnetDriver',  # bacnet server name
        'max_apdu': 1024,  # bacnet server max apdu
        'segmentation': 'segmentedBoth',  # bacnet server segmentation
        'vendor_identifier': 15,  # bacnet server vendor
        'multi_read': 20,  # bacnet 批量读取个数
        'cmd_interval': 0.3,  # bacnet命令间隔
        'time_out': 3000  # 超时时间
    }

    client = BacnetClient(**dict_config)
    result = client.read_property('6:2', 'analogValue', 1, 'presentValue')
    print(result)

def test_cov():

    dict_config = {
        'address': '192.168.1.36/24:47808',  # bacnet server ip(绑定网卡)
        'identifier': 555,  # bacnet server identifier
        'name': 'BacnetDriver',  # bacnet server name
        'max_apdu': 1024,  # bacnet server max apdu
        'segmentation': 'segmentedBoth',  # bacnet server segmentation
        'vendor_identifier': 15,  # bacnet server vendor
        'multi_read': 20,  # bacnet 批量读取个数
        'cmd_interval': 0.3,  # bacnet命令间隔
        'time_out': 3000  # 超时时间
    }

    client = BacnetClient(**dict_config)
    result = client.cov('6:2', 'analogValue', 1, 180, True)
    print(result)


def test_scan():
    dict_config = {
        'address': '192.168.1.36/24:47809',  # bacnet server ip(绑定网卡)
        'identifier': 555,  # bacnet server identifier
        'name': 'BacnetDriver',  # bacnet server name
        'max_apdu': 1024,  # bacnet server max apdu
        'segmentation': 'segmentedBoth',  # bacnet server segmentation
        'vendor_identifier': 15,  # bacnet server vendor
        'multi_read': 20,  # bacnet 批量读取个数
        'cmd_interval': 0.3,  # bacnet命令间隔
        'time_out': 3000  # 超时时间
    }

    client = BacnetClient(**dict_config)
    objects = client.scan('6:2', '192.168.1.184', True)
    print(client.devices())
    reads = []
    for object in objects:
        target_address, object_type, instance_number = object.split('_')
        reads.append([object_type, int(instance_number), 'presentValue'])
    values = client.read('6:2', reads, '192.168.1.184')
    print(values)
    print(client.devices())


def test_simulate():
    dict_config = {
        'address': '192.168.1.36/24:47808',  # bacnet server ip(绑定网卡)
        'identifier': 555,  # bacnet server identifier
        'name': 'BacnetDriver',  # bacnet server name
        'max_apdu': 1024,  # bacnet server max apdu
        'segmentation': 'segmentedBoth',  # bacnet server segmentation
        'vendor_identifier': 15,  # bacnet server vendor
        'multi_read': 20,  # bacnet 批量读取个数
        'cmd_interval': 0.3,  # bacnet命令间隔
        'time_out': 3000  # 超时时间
    }

    client = BacnetClient(**dict_config)
    objects = [SimulateObject('analogInput', 0, 0), SimulateObject('analogOutput', 0, 0), SimulateObject('analogValue', 0, 0), SimulateObject('binaryInput', 0, 0)]
    client.simluate(objects)
    while True:
        client.update_object('analogInput', 0, random.randint(0,100))
        client.update_object('analogOutput', 0, random.randint(0, 100))
        client.update_object('analogValue', 0, random.randint(0, 100))
        client.update_object('binaryInput', 0, random.randint(0, 100))
        time.sleep(1)

test_scan()