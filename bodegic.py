import subprocess

def run_dockerfile(path, repo):
    """
    Run the Docker container and capture the output
    @param path: the path to the folder containing the Git repository
    @param repo: the Git repository

    @return: the output of the Docker container
    """
 
    result = subprocess.run(["docker", "run", "--rm", "-v" , f'{path}:/bodegic/repos' , "bodegic", f'repos/{repo}', "--csv"], capture_output=True, text=True)

    output_lines = result.stdout.split('\n') 
    output_lines.pop(0) # headers are not needed

    parsed = []
    for line in output_lines:
        if line and line not in ['','\n']:
            line = line.split(',')
            print(line)
            line[1] = line[1].strip()
            if line[1] == 'Unknown':
                continue
            elif line[1] == 'Human':
                parsed.append((line[0], False))
            elif line[1] == 'Bot':
                parsed.append((line[0], True))
            else:
                print("parsing error: ", line)

    return parsed

def bodegic(repos_path, repo):
    return run_dockerfile(repos_path, repo)