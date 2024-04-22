import subprocess

def run_dockerfile(token, repo, verbose):
    """
    Run the Docker container and capture the output
    @param token: the GitHub token
    @param repo: the GitHub repository

    @return: the output of the Docker container
    """
    # "docker", "run", "--rm", 
    result = subprocess.run(["bodegha", repo, "--key", token, "--csv"], capture_output=True, text=True)

    if verbose:
        print("Bodegha:", result.stdout)

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

def bodegha(token, repo, verbose):
    return run_dockerfile(token, repo, verbose)