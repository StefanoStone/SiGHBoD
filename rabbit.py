import subprocess
import re

def run_dockerfile(token, names, verbose):
    """
    Run the Docker container and capture the output
    @param token: the GitHub token
    @param names: the List of GitHub users (.txt file)

    @return: the output of the Docker container
    """    

    output_lines = []
    for name in names:
        result = subprocess.run(['rabbit', name, '--key', token], capture_output=True, text=True)
        lines = result.stdout.split('\n') 
        lines.pop(0) # headers are not needed
        output_lines.extend(lines)

    parsed = []
    print(output_lines)
    for line in output_lines:
        if line == '':
            continue
        elif line == '\n':
            continue
        elif not line:
            continue
        else:
            regex = re.compile(r'(.+)\s+([A-z0-9]+)\s+(.+)') # regex to parse the output
            line = list(regex.findall(line)[0])
            line[1] = line[1].strip()
            
            # if the confidence is less than 0.5, ignore
            # if float(line[2]) <= 0.5:
            #     continue

            if line[1] == 'unknown':
                continue
            elif line[1] == 'human':
                parsed.append((line[0], False))
            elif line[1] == 'bot':
                parsed.append((line[0], True))
            else:
                if verbose:
                    print("parsing error: ", line)

    return parsed

def rabbit(token, repo, verbose):
    return run_dockerfile(token, repo, verbose)