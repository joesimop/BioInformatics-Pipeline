import os, sys
from byop.environment_setup import user_root
from byop.file_parser_keys import StageParseKeys

def already_exists(path):
    return os.path.exists(path)

def isfile(path):
    return os.path.isfile(path)

def in_pipeline_dir():
    return user_root.split('/')[-1] == 'pipelines'

def pipeline_exists(pipeline):
    return os.path.exists(f"{user_root}/pipelines/{pipeline}")

def stage_exists(pipeline, stage_name):
    return os.path.exists(f'{user_root}/pipelines/{pipeline}/stages/{stage_name}')

def data_source_exists(data_source):
    return os.path.exists(f"{user_root}/data/{data_source}")

def list_avaialble_pipelines():
    return os.listdir('pipelines')

def list_available_programs():
    for program in os.listdir('supported_programs'):
        if program != "README":
            print(program[0:-4])

#Check if the last created stage exists
def last_created_stage(pipeline):
    if isfile(f"{user_root}/pipelines/{pipeline}/.{pipeline}_metadata.txt"):
        with open(f"{user_root}/pipelines/{pipeline}/.{pipeline}_metadata.txt", 'r') as file:
            file.readline()     # Skip the first line
            stage = file.readline().split(': ')[1]

            if stage == 'None':
                return None
            
            return stage
        
def set_last_created_stage(pipeline, stage):
    with open(f"{user_root}/pipelines/{pipeline}/.{pipeline}_metadata.txt", 'r+') as file:
        file.readline()     # Skip the first line
        file.seek(8)        #Hardcoded, but right now, its the only way I know how

        #Clear the line and hope to God it's long enough
        file.write("                                                                           ")
        
        file.seek(8)
        file.write(f"last_created_stage: {stage}")
        file.close()

def byop_error(message):
    print(f"BYOP Error: {message}")
    sys.exit(1)

def contstruct_input_dir(stage, stage_output_dir):
    """
    Creates a list of input directories for the stage based on the optional parameters and the stage's data source.
    """

    # If the user did specify input subdirectories, we need to create a list of input directories
    if stage.optional_parameters.get(StageParseKeys.input_subdir.value, None) and stage_output_dir is not None:
         input_dir = [f"{stage_output_dir}/{subdir}/" for subdir in stage.optional_parameters[StageParseKeys.input_subdir.value]]
        
    #Otherwise, just use default logic
    else:
        if stage.data_source_is_stage:
            input_dir = [f"{stage_output_dir}/"]
        else:
            input_dir = [f"{user_root}/data/{stage.data_source}/"]
       

    for directory in input_dir:
        if not os.path.exists(directory):
            byop_error(f"Input directory {directory} does not exist")

    return input_dir

def construct_file_extension_identifiers(stage, input_directories):
    """
    Creates a input file for each identified file type for each input directory.
    """

    #Note: The file types of the output program within the stage are overwritten
    #      if the user specifies a file type in the optional parameters, so the filetypes will already by loaded in
    
    #If the user specified a specific file, use that as input
    #At the moment, only allow for one directory if the uses specifies files
    if stage.optional_parameters.get(StageParseKeys.specific_file_input, None):
        for file in stage.optional_parameters[StageParseKeys.specific_file_input]:
            yield f"{input_directories[0]}*{file}"
    else:
        file_types = stage.process.program.input_file_types
        for file_type in file_types:
            for directory in input_directories:
                yield f"{directory}*{file_type}"


def update_run_count(file_path):
    with open(file_path, 'r+') as file:
            run_number = int(file.readline()[6])
            updated_run = f"runs: {run_number + 1}"
            file.seek(0)
            file.write(updated_run)
            file.close()

    return run_number

def execute_command(command, program_name, output_dir):
    
    import subprocess

    subprocess_input = command.strip().split(" ")

    with open(f"{output_dir}/{program_name}_output.txt", 'w') as output_file:
        process = subprocess.Popen(subprocess_input, stdout=subprocess.PIPE, check=True)

        for c in iter(lambda: process.stdout.read(1), ""):
            sys.stdout.write(c)
            output_file.write(c)

        process.wait()

    return