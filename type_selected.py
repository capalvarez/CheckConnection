from settings import base_sources_path, base_files_path
from exceptions.devices_exceptions import UnknownFacultadOrOOMM


class NameTypePair:
    def __init__(self, name, ty):
        self.name = name
        self.type = ty

    def get_complete_sources_path(self, relative_source):
        return base_sources_path + self.type + '/' + relative_source

    def get_base_path(self):
        return base_files_path + self.type + '/'

    def __str__(self):
        return self.name + '_' + self.type

    def get_name(self):
        return self.name


class FacultadesPair(NameTypePair):
    def __init__(self, name):
        NameTypePair.__init__(self, name, 'facultad')


class OOMMPair(NameTypePair):
    def __init__(self, name):
        NameTypePair.__init__(self, name, 'oomm')


class DatacenterPair(NameTypePair):
    def __init__(self, name):
        NameTypePair.__init__(self, name, 'datacenter')


class TypeSelected:
    def __init__(self):
        self.facultades = set()
        self.oomm = set()
        self.datacenter = set()

    def add_facultad(self, fac):
        self.facultades.add(fac)

    def add_oomm(self, oomm):
        self.oomm.add(oomm)

    def add_datacenter(self, data):
        self.datacenter.add(data)

    def add_facultades(self, facs):
        for f in facs:
            self.facultades.add(f)

    def add_oomms(self, oomms):
        for o in oomms:
            self.oomm.add(o)

    def add_datacenters(self, datas):
        for d in datas:
            self.datacenter.add(d)

    def clear(self):
        self.facultades = set()
        self.oomm = set()

    def __str__(self):
        string = ''

        if self.facultades:
            fac_list = list(self.facultades)
            string += 'Facultades: '
            for i in range(0, len(fac_list)-1):
                string += fac_list[i] + ', '
            string += fac_list[-1]

        if self.oomm:
            if self.facultades:
                string += '\n'
            oomm_list = list(self.oomm)
            string += 'Organismos menores: '
            for i in range(0, len(oomm_list)-1):
                string += oomm_list[i] + ', '
            string += oomm_list[-1]

        if self.datacenter:
            if self.oomm:
                string += '\n'
            datacenter_list = list(self.datacenter)
            string += 'Equipos datacenter: '
            for i in range(0, len(datacenter_list)-1):
                string += datacenter_list[i] + ', '
            string += datacenter_list[-1]

        return string

    def get_all(self):
        facultades = list(map(lambda x: FacultadesPair(x), list(self.facultades)))
        oomm = list(map(lambda x: OOMMPair(x), list(self.oomm)))
        datacenter = list(map(lambda x: DatacenterPair(x), list(self.datacenter)))

        return facultades + oomm + datacenter


