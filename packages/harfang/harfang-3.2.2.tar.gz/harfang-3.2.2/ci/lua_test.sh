#!/usr/bin/env bash

module_dir=$1
script_dir=$2

module_file=`(find $module_dir \( -iname "harfang.dll" -o -iname "harfang.so" \) -print &) | head -n 1`
module_file=$(realpath $module_file)
if [ ! -f "$module_file" ]; then
    echo "missing harfang lua module" 1>&2
    exit 1
fi

test_script="$script_dir/dummy.lua"
if [ ! -f "$test_script" ]; then
    echo "missing test script" 1>&2
    exit 1
fi

work_dir=$(mktemp -d)

cp -f "$module_dir"/* "$work_dir"
cp -f "$test_script" "$work_dir"

pushd $work_dir

LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:.
export LD_LIBRARY_PATH
./lua dummy.lua
ret=$?
if [ ! $? -eq 0 ]; then
    echo "test script failed" 1>&2
fi

popd
rm -rf $work_dir

if [ ! $ret -eq 0 ]; then
    exit $ret
fi