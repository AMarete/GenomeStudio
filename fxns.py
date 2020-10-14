#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gzip
import io
from platform import python_version


def error(message):
    print("ERROR: " + message)
    raise SystemExit


def py_version():
    if not float(python_version()[0:3]) >= 3.5:
        return error("Python version not satisfied, install Python V3.5 or later\n")


def msg():
    return '''Andrew Marete (C) 2016
    This function converts an Illumina GenomeStudio Report to Plink Ped/Map format
    This version supports conversion of Forward/Reverse strand i.e. `Allele1 - Forward` and  `Allele2 - Forward`

    basic usage : 
    ./report2plink -f [FinalReport.txt] -s [SNPMap.txt] -o [prefix]
    '''


# Function to read various index formats
def open_by_suffix(filename):
    """io allows to return with universal new lines 'U'"""
    if filename.endswith('.gz'):
        return io.TextIOWrapper(io.BufferedReader(gzip.open(filename)))
    else:
        return open(filename)
