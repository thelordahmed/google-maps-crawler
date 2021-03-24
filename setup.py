from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["six","numpy","pil"], 'excludes': []}

base = 'Console'

executables = [
    Executable('gui.py', base=base, targetName = 'Gmaps Crawler')
]

setup(name='Gmaps Crawler',
      version = '1',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
