#!/bin/bash

script_folder="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_folder="$(dirname $script_folder)"

source $project_folder/api/env/bin/activate
cd $project_folder/api
. serve_api.sh
