from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('pylen_main.py', base=base, target_name = 'pylen')
]

setup(name='pylen',
      version = '1.1.0',
      description = 'Python Filament Length Generator',
      options = {'build_exe': build_options},
      executables = executables)
