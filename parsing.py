from classes import Argument, Program

def parse_program_file(text):
    config = {
        'arguments': [],
        'extra_params': ''
    }
    current_arg = None
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('arguments:'):
            current_arg = 'arguments'
        elif current_arg == 'arguments' and line.startswith('-'):
            symbol, description = line.split(': ', 1)
            config['arguments'].append(Argument(symbol.strip(), description.strip()))
        elif line:
            if ':' in line:
                key, value = line.split(': ', 1)
                key = key.strip()
                value = value.strip()
                if key in ['input_file_types', 'output_file_types', 'pipeline_stages']:
                    config[key] = value.split(', ')
                else:
                    config[key] = value

    #Error Checking values
    if not config.get('name'):
        raise ValueError("Name is a required field. Please provide a name in the configuration file.")
    if not config.get('exec'):
        raise ValueError("Executable name is a required field. Please provide an executable name in the configuration file.")
    if not config.get('input_identifier'):
        raise ValueError("Input identifier is a required field. Please provide an input identifier in the configuration file.")
    if not config.get('output_identifier'):
        raise ValueError("Output identifier is a required field. Please provide an output identifier in the configuration file.")
    if not config.get('input_file_types'):
        raise ValueError("Input file types is a required field. Please provide an input file type in the configuration file.")
    if not config.get('output_file_types'):
        raise ValueError("Output file types is a required field. Please provide an output file type in the configuration file.")

    # Creating the Program instance with parsed data
    return Program(
        name=config.get('name', ''),
        exec_name=config.get('exec', ''),
        input_file_types=config.get('input_file_types', []),
        output_file_types=config.get('output_file_types', []),
        input_cl_identfier=config.get('input_identifier', ''),
        output_cl_identifier=config.get('output_identifier', ''),
        arguments=config.get('arguments', []),
        pipeline_stages=config.get('pipeline_stages', [])
    )