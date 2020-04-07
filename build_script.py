import os
import re
import shutil
import sys

sys.path.insert(0, os.path.abspath('src'))

from src.__init__ import __version__


def success(tip):
    print('SUCCESS - ' + str(tip))


def error(info):
    print('\n' + info)
    print('CANCELLED AND REVERSED.')
    print('ABORTED.\n')
    exit()


def remove_pycache_info(filename):
    return re.sub('\.cpython-[0-9]+', '', filename)


if os.path.isdir('dist/mdcl-' + str(__version__)):
    error('AN EXPORT OF VERSION ' + str(__version__) + ' ALREADY EXISTS.')
elif os.path.isdir('dist/mdcl'):
    shutil.rmtree('dist/mdcl')
    success('AN INCOMPLETE EXPORT WAS FOUND BUT SAFELY DELETED.')
elif os.path.isfile('dist/mdcl-' + str(__version__)):
    error('THERE IS A FILE IN THE WAY OF PATH '
        'dist/mdcl-' + str(__version__) + ' WHICH MUST BE REMOVED.')
elif os.path.isfile('dist/mdcl'):
    error('THERE IS A FILE IN THE WAY OF PATH '
        'dist/mdcl WHICH MUST BE REMOVED.')

os.system('pyinstaller src/mdcl.py')
success('SOURCE HAS BEEN BUILT')

os.remove('dist/mdcl/mdcl.exe.manifest')
success('REMOVED MANIFEST')

shutil.rmtree('build')
success('REMOVED TEMP BUILD FOLDER')

os.remove('mdcl.spec')
success('REMOVED TEMP SPEC FILE')

if not os.path.isfile('src/__pcd__.py'):
    error('src/__pcd__.py POST-COMPILED-DATA FILE NOT FOUND.')
shutil.copy2('src/__pcd__.py', 'dist/mdcl/__pcd__.py')
success('COPIED POST-COMPILED-DATA FILE (src/__pcd__.py).')

try:
    os.rename('dist/mdcl', 'dist/mdcl-' + str(__version__))
    success('EXPORT FOLDER RENAMED')
except FileExistsError:
    shutil.rmtree('dist/mdcl')
    error('AN EXPORT OF VERSION ' + str(__version__) + ' ALREADY EXISTS.')

print('\nSUCCESS.')
print('Version ' + str(__version__) + ' has been exported and is waiting in '
    '/dist/mdcl-' + str(__version__) + '/\n')
