import subprocess
import re

def run_dockerfile(token, names, verbose):
    """
    Run the Docker container and capture the output
    @param token: the GitHub token
    @param names: the List of GitHub users (.txt file)

    @return: the output of the Docker container
    """

    command = names
    command.insert(0, 'rabbit')
    command.append('--key')
    command.append(token)

    # "docker", "run", "--rm", 
    result = subprocess.run(command, capture_output=True, text=True)
    output_lines = result.stdout.split('\n') 
    output_lines.pop(0) # headers are not needed

    parsed = []
    for line in output_lines:
        if line and line not in ['','\n']:
            
            regex = re.compile(r'([A-z0-9]+)\s+([A-z0-9]+)\s+(.+)')
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