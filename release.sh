#!/bin/bash
pytest
if [ $? -eq 0 ]; then
    if [ -z "$1" ]; then
        echo "Please specify a version number"
        exit 1
    fi
    #echo "version='"$1"'" > yglu/__init__.py
    git add .
    git commit -m"Release $1"
    git push
    git tag "v$1"
    git push --tags
fi
