#!/bin/sh


# Setting up env variables
# export WORKON_HOME=$HOME/.virtualenvs
# export WORKON_HOME=$1
# export PROJECT_HOME=$HOME/hg_hw
# export PROJECT_HOME=$WORKON_HOME/hg_hw
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source `which virtualenvwrapper.sh`

if [ "$#" -ne 2 ]; then
	echo "Not enough parameters. Script expects WORKON_home virtualenv_project"
	exit 1
fi

workonhome=$1
hw_project=$2
echo "Script location" `dirname "$0"`
# echo "project is..." $hw_project
# echo "workon home "$workonhome


declare -a virtualenvs=(`lsvirtualenv -b`)
# echo 'installed env....'$virtualenvs

# Create virtualenv if it doesn't exist
if [[ ! " ${virtualenvs[@]} " =~ " ${hw_project} " ]]; then
    echo "Env doesn't exists...Creating new virtual env\n"
    mkvirtualenv $hw_project
fi

echo "Copying scripts to venv....\n"
if [ -d $workonhome/$hw_project/scripts ]; then
	rm -rf $workonhome/$hw_project/scripts
fi
cp -R scripts $workonhome/$hw_project/scripts

echo "Copying requirements file...\n"
cp requirements.txt $workonhome/$hw_project/requirements.txt

workon $hw_project

cd $workonhome/$hw_project/

echo "Installing required Python libraries...\n"
pip install -r requirements.txt

cd $workonhome/$hw_project/scripts/sh
chmod a+x *.sh

deactivate





