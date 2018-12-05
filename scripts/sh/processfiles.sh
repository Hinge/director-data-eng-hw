#!/bin/sh

#####################################################################
################ This script executes python scripts ################
#####################################################################

if [ "$#" -ne 4 ]; then
	echo "Not enough parameters. script.sh workon_home venv pyscript files_to_process"
	exit 1
fi

source `which virtualenvwrapper.sh`

workonhome=$1
hw_project=$2
pythonscriptfile=$3
files_to_process=$4

# echo $workonhome
# echo $hw_project
# echo $pythonscriptfile

#Switch to the project
workon $hw_project

#Set dates
rundate=`date +%Y%m%d`
starttime=`date +%Y%m%d_%H:%M:%S`
SECONDS=0


#Scripts location
# projectname=$1
# githubproject=$2
# jobcategory=$3


projectdir=$workonhome/$hw_project
scriptsdir=$projectdir/scripts/python
sqldir=$projectdir/scripts/sql
logdir=$projectdir/logs
echo 'log directory' $logdir

#Create logs directory, if doesn't exist
if [ ! -d $logdir ]; then
	mkdir -p $logdir
fi

# echo 'projectdirectory' $projectdir
# echo 'scritsdir' $scriptsdir

#Set files
scriptfile=$scriptsdir/$pythonscriptfile
logfile=$logdir/$(echo $pythonscriptfile| cut -d'.' -f 1)_$starttime

echo 'scriptsfile' $scriptfile

#Execute script
echo '-----' > $logfile
echo 'Start time of the script: '$starttime >> $logfile
echo '-----' >> $logfile

python $scriptfile $sqldir $files_to_process >> $logfile

endtime=`date +%Y%m%d_%H:%M:%S`

echo 'End time of the script: '$endtime >> $logfile
echo '-----' >> $logfile
echo '' >> $logfile

duration=$SECONDS

echo "Total duration of the script is: $(($duration / 60)) minutes and $(($duration % 60)) seconds">> $logfile

deactivate