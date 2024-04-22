
from dotenv import load_dotenv
from datetime import datetime
from bodegha import bodegha
from rabbit import rabbit
from bodegic import bodegic
from bin import bin, get_users
import pandas as pd
import argparse
import sys
import os

# import warnings
# warnings.filterwarnings("ignore")

def extract_github_users(file_path, token, verbose):
    users = get_users(file_path, token, verbose)
    names = set()
    for user in users:
        if user[2] is not None:
            names.add(user[2])
    
    return list(names)

def env_parser():
    load_dotenv()
    token = os.getenv("GH_TOKEN")
    repos_path = os.getenv("REPOS_DIR")
    repo = 'sparklemotion/nokogiri'
    file = './SiGHBoD/example.csv'


def weighted_average(boolean_list):
    if len(boolean_list) != 4:
        raise ValueError("Input list must contain exactly four booleans")

    # Bin = 0.45, Bodegha = 0.20, Bodegic = 0.20, Rabbit = 0.25
    weights = [0.35, 0.20, 0.20, 0.25]

    sum = 0
    total = 0
    for index, boolean in enumerate(boolean_list):
        if boolean is not None:
            total += weights[index]

        if boolean:
            sum += weights[index]

    return sum >= total / 2

def main(args):
    verbose = args.verbose
    token = args.key
    repo = args.remote
    repos_path = args.local
    file = args.users

    if verbose:
        start_time = datetime.now()
        print("Starting at:", start_time)

    result_bodegha = bodegha(token, repo, verbose)
    if verbose:
        bodegha_execution_time = datetime.now() - start_time
        print("Bodegha execution time:", bodegha_execution_time)

    result_bodegic = bodegic(repos_path, repo, verbose)
    if verbose:
        bodegic_execution_time = datetime.now() - bodegha_execution_time
        print("Bodegic execution time:", bodegha_execution_time)

    # get the list of users from the csv file
    if verbose:
        print("Extracting GitHub users from the file:", file)
    names = extract_github_users(file, token, verbose)

    result_bin = bin(names)
    if verbose:
        bin_execution_time = datetime.now() - bodegic_execution_time
        print("Bin execution time:", bin_execution_time)

    result_rabbit = rabbit(token, names, verbose)
    if verbose:
        rabbit_execution_time = datetime.now() - bin_execution_time
        print("Rabbit execution time:", rabbit_execution_time)

        execution_time = datetime.now() - start_time
        print("Execution time:", execution_time)

        print('---')
        print("Bodegha:", result_bodegha)
        print('---')
        print("Bodegic:", result_bodegic)
        print('---')
        print("Bin:", result_bin)
        print('---')
        print("Rabbit:", result_rabbit)
        print('---')

    df = pd.DataFrame(result_bin, columns =['Name', 'Email', 'Login', 'Bin'])
    df['Bodegha'] = None
    df['Bodegic'] = None
    df['Rabbit'] = None
    df['Bot'] = None

    for element in result_bodegha:
        for index, row in df.iterrows():
            row_list = row.to_list()
            if element[0] in row_list:
                df.at[index, 'Bodegha'] = element[1]

    for element in result_bodegic:
        for index, row in df.iterrows():
            row_list = row.to_list()
            if element[0] in row_list:
                df.at[index, 'Bodegic'] = element[1]

    for element in result_rabbit:
        for index, row in df.iterrows():
            row_list = row.to_list()
            if element[0] in row_list:
                df.at[index, 'Rabbit'] = element[1]

    for index, row in df.iterrows():
        results = [row['Bin'], row['Bodegha'], row['Bodegic'], row['Rabbit']]
        # compute weighted average of the results
        average = weighted_average(results)
        df.at[index, 'Bot'] = average

    if args.json:
        return (df.reset_index().to_json(orient='records'))
    elif args.csv:
        return (df.to_csv())
    else:
        return (df)
        


def arg_parser():
    parser = argparse.ArgumentParser(description='SiGHBoD - Bot detection in Github')
    parser.add_argument('--remote', required=True, help='Name of a repository on GitHub ("owner/repo")')
    parser.add_argument('--local', required=True, help='Path to a local Git repository')
    parser.add_argument('--users', required=True, help='Path to a csv file containing a list of users to check (name,email)')
    parser.add_argument(
        '--verbose', action="store_true", required=False, default=False,
        help='To have verbose output result')
    parser.add_argument(
        '--key', metavar='TOKEN', required=True, type=str, default='',
        help='GitHub APIv4 key to download comments from GitHub APIs')
    
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--text', action='store_true', help='Print results as text')
    group2.add_argument('--csv', action='store_true', help='Print results as csv')
    group2.add_argument('--json', action='store_true', help='Print results as json')

    return parser.parse_args()


def cli():
    args = arg_parser()
    if args.key == '' or len(args.key) < 35:
        sys.exit('A GitHub personal access token is required to start the process. Please provide a valid token.')
    print(main(args))

if __name__ == '__main__':
    """     
    file_path = './SiGHBoD/example.csv'
    users = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            users.append((row[0], row[1], None))
    """    
    cli()