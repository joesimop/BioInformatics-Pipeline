import os
from classes import Argument, Program, Stage, Process
from helpers import get_program_by_name

def write_config_file(filepath, program_name, input_dir, output_dir, arguments, extra_params):
    with open(filepath, 'w') as file:
        # Write basic configuration parameters
        file.write(f"program_name: {program_name}\n")
        file.write(f"input_dir: {input_dir}\n")
        file.write(f"output_dir: {output_dir}\n")

        # Write arguments if there are any
        if arguments:
            file.write("arguments:\n")
            for arg in arguments:
                file.write(f"    {arg.symbol}:  {arg.description}\n")

        # Write extra parameters
        file.write(f"extra_params: {extra_params}\n")

def create_pipeline(pipeline_name):
    create_pipline_directory()
    if not os.path.exists(f"pipelines/{pipeline_name}"):
        os.mkdir(f"pipelines/{pipeline_name}")

def create_pipline_directory():
    if not os.path.exists('pipelines'):
        os.makedirs('pipelines')

def create_stage(pipeline_name, stage_name, program_name, input_path_location=None, previous_stage=None):

    #Ensure there is a pipeline directory
    create_pipeline(pipeline_name)

    #Create Stage Directory if it does not exist
    if not os.path.exists(f"pipelines/{pipeline_name}/{stage_name}"):
        os.mkdir(f"pipelines/{pipeline_name}/{stage_name}")

    #Get the program the user wants to have in the stage
    program = get_program_by_name(program_name)


    if input_path_location is None:
        input_path_location = f"pipelines/{pipeline_name}/{stage_name}/input"

    #Create the process object
    process = Process(program, program.input_dir, program.output_dir, program.arguments)
    
    
    write_config_file(f"pipelines/{pipeline_name}/{stage_name}/config.txt", 
                        program.name, program.input_dir, program.output_dir, program.arguments, program.extra_params)
    

    