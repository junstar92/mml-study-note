import os
import glob
import re
import argparse
from tqdm import tqdm

DOCS_DIR = './docs'

def fix_escape_char(line, revert):
    if revert is False:
        processed_text = re.sub('\\\\', '\\\\\\\\', line)
        processed_text = re.sub('align\\*', 'align\\\\*', processed_text)
        processed_text = re.sub('(?<=[^\\$])\\$([\\w0-9\\\\ ,=!<>\\+_\\-\\{\\}\\|\\(\\)\\^\\.]+)\\$', '\\\\\\\\(\\1\\\\\\\\)', processed_text)
    
    return processed_text

def file_process(file_path, revert = False):
    if os.path.isfile(file_path) is False:
        return

    i = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            line = fix_escape_char(line, revert)
            f.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--revert', help='Revert fixed escape character for origin markdown docs', default=False, action='store_true')
    args = parser.parse_args()

    docs_dir_list = os.listdir(DOCS_DIR)
    
    for dir in docs_dir_list:
        if os.path.isdir(os.path.join(DOCS_DIR, dir)) is True:
            file_list = glob.glob(os.path.join(DOCS_DIR, f'{dir}/*.md'))
            
            for file in tqdm(file_list, desc=dir):
                file_process(file, args.revert)

    pass