import os
from environment_setup import user_root

def already_exists(path):
    return os.path.exists(path)

def in_pipeline_dir():
    return user_root.split('/')[-1] == 'pipelines'

def pipeline_exists(pipeline):
    return os.path.exists(f"{user_root}/pipelines/{pipeline}")

def stage_exists(pipeline, stage_name):
    return os.path.exists(f'{user_root}/pipelines/{pipeline}/{stage_name}')

def data_source_exists(data_source):
    return os.path.exists(f"{user_root}/data/{data_source}")

#Check if the last created stage exists
def last_created_stage(pipeline):
    if os.path.isfile(f"{user_root}/pipelines/{pipeline}/.{pipeline}_metadata.txt"):
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
