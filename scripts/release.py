#!/usr/bin/env python3

import datetime
import os
import shutil
import sys
from tempfile import mkstemp


def get_version():
    fh = open('VERSION', 'r')
    try:
        return fh.read().strip()
    finally:
        fh.close()


def update_changelog(version, msg):
    today = datetime.date.today()
    wfh = open('CHANGELOG.rst.tmp', 'w')
    try:
        lines_count = 0
        for line in open('CHANGELOG.rst', 'r'):
            lines_count += 1
            if lines_count == 4:
                wfh.write(f'Version {version} (on {today: %b %d %Y})\n')
                wfh.write('-------------------------------\n')
                wfh.write(f'* {msg}')
                wfh.write('\n\n')
            wfh.write(line)
    finally:
        wfh.close()
        shutil.move('CHANGELOG.rst.tmp', 'CHANGELOG.rst')


def main():
    version = get_version()
    print(f'New version is {version}')
    print('Creating archives ...')
    os.system('python3 setup.py sdist bdist_wheel')
    print('Updating the changelog ...')
    changelog_msg = input("Please enter a changelog message: ")
    if changelog_msg == "":
        print("ERROR: You didn't enter a changelog message!")
        sys.exit(-1)

    update_changelog(version, changelog_msg)
    print('Uploading the new release...')
    os.system('twine upload dist/*')

if __name__ == '__main__':
    main()
