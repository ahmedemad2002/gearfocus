from Scripts.selenium_script import update_file
import subprocess
import os
import json

input_path = input('Enter the path of input file which contains the listings: eg. path/to/filename.json \n you can skip to use curr_run.json as the default input\n')

output_path = input('Enter the path and name of output  file: eg. path/to/filename.json \n')

command = ['scrapy', 'crawl', 'sold', '-O', f'data/{output_path}']
if input_path:
    command.extend(['-a', f'input_path=data/{input_path}'])

subprocess.run(command)

input('The code finished successfully, press Enter to exit....')