# Author: Moses Gameli
# Description: Python script to automate versioning of Flutter apps

import argparse
from pathlib import Path
import ruamel.yaml

parser = argparse.ArgumentParser('Automatically update flutter app version')
parser.add_argument('--major', '-m', action='store_true',
                    help='bump flutter app to next major version (default: False)')
parser.add_argument('--minor', '-n', action='store_true',
                    help='bump flutter app to next minor version (default: False)')
parser.add_argument('--patch', '-p', action='store_true',
                    help='bump flutter app to next patch version (default: False)')

args = parser.parse_args()

pubspec_path = Path('pubspec.yaml')

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True


try:
    if(pubspec_path.is_file()):

        with open('pubspec.yaml', 'r') as input_file:
            pubspec = yaml.load(input_file)

        version = pubspec["version"]
        version_arr = version.split(".")

        new_major = int(version_arr[0])
        new_minor = int(version_arr[1])
        new_patch = int(version_arr[2].split("+")[0])
        new_build = int(version_arr[2].split("+")[1]) + 1

        if(args.patch is True):
            new_patch += 1

        if(args.minor is True):
            new_patch = 0
            new_minor += 1

        if(args.major is True):
            new_patch = 0
            new_minor = 0
            new_major += 1

        new_version = f'{new_major}.{new_minor}.{new_patch}+{new_build}'
        pubspec['version'] = new_version

        with open('pubspec.yaml', 'wb') as output_file:
            yaml.dump(pubspec, output_file)
            print(f'v{new_version}')

    else:
        raise Exception('Pubspec file not found')

except Exception as exc:
    print(f'Could not execute python script: {exc}')
