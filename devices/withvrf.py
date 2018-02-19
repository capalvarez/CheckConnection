from devices.cisco import Cisco
from devices.devices_functions import ping_vrf


class WithVRF(Cisco):
    def __init__(self):
        Cisco.__init__(self, ping_vrf)
