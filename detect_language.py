from os import listdir
from os.path import join, isdir, isfile
import langdetect as ld

def get_files_from_dir(path_to_dir):
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(path_to_output)
        elif isfile(path_to_output):
            file_name = path_to_output.split('/')[-1]
            with open(path_to_output, 'r', encoding='utf-8', errors='surrogateescape') as f:
                content = f.read()
                lang = ld.detect(content)
            print(file_name + ' : ' + lang)

def main():
    get_files_from_dir('C:/Users/Ambroise Prevel/Dropbox/HEC/Cours/Digital/DGA/formated_data/Archives coalition')

if __name__ == '__main__':
    main()
