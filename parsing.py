import os
from classes import Argument, Program, Process, Stage
from helpers import stage_exists, data_source_exists

def get_program_by_name(program_name):
    if os.path.exists('supported_programs'):
        programs = os.listdir('supported_programs')
        for program_cfg in programs:
            print(program_cfg[0:-3])
            if program_cfg[0:-4] == program_name:

                try:
                    return parse_program_file(program_cfg)
                except ValueError as e:
                    print(f"Error parsing {program_cfg}: {e}")
                    continue
    else:
        raise ValueError("Cannot find supported_programs directory")
    
def get_stage_by_name(pipeline, stage_name):
    dir = f'pipelines/{pipeline}/{stage_name}'
    if os.path.exists(dir):
        try:
            return load_stage_config(dir, f"{stage_name}.config")
        except ValueError as e:
            print(f"Error loading {stage_name}: {e}")
    else:
        raise ValueError("Cannot find stages directory")

def parse_program_file(program_name):

    with open(f"supported_programs/{program_name}", 'r') as file:
        text = file.read()

    config = {
        'arguments': [],
        'extra_params': ''
    }
    current_arg = None
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('arguments:'):
            current_arg = 'arguments'
        elif current_arg == 'arguments' and line.startswith('-'):
            symbol, description = line.split(': ', 1)
            config['arguments'].append(Argument(symbol.strip(), description.strip()))
        elif line:
            if ':' in line:
                key, value = line.split(': ', 1)
                key = key.strip()
                value = value.strip()
                if key in ['input_file_types', 'output_file_types', 'pipeline_stages']:
                    config[key] = value.split(', ')
                else:
                    config[key] = value

    #Error Checking values
    if not config.get('name'):
        raise ValueError("Name is a required field. Please provide a name in the configuration file.")
    if not config.get('exec'):
        raise ValueError("Executable name is a required field. Please provide an executable name in the configuration file.")
    if not config.get('input_identifier'):
        raise ValueError("Input identifier is a required field. Please provide an input identifier in the configuration file.")
    if not config.get('output_identifier'):
        raise ValueError("Output identifier is a required field. Please provide an output identifier in the configuration file.")
    if not config.get('input_file_types'):
        raise ValueError("Input file types is a required field. Please provide an input file type in the configuration file.")
    if not config.get('output_file_types'):
        raise ValueError("Output file types is a required field. Please provide an output file type in the configuration file.")

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

def load_stage_config(stage_file_path):

    file_name = f"{stage_file_path.split('/')[-1]}.config"

    # Read the configuration file
    with open(f"{stage_file_path}/{file_name}", 'r') as file:
        lines = file.readlines()
    
    # Prepare a dictionary to store configuration data
    config = {}
    in_arguments = False
    for line in lines:
        if line.startswith("Arguments:"):
            in_arguments = True
            config['Arguments'] = []
            continue
        elif in_arguments:
            symbol, description = line.split(": ", 1)
            config['Arguments'].append(Argument(symbol.strip(), description.strip()))
        else:
            key, value = line.split(": ", 1)
            config[key.strip()] = value.strip()
    
    # Extract process related information assuming it's already included
    program_name = config.get("Program Name")
    input_dir = config.get("Input Directory")
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
        raise ValueError("Cannot find input path location for processing")
    
    # Create and return a Stage object
    stage_name = config.get("Stage Name")
    return Stage(stage_name, process, stage_file_path, data_source, connect_to_previous_stage)