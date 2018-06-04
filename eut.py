#!/usr/bin/env python3
"""
eut.py - A test harness for Eucalypt implementations.
"""

import subprocess
import sys
import re
import timeit
import argparse
from enum import Enum
from pathlib import (Path)

test_directory = Path("test")
output_directory = Path(".build/output")

def prepare_directories():
    if not test_directory.is_dir():
        raise RuntimeError("Cannot locate test directory")

class Result(Enum):
    SUCCESS = 1
    IGNORE = 2
    FAIL = 3

class Test:

    """ A test that by default passes with a zero return code """

    RE = re.compile(r"(x?)(\d+)_(.*?).eu")

    def __init__(self, filepath):
        self.filepath = filepath
        (ignore, id, name) = Test.RE.fullmatch(filepath.name).groups()
        self.ignore = ignore == 'x'
        self.id = id
        self.name = name
        self.outfile = output_directory / filepath.relative_to(test_directory).with_suffix(".out")
        self.outfile.parent.mkdir(parents = True, exist_ok = True)
        self.errfile = output_directory / filepath.relative_to(test_directory).with_suffix(".err")
        self.errfile.parent.mkdir(parents = True, exist_ok = True)
        self.eu_args = ["eu", "-B", filepath]

    def failed(self):
        return self.result is Result.FAIL

    def check(self):
        return self.proc.returncode == 0

    def execute(self):
        with open(self.outfile, "wb") as out:
            with open(self.errfile, "wb") as err:
                proc = subprocess.run(self.eu_args,
                                      stdout=out,
                                      stderr=err)
        self.proc = proc


    def run(self):

        """ Run eucalypt files """

        print(self.id, self.name, sep=' ', end=' ')

        if self.ignore:

            self.result = Result.IGNORE
            print("ignore")

        else:
            self.execute()

            if self.check():
                print("pass")
                self.result = Result.SUCCESS
            else:
                print("FAIL\n")
                with open(self.errfile, "r") as err:
                    print("error output:\n---")
                    sys.stdout.write(err.read())
                    print("---\n")
                self.result = Result.FAIL

        return self

    def bench(self, repeats):

        """ Time repeated runs. """

        if self.ignore:
            return

        print(self.id, self.name, sep=' ', end=' ')

        self.sec = timeit.timeit(self.execute, number=repeats)

        print(f"{self.sec}s")

        return self


class ErrorTest(Test):

    """A test that expects a non-zero returncode"""

    def __init__(self, filepath):
        super().__init__(filepath)
        self.id = "E" + self.id

    def check(self):
        return self.proc.returncode > 0

def find_simple_tests():
    return [Test(p) for p in sorted(test_directory.glob("*.eu"))]

def find_error_tests():
    return [ErrorTest(p) for p in sorted(test_directory.glob("errors/*.eu"))]

parser = argparse.ArgumentParser("Eucalypt test harness")
parser.add_argument("-b", "--bench", action='store_true', default=False)
parser.add_argument("-n", "--repeats", action='store', type=int, default=100)

def main():
    opts = parser.parse_args()
    prepare_directories()
    tests = find_simple_tests() + find_error_tests()

    if opts.bench:
        print(f"Timing tests with {opts.repeats} repeats.")
        results = [t.bench(opts.repeats) for t in tests]
    else:
        results = [t.run() for t in tests]
        if any(r.failed() for r in results):
            print("FAIL")
            return 1
        else:
            return 0

if __name__ == '__main__':
    main()
