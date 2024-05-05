import PyInstaller.__main__
import shutil
import os

PyInstaller.__main__.run([
    'WizardArcade.py',
    '-y',
    '--noconsole',
    '--icon=favicon.ico'
])

try:
    shutil.rmtree("_internal")
    os.remove("WizardArcade.exe")
except FileNotFoundError:
    pass
shutil.move("dist/WizardArcade/_internal", os.getcwd())
shutil.move("dist/WizardArcade/WizardArcade.exe", os.getcwd())
