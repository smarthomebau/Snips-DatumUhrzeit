#/usr/bin/env bash
set -e

VENV=venv

if [ -d "$VENV" ]
then
    rm -r $VENV
fi

if [ ! -d "$VENV" ]
then

    PYTHON=`which python3`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate

pip install -r requirements.txt
