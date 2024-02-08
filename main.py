from bodegha import bodegha
from bodegic import bodegic
from bin import bin
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GH_TOKEN")
repos_path = os.getenv("REPOS_DIR")
repo = 'sparklemotion/nokogiri'
file = './SiGHBoD/example.csv'

result_bodegha = bodegha(token, repo)
result_bodegic = bodegic(repos_path, repo)
result_bin = bin(token, file)

print("Bodegha:", result_bodegha)
print('---')
print("Bodegic:", result_bodegic)
print('---')
print("Bin:", result_bin)