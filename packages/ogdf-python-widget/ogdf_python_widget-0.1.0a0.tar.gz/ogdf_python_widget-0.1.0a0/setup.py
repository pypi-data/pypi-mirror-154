from __future__ import print_function
from setuptools import setup, find_packages
import os
from os.path import join as pjoin
from distutils import log

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)


here = os.path.dirname(os.path.abspath(__file__))

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

name = 'ogdf_python_widget'
LONG_DESCRIPTION = 'A Custom Jupyter Widget Library'

# Get ogdf_python_widget version
version = get_version(pjoin(name, '_version.py'))

js_dir = pjoin(here, 'js')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(js_dir, 'dist', 'index.js'),
]

data_files_spec = [
    ('share/jupyter/nbextensions/ogdf-python-widget', 'ogdf_python_widget/nbextension', '*.*'),
    ('share/jupyter/labextensions/ogdf-python-widget', 'ogdf_python_widget/labextension', '**'),
    ('share/jupyter/labextensions/ogdf-python-widget', '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'ogdf-python-widget.json'),
]

cmdclass = create_cmdclass('jsdeps', data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(js_dir, npm=['yarn'], build_cmd='build:prod'), ensure_targets(jstargets),
)

setup_args = dict(
    name=name,
    version=version,
    description='A Custom Jupyter Widget Library',
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    install_requires=[
        'ipywidgets>=7.6.0',
        'ogdf-python',
        'importlib_resources'
    ],
    packages=find_packages(),
    package_data={"": ["*.html", "*.json", "*.js", "*.txt"]},
    zip_safe=False,
    cmdclass=cmdclass,
    author='Andreas Strobl',
    author_email='strobland@fim.uni-passau.de',
    url='https://github.com/ogdf/ogdf-python-widget',
    keywords=[
        'ipython',
        'jupyter',
        'widgets',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

setup(**setup_args)
