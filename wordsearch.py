#!/usr/bin/python

import subprocess
import os


def		wordsearch(word):
	directory = '.'
	dic = {}
	f = subprocess.check_output(["grep -ri '"+directory+"' -e '"+word+"'"], shell=True)
	i = 0
	for line in str(f).split('\n'):
		s = line.split(':')[0]
		if (s == ""):
			break
		if s in dic:
			dic[s] += 1
		else:
			dic[s] = 1
	return dic

def		display_dict(dict):
	for key in dict:
		print(str(key)+" -> "+str(dict[key]))


def main():
	d = wordsearch("yo")
	display_dict(d)

if __name__ == '__main__':
	main()
