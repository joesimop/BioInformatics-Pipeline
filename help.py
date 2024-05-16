import os

def list_avaialble_pipelines():
    return os.listdir('pipelines')

def list_available_programs():
    for program in os.listdir('supported_programs'):
        if program != "README":
            print(program[0:-4])