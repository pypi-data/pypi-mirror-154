import os
import sys
import json
import pathlib
import pprint
from lmfa.multifamily_analysis import MultiFamily
from lmfa.multifamily_analysis import MultiFamilyCharts
from lmfa.utilities import add_and_get_output_folder


def run_analysis(config_filenames=[]):
    mf = MultiFamily()

    config_outputs = []

    for config_filename in config_filenames:
        config = mf.get_config_data(config_filename=config_filename)
        config = mf.add_missing_inputs(config=config)
        config = mf.get_metrics(config)

        config_outputs.append(config)
        print("=======================================")
        print("For Project A:")
        pprint.pprint(config['projects'][0])

        parent_path = pathlib.Path(config_filename).parent.absolute()
        output_folder = add_and_get_output_folder(parent_path)

        output_filename = os.path.join(
            output_folder,
            config_filename.split('.')[0] + '_out.yaml')
        with open(output_filename, 'w') as output_file:
            output_file.write(json.dumps(config, indent=4))

    mfc = MultiFamilyCharts()
    mfc.get_common_chart_data(config_outputs)
    mfc.get_all_charts(output_folder)


'''
TODO 
a/ Increase LP incentive brackets further
b/ Add more breakdown to expenses, renovations, etc.
c/ Automate market research numbers using python tools
d/ Include Class A and B shares if amount is significantly high
e/ Implement sensitivity analysis for financial stress tests
'''