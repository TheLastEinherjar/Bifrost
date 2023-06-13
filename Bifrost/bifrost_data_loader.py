def load_txt_lines(path) :
    with open(path, 'r') as f:
        lines = [line.strip() for line in f]
    return lines
