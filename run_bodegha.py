import subprocess

def run_dockerfile(token, repo):
    # Run the Docker container and capture the output
    result = subprocess.run(["docker", "run", "--rm", "bodegha", repo, "--key", token, "--csv"], capture_output=True, text=True)

    output_lines = result.stdout.split('\n') 
    output_lines.pop(0) # headers are not needed

    parsed_output = [tuple(line.split(',')) for line in output_lines if line]
    parsed_output = [t for t in parsed_output if t[1] != 'Unknown']
    parsed_output = [(t[0], False) if t[1] in ['Human'] else t for t in parsed_output]
    parsed_output = [(t[0], False) if t[1] in ['Bot'] else t for t in parsed_output] 

    return parsed_output

# export the function
def bodegha(token, repo):
    return run_dockerfile(token, repo)


