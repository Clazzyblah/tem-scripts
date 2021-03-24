#!/usr/bin/python3
import os, sys, re, argparse
import numpy as np

parser = argparse.ArgumentParser(description='A script for applying symmetry to MOTL files extracted from a PEET .epe file. The rotated angles are then re-inserted into the epe and prm files.\nThis script should be run from the directory your .epe/prm files are located in.')
parser.add_argument('epe_in', metavar='input.epe', type=str,
                    help='input .epe file')
parser.add_argument('sym_y', metavar='symmetry_value', type=int,
                    help='symmetry around the Y-axis you wish to apply, e.g. for five-fold (C5) symmetry enter 5')
parser.add_argument('epe_out', metavar='output.epe', type=str,
                    help='output .epe file')
args = parser.parse_args()

# variables
epe_in = sys.argv[1]
sym_y = sys.argv[2]
epe_out = sys.argv[3]
old_rootname = epe_in[:-4]
rootname = epe_out[:-4]
prm_in = old_rootname + '.prm'
prm_out = rootname + '.prm'

# variables for epe
index = 0
line_motl = 'Peet.InitMotlFile.'
line_motllast = 'Peet.InitMotlFile.Last'
line_tiltstart = 'Peet.TiltRange.Start.'
line_tiltend = 'Peet.TiltRange.End.'
line_tiltlast = 'Peet.TiltRangeMultiAxesFile.Last'
line_tiltrangeend = 'Peet.TiltRange.End.Last'
line_tiltrangestart = 'Peet.TiltRange.Start.Last'
last = '.Last'
rootstr = 'RootName='
first = '.First'
csv = 'csv'
tomos = []
tilts_start = []
tilts_end = []

#################
### functions ###
#################

# function that will filter out the motl lines that contain the csv files
def table_create_from_file(line_type,table):
	filename = open(epe_in, "r")
	index = 0
	for line in filename:
		if line_type in line:
#			if not last in line:
#				if not first in line:
			linesplit = line.rsplit('=', 1)
			table.append(linesplit[1])
		index += 1
	filename.close()

#########################
######### PRM ###########
#########################
print('Loading prm file...')
file = open(prm_in, "r")
test = file.read()
#array_read('fnVolume', 'fnModParticle:', ',', array4)
recfiles = re.compile('fnVolume = {(.*)}(.*)fnModParticle:', re.DOTALL).search(test)
recfiles = recfiles.group(1)
recfiles = recfiles.replace('\n', '')
recfiles = recfiles.replace(' ', '')
array4 = recfiles.split(',')
array4 = [ x[1:-1] for x in array4 ]	
	
modfiles = re.compile('fnModParticle = {(.*)}(.*)initMOTL:', re.DOTALL).search(test)
modfiles = modfiles.group(1)
modfiles = modfiles.replace('\n', '')
modfiles = modfiles.replace(' ', '')
array = modfiles.split(',')
array = [ x[1:-1] for x in array ]	
	
motlfiles = re.compile('initMOTL = {(.*)}(.*)tiltRange:', re.DOTALL).search(test)
motlfiles = motlfiles.group(1)
motlfiles = motlfiles.replace('\n', '')
motlfiles = motlfiles.replace(' ', '')
array2 = motlfiles.split(',')
array2 = [ x[1:-5] for x in array2 ]	

tiltrange = re.compile('tiltRange = {\[(.*)\]}(.*)dPhi:', re.DOTALL).search(test)
tiltrange = tiltrange.group(1)
tiltrange = tiltrange.replace('\n', '')
tiltrange = tiltrange.replace(' ', '')
array3 = tiltrange.split('],[')


total = len(array2)
#sym_y = 5
j = 1
i = 0
#motl_new = []
#print(total)		
while i < total:
	while j < int(sym_y):
		angle = float(j) * 360 / int(sym_y)
		newrec = array4[i]
		newmotl =  array2[i] + '_' + str(angle)# + '.csv'
		newmod =  array[i]
		newtilt = array3[i]
		print('modifyMotiveList ' + array2[i] + '.csv ' + newmotl + '.csv' + ' 0,' + str(angle) + ',0')
		os.system('modifyMotiveList ' + array2[i] + '.csv ' + newmotl + '.csv' + ' 0,' + str(angle) + ',0')
		array4.append(newrec)
		array2.append(newmotl)
		array.append(newmod)
		array3.append(newtilt)
		j += 1
	i += 1
	j = 1
	
#print(str(array4) + '\n\n')
#print(str(array) + '\n\n')
#print(str(array2) + '\n\n')
#print(str(array3) + '\n\n')







