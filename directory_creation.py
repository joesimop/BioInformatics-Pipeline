import os
from classes import Argument, Program, Stage, Process
from parsing import get_program_by_name
from helpers import stage_exists, data_source_exists

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

    #Ensure there is a pipeline directory
    create_pipline_directory()

    if not os.path.exists(f"pipelines/{pipeline_name}"):
        os.mkdir(f"pipelines/{pipeline_name}")

    #Create the base log file
    if not os.path.isfile(f"pipelines/{pipeline_name}/.{pipeline_name}_meta_data.log"):
        with open(f"pipelines/{pipeline_name}/.{pipeline_name}_metadata.txt", 'w') as file:
            file.write("runs: 0")
            file.write("last_created_stage: None")
            file.close()

    #Create the executions directory
    if not os.path.exists(f"pipelines/{pipeline_name}/executions"):
        os.mkdir(f"pipelines/{pipeline_name}/executions")

def create_pipline_directory():
    if not os.path.exists('pipelines'):
        os.makedirs('pipelines')

def create_stage(pipeline_name, stage_name, program_name, data_source=None):

    #Ensure there is a pipeline directory
    create_pipeline(pipeline_name)

    #Create Stage Directory if it does not exist
    if not os.path.exists(f"pipelines/{pipeline_name}/{stage_name}"):
        os.mkdir(f"pipelines/{pipeline_name}/{stage_name}")

    stage_path = f"pipelines/{pipeline_name}/{stage_name}"

    #Get the program the user wants to have in that stage
    program = get_program_by_name(program_name)

    #Check if we either have a stage or a data source
    if data_source is not None:
        if stage_exists(pipeline_name, data_source):
            connects_to_previous_stage = True
        elif data_source_exists(data_source):
            connects_to_previous_stage = False
        raise ValueError("Input path location is required for processing")

    #Create the base log file
    if not os.path.isfile(f"{stage_path}/{stage_name}_metadata.txt"):
        with open(f"{stage_path}/{stage_name}_metadata.txt", 'w') as file:
            file.write("runs: 0")
            file.close()

        
    #Create the process object
    process = Process(program, [])

    #Create the stage object
    stage = Stage(stage_name, process, stage_path, data_source, connects_to_previous_stage)
    
    #Save the configuration
    stage.save_configuration()
    

    