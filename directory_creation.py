import os, sys
from classes import Argument, Program, Stage, Process
from parsing import get_program_by_name
from helpers import *
from environment_setup import user_root

def create_pipline_directory():
    if not os.path.exists(f'{user_root}/pipelines'):
        os.makedirs(f'{user_root}/pipelines')

def create_pipeline(pipeline_name):

    #Ensure there is a pipeline directory
    create_pipline_directory()

    if not os.path.exists(f"{user_root}/pipelines/{pipeline_name}"):
        os.mkdir(f"{user_root}/pipelines/{pipeline_name}")

    #Create the base log file
    if not isfile(f"{user_root}pipelines/{pipeline_name}/.{pipeline_name}_metadata.txt"):
        with open(f"{user_root}/pipelines/{pipeline_name}/.{pipeline_name}_metadata.txt", 'w') as file:
            file.write("runs: 0\n")
            file.write("last_created_stage: None")
            file.close()

    #Create the executions directory
    if not os.path.exists(f"{user_root}/pipelines/{pipeline_name}/executions"):
        os.mkdir(f"{user_root}/pipelines/{pipeline_name}/executions")

    #Create the stages directory
    if not os.path.exists(f"{user_root}/pipelines/{pipeline_name}/stages"):
        os.mkdir(f"{user_root}/pipelines/{pipeline_name}/stages")

def create_stage(cli_input):

    #Get the arguments
    pipeline_name = cli_input.pipeline_name
    stage_name = cli_input.stage_name
    program_name = cli_input.program_name
    data_source = cli_input.data_source

    if not pipeline_exists(pipeline_name):
        byop_error(f"Pipeline \"{pipeline_name}\" does not exist")

    #Create Stage Directory if it does not exist
    if not os.path.exists(f"{user_root}/pipelines/{pipeline_name}/stages/{stage_name}"):
        os.mkdir(f"{user_root}/pipelines/{pipeline_name}/stages/{stage_name}")

    stage_path = f"{user_root}/pipelines/{pipeline_name}/stages/{stage_name}"

    #Get the program the user wants to have in that stage
    program = get_program_by_name(program_name)

    #Check if we either have a stage or a data source
    if data_source is not None:
        if stage_exists(pipeline_name, data_source):
            connects_to_previous_stage = True
        elif data_source_exists(data_source):
            connects_to_previous_stage = False
        else:
            byop_error("Input data source does not exist")
    else:
        #If we no data source was given, we connect to previously created stage
        connects_to_previous_stage = True
        data_source = last_created_stage(pipeline_name)
        if data_source is None:
            byop_error("No previous stage to connect to, please specify a data source")


    #Create the base log file
    if not isfile(f"{stage_path}/{stage_name}_metadata.txt"):
        with open(f"{stage_path}/{stage_name}_metadata.txt", 'w') as file:
            file.write("runs: 0")
            file.close()

        
    #Create the process object
    process = Process(program, [])

    #Create the stage object
    stage = Stage(stage_name, process, stage_path, data_source, connects_to_previous_stage)
    
    #Save the configuration
    stage.save_configuration(cli_input)

    #Set the last created stage
    set_last_created_stage(pipeline_name, stage_name)
    

    