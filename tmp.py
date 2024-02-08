from bodegha import bodegha
from bodegic import bodegic
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

token = os.getenv("GH_TOKEN")
repos_path = os.getenv("REPOS_DIR")
repo = 'sparklemotion/nokogiri'
file = './SiGHBoD/example.csv'

result_bodegha = bodegha(token, repo)
dataset = pd.read_csv('./example.csv')
dataset['Bodegha'] = None

for element in result_bodegha:
    for index, row in dataset.iterrows():
        row_list = row.to_list()
        if element[0] in row_list:
            dataset.at[index, 'Bodegha'] = element[1]

