from devices.dellforce import DellForce
from devices.cisco import Cisco
from devices.hp import HP
from devices.delln import DellN
from exceptions.devices_exceptions import DeviceTypeUnknown


devices_type = {
    'dell': {'name': 'dell_force10', 'controller': DellForce()},
    'cisco': {'name': 'cisco_ios', 'controller': Cisco()},
    'hp': {'name': 'hp_procurve', 'controller': HP()},
    'dell n': {'name': 'dell_force10', 'controller': DellN()},
    'cisco - telnet': {'name': 'cisco_ios_telnet', 'controller': Cisco()}
}


def get_type(device_type):
    try:
        return devices_type[device_type.lower()]
    except KeyError:
        raise DeviceTypeUnknown(device_type)
