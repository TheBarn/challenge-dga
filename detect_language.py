from os import listdir
from os.path import join, isdir, isfile
from langdetect import detect

def get_files_from_dir(total, path_to_dir):
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(total, path_to_output)
        elif isfile(path_to_output):
            file_name = path_to_output.split('/')[-1]
            with open(path_to_output, 'r') as f:
                content = f.read()
                lang = detect(content)
            print(file_name + ' : ' + lang)

def main():
    get_files_from_dir(total, '/Users/thebarn/challenge-dga/formated_data/Archives coalition')

if __name__ == '__main__':
    main()
