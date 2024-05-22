import os
from classes import Argument, Program, Process, Stage
from helpers import stage_exists, data_source_exists, byop_error
from environment_setup import program_root, user_root
from file_parser_keys import ProgramParseKeys, StageParseKeys

def get_program_by_name(program_name):
    if os.path.exists(f'{program_root}/supported_programs'):
        programs = os.listdir(f'{program_root}/supported_programs')
        found_program = False
        for program_cfg in programs:
            if program_cfg[0:-4] == program_name.capitalize():
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
    


list_parameters = [ProgramParseKeys.input_file_types.value,
                   ProgramParseKeys.output_file_types.value,
                   StageParseKeys.input_file_type.value,
                   StageParseKeys.specific_file_input.value,
                   StageParseKeys.input_subdir.value]
# Parses a configuration file and returns a dictionary with the parsed data
def parse_config_file(file_path, parse_dict):

    with open(file_path, 'r') as file:
        text = file.read()


    lines = text.strip().split('\n')
    in_arguments = False
    for line in lines:
        line = line.strip()
        if line.lower().startswith('arguments:'):
            in_arguments = True
        elif in_arguments and line.startswith('-'):
            symbol, description = line.split(': ', 1)
            parse_dict['arguments'].append(Argument(symbol.strip(), description.strip()))
        elif line:
            if ':' in line:
                key, value = line.split(': ', 1)
                key = key.strip().lower()
                value = value.strip()
                if key in list_parameters:
                    parse_dict[key] = value.split(', ')
                else:
                    parse_dict[key] = value
    return parse_dict



def parse_program_file(program_name):

    with open(f"{program_root}/supported_programs/{program_name}", 'r') as file:
        text = file.read()

    config = {
        ProgramParseKeys.arguments.value: [],
        ProgramParseKeys.extra_params: ''
    }
    
    config = parse_config_file(f"{program_root}/supported_programs/{program_name}", config)

    #Error Checking values
    if not config.get(ProgramParseKeys.program_name.value):
        byop_error("Name is a required field. Please provide a name in the configuration file.")
    if not config.get(ProgramParseKeys.exec.value):
        byop_error("Executable name is a required field. Please provide an executable name in the configuration file.")
    if not config.get(ProgramParseKeys.input_identifier.value):
        byop_error("Input identifier is a required field. Please provide an input identifier in the configuration file.")
    if not config.get(ProgramParseKeys.output_identifier.value):
        byop_error("Output identifier is a required field. Please provide an output identifier in the configuration file.")
    if not config.get(ProgramParseKeys.input_file_types.value):
        byop_error("Input file types is a required field. Please provide an input file type in the configuration file.")
    if not config.get(ProgramParseKeys.output_file_types.value):
        byop_error("Output file types is a required field. Please provide an output file type in the configuration file.")

    # Creating the Program instance with parsed data
    return Program(
        name=config.get(ProgramParseKeys.program_name.value, ''),
        exec_name=config.get(ProgramParseKeys.exec.value, ''),
        input_file_types=config.get(ProgramParseKeys.input_file_types.value, []),
        output_file_types=config.get(ProgramParseKeys.output_file_types.value, []),
        input_cl_identfier=config.get(ProgramParseKeys.input_identifier.value, ''),
        output_cl_identifier=config.get(ProgramParseKeys.output_identifier.value, ''),
        common_arguments=config.get(ProgramParseKeys.arguments.value, []),
        pipeline_stages=config.get(ProgramParseKeys.pipeline_stages.value, [])
    )

#Loads in a stage, given the path to the stage
def load_stage_config(stage_file_path):

    # Get file name from the path.
    file_name = f"{stage_file_path.split('/')[-1]}.config"

    config = parse_config_file(f"{stage_file_path}/{file_name}", {StageParseKeys.arguments.value: []})
    
    # Extract process related information assuming it's already included
    program_name = config.get(StageParseKeys.program_name.value)
    arguments = config.get(StageParseKeys.arguments.value)

    #Get program
    program = get_program_by_name(program_name)
    
    # Create a Process object
    process = Process(program, arguments)
    
    # Get the path and previous stage information
    data_source = config.get(StageParseKeys.data_source.value, "None")

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
    stage_name = config.get(StageParseKeys.stage_name.value)

    #Remove all mandatory parameters from config so only optionals are left:
    config.pop(StageParseKeys.program_name.value)
    config.pop(StageParseKeys.stage_name.value)
    config.pop(StageParseKeys.data_source.value)
    config.pop(StageParseKeys.arguments.value)

    return Stage(stage_name, process, stage_file_path, data_source, connect_to_previous_stage, config)