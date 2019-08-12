#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: getNodeFromNWK.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2018-11-05 22:04:21
Last modified: 2018-11-05 22:04:21
'''

import sys
from Bio import Phylo

nwkFile = sys.argv[1]
tree = Phylo.read(nwkFile, "newick")
for leaf in tree.get_terminals():
    print leaf.name
