#!/usr/bin/env bash

# It's more convenient to test the generated wheel using bash scripts because
# venv and pip are not really designed to be used like standard Python modules.
# Especially venv and its activation scripts.

python_bin=$1
whl_dir=$2
script_dir=$3

if [ ! -x "$python_bin" ]; then
    echo "missing python binary" 1>&2
    exit 1
fi

whl_file=`(find $whl_dir -iname "harfang-*.whl" -print &) | head -n 1`
whl_file=$(realpath $whl_file)
if [ ! -f "$whl_file" ]; then
    echo "missing wheel file" 1>&2
    exit 1
fi

test_script="$script_dir/dummy.py"
if [ ! -f "$test_script" ]; then
    echo "missing test script" 1>&2
    exit 1
fi

work_dir=$(mktemp -d)

$python_bin -m venv $work_dir --copies --clear
cp -f "$test_script" "$work_dir"

pushd $work_dir
source ./bin/activate

python -m pip install $whl_file --upgrade
ret=$?
if [ ! $? -eq 0 ]; then
    echo "wheel installation failed" 1>&2
else
    python dummy.py
    ret=$?
    if [ ! $? -eq 0 ]; then
        echo "test script failed" 1>&2
    fi
fi

deactivate

popd
rm -rf $work_dir

if [ ! $ret -eq 0 ]; then
    exit $ret
fi