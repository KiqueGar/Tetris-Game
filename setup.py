from cx_Freeze import setup, Executable

base = None


executables = [Executable("Tetris.py", base=base)]

packages = ["idna", "pygame"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Tetris",
    options = options,
    version = "0.2",
    description = 'A simple Game',
    executables = executables
)