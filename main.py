from bodegha import bodegha
from bin import bin
# from bim import bim
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GH_TOKEN")
repo = 'sparklemotion/nokogiri'
file = './SiGHBoD/example.csv'

result_array = bodegha(token, repo)
result_names = bin(token, file)
print(result_array, result_names)