#!/bin/sh

# Creates folders for all samples that exist within the folder
	sample=`ls|grep -o "^[^_]*_\?[^_]*" |sort -u` 			# detects everything before the second underscore i.e. in "PilN_8sec_11_001[0.00]-295578-0001" it will extract "PilN_8sec" and displays once for each dataset
	echo $sample
	mkdir -p $sample


maxnum=$(ls|grep -m 1 \\\[2.00 |cut -d_ -f4 | cut -d[ -f1 ) 		# find the first file at 2.00 deg, i.e. everything before this file is negative or zero and defines as variable "maxnum"


# Loop that renames all the files in the datasets
for k in *.mrc; do

	oldnum=`ls $k|cut -d_ -f4 | cut -d[ -f1`			# find the first number defined before the angles
	newnum=`expr $maxnum - $oldnum - 1`				# determine what the old number will be replaced by
	addnum=`expr $oldnum - 1`					# this fixes the gap between 0 and +2 deg

	if [ "$newnum" -gt "0" ]; then
		if [ "$newnum" -lt "10" ]; then	
			rename s/"$oldnum"/00"$newnum"/ $k		# replace the old number with the new number where the number is less than 10 (appends 2 zeros)
		else	
			rename s/"$oldnum"/0"$newnum"/ $k		# replace the old number with the new number for other numbers (appends 1 zero)
		fi
	else
		rename s/"$oldnum"/"$addnum"/ $k			# renumbers positive angles so there is no gap
	fi


done

for i in *.mrc; do
	samplename=` ls $i|grep -o "^[^_]*_\?[^_]*" `			# same as sample function above but specific to the loop
	mv $i ./"$samplename"
	rename s/"$samplename"_// ./"$samplename"/$i 					# removes everything before second underscore now that they are in a folder with this name

done
