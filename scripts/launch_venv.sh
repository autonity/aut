#!/bin/bash -x

##
## Launch the aut virtual environment that pipx installed (for testing and debugging).
## When finished, type `deactivate`

PIPX_HOME=$(pipx environment | grep PIPX_HOME | head -n 1 | sed -r 's/^PIPX\_HOME=//')
AUTCLI_VENV=$PIPX_HOME/venvs/aut

source $AUTCLI_VENV/bin/activate > /dev/null
