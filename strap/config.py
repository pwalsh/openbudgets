import os

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
