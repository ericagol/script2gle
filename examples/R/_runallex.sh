#!/bin/bash
source ~/.bash_profile # so that knows what "s2g" is
for file in $( ls *.[rR]); do
    printf "\nFILE: $file..."
    s2g $file -tex
done
