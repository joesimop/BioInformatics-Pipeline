import os
from enums import PipelineStage

class Argument:
    def __init__(self, symbol, description):
        self.symbol = symbol
        self.description = description
        self.cl_input = f"{self.symbol} {self.description} "

class Program:
    def __init__(self, name, exec_name, input_file_types, output_file_types, input_cl_identfier, output_cl_identifier, common_arguments, pipeline_stages):
        self.name = name
        self.exec_name = exec_name
        self.input_file_types = input_file_types
        self.output_file_types = output_file_types
        self.input_cl_identfiier = input_cl_identfier
        self.output_cl_identifier = output_cl_identifier
        self.pipeline_stages = pipeline_stages
        self.common_arguments = common_arguments
        

    def print_arguments(self):
        for arg in self.common_arguments:
            print(f"{arg.symbol}: {arg.description}")

    def is_executable(self):
        return os.path.isdir(self.input_dir) and os.path.isdir(self.output_dir)

class Process:
    def __init__(self, program, input_dir, output_dir, arguments):
        self.program = program
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.arguments = arguments
        
    def create_executable(self):
        return f"{self.program.exec_name} 
                 {self.program.input_cl_identfiier} {self.input_dir} 
                 {self.program.output_cl_identifier} {self.output_dir} 
                 {str([arg.cl_input for arg in self.arguments])[1:-1]}"
    
class Stage:
    def __init__(self, stage_name, process, path_location, previous_stage=None):
        self.name = stage_name                  #Will be the name of the folder it resides in
        self.process = process
        self.path_location = path_location
        self.previous_stage = previous_stage

    def __str__(self):
        return f"""{self.name} - {self.process.program.name}
                    Input Directory: {self.process.input_dir}
                    Output Directory: {self.process.output_dir}
                """
    def verify_next_stage_compatibility(self):
        if self.next_stage is not None:
            if self.previous_stage.process.program.output_file_types != self.process.program.input_file_types:
                raise ValueError("Output file types of the previous stage do not match input file types of current stage")