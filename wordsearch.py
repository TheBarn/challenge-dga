import subprocess
import os
#import os.path import splitext

def		wordsearch(directory, word, dict):
	
	f = subprocess.check_output(["grep -rnw '"+directory+"' -e '"+word+"'"], shell=True)
	i = 0
	for line in str(f).split('\n'):
		s = line.split(':')[0]
		if (s == ""):
			return
		if s in dict:
			dict[s] += 1
		else:
			dict[s] = 1

def		display_dict(dict):
	for key in dict:
		print(str(key)+" -> "+str(dict[key]))

def main():
	dict = {}
	wordsearch(".", "COPD", dict)
	display_dict(dict)

if __name__ == '__main__':
	main()
