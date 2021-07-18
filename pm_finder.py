#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# -- importing important libraries --
import sys
from numpy import loadtxt
from os import walk

# -- adding directories to path --
sys.path.append('./classes')

# -- importing my super classes --
from multiple_epochs import multiple_epochs_cl


# -- creating list of files --
spots_path = "./examples/CepA/"

files_in_dir = next( walk( spots_path ), ( None, None, [] ) ) [2]
for i in range(len(files_in_dir)):
    files_in_dir[i] = spots_path + files_in_dir[i]

# -- creating multiple epochs --
dw = multiple_epochs_cl(files_in_dir)
for i in dw.epochs:
    print("Date:", i.time_string, "Code:", i.project_code, "PI:", i.project_pi)