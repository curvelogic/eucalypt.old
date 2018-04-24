#!/usr/bin/env python3
"""
eut.py - A test harness for Eucalypt implementations.
"""

import subprocess
import sys
import re
from enum import Enum
from pathlib import (Path)

test_directory = Path("test")
output_directory = Path(".build/output")

def prepare_directories():
    if not test_directory.is_dir():
        raise RuntimeError("Cannot locate test directory")
    output_directory.mkdir(parents = True, exist_ok = True)

class Result(Enum):
    SUCCESS = 1
    IGNORE = 2
    FAIL = 3

class Test:

    RE = re.compile(r"(x?)(\d+)_(.*?).eu")

    def __init__(self, filepath):
        self.filepath = filepath
        (ignore, id, name) = Test.RE.fullmatch(filepath.name).groups()
        self.ignore = ignore == 'x'
        self.id = id
        self.name = name
        self.outfile = output_directory / filepath.with_suffix(".out").name
        self.errfile = output_directory / filepath.with_suffix(".err").name

    def failed(self):
        return self.result is Result.FAIL

def run_test(test):

    """ Run shebang eucalypt files """

    print(test.id, test.name, sep='\t', end='\t')

    if test.ignore:

        test.result = Result.IGNORE
        print("ignore")

    else:

        with open(test.outfile, "wb") as out:
            with open(test.errfile, "wb") as err:
                proc = subprocess.run([test.filepath],
                                      shell=True,
                                      stdout=out,
                                      stderr=err)

        if proc.returncode == 0:
            print("pass")
            test.proc = proc
            test.result = Result.SUCCESS
        else:
            print("FAIL\n")
            with open(test.errfile, "r") as err:
                print("error output:\n---")
                sys.stdout.write(err.read())
                print("---\n")
            test.proc = proc
            test.result = Result.FAIL

    return test

def find_tests():
    return [Test(p) for p in sorted(test_directory.glob("*.eu"))]

def main(args):
    prepare_directories()
    results = [run_test(t) for t in find_tests()]
    if any(r.failed() for r in results):
        print("FAIL")
        return 1
    else:
        return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
