#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gzip
import io
from platform import python_version


class MyCols:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def error(message):
    print(f"{MyCols.FAIL}Error:\t{message}{MyCols.ENDC}")
    raise SystemExit


def py_version():
    if float(python_version()[0:3]) < 3.5:
        return error("Python version not satisfied, install Python V3.5 or later\n")


def msg():
    return '''Andrew Marete (C) 2016
    This program converts an Illumina GenomeStudio Report to Plink Ped/Map format
    This version supports conversion of Forward/Reverse strand i.e. `Allele1 - Forward` and  `Allele2 - Forward`

    basic usage : 
    report2plink -r [FinalReport.txt] -m [SNPMap.txt] -p [prefix]
    '''


# Function to read various index formats
def open_by_suffix(filename):
    """io allows to return with universal new lines 'U'"""
    if filename.endswith('.gz'):
        return io.TextIOWrapper(io.BufferedReader(gzip.open(filename)))
    else:
        return open(filename)
