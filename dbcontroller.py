import settings as settings
import facultades as f
import ruamel.yaml as yaml


class DBController:
    def __init__(self):
        self.campus, self.facultades, self.oomm = self.init_variables()
        self.selected = []

    @staticmethod
    def init_variables():
        with open(settings.lista_campus) as file:
            campus = yaml.load(file, Loader=yaml.RoundTripLoader)

        with open(settings.lista_facultades) as file:
            facultades = yaml.load(file, Loader=yaml.RoundTripLoader)

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
            hits.extend([x for x in options if s in x])

        return list(set(hits))