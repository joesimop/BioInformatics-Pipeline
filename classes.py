import os
from file_parser_keys import ProgramParseKeys, StageParseKeys
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
        print(self.arguments)
        inputs = " ".join(input_dir)
        return f"{self.program.exec_name} \\\n\t{self.program.input_cl_identfiier} {inputs} \\\n\t{self.program.output_cl_identifier} {output_dir} \\\n\t{''.join([arg.cl_input for arg in self.arguments])}"
        
    def set_input_dir(self, input_dir):
        self.input_dir = input_dir
    
class Stage:
    def __init__(self, stage_name, process, path_location, data_source, data_source_is_stage, optional_parameters={}):

        self.name = stage_name                              # The name of the folder it resides in
        self.process = process                              # The process object that will be executed
        self.path_location = path_location                  # The path to the stage's directory
        self.data_source = data_source                      # Where the stage gets its data from, can be from /data or from a previous stage
                                                            # Note: The path is indeterminable, because we generate paths when executing. If we 
                                                            #       don't connect to the previous stage however, we can just use the data source itself
        self.data_source_is_stage = data_source_is_stage
        self.optional_parameters = optional_parameters

        #If the user has specified input file types, overwrite the default
        if optional_parameters.get(StageParseKeys.input_file_type.value):
            self.process.program.input_file_types = optional_parameters.get(StageParseKeys.input_file_type.value)

    def __str__(self):
        name = self.name if self.name == self.process.program.name else f"{self.name} - {self.process.program.name}"
        input = f"Input Stage: {self.data_source}" if self.data_source_is_stage else f"Input Data: {self.data_source}"
        args = f"Program Arguments: \n" if self.process.arguments else "Program Arguments: None\n"
        for arg in self.process.arguments:
            args += f"\t{arg.symbol}: {arg.description}\n"

        modifiers ="Modifiers: \n" if self.optional_parameters else "Modifiers: None"
        for p in self.optional_parameters:
            parameters = ", ".join(self.optional_parameters[p])
            modifiers += f"\t{p}: {parameters}\n"

        return f"""{name}
{input}
{args}{modifiers}
---------------------------------------------------------------
                """
                
    def get_run_number(self):
        if os.path.isfile(f"self.path_location/{self.name}_base.log"):
            with open(f"self.path_location/{self.name}_base.log", 'r') as file:
                return int(file.readline()[6])
            
    def save_configuration(self, optional_args):
        with open(f"{self.path_location}/{self.name}.config", 'w') as file:
            file.write(f"{StageParseKeys.stage_name.value}: {self.name}\n")
            file.write(f"{StageParseKeys.program_name.value}: {self.process.program.name}\n")
            file.write(f"{StageParseKeys.data_source.value}: {self.data_source}\n")

            if optional_args.input_file_type:
                encoded = ", ".join(optional_args.input_file_type)
                file.write(f"{StageParseKeys.input_file_type.value} {encoded}\n")

            if optional_args.specific_file_input:
                encoded = ", ".join(optional_args.specific_file_input)
                file.write(f"{StageParseKeys.specific_file_input.value}: {encoded}\n")

            if optional_args.input_subdir:
                encoded = ", ".join(optional_args.input_subdir)
                file.write(f"{StageParseKeys.input_subdir.value}: {encoded}\n")

            file.write(f"{StageParseKeys.arguments.value}: {str(self.process.arguments)[1:-1]}\n")
            file.close()
                