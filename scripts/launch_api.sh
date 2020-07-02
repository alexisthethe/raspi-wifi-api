#!/bin/bash

script_folder="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
project_folder="$(dirname $script_folder)"

source $project_folder/env/bin/activate
$project_folder/serve_api.sh
