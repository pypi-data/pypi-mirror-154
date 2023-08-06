import os
import sys
import pathlib


def add_and_get_output_folder(parent_path=None):
    if parent_path is None:
        parent_path = pathlib.Path(__file__).resolve().parent
    output_folder = os.path.join(parent_path, 'output')
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    return output_folder


def get_config_files():
    argv = sys.argv[1:]
    if len(config_filenames) == 0:
        config_filenames = [arg for arg in argv if arg.find('=') < 0]
    if len(config_filenames) == 0:
        config_filenames = ['multifamily_2.yaml', 'multifamily_4.yaml']
