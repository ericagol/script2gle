#!/bin/bash
source ~/.bash_profile # so that knows what "s2g" is
for file in $( ls *.jl); do
    printf "\nFILE: $file...\n"
    s2g $file -tex
done

# Rem: expect side scripts to fail (normal, they might call objects that haven't been defined)