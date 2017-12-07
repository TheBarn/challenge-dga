from os import listdir
from os.path import join, isdir, isfile
import subprocess
from timeout import timeout

def mkdir_on_path(path):
    directories = [ d for d in path.split('/') if d][:-1]
    path_to_dir = '/'
    for dir in directories:
        path_to_dir = join(path_to_dir, dir)
        if not isdir(path_to_dir):
            subprocess.run(['mkdir', path_to_dir])

@timeout(30)
def convert_to_pdf(path):
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', 'pdf', path])

def move_file(old_path, new_path):
    mkdir_on_path(new_path)
    subprocess.run(['mv', old_path, new_path])

def get_files_from_dir(count, path_to_dir):
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            count = get_files_from_dir(count, path_to_output)
        elif isfile(path_to_output):
            count += 1
            ext = path_to_output.split('.')[-1]
            if ext == 'docx' or ext == 'doc' or ext=='ppt' or ext=='pptx' or ext=='xlsx':
                new_path = path_to_output.replace('/Users/thebarn/challenge-dga/data', '/Users/thebarn/challenge-dga/website/django_site/challenge/static/challenge').replace('.'+ext, '.pdf')
                if not isfile(new_path):
                    print('Processing: file #'+str(count))
                    try:
                        print(path_to_output)
                        convert_to_pdf(path_to_output)
                        this_path = './' + path_to_output.split('/')[-1].replace('.'+ext,'.pdf')
                        print(this_path)
                        print(new_path)
                        move_file(this_path, new_path)
                    except Exception as e:
                        print(e)
    return count

def main():
    count = 0
    get_files_from_dir(count, '/Users/thebarn/challenge-dga/data/Archives coalition')

if __name__ == '__main__':
    main()
