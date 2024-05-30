import argparse
from argparse import RawTextHelpFormatter

def get_parser():
    
    
    parser = argparse.ArgumentParser(prog='byop',
                                     description='A tool to build and run your own bioinformatics pipelines.', 
                                     formatter_class=RawTextHelpFormatter)
    

    subparsers = parser.add_subparsers(dest='command', metavar="", title="Commands")

    pipeline_parent_parser = argparse.ArgumentParser(add_help=False)
    pipeline_parent_parser.add_argument('pipeline_name', help='Name of the pipeline')

    stage_parent_parser = argparse.ArgumentParser(add_help=False)
    stage_parent_parser.add_argument('stage_name', help='Name of the stage')

    """
    COMMNNDS FOR PROGRAM
    """

    #Print the supported programs
    list_programs = subparsers.add_parser('list_programs', help='Lists all supported programs')

    #Create a pipeline
    create_pipeline = subparsers.add_parser('create_pipeline', help='Create a new pipeline', parents=[pipeline_parent_parser])

    #Create a stage, within a pipeline
    create_stage = subparsers.add_parser('create_stage', help='Create a new stage in a pipeline', parents=[pipeline_parent_parser, stage_parent_parser], formatter_class=RawTextHelpFormatter)
    create_stage.add_argument('program_name', help='Name of the program to run in the stage')
    create_stage.add_argument('-data_source', help='Name of the data source to use in the stage.\nIt can be a stage in this pipeline or a directory/file in your data folder.\n\n', default=None, metavar="")
    create_stage.add_argument('-input_file_type', help="Custom file extension to get from previous stage.\nThere are default expected file types for each program.\nIf you want to use a different file type, you can specify it here.\nI.E: -input_file_type .txt .cfg\n\n", default=None, metavar="", nargs='+')
    create_stage.add_argument('-specific_file_input', help='If you want specific files from the preivous, designate it here.\nMust be a file you know is output by the previous stage.\n The file will be relative to the /output directory.\n\n', default=None, metavar="", nargs='+')
    create_stage.add_argument('-input_subdir', help='If you want the input of this stage to be in a subdirectory of the previous stage, specify it here.\nCan be multiple, designate each folder with spaces\n\n', default=None, metavar="", nargs='+')

    #Run a pipeline
    run_pipeline = subparsers.add_parser('run', help='Run a pipeline', parents=[pipeline_parent_parser])

    #Print pipeline information
    print_pipeline = subparsers.add_parser('p', help='Print pipeline information', parents=[pipeline_parent_parser])

    #Format subparser
    print_pipeline = subparsers.add_parser('                 ', help="  ")

    return parser
