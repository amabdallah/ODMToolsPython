"""
py2app/py2exe build script for MyApplication.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
 python setup.py py2app

Usage (Windows):
 python setup.py py2exe
"""


import sys
import os
'''
from setuptools import setup

import ez_setup

ez_setup.use_setuptools()
'''



NAME = 'ODM2Tools'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ICON_DIR = os.path.join('odmtools', 'common', "icons")
WIN_ICON_FILE = os.path.join(ICON_DIR, "ODMTools.ico")
MAC_ICON_FILE = os.path.join(ICON_DIR, "ODMTools.icns")

#APP = ['/Users/stephanie/DEV/ODMToolsPython/ODMTools.py']
APP = os.path.join(BASE_DIR, 'ODMTools.py')
extra_options = None
sys.setrecursionlimit(2000)
if sys.platform == 'darwin':
    sys.argv.append('py2app')
    from setuptools import setup
    # APP = ['/Users/stephanie/DEV/ODMToolsPython/ODMTools.py']
    LIBS = ['/usr/X11/lib/libfreetype.6.dylib', '/usr/X11/lib/libstdc++.6.dylib', '/usr/X11/lib/libpng15.15.dylib']
    OPTIONS = {'iconfile': MAC_ICON_FILE,
               'includes': ['pymysql', 'sqlalchemy', 'dateutil'], 'frameworks': LIBS}
    extra_options = dict(app=APP, setup_requires=['py2app'], options={'py2app': OPTIONS})

elif sys.platform == 'win32':
    sys.argv.append('py2exe')
    from distutils.core import setup
    APP = ['D:\Dev\ODMTools\ODMTools.py']
    import numpy
    import py2exe
    from glob import glob
    data_files = [
        ("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\Microsoft.VC90.CRT\*.*')),
        (r'mpl-data', [r'C:\Anaconda3\envs\odmtools\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
        (r'mpl-data\images', glob(r'C:\Anaconda3\envs\odmtools\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
        (r'mpl-data\fonts', glob(r'C:\Anaconda3\envs\odmtools\Lib\site-packages\matplotlib\mpl-data\fonts\*.*')),
        (r'mpl-data\stylelib', glob(r'C:\Anaconda3\envs\odmtools\Lib\site-packages\matplotlib\mpl-data\stylelib\*.*'))]

    OPTIONS = {
        #'excludes': ['_ssl', 'pyreadline', 'difflib', 'doctest', 'optparse', 'pickle', 'calendar'],
        "compressed": 1,
        'dll_excludes': ['msvcr71.dll', 'OLEAUT32.dll', 'USER32.dll', 'IMM32.dll', 'SHELL32.dll',
                         'ole32.dll', 'ODBC32.dll', 'WSOCK32.dll', 'WINMM.dll', 'ADVAPI32.dll',
                         'MSVCP90.dll', 'WS2_32.dll', 'WINSPOOL.DRV', 'GDI32.dll', 'KERNEL32.dll',
                         'ntdll.dll', 'COMCTL32.dll', 'COMDLG32.dll', 'msvcrt.dll', 'RPCRT4.dll'],
        "optimize": 2,
        "bundle_files": 3,
        "dist_dir": "dist",
        "xref": False,
        "skip_archive": False,
        "ascii": False,
        "custom_boot_script": '',
        "packages": ['wx.lib.pubsub',  'pyodbc', 'numpy', 'scipy', 'sqlalchemy', 'wx', 'geoalchemy2'], #'ObjectListView',
    }


    sys.path.append("C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\VC\\Microsoft.VC90.CRT")
    sys.path.append(BASE_DIR)
    extra_options = dict(console=APP, data_files=data_files, options={'py2exe': OPTIONS})

setup(name=NAME, **extra_options)
