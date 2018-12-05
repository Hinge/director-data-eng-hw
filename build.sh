#!/bin/sh

#####################################################################
################ This script executes python scripts ################
#####################################################################


# main_dir=$HOME/'hw_dir'

# echo "Creating main folder....\n"
# # Create a folder in Home folder
# if [ ! -d $main_dir ]; then
# 	mkdir -p $main_dir
# fi

# echo "Cloning git repo...."
# git clone https://github.com/saggusher/director-data-eng-hw $main_dir

echo "Installing required Python libraries...\n"
pip install -r requirements.txt





