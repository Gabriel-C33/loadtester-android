
from pythonforandroid.recipe import PythonRecipe

class LoadTesterRecipe(PythonRecipe):
    version = '1.0'
    url = 'file://.'
    depends = ['python3', 'requests', 'urllib3']
    site_packages_name = 'loadtester'
    call_hostpython_via_targetpython = False

recipe = LoadTesterRecipe()
