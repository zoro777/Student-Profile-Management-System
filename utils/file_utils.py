import os

def read_file(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def write_file(filename, lines):
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))

def update_line(filename, match_key, new_line):
    lines = read_file(filename)
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(match_key + ','):
            lines[i] = new_line
            updated = True
            break
    if not updated:
        lines.append(new_line)
    write_file(filename, lines)

def delete_line(filename, match_key):
    lines = [line for line in read_file(filename) if not line.startswith(match_key + ',')]
    write_file(filename, lines)
