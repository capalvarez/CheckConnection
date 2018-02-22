import settings as settings
import ruamel.yaml as yaml


class DBController:
    def __init__(self):
        self.campus, self.facultades, self.oomm = self.init_variables()
        self.selected = []

    @staticmethod
    def init_variables():
        with open(settings.lista_campus) as file:
            campus = yaml.load(file, Loader=yaml.RoundTripLoader)

        facultades = []
        for c in campus.values():
            facultades.extend(c['Facultades'])

        with open(settings.lista_oomm) as file:
            oomm = yaml.load(file, Loader=yaml.RoundTripLoader)

        return campus, facultades, oomm

    def get_campus(self):
        return self.campus

    def get_facultades(self):
        return self.facultades

    def get_oomms(self):
        return self.oomm

    def get_facultades_campus(self, c):
        return self.campus[c]['Facultades']

    def parse_oomm(self, string):
        return self.parse_list(self.oomm, string)

    def parse_campus(self, string):
        return self.parse_list(self.campus.keys(), string)

    def parse_facultades(self, string):
        return self.parse_list(self.facultades, string)

    def parse_list(self, options, selected):
        separated = selected.split()
        hits = []

        for s in separated:
            hits.extend([x for x in options if s in x.split()])

        return list(set(hits))

    def get_file_name(self, device):
        return device.get_name().lower() + '.txt', device.get_name().lower()