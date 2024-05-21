import sys
import os
import argparse
from byop_interface import get_parser
from directory_creation import *
from parsing import *
from pipeline import Pipeline
from help import *
from environment_setup import user_root

def main(command_line=None):

    parser = get_parser()
    args = parser.parse_args(command_line)

    if args.command == 'create_pipeline':
        create_pipeline(args.pipeline_name)
    elif args.command == 'create_stage':
        create_stage(args.pipeline_name, args.stage_name, args.program_name, args.data_source)
    elif args.command == 'list_programs':
        list_available_programs()
    elif args.command == "run":
         pipeline = Pipeline(args.pipeline_name)
         pipeline.load()
         pipeline.execute()
    elif args.command == 'p':
        pipeline = Pipeline(args.pipeline_name)
        pipeline.load()
        pipeline.print()
    else:
        print("Invalid command")
        sys.exit(1)

if __name__ == "__main__":
    main()