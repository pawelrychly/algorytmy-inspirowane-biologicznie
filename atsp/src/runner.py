import subprocess
import os

def listFiles(dir):
	result = []
	for item in os.listdir(dir):
		if item.endswith('.atsp'):
			result.append(os.path.join(dir, item))
	return result


def runProgram(test_file):
	p = subprocess.Popen(['./a.out', test_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	return out.split("\n")

for file in listFiles('../data-atsp/'):
	print file
	result = runProgram(file)
	#print result 
	for line in result:
		if len(line) < 4:
			continue
		print line
		splitted = line.split(" ")
		f = open(splitted[0], 'a')
		f.write(file + " " + splitted[1] + "\n")
		f.close()	