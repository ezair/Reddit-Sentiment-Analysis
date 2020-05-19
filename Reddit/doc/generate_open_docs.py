#!/usr/bin/env python

"""
Author: Eric Zair
File: run.py
Created on: 10/28/2019
Description:    Build doxygen documentation and then open the index webpage.
"""
from os.path import exists, join
from os import getcwd, chdir
import subprocess
import webbrowser


def main():
    """
    Build doxygen documention and then open the index webpage.

    Raises:
        SystemExit: If doxyfile cannot be found.
        SystemExit: if index.html cannot be found.
    """

    doxyfile_location = 'Doxyfile'
    index_html_location = 'html/index.html'

    chdir('doc/')

    if not exists(doxyfile_location):
        raise SystemExit('Error, missing {}'.format(doxyfile_location))

    subprocess.call(['doxygen', 'Doxyfile'])

    if not exists(index_html_location):
        raise SystemExit(f'Error, missing {index_html_location}.')

    webbrowser.open(join(getcwd(), index_html_location))


if __name__ == '__main__':
    main()
