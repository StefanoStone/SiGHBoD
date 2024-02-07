from run_bodegha import bodegha
from name_based_detection import bin
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GH_TOKEN")
repo = 'sparklemotion/nokogiri'
file = './SiGHBoD/example.csv'

result_array = bodegha(token, repo)
result_names = bin(token, file)
print(result_array, result_names)