import argparse

def get_parser():
    
    
    parser = argparse.ArgumentParser(prog='byop',
                                     description='A tool to build and run your own bioinformatics pipelines')
    

    subparsers = parser.add_subparsers(dest='command', help='idk just print this to know when it prints')

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
    create_stage = subparsers.add_parser('create_stage', help='Create a new stage in a pipeline', parents=[pipeline_parent_parser, stage_parent_parser])
    create_stage.add_argument('program_name', help='Name of the program to run in the stage')
    create_stage.add_argument('--data_source', help='Name of the data source to use in the stage.\n\n It can be a stage in this pipeline or a directory/file in your data folder', default=None)

    #Run a pipeline
    run_pipeline = subparsers.add_parser('run', help='Run a pipeline')

    return parser
