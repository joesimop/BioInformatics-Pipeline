import os
from parsing import parse_program_file

def get_program_by_name(program_name):
    if os.path.exists('supported_programs'):
        programs = os.listdir('programs')
        for program in programs:
            if program.name == program_name:

                try:
                    return parse_program_file(program)
                except ValueError as e:
                    print(f"Error parsing {program}: {e}")
                    continue
    else:
        raise ValueError("Cannot find supported_programs directory")