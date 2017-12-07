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

def convert_xlsx(path):
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', 'csv', path])

def move_file(path):
    new_path = path.replace('/Users/thebarn/challenge-dga/data', '/Users/thebarn/challenge-dga/formated_data')
    mkdir_on_path(new_path)
    new_path = new_path.replace('.xlsx', '.xlsx.csv')
    path = path.replace('.xlsx', '.csv')
    file_name = path.split('/')[-1]
    subprocess.run(['mv', './' + file_name, new_path])

def get_files_from_dir(path_to_dir):
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(path_to_output)
        elif isfile(path_to_output) and path_to_output.split('.')[-1] == 'xlsx':
            new_path = path_to_output.replace('/Users/thebarn/challenge-dga/data', '/Users/thebarn/challenge-dga/formated_data') + '.csv'
            if not isfile(new_path):
                print('copying: '+ path_to_output)
                convert_xlsx(path_to_output)
                move_file(path_to_output)

def main():
    get_files_from_dir('/Users/thebarn/challenge-dga/data/Archives coalition')

if __name__ == '__main__':
    main()
