from os import listdir
from os.path import join, isdir, isfile
import langdetect as ld

def get_files_from_dir(path_to_dir, output_f):
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(path_to_output, output_f)
        elif isfile(path_to_output):
            file_name = path_to_output.split('/')[-1]
            with open(path_to_output, 'r', encoding='utf-8', errors='surrogateescape') as f:
                content = f.read()
                try:
                    lang = ld.detect(content)
                except ld.lang_detect_exception.LangDetectException:
                    lang='NAN'
            print(file_name)
            output_f.write('"'+ path_to_output + '","' + file_name + '",' + lang + "\n")

def main():
    with open('languages.csv', 'w', encoding='utf-8') as output_f:
        output_f.write("file_path,file_name,language\n")
        get_files_from_dir('C:/Users/Ambroise Prevel/Dropbox/HEC/Cours/Digital/DGA/formated_data/Archives coalition', output_f)

if __name__ == '__main__':
    main()
