#!/bin/sh
printf "Please enter the binning change between original and new. e.g. if your original tomogram was 3x binning and the new one is unbinned, the change is 3, if you go from 3x to 2x then enter 2\n\n"
read bin
printf "Please enter the full name of your tomogram rec file (including .rec) that the model is based on. If in a different directory, please include the full path\n\n"
read -e old_tomo
printf "Please enter the name of your new tomogram rec file. If in a different directory, please include the full path\n\n"
read -e new_tomo
printf "Please enter the name of your model file. If in a different directory, please include the full path\n\n"
read -e model_file

printf "Running command: imodtrans -i $old_tomo $model_file temp.mod \n\n"
printf "Running command: imodtrans -i $new_tomo temp.mod bin${bin}_$model_file \n\n"
printf "Deleting temp.mod"
imodtrans -i $old_tomo $model_file temp.mod
imodtrans -i $new_tomo temp.mod bin${bin}_$model_file
rm temp.mod



for j in *.csv; do
	printf "Applying binning scale changes to $j into new file bin${bin}_$j\n"
	awk -v bin="$bin" -F "," -v OFS=, '{$11=$11*bin; $12=$12*bin; $13=$13*bin;print $0}' $j > bin${bin}_$j
	sed -i 's/NA,0,0,0,NA/NA,xOffset,yOffset,zOffset,NA/g' bin${bin}_$j
done

while true; do
    read -p "Do you want to rescale more model files?" yn
    case $yn in
        [Yy]* ) printf "\n\nPlease enter the full name of your tomogram rec file (including .rec) that the model is based on. If in a different directory, please include the full path\n\n";read -e old_tomo;printf "Please enter the name of your new tomogram rec file. If in a different directory, please include the full path\n\n";read -e new_tomo;printf "Please enter the name of your model file. If in a different directory, please include the full path\n\n";read -e model_file;imodtrans -i $old_tomo $model_file temp.mod;imodtrans -i $new_tomo temp.mod bin${bin}_$model_file;rm temp.mod;printf "Running command: imodtrans -i $old_tomo $model_file temp.mod \n\n";printf "Running command: imodtrans -i $new_tomo temp.mod bin${bin}_$model_file \n\n";printf "Deleting temp.mod";;

        [Nn]* ) printf "Exiting script\n";exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

