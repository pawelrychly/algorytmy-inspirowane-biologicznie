import subprocess
import os

def listFiles(dir):
	result = []
	for item in os.listdir(dir):
		if item.endswith('.atsp'):
			result.append(os.path.join(dir, item))
	return result


def runProgram(test_file):
	p = subprocess.Popen(['../Debug/atsp.exe', test_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return out.split("\n")



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
		f.write(file + " " + splitted[1] + " " + splitted[2] + " " + splitted[3] + " " + str(int(splitted[3])-best[exact_filename]) + " " + str((float(splitted[3])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[4] + " " + str(float(splitted[4])-float(best[exact_filename])) + " " + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[5] + " " + splitted[6] +" \n")
		#file + " " + splitted[1] + " " + splitted[2] + " " + splitted[3] + " " + str(int(splitted[3])-best[exact_filename]) + " " + str((float(splitted[3])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[4] + " " + str(int(splitted[4])-best[exact_filename]) + " " + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[5] +"\n"
		f.close()	