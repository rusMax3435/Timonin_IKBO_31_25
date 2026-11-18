#!/bin/bash
if [ $# -eq 0 ]; then
    python3 src/main.py -p "cargo" -r "https://github.com/rust-lang/cargo" \
    -o "graph.png" -v "latest"
else
    python3 src/main.py "$@"
fi