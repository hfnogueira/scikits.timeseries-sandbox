"""
Python script for building documentation. This script was designed for
building the docs on windows, but may work on other platforms as well.

To build the docs you must have all optional dependencies for the timeseries
installed. See the installation instructions for a list of these.

Note: currently latex builds do not work because of table formats that are not
supported in the latex generation.

Usage
-----

python make.py clean
python make.py html
"""

import os
import shutil
import sys

sphinx_build = os.path.join(sys.prefix, 'Scripts', 'sphinx-build')

def check_build():
    build_dirs = [
        'build', 'build/doctrees', 'build/html', 'build/latex', 'build/plots']
    for d in build_dirs:
        try:
            os.mkdir(d)
        except OSError:
            pass

def html():

    check_build()
    os.chdir('source')
    if os.system(sphinx_build + ' -a -b html -d ../build/doctrees . ../build/html'):
        raise SystemExit("Building HTML failed.")
    os.chdir('..')

def latex():

    check_build()
    os.chdir('source')
    # LaTeX format.
    if os.system(sphinx-build + ' -a -b latex -d ../build/doctrees . ../build/latex'):
        raise SystemExit("Building LaTeX failed.")

    # Produce pdf.
    os.chdir('../build/latex')

    # first call to pdflatex used to generate .idx files
    os.system('pdflatex scikitstimeseries.tex')

    # convert .idx files to indices
    os.system('makeindex -s python.ist scikitstimeseries.idx')
    os.system('makeindex -s python.ist modscikitstimeseries.idx')

    # regenerate pdf with proper indices
    os.system('pdflatex scikitstimeseries.tex')

    os.chdir('../..')

def clean():
    if os.path.exists('build'):
        shutil.rmtree('build')

def all():
    clean()
    html()
    latex()

funcd = {'html':html,
         'latex':latex,
         'clean':clean,
         'all':all,
         }

if len(sys.argv)>1:
    for arg in sys.argv[1:]:
        func = funcd.get(arg)
        if func is None:
            raise SystemExit('Do not know how to handle %s; valid args are'%(
                    arg, funcd.keys()))
        func()
else:
    all()