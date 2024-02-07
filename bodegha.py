import subprocess

def run_dockerfile(token, repo):
    """
    Run the Docker container and capture the output
    @param token: the GitHub token
    @param repo: the GitHub repository

    @return: the output of the Docker container
    """
    result = subprocess.run(["docker", "run", "--rm", "bodegha", repo, "--key", token, "--csv"], capture_output=True, text=True)

    output_lines = result.stdout.split('\n') 
    output_lines.pop(0) # headers are not needed

    parsed = []
    for line in output_lines:
        if line:
            line = line.split(',')
            line[1] = line[1].strip()
            if line[1] == 'Unknown':
                continue
            if line[1] == 'Human':
                parsed.append((line[0], False))
            if line[1] == 'Bot':
                parsed.append((line[0], True))
            else:
                print("parsing error: ", line)

    return parsed