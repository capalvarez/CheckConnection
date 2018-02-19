from cmd2 import Cmd, with_argparser
import argparse
import default_values
from dbcontroller import DBController
from testrunner import TestRunner
from analyzer.analyze_test_results import write_results
from settings import current_path


class TestsCmd(Cmd):
    prompt = 'tests>'

    def __init__(self, user, pswd):
        Cmd.__init__(self)
        self.controller = DBController()
        self.runner = TestRunner(self.controller)
        self.user = user
        self.pswd = pswd
        self.current_results = {}

    def do_listar_campus(self, line):
        "Lista de campus disponibles"
        for f in self.controller.get_campus():
            print(f)

    def do_listar_facultades(self, line):
        "Lista de facultades disponibles"
        for f in self.controller.get_facultades():
            print(f)

    def do_listar_oomm(self, lines):
        "Lista de organismos menores"
        for f in self.controller.get_oomms():
            print(f)

    def complete_seleccionar_campus(self, text, line, begidx, endidx):
        if not text:
            options = self.controller.get_campus()
        else:
            if text.startswith('-'):
                options = ['-todos']
            else:
                options = [f for f in self.controller.get_campus() if f.lower().startswith(text.lower())]

        return options

    def do_seleccionar_campus(self, line):
        if line:
            if line.startswith('-todos'):
                self.runner.add_facultades(self.controller.get_facultades())
            else:
                self.runner.add_facultades(self.controller.parse_campus(line))
        else:
            campus = self.select(self.controller.get_campus(), 'Campus? ')
            self.runner.add_facultades(self.controller.get_facultades_campus(campus))

    def do_seleccionar_facultad(self, line):
        campus = self.select(self.controller.get_campus(), 'Campus? ')
        facultad = self.select(self.controller.get_facultades_campus(campus), 'Facultad? ')

        self.runner.add_facultad(facultad)

    def complete_seleccionar_oomm(self,  text, line, begidx, endidx):
        if not text:
            options = self.controller.get_oomms()
        else:
            if text.startswith('-'):
                options = ['-todos']
            else:
                options = [f for f in self.controller.get_oomms() if f.lower().startswith(text.lower())]

        return options

    def do_seleccionar_oomm(self, line):
        if line:
            if line.startswith('-todos'):
                self.runner.add_oomms(self.controller.get_oomms())
            else:
                self.runner.add_oomms(self.controller.parse_oomm(line))

    def do_seleccionar_todo(self, line):
        self.runner.add_oomms(self.controller.get_oomms())
        self.runner.add_facultades(self.controller.get_facultades())

    run_parser = argparse.ArgumentParser()
    run_parser.add_argument('--packets', nargs='?', default=default_values.number_pings)
    run_parser.add_argument('--threads', nargs='?', default=default_values.default_threads)
    run_parser.add_argument('--destination', nargs='?', default=default_values.default_destination)
    run_parser.add_argument('--time', action='store_true')

    @with_argparser(run_parser)
    def do_correr_prueba(self, args):
        config = {
            'user': self.user,
            'pswd': self.pswd,
            'pings': args.packets,
            'threads': args.threads,
            'destination': args.destination,
            'measure_time': args.time
        }

        self.current_results = self.runner.run_selected_tests(config)

    save_parser = argparse.ArgumentParser()
    save_parser.add_argument('--output', nargs='?', default=default_values.default_output)

    @with_argparser(save_parser)
    def do_guardar_resultados(self, args):
        output = args.output
        output_path = current_path + '/' + output

        write_results(self.current_results, output_path)

    def do_ver_seleccionados(self, line):
        print(self.runner.get_selected())

    def do_borrar(self, line):
        self.runner.delete_selected()