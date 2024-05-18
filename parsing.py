import os
from classes import Argument, Program, Process, Stage
from helpers import stage_exists, data_source_exists, byop_error
from environment_setup import program_root, user_root

def get_program_by_name(program_name):
    if os.path.exists(f'{program_root}/supported_programs'):
        programs = os.listdir(f'{program_root}/supported_programs')
        found_program = False
        for program_cfg in programs:
            if program_cfg[0:-4] == program_name:
                found_program = True
                try:
                    return parse_program_file(program_cfg)
                except ValueError as e:
                    print(f"Error parsing {program_cfg}: {e}")
                    continue
        if not found_program:
            byop_error("Cannot find program in supported_programs directory")
    else:
        byop_error("Cannot find supported_programs directory")
    
def get_stage_by_name(pipeline, stage_name):
    dir = f'{user_root}/pipelines/{pipeline}/{stage_name}'
    if os.path.exists(dir):
        try:
            return load_stage_config(dir, f"{stage_name}.config")
        except ValueError as e:
            print(f"Error loading {stage_name}: {e}")
    else:
        byop_error("Cannot find stages directory")
    
def parse_config_file(file_path, parse_dict):

    with open(file_path, 'r') as file:
        text = file.read()


    lines = text.strip().split('\n')
    in_arguments = False
    for line in lines:
        line = line.strip()
        if line.startswith('Arguments:'):
            in_arguments = True
        elif in_arguments and line.startswith('-'):
            symbol, description = line.split(': ', 1)
            parse_dict['Arguments'].append(Argument(symbol.strip(), description.strip()))
        elif line:
            if ':' in line:
                key, value = line.split(': ', 1)
                key = key.strip()
                value = value.strip()
                if key in ['input_file_types', 'output_file_types']:
                    parse_dict[key] = value.split(', ')
                else:
                    parse_dict[key] = value
    
    return parse_dict



def parse_program_file(program_name):

    with open(f"{program_root}/supported_programs/{program_name}", 'r') as file:
        text = file.read()

    config = {
        'Arguments': [],
        'Extra Params': ''
    }
    
    config = parse_config_file(f"{program_root}/supported_programs/{program_name}", config)

    #Error Checking values
    if not config.get('name'):
        byop_error("Name is a required field. Please provide a name in the configuration file.")
    if not config.get('exec'):
        byop_error("Executable name is a required field. Please provide an executable name in the configuration file.")
    if not config.get('input_identifier'):
        byop_error("Input identifier is a required field. Please provide an input identifier in the configuration file.")
    if not config.get('output_identifier'):
        byop_error("Output identifier is a required field. Please provide an output identifier in the configuration file.")
    if not config.get('input_file_types'):
        byop_error("Input file types is a required field. Please provide an input file type in the configuration file.")
    if not config.get('output_file_types'):
        byop_error("Output file types is a required field. Please provide an output file type in the configuration file.")

    # Creating the Program instance with parsed data
    return Program(
        name=config.get('name', ''),
        exec_name=config.get('exec', ''),
        input_file_types=config.get('input_file_types', []),
        output_file_types=config.get('output_file_types', []),
        input_cl_identfier=config.get('input_identifier', ''),
        output_cl_identifier=config.get('output_identifier', ''),
        common_arguments=config.get('arguments', []),
        pipeline_stages=config.get('pipeline_stages', [])
    )

#Loads in a stage, given the path to the stage
def load_stage_config(stage_file_path):

    # Get file name from the path.
    file_name = f"{stage_file_path.split('/')[-1]}.config"

    config = parse_config_file(f"{stage_file_path}/{file_name}", {'Arguments': []})
    
    # Extract process related information assuming it's already included
    program_name = config.get("Program Name")
    arguments = config.get("Arguments")

    #Get program
    program = get_program_by_name(program_name)
    
    # Create a Process object
    process = Process(program, arguments)
    
    # Get the path and previous stage information
    data_source = config.get("Data Source")

    pipeline = stage_file_path.split('/')[-2]

    if data_source == "None":
        data_source = None
        connect_to_previous_stage = False
    elif stage_exists(pipeline, data_source):
        connect_to_previous_stage = True
    elif data_source_exists(data_source):
        connect_to_previous_stage = False
    else:
        byop_error("Cannot find input path location for processing")
    
    # Create and return a Stage object
    stage_name = config.get("Stage Name")
    return Stage(stage_name, process, stage_file_path, data_source, connect_to_previous_stage)