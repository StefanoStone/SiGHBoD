from bodegha import bodegha
from bodegic import bodegic
from bin import bin
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

token = os.getenv("GH_TOKEN")
repos_path = os.getenv("REPOS_DIR")
repo = 'sparklemotion/nokogiri'
file = './SiGHBoD/example.csv'

start_time = datetime.now()
print("Starting at:", start_time)

result_bodegha = bodegha(token, repo)
bodegha_execution_time = datetime.now() - start_time
print("Bodegha execution time:", bodegha_execution_time)

result_bodegic = bodegic(repos_path, repo)
bodegic_execution_time = datetime.now() - bodegha_execution_time
print("Bodegic execution time:", bodegha_execution_time)

result_bin = bin(token, file)
bin_execution_time = datetime.now() - bodegic_execution_time
print("Bin execution time:", bin_execution_time)

execution_time = datetime.now() - start_time
print("Execution time:", execution_time)

print('---')
print("Bodegha:", result_bodegha)
print('---')
print("Bodegic:", result_bodegic)
print('---')
print("Bin:", result_bin)

df = pd.DataFrame(result_bin, columns =['Name', 'Email', 'Login', 'Bin'])
df['Bodegha'] = None
df['Bodegic'] = None

df.to_csv('example.csv', index=False)