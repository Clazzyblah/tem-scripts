
for i in *.mrc; do
	sample=`ls $i|grep -o "^[^_]*_\?[^_]*" ` 			# detects everything before the second underscore i.e. in "PilN_8sec_11_001[0.00]-295578-0001" it will extract "PilN_8sec"
	mkdir -v "$sample"
	mv $i ./"$sample"
	cd "$sample"
	rename s/"$sample"_// *.mrc 					# removes everything before second underscore now that they are in a folder with this name
	for j in *.mrc; do
		dataset=`ls $j|cut -d_ -f1 `  				# detects everything before the first underscore i.e. in "11_001[0.00]-295578-0001" it will extract "11"
		mkdir -v "$dataset"
		mv $j ./"$dataset"
		cd "$dataset"
		rename s/"$dataset"_// *.mrc 				# removes dataset number
		rename 's/_002\[\-2.00]/_031\[\-2.00]/' *.mrc		# for every file, it now checks the -2,-4,-6, etc. tilts and renames them in reverse order, i.e. image 002 (-2.00) becomes
		rename 's/_003\[\-4.00]/_030\[\-4.00]/' *.mrc		# image 031 (-2.00) and image 031 (-60.00) becomes image 002 (-60.00). This DOES NOT WORK if the dataset doesn't go
		rename 's/_004\[\-6.00]/_029\[\-6.00]/' *.mrc		# up to -60 degrees!
		rename 's/_005\[\-8.00]/_028\[\-8.00]/' *.mrc
		rename 's/_006\[\-10.00]/_027\[\-10.00]/' *.mrc
		rename 's/_007\[\-12.00]/_026\[\-12.00]/' *.mrc
		rename 's/_008\[\-14.00]/_025\[\-14.00]/' *.mrc
		rename 's/_009\[\-16.00]/_024\[\-16.00]/' *.mrc
		rename 's/_010\[\-18.00]/_023\[\-18.00]/' *.mrc
		rename 's/_011\[\-20.00]/_022\[\-20.00]/' *.mrc
		rename 's/_012\[\-22.00]/_021\[\-22.00]/' *.mrc
		rename 's/_013\[\-24.00]/_020\[\-24.00]/' *.mrc
		rename 's/_014\[\-26.00]/_019\[\-26.00]/' *.mrc
		rename 's/_015\[\-28.00]/_018\[\-28.00]/' *.mrc
		rename 's/_016\[\-30.00]/_017\[\-30.00]/' *.mrc
		rename 's/_017\[\-32.00]/_016\[\-32.00]/' *.mrc
		rename 's/_018\[\-34.00]/_015\[\-34.00]/' *.mrc
		rename 's/_019\[\-36.00]/_014\[\-36.00]/' *.mrc
		rename 's/_020\[\-38.00]/_013\[\-38.00]/' *.mrc
		rename 's/_021\[\-40.00]/_012\[\-40.00]/' *.mrc
		rename 's/_022\[\-42.00]/_011\[\-42.00]/' *.mrc
		rename 's/_023\[\-44.00]/_010\[\-44.00]/' *.mrc
		rename 's/_024\[\-46.00]/_009\[\-46.00]/' *.mrc
		rename 's/_025\[\-48.00]/_008\[\-48.00]/' *.mrc
		rename 's/_026\[\-50.00]/_007\[\-50.00]/' *.mrc
		rename 's/_027\[\-52.00]/_006\[\-52.00]/' *.mrc
		rename 's/_028\[\-54.00]/_005\[\-54.00]/' *.mrc
		rename 's/_029\[\-56.00]/_004\[\-56.00]/' *.mrc
		rename 's/_030\[\-58.00]/_003\[\-58.00]/' *.mrc
		rename 's/_031\[\-60.00]/_002\[\-60.00]/' *.mrc

		cd .. 							# back to sample folder
		cd .. 							# back to root folder
	done
done
