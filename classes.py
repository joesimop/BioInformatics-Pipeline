import os

class Argument:
    def __init__(self, symbol, description):
        self.symbol = symbol
        self.description = description
        self.cl_input = f"{self.symbol} {self.description} \\\n"

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
        

    def print_argument_descriptions(self):
        for arg in self.common_arguments:
            print(f"{arg.symbol}: {arg.description}")

class Process:
    def __init__(self, program, arguments):
        self.program = program
        self.arguments = arguments
        
    def create_executable(self, input_dir, output_dir):

        return f"""{self.program.exec_name} \\
                {self.program.input_cl_identfiier} {input_dir} \\ 
                {self.program.output_cl_identifier} {output_dir} \\ 
                {''.join([arg.cl_input for arg in self.arguments])}"""
        
    def set_input_dir(self, input_dir):
        self.input_dir = input_dir
    
class Stage:
    def __init__(self, stage_name, process, path_location, data_source, data_source_is_stage):

        self.name = stage_name                  # The name of the folder it resides in
        self.process = process                  # The process object that will be executed
        self.path_location = path_location      # The path to the stage's directory
        self.data_source = data_source          # Where the stage gets its data from, can be from /data or from a previous stage
                                                # Note: The path is indeterminable, because we generate paths when executing. If we 
                                                #       don't connect to the previous stage however, we can just use the data source itself
        self.data_source_is_stage = data_source_is_stage

    def __str__(self):
        return f"""{self.name} - {self.process.program.name}
                    Input Directory: {self.process.input_dir}
                """
                
    def get_run_number(self):
        if os.path.isfile(f"self.path_location/{self.name}_base.log"):
            with open(f"self.path_location/{self.name}_base.log", 'r') as file:
                return int(file.readline()[6])
            
    def save_configuration(self):
        with open(f"{self.path_location}/{self.name}.config", 'w') as file:
            file.write(f"Stage Name: {self.name}\n")
            file.write(f"Program Name: {self.process.program.name}\n")
            file.write(f"Data Source: {self.data_source}\n")
            file.write(f"Arguments: {str(self.process.arguments)[1:-1]}\n")
            file.close()
                