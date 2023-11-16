from Scripts.selenium_script import update_file
import subprocess
import os
import json

API_KEY = input('Enter the API key if it require update: *press enter to skip* \n')
if API_KEY:
    #write the API_KEY to the file API_KEY.json
    with open('Scripts/Env Data/API_KEY.json', 'w') as f:
        API_KEY_json = {"API_KEY": API_KEY}
        json.dump(API_KEY_json, f)

output_name = input('Enter the path and name of output  file: eg. path/to/filename.json \n')

#reading the API_KEY from the json file
with open('Scripts/Env Data/API_KEY.json') as f:
    key = json.load(f)['API_KEY']
API_KEY = key

# Run the Scrpay spider "gears" to get the data from the API
subprocess.run(['scrapy', 'crawl', 'gears', '-O', 'data/curr_run.json'])

update_file(f'data/{output_name}')

input('The code finished successfully, press Enter to exit....')