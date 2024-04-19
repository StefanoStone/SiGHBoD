import subprocess

def run_dockerfile(token, names, verbose):
    """
    Run the Docker container and capture the output
    @param token: the GitHub token
    @param names: the List of GitHub users (.txt file)

    @return: the output of the Docker container
    """
    # "docker", "run", "--rm", 
    result = subprocess.run(["rabbit", names, "--key", token], capture_output=True, text=True)
    print(result.stdout)

    output_lines = result.stdout.split('\n') 
    output_lines.pop(0) # headers are not needed

    parsed = []
    for line in output_lines:
        if line and line not in ['','\n']:
            line = line.split(',')
            line[1] = line[1].strip()
            if line[1] == 'Unknown':
                continue
            elif line[1] == 'Human':
                parsed.append((line[0], False))
            elif line[1] == 'Bot':
                parsed.append((line[0], True))
            else:
                if verbose:
                    print("parsing error: ", line)

    return parsed

def rabbit(token, repo, verbose):
    return run_dockerfile(token, repo, verbose)