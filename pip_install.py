import sys
import subprocess
import os
import platform
import bpy

# Import code --
# https://github.com/luckychris/install_blender_python_modules/blob/main/install_blender_python_module.py


def isWindows():
    return os.name == 'nt'


def isMacOS():
    return os.name == 'posix' and platform.system() == "Darwin"


def isLinux():
    return os.name == 'posix' and platform.system() == "Linux"


def python_exec():

    if isWindows():
        return os.path.join(sys.prefix, 'bin', 'python.exe')
    elif isMacOS():

        try:
            # 2.92 and older
            path = bpy.app.binary_path_python
        except AttributeError:
            # 2.93 and later
            import sys
            path = sys.executable
        return os.path.abspath(path)
    elif isLinux():
        import sys
        return os.path.join(sys.prefix, 'bin', 'python3.11')
    else:
        print("sorry, still not implemented for ",
              os.name, " - ", platform.system)


def installModule(packageName):
    try:
        subprocess.call([python_exec, "import ", packageName])
    except (Exception):
        python_exe = python_exec()
        # upgrade pip
        subprocess.call([python_exe, "-m", "ensurepip"])
        subprocess.call(
            [python_exe, "-m", "pip", "install", "--upgrade", "pip"])
        # install required packages
        subprocess.call([python_exe, "-m", "pip", "install", packageName])
        # Check repo if you run into any issues

with open("./import.txt", 'r') as file:
    if python_exec() not in sys.path:
        sys.path.append(python_exec())
    try:
        packages = file.read().splitlines()
    except Exception:
        print("Could not open file--Setting packages to install as empty")
        packages = []
    
    [installModule(package) for package in packages]
