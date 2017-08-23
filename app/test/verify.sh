#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
PYTHONPATH=$PWD/app python -m unittest discover -s app/test/fetch
