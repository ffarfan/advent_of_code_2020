def load_input_from_file(input_filename):
    input_data = []
    with open(input_filename, 'r') as f_input:
        input_data = [line.strip() for line in f_input.readlines()]

    return input_data
