#!/bin/bash

# Helper script to build this game natively for your platform
# For now only supports linux

dir_check() {
    if [ ! -d "$1" ]; then
        echo "$1 doesnt exist or isnt directory, abort" >&2
        exit 1
    fi
}

file_check() {
    if [ ! -f "$1" ]; then
        echo "$1 doesnt exist or isnt file, abort" >&2
        exit 1
    fi
}

dep_check() {
    if ! command -v $1 &>/dev/null; then
        echo "Couldnt find $1. Please install it and try again"
        exit 1
    fi
}

game_name="WSG"
build_dir="./build/$game_name/linux"
cache_dir="./.temp"
assets_dir="./Assets"
icon_file="./icon.png"
WGF_dir="./WGF"
venv=".venv/bin/activate"

dir_check $WGF_dir
dir_check $assets_dir
file_check $icon_file
file_check $venv
dep_check pip

# #TODO: safety checks that will shutdown further execution on failure of any line
source $venv
pip install -r requirements.txt
pip install -r dev-requirements.txt

dep_check pyinstaller

pyinstaller Game/run.py --onefile --noconsole --clean --workpath $cache_dir --distpath $build_dir --name $game_name
cp -r ./Assets $build_dir/Assets
cp ./icon.png $build_dir

echo "Successfully finished building $game_name!"
