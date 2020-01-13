#!/bin/bash
pytest
if [ $? -eq 0 ]; then
    echo "version='"$1"'" > yglu/__init__.py
    git add .
    git commit -m"Release $1"
    git push
    git tag v$1
    git push --tags
fi