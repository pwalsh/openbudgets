import os
import sys
import platform
import subprocess

STRAP_ROOT = os.path.abspath(
    os.path.dirname(__file__)
)

DEPENDS_ROOT = os.path.abspath(
    os.path.join(
        STRAP_ROOT,
        'depends',
    )
)

PLATFORM_DEPENDS = os.path.abspath(
    os.path.join(
        DEPENDS_ROOT,
        'platform.py',
    )
)

PYTHON_DEPENDS = os.path.abspath(
    os.path.join(
        DEPENDS_ROOT,
        'python.py',
    )
)

NODE_DEPENDS = os.path.abspath(
    os.path.join(
        DEPENDS_ROOT,
        'node.js',
    )
)

# what platform + python are we on?
system, release, this_python = platform.system(), platform.release(), platform.python_version()

sys.stdout = 'Operating system: ' + system + ' ' + release
sys.stdout = 'Python: '

# verify node is installed
node = subprocess.call(['which', 'node'])

if node == 0:
    sys.stdout = 'You have node installed'
else:
    sys.stdout ='You need to install node'

# verify global node dependencies
node_depends = subprocess.call(['node', NODE_DEPENDS])

if node_depends == 0:
    sys.stdout ='You have all the required node dependencies'
else:
    sys.stdout = 'You need to install node dependencies'
