from enum import Enum

## PROGRAM PARSING NAMES ##
class ProgramParseKeys(Enum):
    program_name = "name"
    exec = "exec"
    input_file_types = "input_file_types"
    output_file_types = "output_file_types"
    input_identifier = "input_identifier"
    output_identifier = "output_identifier"
    pipeline_stages = "pipeline_stages"
    docs = "docs"
    arguments = "arguments"
    extra_params = "extra params"


## STAGE PARSING NAMES ##
class StageParseKeys(Enum):
    program_name = "program name"
    arguments = "arguments"
    data_source = "data source"
    stage_name = "stage name"
    specific_file_input = "specific file input"
    input_file_type = "input file type"
    input_subdir = "input subdirectory"

