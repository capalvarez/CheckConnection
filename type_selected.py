import facultades as f
from settings import base_sources_path, base_files_path


class NameTypePair:
    def __init__(self, name, ty):
        self.name = name
        self.type = ty

    def get_file_name(self):
        pass

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

    def get_file_name(self):
        return f.facultades_map[self.name.lower()]


class OOMMPair(NameTypePair):
    def __init__(self, name):
        NameTypePair.__init__(self, name, 'oomm')

    def get_file_name(self):
        return f.oomm_map[self.name.lower()]


class TypeSelected:
    def __init__(self):
        self.facultades = set()
        self.oomm = set()

    def add_facultad(self, fac):
        self.facultades.add(fac)

    def add_oomm(self, oomm):
        self.oomm.add(oomm)

    def add_facultades(self, facs):
        for f in facs:
            self.facultades.add(f)

    def add_oomms(self, oomms):
        for o in oomms:
            self.oomm.add(o)

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

        return string

    def get_all(self):
        facultades = list(map(lambda x: FacultadesPair(x), list(self.facultades)))
        oomm = list(map(lambda x: OOMMPair(x), list(self.oomm)))

        return facultades + oomm


