#!/bin/bash

# clear
function clean
{
    rm -rf dist gplt.egg-info build
}

# build
function build 
{
    python setup.py sdist 
}

# help
function showHelp
{
    echo "Usage:"
    echo $0 build
    echo $0 test
    echo $0 pypi
    echo $0 install
    echo $0 clean
}

# check if input
[[ $# -lt 1 ]] && showHelp && exit

inp=$1
# for testpypi
if [[ "$inp" == "test" ]]; then
    clean && build
    twine upload --repository testpypi dist/*
# for pypi
elif [[ "$inp" == "pypi" ]]; then
    clean && build
    twine upload --repository pypi dist/*
# only build
elif [[ "$inp" == "build" ]]; then
    clean && build
# native install
elif [[ "$inp" == "install" ]]; then
    clean
    python setup.py build && python setup.py install
# only clean old file
elif [[ "$inp" == "clean" ]]; then
    clean
# show help
else
    showHelp
fi