# adds the new data to a new output prm file

with open(prm_out, "w") as o:
	o.write('fnVolume = {\'')
	for line in array4:
		o.write("".join(line) + "','")
	o.write('}\n\nfnModParticle = {\'')
	for line in array:
		o.write("".join(line) + "','")
	o.write('}\n\ninitMOTL = {\'')
	for line in array2:
		o.write("".join(line + '.csv') + "','")
	o.write('}\n\ntiltRange = {[\'')
	for line in array3:
		o.write("".join(line) + "'],['")
	o.write(']}\n\n')

# retrieves all information excluding the existing motl, tomogram, mod file and tilt angle information so we can add it back to the end
# this assumes that the line below (cutoff) appears directly after the tilt information!
cutoff = '# dPhi: dPhi: angular search range around the particle Y axis.'
cutoff_found = False
with open(prm_in) as in_file:
    with open(prm_out, 'a') as out_file:
        for line in in_file:
            if not cutoff_found:
                if line.strip() == cutoff:
                    cutoff_found = True
            else:
                out_file.write(line)


# lazy way to strip out incorrect characters
os.system('sed -i "s/,\'}/}/g" ' + prm_out)
os.system('sed -i "s/,\[\'\]//g" ' + prm_out)
os.system('sed -i "s/\']/]/g" ' + prm_out)
os.system('sed -i "s/\[\'/[/g" ' + prm_out)

print('Finished editing prm file!\n\nLoading epe file...')



#########################
######### EPE ###########
#########################
# generate variables for the motl files, tilt start angles and tilt end angles
table_create_from_file(csv,tomos)

table_create_from_file(line_tiltstart,tilts_start)

table_create_from_file(line_tiltend,tilts_end)

# delete ".csv\n" from each line
tomos = [ x[:-5] for x in tomos ]	

# modify motive lists iteratively through the list of MOTL files found from the .epe file

# variables
i = 0
j = 1
tomos_new = []
angle = float(j) * 360 / int(sym_y)
total = len(tomos)
peet_lines = int(total * sym_y)
#print('Number of tomograms is ' + str(total) + ', total number of lines when this script is finished will be ' + str(peet_lines))
while i < total:
	while j < int(sym_y):
		angle = float(j) * 360 / int(sym_y)
		newmotl =  tomos[i] + '_' + str(angle) + '.csv'
#		print('modifyMotiveList ' + tomos[i] + '.csv ' + newmotl + ' 0,' + str(angle) + ',0')
		tomos_new.append(newmotl)
		j += 1
	i += 1
	j = 1
	
# edit the .epe file to include new MOTL files	

total_motls = len(tomos_new) + len(tomos) - 1

# read in original epe file in full
file1 = open(epe_in, "r")
alllines = file1.readlines()
file1.close()

# create new epe file
file2 = open(epe_out, "w")

for line in alllines:
	if not last in line:
		file2.write(line)
line_motllast_new = "Peet.InitMotlFile.Last=" + str(total_motls) + '\n'
line_tiltlast_new = "Peet.TiltRangeMultiAxesFile.Last=" + str(total_motls) + '\n'
line_tiltrangeend_new = 'Peet.TiltRange.End.Last=' + str(total_motls) + '\n'
line_tiltrangestart_new = 'Peet.TiltRange.Start.Last=' + str(total_motls) + '\n'
file2.write(str(line_motllast_new))
file2.write(str(line_tiltlast_new))
file2.write(str(line_tiltrangeend_new))
file2.write(str(line_tiltrangestart_new))
i = total
j = 0

while i < total_motls + 1:
#	print(str(i))
	line_motl_new = str(line_motl) + str(i) + '=' + str(tomos_new[j]) + '\n'
	file2.write(line_motl_new)
#	print(line_motl_new)
	i += 1
	j += 1
#file2.close()

i = total
j = 1
k = 0
while i < total_motls + 1:
	while j < int(sym_y):
#		print(str(i))
		tilts_start_new = str(line_tiltstart) + str(i) + '=' + str(tilts_start[k])
		tilts_end_new = str(line_tiltend) + str(i) + '=' + str(tilts_end[k])
		file2.write(tilts_start_new)
		file2.write(tilts_end_new)
#		print(tilts_start_new)
		j += 1
		i += 1
	j = 1
	k += 1

	
file2.close()
os.system('sed -i "s/=' + old_rootname + '/=' + rootname + '/g" ' + epe_out)
print('\n\nAll done! Load your new etomo file by running etomo ' + rootname + '.epe')
