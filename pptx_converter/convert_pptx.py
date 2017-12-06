from os import listdir
from os.path import join, isdir, isfile
import subprocess

def mkdir_on_path(path):
    directories = [ d for d in path.split('/') if d][:-1]
    path_to_dir = '/'
    for dir in directories:
        path_to_dir = join(path_to_dir, dir)
        if not isdir(path_to_dir):
            subprocess.run(['mkdir', path_to_dir])

def convert_pptx(path):
    if path.split('.')[-1] != 'pptx':
        return
    new_path = path.replace('/Users/thebarn/challenge-dga/data', '/Users/thebarn/challenge-dga/formated_data') + '.txt'
    mkdir_on_path(new_path)
    print('converting: ' + new_path)
    with open(new_path, 'w') as output_file:
        subprocess.call(['/Users/thebarn/challenge-dga/scripts/pptx_converter/pptx2txt.sh', '-v', path], stdout=output_file)


def get_files_from_dir(path_to_dir):
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(path_to_output)
        elif isfile(path_to_output):
            convert_pptx(path_to_output)

def main():
    get_files_from_dir('/Users/thebarn/challenge-dga/data/Archives coalition')

if __name__ == '__main__':
    main()
