import subprocess
import os
import sys

def listFiles(dir):
	result = []
	for item in os.listdir(dir):
		if item.endswith('.atsp'):
			result.append(os.path.join(dir, item))
	return result


def runProgram(test_file, alg = "non"):
	print "alg:" + alg
	print test_file
	p = subprocess.Popen(['../Debug/atsp.exe', test_file, alg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return out.split("\n")

def best_vs_start(file, alg = "steepest"):
	results = open('../best-known-results/results.txt', 'r')
	best = dict()
	for line in results:
		d = line.split(":")
		best[d[0].strip()] = int(d[1].strip())
	file_name = '../data-atsp/' + file
	exact_filename=file[file.rfind('/')+1:file.rfind('.')]
	result = runProgram(file_name, alg)
	f = open('first_vs_best/' + exact_filename + '.txt', 'a+')
	for line in result:
		splitted = line.split(" ")
		if splitted[0] == "out":
			value = splitted[1] + " value ";
			efficiency =  splitted[1] + " efficiency ";
			efficiency2 = splitted[1] + " efficiency2 ";
			
			for i in range(2, len(splitted)-1):
				value = value + splitted[i] + " "
				efficiency = efficiency + str(float(splitted[i])-best[exact_filename]) + " " 
				efficiency2 = efficiency2 + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " "
				
			value += " \n"
			efficiency += " \n"
			efficiency2 += " \n"
			f.write(value)
			f.write(efficiency)
			f.write(efficiency2)
			#file + " " + splitted[1] + " " + splitted[2] + " " + splitted[3] + " " + str(int(splitted[3])-best[exact_filename]) + " " + str((float(splitted[3])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[4] + " " + str(int(splitted[4])-best[exact_filename]) + " " + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[5] +"\n"
	f.close()

def default():
	results = open('../best-known-results/results.txt', 'r')
	best = dict()
	for line in results:
		d = line.split(":")
		best[d[0].strip()] = int(d[1].strip())
	
	for file in listFiles('../data-atsp/'):
		print file
		exact_filename=file[file.rfind('/')+1:file.rfind('.')]
		#print exact_filename
		result = runProgram(file)
		#print result 
		for line in result:
			if len(line) < 4:
				continue
			print line
			splitted = line.split(" ")
			f = open('res/' + splitted[0] + '.txt', 'a')
			f.write(file + " " + splitted[1] + " " + splitted[2] + " " + splitted[3] + " " + str(int(splitted[3])-best[exact_filename]) + " " + str((float(splitted[3])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[4] + " " + str(float(splitted[4])-float(best[exact_filename])) + " " + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[5] + " " + splitted[6] + " " + splitted[7] + " " + splitted[8] + " \n")
			#file + " " + splitted[1] + " " + splitted[2] + " " + splitted[3] + " " + str(int(splitted[3])-best[exact_filename]) + " " + str((float(splitted[3])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[4] + " " + str(int(splitted[4])-best[exact_filename]) + " " + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[5] +"\n"
			f.close()
	
			
if len(sys.argv) >= 2 and sys.argv[1] == "2":
	
	alg = sys.argv[3]
	file = sys.argv[2]
	print "alg: " + alg
	best_vs_start(file, alg)
else:
	default()
	